# ปฏิบัติการ บทที่ 8: การสร้างแอปบันทึกข้อคิดเห็นออนไลน์แบบจดจำประวัติ (Lab)

ปฏิบัติการนี้จะฝึกทักษะการประยุกต์ใช้งานหน่วยความจำถาวรภายในเครื่องร่วมกับการจัดการส่งต่อข้อมูลขึ้นสู่คลาวด์ผ่านเครือข่าย โดยผู้เรียนจะได้สร้างแอปพลิเคชัน **"สมุดโน้ตบันทึกและซิงก์ความคิดเห็นออนไลน์ (Synchronized Note Keeper)"** ซึ่งจะทำหน้าจอดึงข้อมูลบันทึกส่วนกลางมาจาก REST API ด้วย HTTP GET แสดงผลในลิสต์ และเปิดฟอร์มเขียนเพิ่มโพสต์ส่งกลับขึ้นเซิร์ฟเวอร์ด้วย HTTP POST พร้อมเพิ่มความเสถียรโดยการบันทึกสำรอง (Cache) ข้อมูลรอบล่าสุดเก็บลงเครื่องผ่าน `AsyncStorage` เพื่อให้อ่านประวัติโน้ตเก่าขึ้นมารายงานหน้าต่างจอได้ทันทีแม้กรณีสัญญาณอินเทอร์เน็ตขาดหาย

---

## 1. วัตถุประสงค์การเรียนรู้
1. สามารถติดตั้งและเขียนโปรแกรมดึงข้อมูลแบบออฟไลน์แคชชิ่ง (Offline-First caching) โดยเรียกอ่านประวัติเก่าจาก AsyncStorage ขึ้นมาจัดแสดงเมื่อแอปเริ่มต้นทำงาน
2. สามารถเขียนระบบดักส่งข้อมูลด้วย Fetch API (HTTP POST Method) เพื่อบันทึกโน้ตใหม่ขึ้นสู่เซิร์ฟเวอร์ภายนอกสำเร็จ
3. สามารถจัดสร้างสถานะ Loading และจัดการป๊อปอัพ Alert แจ้งเตือนข้อผิดพลาดกรณีการติดต่อเครือข่ายล้มเหลวได้อย่างถูกต้อง
4. สามารถสลักแปลงข้อมูลอาร์เรย์ของโพสต์แบบซับซ้อนให้กลายเป็น JSON String และแกะกลับคืนเพื่อจัดสรรร่วมกับคอมโพเนนต์ `FlatList` ได้ถูกต้อง

---

## 2. โจทย์และข้อกำหนดปฏิบัติการ (Requirements)

ผู้เรียนต้องเขียนสร้างแอปพลิเคชันที่มีโครงสร้างองค์ประกอบและการทำงานตามเงื่อนไขดังนี้:

### 1. การทำงานร่วมกับเซิร์ฟเวอร์ภายนอก (Fetch API Integration):
* **ดึงข้อมูลเริ่มต้น (GET Request):** เมื่อเปิดแอปขึ้นมาเป็นครั้งแรก ให้ทำการยิง GET request ไปที่:
  ```http
  GET https://jsonplaceholder.typicode.com/posts?_limit=5
  ```
  เพื่อดึงรายการโน้ตจำนวน 5 โพสต์ล่าสุดมาแสดงผล
* **ออฟไลน์แคชชิ่ง (Local Caching):** เมื่อดึงข้อมูลสำเร็จ ให้บันทึกชุดข้อมูลอาร์เรย์นี้เก็บสำรองถาวรลงใน `AsyncStorage` ภายใต้คีย์ `'cached_notes'` เสมอ
* **การส่งข้อมูลโพสต์ใหม่ (POST Request):** มีแบบฟอร์มให้กรอก "หัวข้อโน้ต (Title)" และ "รายละเอียดเนื้อหา (Content)" เมื่อกดปุ่มส่งข้อมูลให้ยิง POST request ไปที่:
  ```http
  POST https://jsonplaceholder.typicode.com/posts
  ```
  โดยเมื่อได้ผลลัพธ์ตอบกลับสำเร็จ (Response Code: 201) ให้นำรายการที่บันทึกสำเร็จสมมุตินั้น ไปพ่วงแทรกต่อเพิ่มไว้ด้านบนสุดของรายการแสดงผลในหน้าจอทันที เพื่อสะท้อนภาพข้อมูลอัปเดตแบบเรียลไทม์

