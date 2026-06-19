# ปฏิบัติการ บทที่ 6: การสร้างระบบนำทางหน้าข้อมูลจุดท่องเที่ยวแบบไดนามิก (Lab)

ปฏิบัติการนี้จะฝึกทักษะการประยุกต์ใช้งานระบบจัดเส้นทางเดินหน้าจอด้วยโครงสร้างโฟลเดอร์และไฟล์ของ **Expo Router** โดยผู้เรียนจะได้ออกแบบแอปพลิเคชัน **แนะแนวแหล่งท่องเที่ยวออนไลน์ (Travel Guide & Destinations Directory)** ซึ่งเชื่อมโยงการทำงานแบบหน้าจอหลักเชื่อมสู่หน้ารายละเอียดแบบส่งผ่านค่าตัวแปรไดนามิกพารามิเตอร์ข้ามหน้าจอ

---

## 1. วัตถุประสงค์การเรียนรู้
1. สามารถออกแบบและตั้งค่าสถาปัตยกรรมระบบนำทางแบบซ้อนทับ (`Stack`) ด้วยไฟล์ `_layout.tsx`
2. สามารถเขียนฟังก์ชันนำทางไปยังจุดหมายต่าง ๆ โดยเรียกใช้ออบเจกต์คำสั่ง `router` 
3. สามารถกำหนดโครงสร้างแฟ้มงานในรูปแบบไดนามิกลิงก์ (`app/destination/[id].tsx`) เพื่อดักจับรับค่าพารามิเตอร์
4. สามารถเรียกใช้ Hook `useLocalSearchParams` เพื่อรับข้อมูลรหัสประจำเมืองและนำมาจัดทำเนื้อหาเฉพาะตัวสำเร็จ
5. สามารถอัปเดตสไตล์และข้อความแถบส่วนหัวบาร์ (Dynamic Header Options) ผ่านคอมโพเนนต์ `<Stack.Screen>`

---

## 2. โจทย์และข้อกำหนดปฏิบัติการ (Requirements)
ผู้เรียนจะต้องเขียนโค้ดจัดโครงสร้างระบบสตรีมนำทางภายใต้โฟลเดอร์หลัก `app/` ดังนี้:

```text
โครงสร้างโฟลเดอร์ปฏิบัติการ:
app/
├── _layout.tsx                     => เลย์เอาต์ Stack ควบคุมหลัก
├── index.tsx                       => หน้าหลักรวมการ์ดเมืองท่องเที่ยว (Home List Screen)
└── destination/
    └── [id].tsx                    => หน้ารายละเอียดท่องเที่ยวเจาะลึกเฉพาะเมือง (Dynamic details)
```

### รายละเอียดและเงื่อนไขการนำทาง:
1. **เลย์เอาต์หลัก (`app/_layout.tsx`):**
   * กำหนดให้เป็นระบบ `<Stack>` 
   * ตกแต่งบาร์ด้านบนให้เป็นเฉดสี Slate โทนน้ำเงินเข้ม (`#1e293b`) ตัวหนังสือสีขาว
   * เปิดระบบแสดงผลปุ่มย้อนกลับสีฟ้าสว่าง (`#38bdf8`) อัตโนมัติบนหน้าย่อย
2. **หน้าหลักรวมจุดท่องเที่ยว (`app/index.tsx`):**
   * มีคลังข้อมูลเมืองท่องเที่ยวเป็นอาร์เรย์ (เช่น Tokyo, Paris, New York) ประกอบด้วย ID ชื่อประเทศ และชื่อภาพ
   * แสดงรูปภาพเมืองและป้ายสั้นโดยจัดด้วย `FlatList`
   * เมื่อผู้เรียนกดคลิกสัมผัสการ์ดเมืองใด ๆ จะต้องทริกเกอร์เรียกคำสั่ง `router.push()` เพื่อนำทางไปยังหน้ารายละเอียดเมืองนั้น พร้อมระบุพ่วงส่ง ID และพารามิเตอร์ชื่อเมือง (Query string) ไปด้วย
