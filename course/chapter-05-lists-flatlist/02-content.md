# บทที่ 5: การแสดงผลรายการข้อมูลและประสิทธิภาพการทำงาน (Content)

ความเร็วและความลื่นไหลในการเลื่อนดูข้อมูลยาว ๆ (Scrolling Performance) ถือเป็นปัจจัยหลักที่ส่งผลต่อคะแนนความพึงพอใจของผู้ใช้งานโมบายแอปพลิเคชัน ในบทเรียนนี้เราจะศึกษาข้อจำกัดของคอมโพเนนต์ `ScrollView` และเจาะลึกวิธีการนำเสนอรายการข้อมูลประสิทธิภาพสูงด้วย `FlatList` และ `SectionList` รวมถึงแนวทางการเชื่อมต่อข้อมูลสดผ่านเน็ตเวิร์ก

---

## 5.1 ปัญหาประสิทธิภาพของ ScrollView กับข้อมูลขนาดใหญ่

คอมโพเนนต์ `ScrollView` มีลักษณะการเรนเดอร์ข้อมูลแบบ **กระตือรือร้น (Eager Rendering)** หมายความว่า ทันทีที่คอมโพเนนต์ถูกเปิดขึ้นมารันบนหน้าจอ มันจะประมวลผลวาดโครงสร้างของคอมโพเนนต์ลูกย่อยทุกชิ้นภายในลิสต์ลงสู่หน่วยความจำ (RAM) พร้อมกันในคราวเดียว:

* **จุดเด่น:** ใช้งานง่าย รันคอมโพเนนต์ลูกที่แตกต่างรูปแบบกันได้อย่างอิสระ
* **จุดด้อยที่รุนแรง:** หากข้อมูลมีจำนวนมาก (เช่น เกิน 100 รายการขึ้นไป หรือมีรูปภาพความละเอียดสูงประกอบ) ระบบปฏิบัติการจะต้องสร้าง Native Views คาไว้ใน RAM มหาศาล ส่งผลให้แอปพลิเคชันเกิดการสะดุด เฟรมเรตตก (Frame Drops) และแอปเด้งดับเนื่องจากหน่วยความจำเต็ม (Out of Memory)

ดังนั้น `ScrollView` จึงควรเลือกใช้เฉพาะหน้ารายละเอียดทั่วไป หรือแบบฟอร์มที่มีจำนวนวัตถุคงที่สั้น ๆ เท่านั้น

---

## 5.2 การแก้ไขด้วย FlatList: Virtualization และ Recycling

เพื่อจัดการปัญหาข้อมูลล้นจอ React Native ได้จัดเตรียมคอมโพเนนต์ **`FlatList`** (ซึ่งสืบทอดกลไกมาจาก `VirtualizedList`) โดยใช้เทคนิคสถาปัตยกรรมระดับเนทีฟในการจัดระเบียบพื้นที่หน่วยความจำดังนี้:

### 1. ระบบจำลองเสมือนจริง (Virtualization)
`FlatList` จะวาดเรนเดอร์เฉพาะคอมโพเนนต์รายการที่ **ปรากฏตัวอยู่ในขอบเขตหน้าจอจริงเท่านั้น** (บวกกับพื้นที่ข้างเคียงล่วงหน้าเล็กน้อย เรียกว่า Window Buffer) ข้อมูลที่อยู่นอกจอจะยังไม่ถูกนำมาประมวลผล

### 2. การหมุนเวียนมุมมองกลับมาใช้ใหม่ (Item View Recycling)
เมื่อผู้ใช้งานใช้นิ้วปัดหน้าจอเพื่อเลื่อนลง กล่อง View รายการที่เคลื่อนล้นหลุดขอบจอด้านบนออกไป จะถูกส่งกลับเข้าไปในคลังสะสมและนำโครงสร้างกล่องนั้นมา **"รีไซเคิลปรับเปลี่ยนข้อมูลข้างในใหม่"** เพื่อนำมารอแสดงผลเป็นรายการใหม่ที่วิ่งเข้ามาจากขอบจอด้านล่าง ส่งผลให้หน่วยความจำถูกจำกัดอยู่คงที่ตามขนาดจอเสมอ ไม่ว่าจะโหลดข้อมูล 100 หรือ 100,000 ชิ้นก็ตาม

