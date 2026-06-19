# ปฏิบัติการ บทที่ 10: การสร้างแอปพลิเคชันซิงก์ข้อมูลสินค้าโปรดด้วย Supabase CRUD (Lab)

ปฏิบัติการนี้จะฝึกทักษะการรวบรวมฟังก์ชันการติดต่อกับคลาวด์ดาต้าเบสระดับโลกอย่าง Supabase โดยผู้เรียนจะได้ออกแบบแอปพลิเคชัน **"สมุดจดสินค้าที่ต้องการและรายการโปรดออนไลน์ (Supabase Wishlist Manager)"** ซึ่งผู้ใช้สามารถพิมพ์บันทึกชื่อสินค้าและราคา (Create / Insert) โหลดลิสต์สินค้ามาเรนเดอร์ในแอป (Read / Select) กดจิ้มหัวใจสลับสถานะสินค้าโปรด (Update) และกดถอนรายการทิ้งออกจากตาราง (Delete) โดยทุกจังหวะการทำงานจะซิงก์ประสานกับตาราง SQL บนเซิร์ฟเวอร์ Supabase แบบเรียลไทม์

---

## 1. วัตถุประสงค์การเรียนรู้
1. สามารถตั้งค่าและลงทะเบียนใช้งาน `@supabase/supabase-js` ร่วมกับระบบคีย์ลับสภาพแวดล้อม `.env` ได้สำเร็จ
2. สามารถพัฒนาฟังก์ชันสำหรับค้นหาดึงข้อมูล (GET/Select) แถวจากคลาวด์มาเรนเดอร์ลงในคอมโพเนนต์ `FlatList`
3. สามารถเขียนระบบฟอร์มนำเข้าและยิงส่งข้อมูลแถวใหม่ (POST/Insert) ขึ้นสู่ตารางคลาวด์ได้ถูกต้อง
4. สามารถระบุคำสั่งแก้ไขค่าฟิลด์ตาราง (PATCH/Update) และคำสั่งลบข้อมูล (DELETE/Delete) ร่วมกับการคัดกรอง `.eq()`
5. สามารถจัดการสถานะกล่องความคืบหน้า (Loading) และรับมือข้อผิดพลาดเครือข่ายฐานข้อมูลได้ถูกต้อง

---

## 2. โจทย์และข้อกำหนดปฏิบัติการ (Requirements)

ผู้เรียนต้องสร้างโครงสร้างโปรเจกต์ประกอบด้วยไฟล์ดังต่อไปนี้:

```text
โครงสร้างไฟล์ปฏิบัติการ:
├── .env                              => บรรจุคีย์โครงการ EXPO_PUBLIC_SUPABASE_URL และ EXPO_PUBLIC_SUPABASE_ANON_KEY
├── lib/
│   └── supabase.ts                   => สร้าง Supabase Client
└── app/
    └── index.tsx                     => หน้าจอหลักควบคุมการทำงานของแอป Wishlist (CRUD Interface)
```

### ข้อมูลโครงสร้างตารางหลังบ้านบน Supabase (Table Schema):
ผู้เรียนต้องไปที่ Supabase SQL Editor หรือ Table Editor เพื่อเปิดสร้างตารางชื่อ **`wishlist`** ประกอบด้วยคอลัมน์ดังนี้:
* `id` (int8 / identity): คีย์หลัก (Primary Key) สั่งสร้างรหัสอัตโนมัติ
* `title` (text): ชื่อของสินค้าที่อยากได้
* `price` (numeric): ราคาสินค้า
* `is_favorite` (boolean): สถานะความชอบพิเศษ (ค่าเริ่มต้น: `false`)
* `created_at` (timestamptz): วันเวลาบันทึก (ค่าเริ่มต้น: `now()`)