3. **หน้ารายละเอียดจุดท่องเที่ยวแบบไดนามิก (`app/destination/[id].tsx`):**
   * ดักจับรหัส ID และตัวแปร Query จากเส้นทางด้วย Hook `useLocalSearchParams`
   * เปลี่ยนข้อความหัวข้อบาร์ด้านบนสุด (Header Title) ของหน้าจอให้กลายเป็น "ข้อมูลของเมือง: [ชื่อเมือง]" ไดนามิกอัตโนมัติด้วย `<Stack.Screen options={{ title: ... }} />`
   * แสดงรายละเอียดคำบรรยายและภาพเมืองนั้น ๆ
   * มีปุ่ม "ย้อนกลับหน้าหลัก" สไตล์โมเดิร์นคุมด้วย `Pressable` ที่จะกระตุ้นคำสั่ง `router.back()` ย้อนหน้ากลับ

---

## 3. ขั้นตอนการลงมือปฏิบัติ (Step-by-Step Tutorial)

### ขั้นตอนที่ 1: ตั้งค่าเลย์เอาต์นำทาง Stack หลักใน `app/_layout.tsx`
สร้างหรือแก้ไขไฟล์ `app/_layout.tsx` เพื่อนำเสนอรูปแบบแผนผังการจัดหน้าซ้อนสะสม (Stack):

```tsx
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: {
          backgroundColor: '#0f172a', // ธีมหัวข้อสีเข้ม
        },
        headerTintColor: '#38bdf8',   // ปุ่มกด Back สีฟ้านีออน
        headerTitleStyle: {
          fontWeight: 'bold',
          color: '#ffffff',           // ตัวหนังสือสีขาว
        },
        contentStyle: {
          backgroundColor: '#0f172a', // คุมสีพื้นหลังหน้าจอทั้งหมดใน Stack
        }
      }}
    >
      {/* หน้าแรกจะแสดงหัวข้อ "แหล่งท่องเที่ยวทั่วโลก" */}
      <Stack.Screen 
        name="index" 
        options={{ title: 'แหล่งท่องเที่ยวทั่วโลก' }} 
      />
      {/* ส่วนหน้าไดนามิกจะตั้งค่า title แบบยืดหยุ่นในไฟล์ตัวเอง */}
      <Stack.Screen 
        name="destination/[id]" 
        options={{ title: 'กำลังโหลดข้อมูลเมือง...' }} 
      />
    </Stack>
  );
}
```

---

### ขั้นตอนที่ 2: สร้างหน้าจอลิสต์เมืองท่องเที่ยวส่งตัวแปรไดนามิกใน `app/index.tsx`
ใช้คำสั่งนำเข้าจาก `expo-router` และเขียนจำลองปุ่มส่งตัวแปรลิงก์:

```tsx
import { View, Text, FlatList, Pressable, Image, StyleSheet } from 'react-native';
import { router } from 'expo-router';

// ชุดข้อมูลจำลองจุดท่องเที่ยว
const DESTINATIONS = [
  { id: '1', name: 'โตเกียว (Tokyo)', country: 'ประเทศญี่ปุ่น', image: 'https://images.unsplash.com/photo-1540959733332-eab4deceeaf7?w=300' },
  { id: '2', name: 'ปารีส (Paris)', country: 'ประเทศฝรั่งเศส', image: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=300' },
  { id: '3', name: 'นิวยอร์ก (New York)', country: 'สหรัฐอเมริกา', image: 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=300' },
];

export default function HomeList() {
  return (
    <View style={styles.container}>
      <FlatList
        data={DESTINATIONS}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <Pressable
            // สั่งนำทางแบบ Push ส่งค่า ID ไปที่ Path และพ่วงชื่อเมืองเป็น Query String
            onPress={() => router.push(`/destination/${item.id}?cityName=${item.name}`)}
            style={({ pressed }) => [
              styles.card,
              { opacity: pressed ? 0.95 : 1 }
            ]}
          >
            <Image source={{ uri: item.image }} style={styles.image} />
            <View style={styles.info}>
              <Text style={styles.title}>{item.name}</Text>
              <Text style={styles.subtitle}>{item.country}</Text>
            </View>
          </Pressable>
        )}
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  // รายละเอียดการจัดสไตล์คาร์ดจะรวมอยู่ในโค้ดเฉลยเต็ม
});
```