---

## 5.3 โครงสร้างและพร็อพส์หลักของ FlatList (data, renderItem, keyExtractor)

การทำงานร่วมกับ `FlatList` จำเป็นต้องส่งค่าพร็อพส์ที่ระบุหน้าที่เฉพาะเจาะจง 3 ตัวหลักเสมอ:

* **`data`**: อาร์เรย์ของข้อมูลดิบที่ต้องการแสดงผล (เช่น `Array<any>`)
* **`renderItem`**: ฟังก์ชันคืนค่า JSX คอมโพเนนต์ที่อธิบายหน้าตาของแต่ละรายการย่อย โดยรับพารามิเตอร์ออบเจกต์ที่มีพร็อพส์ `{ item, index }`
* **`keyExtractor`**: ฟังก์ชันส่งสตริงคีย์ที่เป็นเอกลักษณ์ (Unique Key) ของรายการย่อยแต่ละชิ้น เพื่อช่วยให้ระบบ Diffing Engine ของ React ติดตามและระบุการเปลี่ยนแปลงตำแหน่งชิ้นงานได้ถูกต้องโดยไม่ต้องวาดใหม่ทั้งหมด

```tsx
import { FlatList, Text, View, StyleSheet } from 'react-native';

const mockUsers = [
  { id: '1', name: 'สมชาย' },
  { id: '2', name: 'สมศรี' },
  { id: '3', name: 'สมหวัง' },
];

export default function UserList() {
  return (
    <FlatList
      data={mockUsers}
      keyExtractor={(item) => item.id} // ช่วยส่งคืนสตริงระบุคีย์ที่ไม่ซ้ำกัน
      renderItem={({ item }) => (
        <View style={styles.item}>
          <Text style={styles.itemText}>{item.name}</Text>
        </View>
      )}
    />
  );
}

const styles = StyleSheet.create({
  item: {
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  itemText: {
    fontSize: 16,
  },
});
```

---

## 5.4 การดึงข้อมูลจาก REST API มาใช้ร่วมกับ FlatList

ในระบบงานจริง ข้อมูลรายการมักจะดึงผ่านเน็ตเวิร์กจากเซิร์ฟเวอร์ภายนอก เราสามารถประยุกต์ใช้คำสั่ง `fetch()` ร่วมกับสถานะ `useState` และ `useEffect` ดึงข้อมูลมาอัปโหลดใส่ใน `FlatList` ดังตัวอย่างนี้:

```tsx
import { useState, useEffect } from 'react';
import { 
  FlatList, 
  Text, 
  View, 
  ActivityIndicator, 
  StyleSheet, 
  SafeAreaView 
} from 'react-native';

interface Post {
  id: number;
  title: string;
  body: string;
}

export default function ApiListScreen() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // 1. ฟังก์ชันดึงข้อมูลจาก REST API ของ JSONPlaceholder
  const fetchPosts = async () => {
    try {
      setLoading(true);
      const response = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=15');
      const data = await response.json();
      setPosts(data);
    } catch (error) {
      console.error('ดึงข้อมูลผิดพลาด:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  // 2. แสดงตัวหมุนโหลดข้อมูลชั่วคราวหากเน็ตเวิร์กกำลังดึงข้อมูลอยู่
  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#38bdf8" />
        <Text style={styles.loadingText}>กำลังดึงข้อมูลโพสต์ล่าสุด...</Text>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <FlatList
        data={posts}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.postCard}>
            <Text style={styles.postTitle}>📌 {item.title}</Text>
            <Text style={styles.postBody}>{item.body}</Text>
          </View>
        )}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
  },
  centerContainer: {
    flex: 1,
    backgroundColor: '#0f172a',
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: '#94a3b8',
    marginTop: 10,
  },
  postCard: {
    backgroundColor: '#1e293b',
    padding: 16,
    marginVertical: 8,
    marginHorizontal: 16,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#334155',
  },
  postTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ffffff',
    textTransform: 'capitalize',
    marginBottom: 6,
  },
  postBody: {
    fontSize: 14,
    color: '#cbd5e1',
    lineHeight: 20,
  },
});
```

