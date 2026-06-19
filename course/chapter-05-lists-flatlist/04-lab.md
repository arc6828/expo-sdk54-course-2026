# ปฏิบัติการ บทที่ 5: การพัฒนาแอปแสดงรายการรูปภาพจาก API พร้อมระบบรีเฟรชและโหลดข้อมูลเพิ่ม (Lab)

ปฏิบัติการนี้จะฝึกทักษะการประยุกต์ใช้งานคอมโพเนนต์รายการประสิทธิภาพสูง `FlatList` ร่วมกับการดึงข้อมูลผ่านระบบเครือข่ายออนไลน์จริงด้วย Fetch API (ดึงข้อมูลจำลองจาก JSONPlaceholder) และอัปเดตข้อมูลแบบแบ่งหน้า (Pagination) เพื่อทำระบบโหลดอัตโนมัติเมื่อเลื่อนขอบล่างสุด (Infinite Scroll) พร้อมระบบดึงลงรีเฟรชหน้าจอ (Pull-to-Refresh)

---

## 1. วัตถุประสงค์การเรียนรู้
1. สามารถดึงข้อมูลภาพและข้อความจาก REST API ออนไลน์ภายนอกผ่าน Fetch API ร่วมกับ `useEffect` ได้สำเร็จ
2. สามารถจัดสรรหน่วยความจำและเรนเดอร์ภาพจากอินเทอร์เน็ตปริมาณมากในระบบรายการ `FlatList` ได้อย่างลื่นไหล
3. สามารถพัฒนาฟังก์ชัน Pull-to-Refresh เพื่อเคลียร์สเตตกลับคืนหน้า 1 และประมวลผลข้อมูลใหม่จากเซิร์ฟเวอร์
4. สามารถทำระบบแบ่งหน้าโหลดเนื้อหาต่อด้านท้าย (Infinite Scroll) ด้วยพร็อพส์ `onEndReached`
5. สามารถเขียนจัดวางและตกแต่งชิ้นส่วนย่อยประกอบลิสต์ (`ListHeaderComponent`, `ListFooterComponent`, `ListEmptyComponent`, และ `ItemSeparatorComponent`) ได้ถูกต้อง

---

## 2. โจทย์และข้อกำหนดปฏิบัติการ (Requirements)
ผู้เรียนจะต้องเขียนพัฒนาโมเดลจำลอง **แอปพลิเคชันคลังแกลเลอรีภาพออนไลน์ (Live Photo Gallery Stream)** โดยประกอบด้วยเงื่อนไข 2 ส่วนหลักดังนี้:

### 1. ชิ้นส่วนการ์ดภาพย่อย: `components/PhotoCard.tsx`
* สร้างเป็น Custom Component เพื่อแสดงชิ้นผลงานแต่ละชิ้นประกอบด้วย:
  * รูปภาพขนาดย่อ (`thumbnailUrl`) แสดงผลทรงสี่เหลี่ยมโค้งมนสวยงาม
  * ข้อความหัวเรื่องรูปภาพ (`title`) บรรยายรายละเอียด
  * ตัวเลขดัชนีระบุ ID ของรูปภาพ
* จัดความปลอดภัยด้วย TypeScript Interface `PhotoCardProps`
* ตัวปุ่มการ์ดจัดด้วย `Pressable` ที่มีลูกเล่นการกระพริบสว่างหรือยืดหดน้ำหนักสัมผัสเมื่อถูกคลิก

### 2. หน้าหลักควบคุมแบบต่อเนื่อง: `app/index.tsx`
* ดึงข้อมูลผ่าน URL: `https://jsonplaceholder.typicode.com/photos`
* **การแบ่งหน้าโหลดข้อมูล (Pagination):** กำหนดให้โหลดข้อมูลเพียงครั้งละ 10 รูป (`_limit=10`) โดยส่งผ่านพารามิเตอร์ `_page` เพื่อระบุหน้าข้อมูล (เช่น หน้า 1 โหลดรูป 1-10, หน้า 2 โหลดรูป 11-20)
* **การดึงเพื่อรีเฟรช (Pull-to-Refresh):** เมื่อดึงหน้าจอลง จะเรียกโหลดข้อมูลหน้า 1 ใหม่ พร้อมสั่งล้างคลังสเตตอาร์เรย์เดิมทิ้ง
* **การเลื่อนลงสุดเพื่อโหลดต่อ (Infinite Scroll):** เมื่อใช้นิ้วเลื่อนลงมาจนถึงระยะกึ่งกลางของไอเท็มสุดท้าย จะทริกเกอร์เรียกโหลดหน้าถัดไป (`page + 1`) เพื่อนำรูปภาพชุดใหม่ไปประกอบต่อท้ายอาร์เรย์เดิม พร้อมเรนเดอร์ไอคอนหมุนโหลดข้อมูล (`ActivityIndicator`) ค้างไว้ที่ด้านล่างสุดของตารางรายการ
* **องค์ประกอบตกแต่ง:**
  * **Header:** แสดงข้อความใหญ่ "Photo Stream" และบอกยอดรูปสะสมปัจจุบัน
  * **Separator:** เส้นคั่นสีเทาบางกั้นระหว่างภาพ
  * **Empty:** โชว์ข้อความ "ไม่พบข้อมูลรูปภาพในคลัง" กรณีสเตตอาร์เรย์เป็นศูนย์