---

### ขั้นตอนที่ 3: รับค่าพารามิเตอร์และแสดงหน้าจอเฉพาะเมืองใน `app/destination/[id].tsx`
ดึงพารามิเตอร์มาจำลองข้อมูลเนื้อหาและการเซ็ตค่า Header อัตโนมัติ:

```tsx
import { useLocalSearchParams, router, Stack } from 'expo-router';
import { View, Text, Image, Pressable, StyleSheet } from 'react-native';

// คำบรรยายข้อมูลท่องเที่ยวจำลองแยกตาม ID
const DESTINATION_DETAILS: Record<string, { desc: string; rating: string; cover: string }> = {
  '1': { 
    desc: 'โตเกียว เมืองหลวงของญี่ปุ่น ผสมผสานความทันสมัยจากตึกระฟ้าและวัฒนธรรมโบราณจากวัดและศาลเจ้าได้อย่างลงตัว มีแหล่งช้อปปิ้งและอาหารเลิศรสรอคุณอยู่', 
    rating: '⭐ 4.9 / 5',
    cover: 'https://images.unsplash.com/photo-1540959733332-eab4deceeaf7?w=500'
  },
  '2': { 
    desc: 'ปารีส เมืองหลวงแห่งแฟชั่นและศิลปะของฝรั่งเศส เต็มไปด้วยสถาปัตยกรรมสุดคลาสสิก หอไอเฟล พิพิธภัณฑ์ลูฟร์ และบรรยากาศสุดโรแมนติกริมแม่น้ำแซน', 
    rating: '⭐ 4.8 / 5',
    cover: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=500'
  },
  '3': { 
    desc: 'นิวยอร์ก นครที่ไม่เคยหลับใหลของสหรัฐฯ แหล่งรวมความบันเทิงระดับโลก ไทม์สแควร์ เซ็นทรัลพาร์ก โรงละครบรอดเวย์ และความหลากหลายทางวัฒนธรรม', 
    rating: '⭐ 4.7 / 5',
    cover: 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=500'
  },
};

export default function DestinationDetail() {
  // ดักรับพารามิเตอร์ ID และตัวแปร Query String
  const { id, cityName } = useLocalSearchParams<{ id: string; cityName?: string }>();
  
  const detail = DESTINATION_DETAILS[id];

  if (!detail) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorText}>ไม่พบข้อมูลเมืองท่องเที่ยวนี้</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* ตั้งค่า Title บาร์ด้านบนตามชื่อเมืองที่รับมาแบบเรียลไทม์ */}
      <Stack.Screen options={{ title: cityName || 'รายละเอียดเมือง' }} />

      <Image source={{ uri: detail.cover }} style={styles.coverImage} />
      
      <View style={styles.content}>
        <Text style={styles.title}>{cityName}</Text>
        <Text style={styles.rating}>{detail.rating} คะแนนยอดนิยม</Text>
        <Text style={styles.desc}>{detail.desc}</Text>

        {/* ปุ่มกดย้อนกลับหน้าแรกจัดด้วย Pressable */}
        <Pressable 
          onPress={() => router.back()} 
          style={({ pressed }) => [
            styles.backButton,
            pressed ? styles.backButtonPressed : null
          ]}
        >
          <Text style={styles.backButtonText}>ย้อนกลับหน้าหลัก</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  // การจัดระยะสเปซจะแสดงในส่วนของเฉลยสมบูรณ์
});
```

---

## 4. โค้ดเฉลยฉบับสมบูรณ์ (Complete Solution)

ผู้เรียนสามารถนำข้อมูลชุดโค้ดเฉลยเต็มรูปแบบด้านล่างนี้แยกบันทึกตามเส้นทางไฟล์ของโปรเจกต์ เพื่อทดสอบการเปลี่ยนหน้าจอส่งผ่านพารามิเตอร์ที่สวยงามแบบเนทีฟ:

### 4.1 ซอร์สโค้ดไฟล์เลย์เอาต์: `app/_layout.tsx`
```tsx
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: {
          backgroundColor: '#0f172a',
        },
        headerTintColor: '#38bdf8',
        headerTitleStyle: {
          fontWeight: 'bold',
          color: '#ffffff',
        },
        contentStyle: {
          backgroundColor: '#0f172a',
        }
      }}
    >
      <Stack.Screen 
        name="index" 
        options={{ title: 'จุดหมายปลายทางยอดนิยม' }} 
      />
      <Stack.Screen 
        name="destination/[id]" 
        options={{ title: 'รายละเอียดสถานที่ท่องเที่ยว' }} 
      />
    </Stack>
  );
}
```

### 4.2 ซอร์สโค้ดหน้าหลักสารบัญเมือง: `app/index.tsx`
```tsx
import { View, Text, FlatList, Pressable, Image, StyleSheet } from 'react-native';
import { router } from 'expo-router';

const DESTINATIONS = [
  { id: '1', name: 'โตเกียว (Tokyo)', country: 'ประเทศญี่ปุ่น', image: 'https://images.unsplash.com/photo-1540959733332-eab4deceeaf7?w=300' },
  { id: '2', name: 'ปารีส (Paris)', country: 'ประเทศฝรั่งเศส', image: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=300' },
  { id: '3', name: 'นิวยอร์ก (New York)', country: 'สหรัฐอเมริกา', image: 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=300' },
];

export default function HomeList() {
  return (
    <View style={styles.container}>
      <Text style={styles.listHeader}>สำรวจเมืองในฝันของคุณ</Text>
      
      <FlatList
        data={DESTINATIONS}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <Pressable
            onPress={() => router.push(`/destination/${item.id}?cityName=${item.name}`)}
            style={({ pressed }) => [
              styles.card,
              { transform: [{ scale: pressed ? 0.98 : 1.0 }] }
            ]}
          >
            <Image source={{ uri: item.image }} style={styles.image} />
            <View style={styles.info}>
              <Text style={styles.title}>{item.name}</Text>
              <Text style={styles.subtitle}>{item.country}</Text>
            </View>
            <Text style={styles.arrowIcon}>chevron-right ➔</Text>
          </Pressable>
        )}
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
    paddingHorizontal: 16,
  },
  listHeader: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#94a3b8',
    marginVertical: 16,
  },
  list: {
    paddingBottom: 20,
  },
  card: {
    flexDirection: 'row',
    backgroundColor: '#1e293b',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 16,
    padding: 12,
    alignItems: 'center',
  },
  image: {
    width: 70,
    height: 70,
    borderRadius: 12,
    backgroundColor: '#334155',
  },
  info: {
    flex: 1,
    marginLeft: 16,
  },
  title: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  subtitle: {
    fontSize: 13,
    color: '#94a3b8',
    marginTop: 4,
  },
  arrowIcon: {
    color: '#38bdf8',
    fontSize: 12,
    fontWeight: 'bold',
    marginRight: 4,
  },
});
```