---

## 5.5 การปรับแต่งส่วนประกอบลิสต์ (Header, Footer, Item Separator, และ ListEmptyComponent)

`FlatList` เตรียมอินเทอร์เฟซอรรถประโยชน์อื่น ๆ ที่ทำให้การออกแบบหน้าตารายการทำได้สมบูรณ์แบบโดยไม่ต้องครอบคอมโพเนนต์ด้วย ScrollView ซ้ำซ้อน:

* **`ListHeaderComponent`**: พื้นที่จัดแสดงสำหรับวางหัวตารางหรือแผงควบคุมส่วนบน (เช่น ช่องแถบค้นหา โฆษณา หรือป้ายหัวข้อใหญ่) ซึ่งจะเลื่อนสไลด์ขึ้นไปตามความเร็วของลิสต์
* **`ListFooterComponent`**: พื้นที่จัดแสดงสำหรับวางท้ายตารางรายการ (เช่น ปุ่มแสดงหน้าถัดไป หรือตัวหมุนบอกว่ากำลังดาวน์โหลดข้อมูลต่อท้าย)
* **`ItemSeparatorComponent`**: คอมโพเนนต์คั่นกลางระหว่างชิ้นรายการเพื่อระบุช่องไฟหรือวาดเส้นแบ่งเส้นคั่น (จะตัดขอบไม่วาดท้ายรายการล่างสุดให้เอง)
* **`ListEmptyComponent`**: คอมโพเนนต์แสดงผลทดแทนเมื่ออาร์เรย์ `data` มีขนาดเป็นศูนย์ (ไม่มีข้อมูลใด ๆ ในรายการ) เพื่อแจ้งเตือนผู้ใช้อย่างชัดเจน

---

## 5.6 ฟีเจอร์ Pull-to-Refresh และ Infinite Scroll (onEndReached)

### 1. ระบบ Pull-to-Refresh (ดึงหน้าจอเพื่อรีเฟรชข้อมูล)
เป็นการเปิดโอกาสให้ผู้ใช้งานกวาดนิ้วลงเพื่ออัปโหลดใหม่เพื่อเอาโพสต์ชุดใหม่ โดยควบคุมด้วย 2 พร็อพส์หลัก:
* **`refreshing`**: ตัวแปรสถานะ Boolean ที่บ่งบอกว่าขณะนี้ระบบกำลังดาวน์โหลดรอบใหม่ค้างอยู่หรือไม่ (เพื่อให้ไอคอนหมุนทำงาน)
* **`onRefresh`**: ฟังก์ชันที่จะถูกสั่งงานอัตโนมัติเมื่อตรวจพบการลากนิ้วดึงหน้าจอลำดับล่างลงมา

### 2. ระบบ Infinite Scroll (เลื่อนลงสุดเพื่อดาวน์โหลดต่ออัตโนมัติ)
เทคนิคยอดนิยมบนหน้า Feed ของโซเชียลมีเดียเพื่อรองรับการโหลดข้อมูลแบบแบ่งหน้า (Pagination) ควบคุมผ่าน:
* **`onEndReached`**: ฟังก์ชันสั่งงานเมื่อผู้ใช้งานเลื่อนหน้าจอลิสต์เข้าใกล้ความยาวล่างสุดของรายการ
* **`onEndReachedThreshold`**: ค่าตัวเลขสัดส่วนระยะห่างขอบล่างของหน้าต่าง ตัวเลข `0.5` บ่งบอกว่าถ้าเลื่อนมาถึงกึ่งกลางชิ้นงานรายการสุดท้าย ให้เริ่มเรียกการโหลดข้อมูลหน้าถัดไปเตรียมสแตนด์บายได้ทันที