---

## 3. ขั้นตอนการลงมือปฏิบัติ (Step-by-Step Tutorial)

### ขั้นตอนที่ 1: การสร้าง Custom Component สำหรับจัดสไตล์ชิ้นการ์ดรูปภาพ
สร้างไฟล์คอมโพเนนต์สำหรับการ์ดแสดงรายการรูปภาพตามเส้นทาง `components/PhotoCard.tsx` และใส่โครงสร้างโค้ดดังนี้:

```tsx
import { View, Text, Image, StyleSheet, Pressable } from 'react-native';

// กำหนดประเภทข้อมูล Props ด้วย TypeScript Interface
export interface PhotoCardProps {
  id: number;
  title: string;
  thumbnailUrl: string;
  onPressCard?: () => void;
}

export default function PhotoCard({ id, title, thumbnailUrl, onPressCard }: PhotoCardProps) {
  return (
    <Pressable
      onPress={onPressCard}
      style={({ pressed }) => [
        styles.card,
        { backgroundColor: pressed ? '#1e293b' : '#0f172a' } // เปลี่ยนสีพื้นหลังเล็กน้อยเมื่อแตะ
      ]}
    >
      {/* แสดงรูปภาพจาก URI เครือข่าย */}
      <Image source={{ uri: thumbnailUrl }} style={styles.thumbnail} />
      
      <View style={styles.textContainer}>
        <Text style={styles.idText}>PHOTO ID: #{id}</Text>
        <Text style={styles.titleText} numberOfLines={2}>
          {title}
        </Text>
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    padding: 12,
    alignItems: 'center',
    borderRadius: 8,
  },
  thumbnail: {
    width: 60,
    height: 60,
    borderRadius: 8,
    backgroundColor: '#334155', // พื้นหลังสีเทาขณะรอดึงรูปจริง
  },
  textContainer: {
    flex: 1,
    marginLeft: 16,
  },
  idText: {
    fontSize: 11,
    color: '#38bdf8',
    fontWeight: 'bold',
    marginBottom: 2,
  },
  titleText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#cbd5e1',
    textTransform: 'capitalize',
  },
});
```

---

### ขั้นตอนที่ 2: วางหน้าจอเขียนฟังก์ชัน Fetch API แบบแบ่งหน้าในไฟล์หลัก `app/index.tsx`
เขียนประมวลสเตตจัดการหน้าข้อมูลสัญญานเน็ตเวิร์ก พร้อมประกอบคำสั่งลงในหน้าหลัก:

```tsx
import { useState, useEffect } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  FlatList, 
  ActivityIndicator, 
  SafeAreaView, 
  Alert 
} from 'react-native';
import PhotoCard from '../components/PhotoCard'; // โหลดการ์ดภาพย่อย

interface Photo {
  id: number;
  title: string;
  thumbnailUrl: string;
  url: string;
}

export default function PhotoStreamScreen() {
  // สเตตเก็บคลังอาร์เรย์รูปภาพ
  const [photos, setPhotos] = useState<Photo[]>([]);
  
  // สเตตจัดการคีย์เลขหน้าและการจำสถานะหมุนโหลด
  const [page, setPage] = useState<number>(1);
  const [loadingInitial, setLoadingInitial] = useState<boolean>(true); // โหลดครั้งแรกสุด
  const [loadingMore, setLoadingMore] = useState<boolean>(false);       // โหลดเพิ่มส่วนท้าย
  const [refreshing, setRefreshing] = useState<boolean>(false);         // ดึงหน้าจอลงรีเฟรช
  const [hasMoreData, setHasMoreData] = useState<boolean>(true);        // เช็คว่าหมดคลังหรือยัง

  const LIMIT = 10; // ดึงข้อมูลครั้งละ 10 รายการ

  // 1. ฟังก์ชันดึงข้อมูลผ่านเครือข่าย
  const fetchPhotosData = async (targetPage: number, isRefreshing: boolean = false) => {
    try {
      if (isRefreshing) setRefreshing(true);
      else if (targetPage > 1) setLoadingMore(true);

      const url = `https://jsonplaceholder.typicode.com/photos?_page=${targetPage}&_limit=${LIMIT}`;
      const response = await fetch(url);
      const data: Photo[] = await response.json();

      if (data.length < LIMIT) {
        setHasMoreData(false); // หากข้อมูลส่งมาไม่ครบตามจำนวนจำกัด แปลว่าสิ้นสุดคลังแล้ว
      }

      if (isRefreshing) {
        setPhotos(data); // ล้างสเตตเดิมและใส่ข้อมูลหน้า 1 ชุดใหม่ลงไปตรงๆ
        setHasMoreData(true);
      } else {
        setPhotos((prev) => [...prev, ...data]); // นำไปต่อยอดพรีเพนท์ข้อมูลเดิม
      }
    } catch (error) {
      console.error('การดึงข้อมูลเครือข่ายผิดพลาด:', error);
      Alert.alert('เกิดข้อผิดพลาด', 'ไม่สามารถเชื่อมต่อสัญญาณอินเทอร์เน็ตได้ในขณะนี้');
    } finally {
      setLoadingInitial(false);
      setLoadingMore(false);
      setRefreshing(false);
    }
  };

  // ดึงข้อมูลหน้า 1 ตอนรันหน้าแอปเริ่มต้น
  useEffect(() => {
    fetchPhotosData(1);
  }, []);

  // 2. ฟังก์ชันสั่งลากนิ้วรีเฟรชด้านบน
  const handleRefresh = () => {
    setPage(1);
    fetchPhotosData(1, true);
  };

  // 3. ฟังก์ชันโหลดเพิ่มต่อท้ายเมื่อเลื่อนลงสุดหน้าจอ
  const handleLoadMore = () => {
    if (!loadingMore && hasMoreData) {
      const nextPage = page + 1;
      setPage(nextPage);
      fetchPhotosData(nextPage);
    }
  };

  // ... รายละเอียดสปอตไลท์ Render จะแยกอยู่ในส่วนเฉลยท้ายสุด
  return null;
}
```

---

## 4. โค้ดเฉลยฉบับสมบูรณ์ (Complete Solution)

ผู้เรียนสามารถคัดลอกรายละเอียดโค้ดโปรเจคฉบับสมบูรณ์ที่จัดวางสไตล์ชีทแบบสเปซโมเดิร์นสีเข้ม (Dark Mode) ไปรันผลลัพธ์ผ่านตัวจำลองเพื่อทดสอบระบบดึงภาพได้ทันที:

### 4.1 ซอร์สโค้ดไฟล์ย่อย: `components/PhotoCard.tsx`
```tsx
import { View, Text, Image, StyleSheet, Pressable } from 'react-native';

export interface PhotoCardProps {
  id: number;
  title: string;
  thumbnailUrl: string;
  onPressCard?: () => void;
}

export default function PhotoCard({ id, title, thumbnailUrl, onPressCard }: PhotoCardProps) {
  return (
    <Pressable
      onPress={onPressCard}
      style={({ pressed }) => [
        styles.card,
        { backgroundColor: pressed ? '#1e293b' : '#1e293b' }
      ]}
    >
      <Image source={{ uri: thumbnailUrl }} style={styles.thumbnail} />
      
      <View style={styles.textContainer}>
        <Text style={styles.idText}>ID: #{id}</Text>
        <Text style={styles.titleText} numberOfLines={2}>
          {title}
        </Text>
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    padding: 14,
    alignItems: 'center',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#334155',
  },
  thumbnail: {
    width: 64,
    height: 64,
    borderRadius: 8,
    backgroundColor: '#334155',
  },
  textContainer: {
    flex: 1,
    marginLeft: 16,
  },
  idText: {
    fontSize: 10,
    color: '#38bdf8',
    fontWeight: 'bold',
    marginBottom: 2,
    letterSpacing: 0.5,
  },
  titleText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#cbd5e1',
    textTransform: 'capitalize',
    lineHeight: 18,
  },
});
```

### 4.2 ซอร์สโค้ดหน้าจอหลักเชื่อม API: `app/index.tsx`
```tsx
import { useState, useEffect } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  FlatList, 
  ActivityIndicator, 
  SafeAreaView, 
  Alert 
} from 'react-native';
import PhotoCard from '../components/PhotoCard';

interface Photo {
  id: number;
  title: string;
  thumbnailUrl: string;
  url: string;
}