### เงื่อนไขการจัดการข้อมูลในแอปพลิเคชัน:
1. **การโหลดข้อมูลเริ่มต้น (Read):** ดึงข้อมูลจากตาราง `wishlist` ทั้งหมดมาแสดง เรียงตามเวลาล่าสุด
2. **การบันทึกชิ้นใหม่ (Create):** มีฟอร์มรับอินพุตกรอกชื่อสินค้าและราคา เมื่อส่งสำเร็จ ให้นำผลลัพธ์ข้อมูลแถวล่าสุดที่ได้ย้อนกลับมาจาก Supabase เสียบแทรกด้านบนสุดของสเตตลิสต์ทันที
3. **การสลับหัวใจรายการโปรด (Update):** เมื่อกดแตะรูปสัญลักษณ์หัวใจ ให้ยิงอัปเดตสลับค่าบูลีนของ `is_favorite` เฉพาะไอดีนั้น ๆ บนคลาวด์
4. **การถอนรายการ (Delete):** เมื่อกดไอคอนถังขยะ ให้ลบแถวนั้นทิ้ง และรีแฟกเตอร์ฟิลเตอร์กรองแถว ID นั้นออกจากจอแอป

---

## 3. ขั้นตอนการลงมือปฏิบัติ (Step-by-Step Tutorial)

### ขั้นตอนที่ 1: ติดตั้งคลังไลบรารีและสร้างระบบคีย์ลับ
สั่งรันติดตั้งคำสั่งในแอปพลิเคชัน:
```bash
npm install @supabase/supabase-js react-native-url-polyfill
```
จากนั้นสร้างไฟล์ `.env` ที่โฟลเดอร์นอกสุดของแอป ป้อน URL และ Anon Key ที่ได้มาจาก Supabase:
```text
EXPO_PUBLIC_SUPABASE_URL=https://your-supabase-url.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key-here
```

### ขั้นตอนที่ 2: ตั้งค่าโมดูล Client ใน `lib/supabase.ts`
สร้างไฟล์ `lib/supabase.ts` เพื่ออำนวยความสะดวกในการจัดแชร์ออบเจกต์คำสั่ง:
```typescript
import 'react-native-url-polyfill/auto';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY || '';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
```

### ขั้นตอนที่ 3: เขียนกระบวนการ CRUD เชื่อม Supabase
สร้างฟังก์ชันสำหรับทริกเกอร์เหตุการณ์ต่าง ๆ:
```typescript
// ดึงข้อมูล Select
const fetchItems = async () => {
  const { data, error } = await supabase
    .from('wishlist')
    .select('*')
    .order('created_at', { ascending: false });
  if (!error) setWishlist(data || []);
};

// เขียนบันทึก Insert
const handleAddItem = async () => {
  const { data, error } = await supabase
    .from('wishlist')
    .insert([{ title, price: parseFloat(price), is_favorite: false }])
    .select();
  if (!error) setWishlist([data[0], ...wishlist]);
};
```

---

## 4. โค้ดเฉลยฉบับสมบูรณ์ (Complete Solution)

ผู้เรียนสามารถนำโค้ดอินเทอร์เฟซ Wishlist ฉบับสมบูรณ์ชุดนี้บันทึกใส่ลงในไฟล์ `app/index.tsx` เพื่อสั่งทำงานและซิงก์ฐานข้อมูลออนไลน์แบบเรียลไทม์กับโครงการ Supabase:

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
  Keyboard 
} from 'react-native';
import { supabase } from '../lib/supabase';

// โครงสร้างประเภทข้อมูล Wishlist
interface WishItem {
  id: number;
  title: string;
  price: number;
  is_favorite: boolean;
  created_at: string;
}