---

## 5.7 การจัดกลุ่มข้อมูลด้วย SectionList

เมื่อข้อมูลรายการมีความจำเป็นที่จะต้องจัดแยกจำแนกหมวดหมู่ (เช่น คลังรายชื่ออักษรขึ้นต้น A-Z, การแบ่งหมวดหมู่เมนูอาหาร) คอมโพเนนต์ `SectionList` จะช่วยอำนวยความสะดวกในการจัดสรรความลื่นไหลได้เป็นหมวดหมู่:

### โครงสร้างข้อมูลสำหรับ SectionList
ข้อมูลในพร็อพส์ `sections` ต้องเป็นอาร์เรย์ของออบเจกต์ ซึ่งมีคีย์ชื่อ **`title`** (หรือคีย์จัดกลุ่มใด ๆ) และคีย์อาร์เรย์ชื่อ **`data`** บรรจุรายละเอียดลูกย่อยในกลุ่มนั้น:

```tsx
import { SectionList, Text, View, StyleSheet, SafeAreaView } from 'react-native';

const MENU_DATA = [
  {
    title: 'ของคาว (Main Dishes)',
    data: ['ข้าวผัดปู', 'ต้มยำกุ้งน้ำข้น', 'ผัดไทยกุ้งสด'],
  },
  {
    title: 'เครื่องดื่ม (Drinks)',
    data: ['ชาไทยนมสด', 'กาแฟอเมริกาโน่เย็น'],
  },
];

export default function RestaurantMenu() {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <SectionList
        sections={MENU_DATA}
        keyExtractor={(item, index) => item + index}
        // ฟังก์ชันวาดเมนูอาหารย่อยแต่ละตัว
        renderItem={({ item }) => (
          <View style={styles.item}>
            <Text style={styles.itemText}>{item}</Text>
          </View>
        )}
        // ฟังก์ชันวาดป้ายแถบหัวข้อกลุ่ม (Sticky Header)
        renderSectionHeader={({ section: { title } }) => (
          <View style={styles.header}>
            <Text style={styles.headerText}>{title}</Text>
          </View>
        )}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  header: {
    backgroundColor: '#3b82f6',
    padding: 10,
  },
  headerText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  item: {
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e2e8f0',
  },
  itemText: {
    fontSize: 15,
  },
});
```

## 5.8 สรุปท้ายบทเรียน

**ปัญหาประสิทธิภาพของ ScrollView กับข้อมูลขนาดใหญ่:** ScrollView ทำงานแบบ Eager Rendering ซึ่งจะโหลดและวาดคอมโพเนนต์ย่อยทั้งหมดลงสู่หน่วยความจำ (RAM) พร้อมกันตั้งแต่เริ่มต้น จึงทำให้เมื่อต้องแสดงผลรายการข้อมูลจำนวนมหาศาลหรือมีรูปภาพประกอบจำนวนมาก จะเกิดปัญหาหน่วยความจำล้นและทำให้อัตราการแสดงผลเฟรมเรตตกจนแอปพลิเคชันทำงานสะดุดหรือเด้งออก

**การแก้ไขด้วย FlatList (Virtualization และ Recycling):** เพื่อเพิ่มความลื่นไหลระดับเนทีฟ FlatList ถูกนำเข้ามาช่วยแก้ปัญหาโดยใช้แนวคิด Virtualization ที่เรนเดอร์เฉพาะข้อมูลที่ปรากฏบนขอบจอจริงเท่านั้น และใช้แนวคิด Item View Recycling ในการหมุนเวียนจัดสลับกล่องรายการที่เลื่อนหลุดขอบจอกลับมาสวมใส่ข้อมูลชุดถัดไป ช่วยประหยัดการสร้าง Native Views และประหยัดทรัพยากรระบบได้อย่างมีประสิทธิภาพ