### 4.3 ซอร์สโค้ดหน้าแสดงผลละเอียดท่องเที่ยว: `app/destination/[id].tsx`
```tsx
import { useLocalSearchParams, router, Stack } from 'expo-router';
import { View, Text, Image, Pressable, StyleSheet, ScrollView } from 'react-native';

const DESTINATION_DETAILS: Record<string, { desc: string; rating: string; cover: string }> = {
  '1': { 
    desc: 'โตเกียว เมืองหลวงของญี่ปุ่น ผสมผสานความทันสมัยจากตึกระฟ้าและวัฒนธรรมโบราณจากวัดและศาลเจ้าได้อย่างลงตัว มีแหล่งช้อปปิ้งและอาหารเลิศรสรอคุณอยู่ ไม่ว่าจะเป็นการเดินชมย่านชิบูย่า พักผ่อนที่สวนอูเอโนะ หรือสัมผัสอาหารรสชาติแท้ๆ ในย่านชินจูกุ', 
    rating: '⭐ 4.9 / 5',
    cover: 'https://images.unsplash.com/photo-1540959733332-eab4deceeaf7?w=600'
  },
  '2': { 
    desc: 'ปารีส เมืองหลวงแห่งแฟชั่นและศิลปะของฝรั่งเศส เต็มไปด้วยสถาปัตยกรรมสุดคลาสสิก หอไอเฟล พิพิธภัณฑ์ลูฟร์ และบรรยากาศสุดโรแมนติกริมแม่น้ำแซน การเดินชมสตรีทคาเฟ่ที่มีกลิ่นอายย้อนยุคริมทาง ชิมครัวซองต์อบสดใหม่ และชมแสงสีวิจิตรในยามค่ำคืน', 
    rating: '⭐ 4.8 / 5',
    cover: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600'
  },
  '3': { 
    desc: 'นิวยอร์ก นครที่ไม่เคยหลับใหลของสหรัฐฯ แหล่งรวมความบันเทิงระดับโลก ไทม์สแควร์ เซ็นทรัลพาร์ก โรงละครบรอดเวย์ และความหลากหลายทางวัฒนธรรม ตลอดจนตึกเอ็มไพร์สเตตที่ตั้งตระหง่านท้าทายทุกสายตาผู้มาเยือนจากทั่วสารทิศ', 
    rating: '⭐ 4.7 / 5',
    cover: 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=600'
  },
};

export default function DestinationDetail() {
  const { id, cityName } = useLocalSearchParams<{ id: string; cityName?: string }>();
  
  const detail = DESTINATION_DETAILS[id];

  if (!detail) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorText}>ไม่พบข้อมูลเมืองท่องเที่ยวนี้</Text>
        <Pressable onPress={() => router.back()} style={styles.backButton}>
          <Text style={styles.backButtonText}>ย้อนกลับหน้าแรก</Text>
        </Pressable>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* ตั้งค่าหัวข้อหน้าจอแบบไดนามิกอิงตามชื่อเมือง */}
      <Stack.Screen options={{ title: cityName || 'รายละเอียดสถานที่' }} />

      <Image source={{ uri: detail.cover }} style={styles.coverImage} />
      
      <View style={styles.content}>
        <Text style={styles.title}>{cityName}</Text>
        <View style={styles.ratingBadge}>
          <Text style={styles.ratingText}>{detail.rating}</Text>
        </View>
        
        <Text style={styles.sectionTitle}>เกี่ยวกับสถานที่นี้</Text>
        <Text style={styles.desc}>{detail.desc}</Text>

        <Pressable 
          onPress={() => router.back()} 
          style={({ pressed }) => [
            styles.backButton,
            pressed ? styles.backButtonPressed : null
          ]}
        >
          <Text style={styles.backButtonText}>ย้อนกลับหน้าหลัก</Text>
        </Pressable>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#0f172a',
    padding: 20,
  },
  coverImage: {
    width: '100%',
    height: 250,
    backgroundColor: '#334155',
  },
  content: {
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  ratingBadge: {
    backgroundColor: '#1e293b',
    borderWidth: 1,
    borderColor: '#334155',
    alignSelf: 'flex-start',
    paddingVertical: 4,
    paddingHorizontal: 10,
    borderRadius: 8,
    marginTop: 8,
    marginBottom: 20,
  },
  ratingText: {
    color: '#fbbf24',
    fontSize: 13,
    fontWeight: 'bold',
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#38bdf8',
    marginBottom: 8,
  },
  desc: {
    fontSize: 15,
    color: '#cbd5e1',
    lineHeight: 24,
    marginBottom: 28,
  },
  backButton: {
    backgroundColor: '#38bdf8',
    height: 48,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 20,
  },
  backButtonPressed: {
    backgroundColor: '#0ea5e9',
  },
  backButtonText: {
    color: '#0f172a',
    fontSize: 16,
    fontWeight: 'bold',
  },
  errorText: {
    color: '#f43f5e',
    fontSize: 16,
    marginBottom: 20,
    fontWeight: 'bold',
  },
});
```

---

← [ย้อนกลับแบบทดสอบ: 03-quiz.md](./03-quiz.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ศึกษาบทเรียนถัดไป: บทที่ 7](../chapter-07-styling-icons-images/) →