### 2. ระบบต้านทานสัญญาณอินเทอร์เน็ตล่ม (Offline/Error Resilience):
* หากสมาร์ทโฟนปิดสัญญาณเน็ตหรือเซิร์ฟเวอร์พังจน Fetch ล้มเหลว แอปพลิเคชันต้องไม่ดับพัง แต่ต้องมีกลไกดึงข้อมูลโน้ตที่แคชไว้ล่าสุดใน AsyncStorage ขึ้นมาทำงานแทนที่บนลิสต์ และแจ้งเตือนให้ผู้ใช้งานทราบผ่านคำสั่ง `Alert.alert` ว่า "กำลังทำงานในโหมดออฟไลน์"

### 3. การแสดงผล UI สไตล์โมเดิร์น:
* จัดสไตล์หน้าจอเป็นโทนสี Slate/Sky หรูหราสะอาดตา มีช่องรับข้อมูล Text inputs ของหัวเรื่องและเนื้อหาแยกกัน มีการแสดงผลตัวหมุน ActivityIndicator ในระหว่างเชื่อมเน็ตเวิร์ก และการ์ดแสดงผลโน้ตย่อย

---

## 3. ขั้นตอนการลงมือปฏิบัติ (Step-by-Step Tutorial)

### ขั้นตอนที่ 1: ติดตั้งแพ็คเกจเสริมสำหรับเก็บข้อมูล
สั่งรันคำสั่งติดตั้งคลังหน่วยเก็บข้อมูลถาวรภายในเครื่อง:
```bash
npx expo install @react-native-async-storage/async-storage
```

### ขั้นตอนที่ 2: สร้างฟังก์ชันสำหรับอ่านและเขียนแคช
เขียนแยกโค้ดจัดการข้อมูล JSON เพื่อให้อ่านเข้าใจง่าย:
```tsx
import AsyncStorage from '@react-native-async-storage/async-storage';

const CACHE_KEY = 'cached_notes';

// บันทึกอาร์เรย์ของโพสต์ลงเครื่อง
const cacheNotes = async (notes: any[]) => {
  try {
    await AsyncStorage.setItem(CACHE_KEY, JSON.stringify(notes));
  } catch (e) {
    console.error('ไม่สามารถแคชข้อมูลได้:', e);
  }
};

// กู้ประวัติอาร์เรย์จากเครื่อง
const getCachedNotes = async () => {
  try {
    const raw = await AsyncStorage.getItem(CACHE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    console.error('ไม่สามารถดึงข้อมูลแคชได้:', e);
    return [];
  }
};
```

### ขั้นตอนที่ 3: จัดการกระแสไหลของสเตต (State Workflow)
ประกาศสเตตควบคุม `notes` (เก็บข้อมูลโพสต์), `isLoading` (เช็คเวลาโหลด), และ `isSubmitting` (เช็คเวลาส่งข้อมูล POST) และจัดทำ Logic คัดกรองเครือข่าย:
```tsx
const loadInitialData = async () => {
  try {
    setIsLoading(true);
    const response = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5');
    
    if (response.ok) {
      const data = await response.json();
      setNotes(data);
      await cacheNotes(data); // บันทึกสำรองลง Storage
    } else {
      throw new Error('การตอบรับจากเซิร์ฟเวอร์ไม่สมบูรณ์');
    }
  } catch (error) {
    // กรณีเน็ตหลุด ให้กู้ข้อมูลเก่าขึ้นมาโชว์ตัว
    const localData = await getCachedNotes();
    setNotes(localData);
    Alert.alert('โหมดออฟไลน์', 'ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ได้ ดึงข้อมูลล่าสุดที่บันทึกไว้ในเครื่องขึ้นมาแสดงผลแทน');
  } finally {
    setIsLoading(false);
  }
};
```

---

## 4. โค้ดเฉลยฉบับสมบูรณ์ (Complete Solution)

ผู้เรียนสามารถคัดลอกซอร์สโค้ดของแอปพลิเคชันแบบหน้าต่างเดียวชุดนี้ ไปจัดทำและบันทึกทับในไฟล์หลักของโครงการ (เช่น `app/index.tsx` หรือ `App.tsx`) เพื่อรันและจำลองการดึงส่งข้อมูลเครือข่าย:

```tsx
import React, { useState, useEffect } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  TextInput, 
  TouchableOpacity, 
  FlatList, 
  ActivityIndicator, 
  Alert, 
  SafeAreaView, 
  KeyboardAvoidingView, 
  Platform 
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

// โมเดลข้อมูลโน้ตข้อความ
interface Note {
  id: number;
  title: string;
  body: string;
}

const STORAGE_KEY = 'cached_notes';

export default function SynchronizedNoteKeeper() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // 1. ตรวจจับข้อมูลตอนเปิดหน้าจอแรกสุด
  useEffect(() => {
    fetchNotes();
  }, []);

  // 2. ฟังก์ชันหลักในการดึงรายการโน้ต (GET)
  const fetchNotes = async () => {
    try {
      setIsLoading(true);
      // ส่งคำขอดึงข้อมูลจำกัดจำนวน 5 โพสต์ล่าสุด
      const response = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5');
      
      if (response.ok) {
        const remoteData = await response.json();
        setNotes(remoteData);
        // ทำการเซฟสำรองเก็บในเครื่องเป็น Offline Cache
        await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(remoteData));
      } else {
        throw new Error('เซิร์ฟเวอร์ขัดข้อง');
      }
    } catch (error) {
      // ดักจับกรณีออฟไลน์หรือเน็ตพัง ให้ดึงจาก AsyncStorage
      const localData = await AsyncStorage.getItem(STORAGE_KEY);
      if (localData) {
        setNotes(JSON.parse(localData));
      }
      Alert.alert(
        'สัญญาณขาดหาย',
        'ไม่สามารถดึงข้อมูลจากอินเทอร์เน็ตได้ ระบบทำการดึงข้อมูลล่าสุดที่บันทึกในเครื่องขึ้นแสดงผลทดแทน'
      );
    } finally {
      setIsLoading(false);
    }
  };

  // 3. ฟังก์ชันการส่งข้อมูลโน้ตใหม่ (POST)
  const handleAddNote = async () => {
    if (!title.trim() || !content.trim()) {
      Alert.alert('กรอกข้อมูลไม่ครบ', 'กรุณากรอกหัวข้อโน้ตและรายละเอียดให้ครบถ้วน');
      return;
    }

    try {
      setIsSubmitting(true);
      
      // สั่งส่งข้อมูลชนิด POST ไปเก็บที่ API ปลายทาง
      const response = await fetch('https://jsonplaceholder.typicode.com/posts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: JSON.stringify({
          title: title,
          body: content,
          userId: 1
        }),
      });

      if (response.ok) {
        const newNoteFromServer = await response.json();
        
        // จำลองโครงสร้างการซิงก์โดยนำโน้ตใหม่ไปต่อไว้ด้านบนสุดของสเตตลิสต์ปัจจุบัน
        const updatedNotes = [
          {
            id: newNoteFromServer.id, // รหัสไอดี 101 ที่ได้คืนมาจาก REST API จำลอง
            title: title,
            body: content
          },
          ...notes
        ];
        
        setNotes(updatedNotes);
        
        // อัปเดตไฟล์แคชออฟไลน์ในเครื่องให้มีโน้ตใหม่ติดตัวไปด้วย
        await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(updatedNotes));
        
        Alert.alert('สำเร็จ!', 'บันทึกโน้ตซิงก์ขึ้นระบบเซิร์ฟเวอร์เรียบร้อย');
        setTitle('');
        setContent('');
      } else {
        throw new Error('เกิดข้อผิดพลาดในการประมวลผลบนคลาวด์');
      }
    } catch (error) {
      Alert.alert('ส่งไม่สำเร็จ', 'ไม่สามารถบันทึกข้อมูลขึ้นเซิร์ฟเวอร์ได้ กรุณาเชื่อมต่ออินเทอร์เน็ต');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.container}
      >
        {/* หัวข้อแอป */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>🗒️ Synchronized Note Keeper</Text>
          <Text style={styles.headerSubtitle}>ซิงก์บันทึกผ่าน API และแคชข้อมูลออฟไลน์ถาวร</Text>
        </View>

        {/* แบบฟอร์มเขียนบันทึกส่งข้อมูล */}
        <View style={styles.formCard}>
          <Text style={styles.formLabel}>เขียนโน้ตชิ้นใหม่</Text>
          <TextInput
            style={styles.input}
            placeholder="หัวข้อโน้ต..."
            placeholderTextColor="#64748b"
            value={title}
            onChangeText={setTitle}
          />
          <TextInput
            style={[styles.input, styles.textArea]}
            placeholder="รายละเอียดเนื้อหา..."
            placeholderTextColor="#64748b"
            value={content}
            onChangeText={setContent}
            multiline
          />
          
          {isSubmitting ? (
            <ActivityIndicator size="small" color="#38bdf8" style={styles.spinner} />
          ) : (
            <TouchableOpacity style={styles.submitButton} onPress={handleAddNote}>
              <Text style={styles.submitButtonText}>ซิงก์โพสต์ขึ้นคลาวด์</Text>
            </TouchableOpacity>
          )}
        </View>

        {/* ส่วนแสดงรายการข้อมูลโน้ต */}
        <View style={styles.listContainer}>
          <View style={styles.listHeaderRow}>
            <Text style={styles.listTitle}>บันทึกของคุณในเครื่อง</Text>
            <TouchableOpacity onPress={fetchNotes} disabled={isLoading}>
              <Text style={styles.refreshText}>{isLoading ? 'กำลังโหลด...' : '🔄 รีเฟรชล่าสุด'}</Text>
            </TouchableOpacity>
          </View>

          {isLoading ? (
            <View style={styles.centerLoading}>
              <ActivityIndicator size="large" color="#38bdf8" />
              <Text style={styles.loadingText}>กำลังติดต่อดึงข้อมูล API...</Text>
            </View>
          ) : (
            <FlatList
              data={notes}
              keyExtractor={(item, index) => item.id.toString() + index}
              renderItem={({ item }) => (
                <View style={styles.noteCard}>
                  <Text style={styles.noteCardTitle}>📌 {item.title}</Text>
                  <Text style={styles.noteCardBody}>{item.body}</Text>
                  <View style={styles.badgeRow}>
                    <View style={styles.syncBadge}>
                      <Text style={styles.badgeText}>ID: {item.id} (Synced)</Text>
                    </View>
                  </View>
                </View>
              )}
              ListEmptyComponent={
                <View style={styles.emptyContainer}>
                  <Text style={styles.emptyText}>ไม่มีข้อมูลบันทึกในเครื่องขณะนี้</Text>
                </View>
              }
            />
          )}
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#0f172a',
  },
  container: {
    flex: 1,
    padding: 16,
  },
  header: {
    alignItems: 'center',
    marginVertical: 12,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  headerSubtitle: {
    fontSize: 12,
    color: '#94a3b8',
    marginTop: 4,
  },
  formCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 16,
  },
  formLabel: {
    color: '#38bdf8',
    fontWeight: 'bold',
    fontSize: 14,
    marginBottom: 10,
  },
  input: {
    backgroundColor: '#0f172a',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#334155',
    color: '#ffffff',
    padding: 12,
    fontSize: 14,
    marginBottom: 10,
  },
  textArea: {
    height: 70,
    textAlignVertical: 'top',
  },
  submitButton: {
    backgroundColor: '#38bdf8',
    borderRadius: 8,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  submitButtonText: {
    color: '#0f172a',
    fontWeight: 'bold',
    fontSize: 14,
  },
  spinner: {
    paddingVertical: 10,
  },
  listContainer: {
    flex: 1,
  },
  listHeaderRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  listTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  refreshText: {
    color: '#38bdf8',
    fontSize: 13,
  },
  centerLoading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: '#94a3b8',
    marginTop: 10,
    fontSize: 13,
  },
  noteCard: {
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 14,
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 12,
  },
  noteCardTitle: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 15,
    textTransform: 'capitalize',
    marginBottom: 6,
  },
  noteCardBody: {
    color: '#cbd5e1',
    fontSize: 13,
    lineHeight: 18,
  },
  badgeRow: {
    flexDirection: 'row',
    marginTop: 10,
  },
  syncBadge: {
    backgroundColor: '#0284c7',
    paddingVertical: 2,
    paddingHorizontal: 8,
    borderRadius: 4,
  },
  badgeText: {
    color: '#ffffff',
    fontSize: 10,
    fontWeight: 'bold',
  },
  emptyContainer: {
    alignItems: 'center',
    paddingVertical: 40,
  },
  emptyText: {
    color: '#64748b',
    fontSize: 14,
  },
});
```

---

← [ย้อนกลับแบบทดสอบ: 03-quiz.md](./03-quiz.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ศึกษาบทเรียนถัดไป: บทที่ 9](../chapter-09-native-features-sensors/) →