**โครงสร้างและพร็อพส์หลักของ FlatList:** การประกาศใช้งาน FlatList ต้องการอ็อบชันควบคุมหลัก 3 ประการ ได้แก่ data สำหรับส่งผ่านอาร์เรย์ของข้อมูลดิบทั้งหมด, renderItem ซึ่งคอยทำหน้าที่สร้างรูปแบบ JSX ของแถบข้อมูลรายย่อย และ keyExtractor ที่ใช้กำหนดค่าสตริงคีย์เอกลักษณ์เฉพาะตัวให้แต่ละรายการเพื่อช่วยระบบ Diffing Engine ของ React ประเมินจุดเปลี่ยนได้อย่างรวดเร็ว

**การดึงข้อมูลจาก REST API มาใช้ร่วมกับ FlatList:** การประยุกต์ใช้งานในระบบจริงจะนำฟังก์ชัน fetch() มาประสานร่วมกับ useState และ useEffect เพื่อขอข้อมูลดิบผ่านระบบเครือข่ายอินเทอร์เน็ต โดยเราสามารถแสดงกล่อง ActivityIndicator บ่งบอกความก้าวหน้าขณะรอผลลัพธ์ ก่อนที่จะจัดเก็บข้อมูลลงในสเตตและนำข้อมูลดังกล่าวไปเป็นแหล่งอ้างอิงหลักในโครงสร้างของ FlatList

**การปรับแต่งส่วนประกอบลิสต์:** เพื่อป้องกันความซับซ้อนในการเขียนคอมโพเนนต์ซ้อนทับกัน FlatList ได้เตรียมเครื่องมือเฉพาะตัวมาอำนวยความสะดวก เช่น ListHeaderComponent และ ListFooterComponent สำหรับสร้างหัวและท้ายหน้าเลื่อน, ItemSeparatorComponent ในการวาดเส้นคั่นหรือจัดระเบียบช่องไฟระหว่างแถว และ ListEmptyComponent เพื่อแสดงข้อความแจ้งเตือนเมื่อไม่มีข้อมูลแสดงผล

**ฟีเจอร์ Pull-to-Refresh และ Infinite Scroll:** แอปพลิเคชันที่ทันสมัยสามารถยกระดับความสะดวกได้ด้วยระบบ Pull-to-Refresh ที่เปิดทางให้ผู้ใช้นิ้วปัดหน้าจอลงเพื่อรีเฟรชข้อมูลผ่านพร็อพส์ refreshing และ onRefresh รวมถึงการทำ Infinite Scroll เพื่อดาวน์โหลดหน้าถัดไปแบบต่อเนื่องผ่านพร็อพส์ onEndReached และการกำหนดสัดส่วนระยะเริ่มโหลดผ่าน onEndReachedThreshold

**การจัดกลุ่มข้อมูลด้วย SectionList:** สำหรับข้อมูลที่ต้องจัดแยกเป็นหมวดหมู่อย่างชัดเจน SectionList คือตัวเลือกในการแสดงผลที่ตอบโจทย์ โดยข้อมูลนำเข้าในพร็อพส์ sections จะต้องจัดเรียงกลุ่มข้อมูลในรูปแบบโครงสร้างออบเจกต์ที่มีคีย์ title สำหรับป้ายหัวข้อกลุ่ม และคีย์ data สำหรับบรรจุรายการย่อย ซึ่งระบบจะทำการคำนวณและวาดป้ายแถบหัวข้อกลุ่ม (Sticky Header) ให้สอดคล้องกันโดยอัตโนมัติ

---

← [ย้อนกลับแผนการสอน: 01-lesson-plan.md](./01-lesson-plan.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ทำแบบทดสอบถัดไป: 03-quiz.md](./03-quiz.md) →