export default function App() {
  const [photos, setPhotos] = useState<Photo[]>([]);
  const [page, setPage] = useState<number>(1);
  const [loadingInitial, setLoadingInitial] = useState<boolean>(true);
  const [loadingMore, setLoadingMore] = useState<boolean>(false);
  const [refreshing, setRefreshing] = useState<boolean>(false);
  const [hasMoreData, setHasMoreData] = useState<boolean>(true);

  const LIMIT = 10;

  const fetchPhotosData = async (targetPage: number, isRefreshing: boolean = false) => {
    try {
      if (isRefreshing) setRefreshing(true);
      else if (targetPage > 1) setLoadingMore(true);

      const url = `https://jsonplaceholder.typicode.com/photos?_page=${targetPage}&_limit=${LIMIT}`;
      const response = await fetch(url);
      const data: Photo[] = await response.json();

      if (data.length < LIMIT) {
        setHasMoreData(false);
      }

      if (isRefreshing) {
        setPhotos(data);
        setHasMoreData(true);
      } else {
        setPhotos((prev) => [...prev, ...data]);
      }
    } catch (error) {
      console.error('การดึงข้อมูลเครือข่ายผิดพลาด:', error);
      Alert.alert('เกิดข้อผิดพลาด', 'ไม่สามารถเชื่อมต่อสัญญาณอินเทอร์เน็ตได้ในขณะนี้');
    } finally {
      setLoadingInitial(false);
      setLoadingMore(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchPhotosData(1);
  }, []);

  const handleRefresh = () => {
    setPage(1);
    fetchPhotosData(1, true);
  };

  const handleLoadMore = () => {
    if (!loadingMore && hasMoreData && !loadingInitial) {
      const nextPage = page + 1;
      setPage(nextPage);
      fetchPhotosData(nextPage);
    }
  };

  // A. ส่วนตกแต่งแถบหัวของรายการ
  const renderHeader = () => (
    <View style={styles.header}>
      <Text style={styles.headerTitle}>Photo Gallery Feed</Text>
      <Text style={styles.headerSubtitle}>
        จำนวนภาพแสดงในสเตริม: {photos.length} ภาพ
      </Text>
    </View>
  );

  // B. ตัวแสดงแถบหมุนประมวลผลเพิ่มใต้ตารางลิสต์
  const renderFooter = () => {
    if (!loadingMore) return null;
    return (
      <View style={styles.footerLoader}>
        <ActivityIndicator size="small" color="#38bdf8" />
        <Text style={styles.footerLoaderText}>กำลังโหลดรูปภาพเพิ่มเติม...</Text>
      </View>
    );
  };

  // C. ป้ายเตือนในกรณีลิสต์มีค่าว่าง
  const renderEmpty = () => (
    <View style={styles.emptyContainer}>
      <Text style={styles.emptyText}>ไม่พบข้อมูลรูปภาพในคลังจำลอง</Text>
    </View>
  );

  // D. เส้นประคั่นกลางแบ่งรายการ
  const renderSeparator = () => <View style={styles.separator} />;

  if (loadingInitial) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#38bdf8" />
        <Text style={styles.loadingText}>กำลังเปิดแกลเลอรีภาพออนไลน์...</Text>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <FlatList
          data={photos}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <PhotoCard
              id={item.id}
              title={item.title}
              thumbnailUrl={item.thumbnailUrl}
              onPressCard={() => Alert.alert(`ภาพรหัส #${item.id}`, item.title)}
            />
          )}
          // ผูกสไตล์องค์ประกอบตกแต่งย่อย
          ListHeaderComponent={renderHeader}
          ListFooterComponent={renderFooter}
          ListEmptyComponent={renderEmpty}
          ItemSeparatorComponent={renderSeparator}
          
          // ผูกความสามารถรีเฟรชด้วยนิ้วลาก
          refreshing={refreshing}
          onRefresh={handleRefresh}
          
          // ผูกความสามารถ Infinite Scroll
          onEndReached={handleLoadMore}
          onEndReachedThreshold={0.5} // เลื่อนมาถึงขอบล่าง 50% ของรายการสุดท้ายให้ดึงหน้าใหม่รอทันที
          
          contentContainerStyle={styles.listContent}
        />
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
  },
  centerContainer: {
    flex: 1,
    backgroundColor: '#0f172a',
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: '#94a3b8',
    marginTop: 12,
    fontSize: 14,
  },
  listContent: {
    paddingHorizontal: 16,
    paddingBottom: 24,
  },
  header: {
    paddingVertical: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#1e293b',
    marginBottom: 16,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  headerSubtitle: {
    fontSize: 12,
    color: '#94a3b8',
    marginTop: 4,
  },
  separator: {
    height: 12, // ทำหน้าที่เป็นระยะช่องไฟคั่นระหว่างไอเท็มแต่ละตัว
  },
  footerLoader: {
    paddingVertical: 20,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 8,
  },
  footerLoaderText: {
    color: '#94a3b8',
    fontSize: 12,
  },
  emptyContainer: {
    padding: 40,
    alignItems: 'center',
    justifyContent: 'center',
  },
  emptyText: {
    color: '#64748b',
    fontSize: 16,
  },
});
```

---

← [ย้อนกลับแบบทดสอบ: 03-quiz.md](./03-quiz.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ศึกษาบทเรียนถัดไป: บทที่ 6](../chapter-06-expo-router/) →