export default function SupabaseWishlistManager() {
  const [wishlist, setWishlist] = useState<WishItem[]>([]);
  const [title, setTitle] = useState('');
  const [price, setPrice] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // 1. เรียกดึงข้อมูลตารางตอนเริ่มต้นเปิดแอป
  useEffect(() => {
    fetchWishlist();
  }, []);

  // 2. ฟังก์ชัน READ: ค้นหาข้อมูลสินค้าทั้งหมด
  const fetchWishlist = async () => {
    try {
      setIsLoading(true);
      const { data, error } = await supabase
        .from('wishlist')
        .select('*')
        .order('created_at', { ascending: false });

      if (error) {
        throw error;
      }
      setWishlist(data || []);
    } catch (error: any) {
      Alert.alert('เกิดข้อผิดพลาด', error.message || 'ไม่สามารถโหลดข้อมูลคลาวด์ได้');
    } finally {
      setIsLoading(false);
    }
  };

  // 3. ฟังก์ชัน CREATE: บันทึกข้อมูลสินค้าแถวใหม่
  const handleAddItem = async () => {
    const parsedPrice = parseFloat(price);
    
    if (!title.trim() || isNaN(parsedPrice)) {
      Alert.alert('ข้อมูลไม่ครบ', 'กรุณาระบุชื่อสินค้าและราคาให้ถูกต้อง');
      return;
    }

    try {
      setIsSubmitting(true);
      Keyboard.dismiss();

      // ยิงข้อมูลขึ้นคลาวด์ตาราง wishlist
      const { data, error } = await supabase
        .from('wishlist')
        .insert([
          { 
            title: title.trim(), 
            price: parsedPrice, 
            is_favorite: false 
          }
        ])
        .select();

      if (error) {
        throw error;
      }

      // พ่วงข้อมูลใหม่ต่อหน้าสุดของลิสต์บนจอ
      if (data && data.length > 0) {
        setWishlist([data[0], ...wishlist]);
        setTitle('');
        setPrice('');
        Alert.alert('สำเร็จ!', 'บันทึกรายการโปรดของคุณเรียบร้อย');
      }
    } catch (error: any) {
      Alert.alert('บันทึกไม่สำเร็จ', error.message || 'เกิดข้อขัดข้องในการซิงก์ข้อมูล');
    } finally {
      setIsSubmitting(false);
    }
  };

  // 4. ฟังก์ชัน UPDATE: อัปเดตสลับสถานะความชอบสินค้าโปรด (Favorite status)
  const handleToggleFavorite = async (itemId: number, currentStatus: boolean) => {
    try {
      const { error } = await supabase
        .from('wishlist')
        .update({ is_favorite: !currentStatus })
        .eq('id', itemId);

      if (error) {
        throw error;
      }

      // อัปเดตสเตตบนหน้าจอทันทีเพื่อแสดงสีหัวใจที่สลับตามจริง
      setWishlist(
        wishlist.map((item) => 
          item.id === itemId ? { ...item, is_favorite: !currentStatus } : item
        )
      );
    } catch (error: any) {
      Alert.alert('แก้ไขข้อมูลล้มเหลว', error.message);
    }
  };

  // 5. ฟังก์ชัน DELETE: ถอดรายการสินค้าทิ้ง
  const handleDeleteItem = async (itemId: number) => {
    Alert.alert(
      'ยืนยันการลบ',
      'คุณแน่ใจหรือไม่ว่าต้องการนำรายการโน้ตนี้ออกถาวร?',
      [
        { text: 'ยกเลิก', style: 'cancel' },
        { 
          text: 'ลบทิ้ง', 
          style: 'destructive',
          onPress: async () => {
            try {
              const { error } = await supabase
                .from('wishlist')
                .delete()
                .eq('id', itemId);

              if (error) {
                throw error;
              }

              // กรองลบไอดีออกจากหน้าจอ
              setWishlist(wishlist.filter((item) => item.id !== itemId));
            } catch (error: any) {
              Alert.alert('ไม่สามารถลบข้อมูลได้', error.message);
            }
          }
        }
      ]
    );
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        
        {/* หัวข้อแดชบอร์ด */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>🛒 Supabase Wishlist</Text>
          <Text style={styles.headerSubtitle}>จัดการความต้องการซิงก์คลาวด์เรียลไทม์</Text>
        </View>

        {/* แบบฟอร์มเพิ่มรายการสินค้าใหม่ */}
        <View style={styles.formCard}>
          <TextInput
            style={styles.input}
            placeholder="ชื่อสินค้าที่อยากได้ (เช่น iPhone 16)..."
            placeholderTextColor="#64748b"
            value={title}
            onChangeText={setTitle}
          />
          <TextInput
            style={styles.input}
            placeholder="ระบุราคาสินค้า (บาท)..."
            placeholderTextColor="#64748b"
            value={price}
            onChangeText={setPrice}
            keyboardType="numeric"
          />
          
          {isSubmitting ? (
            <ActivityIndicator size="small" color="#38bdf8" style={styles.spinner} />
          ) : (
            <TouchableOpacity style={styles.submitButton} onPress={handleAddItem}>
              <Text style={styles.submitButtonText}>➕ บันทึกข้อมูลขึ้นคลาวด์</Text>
            </TouchableOpacity>
          )}
        </View>

        {/* รายการแสดงผล Wishlist */}
        <View style={styles.listSection}>
          <View style={styles.listHeader}>
            <Text style={styles.listTitle}>ของที่คุณอยากได้</Text>
            <TouchableOpacity onPress={fetchWishlist} disabled={isLoading}>
              <Text style={styles.refreshText}>{isLoading ? 'กำลังซิงก์...' : '🔄 รีเฟรชฐานข้อมูล'}</Text>
            </TouchableOpacity>
          </View>

          {isLoading ? (
            <View style={styles.centerLoading}>
              <ActivityIndicator size="large" color="#38bdf8" />
              <Text style={styles.loadingText}>กำลังดึงข้อมูลตารางสินค้าโปรด...</Text>
            </View>
          ) : (
            <FlatList
              data={wishlist}
              keyExtractor={(item) => item.id.toString()}
              renderItem={({ item }) => (
                <View style={styles.itemCard}>
                  <View style={styles.itemInfo}>
                    <Text style={styles.itemTitle}>{item.title}</Text>
                    <Text style={styles.itemPrice}>฿{item.price.toLocaleString()}</Text>
                  </View>
                  
                  {/* ปุ่มเปลี่ยนสถานะ Favorite และปุ่มลบ */}
                  <View style={styles.actionRow}>
                    <TouchableOpacity 
                      onPress={() => handleToggleFavorite(item.id, item.is_favorite)}
                      style={styles.actionIcon}
                    >
                      <Text style={styles.heartText}>{item.is_favorite ? '❤️' : '🤍'}</Text>
                    </TouchableOpacity>

                    <TouchableOpacity 
                      onPress={() => handleDeleteItem(item.id)}
                      style={styles.actionIcon}
                    >
                      <Text style={styles.trashText}>🗑️</Text>
                    </TouchableOpacity>
                  </View>
                </View>
              )}
              ListEmptyComponent={
                <View style={styles.emptyContainer}>
                  <Text style={styles.emptyText}>ไม่มีข้อมูลสินค้าในตารางของคุณขณะนี้</Text>
                </View>
              }
            />
          )}
        </View>
      </View>
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
    marginVertical: 10,
  },
  headerTitle: {
    fontSize: 22,
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
    marginBottom: 20,
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
  submitButton: {
    backgroundColor: '#38bdf8',
    borderRadius: 8,
    height: 44,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 4,
  },
  submitButtonText: {
    color: '#0f172a',
    fontWeight: 'bold',
    fontSize: 14,
  },
  spinner: {
    paddingVertical: 10,
  },
  listSection: {
    flex: 1,
  },
  listHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
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
    marginTop: 8,
    fontSize: 13,
  },
  itemCard: {
    flexDirection: 'row',
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 14,
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 10,
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  itemInfo: {
    flex: 1,
  },
  itemTitle: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 15,
    textTransform: 'capitalize',
  },
  itemPrice: {
    color: '#10b981',
    fontWeight: 'bold',
    fontSize: 13,
    marginTop: 4,
  },
  actionRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  actionIcon: {
    marginLeft: 16,
    padding: 6,
  },
  heartText: {
    fontSize: 18,
  },
  trashText: {
    fontSize: 16,
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

← [ย้อนกลับแบบทดสอบ: 03-quiz.md](./03-quiz.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ศึกษาบทเรียนถัดไป: บทที่ 11](../chapter-11-camera-imagepicker/) →
