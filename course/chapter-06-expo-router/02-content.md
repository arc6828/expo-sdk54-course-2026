# บทที่ 6: ระบบนำทางและสถาปัตยกรรมการเปลี่ยนหน้าจอด้วย Expo Router (Content)

ในอดีต การจัดการระบบนำทาง (Navigation) ใน React Native ต้องอาศัยไลบรารี React Navigation ซึ่งมีความซับซ้อนในการตั้งค่าแผนผังหน้าจอ แต่สำหรับ **Expo Router** (เปิดตัวแบบสมบูรณ์ใน Expo SDK 54 / Router v6) ได้นำเสนอแนวคิดใหม่ที่เรียกว่า **File-based Routing** ซึ่งถอดแบบมาจากสถาปัตยกรรมระดับอุตสาหกรรมอย่าง Next.js บนฝั่งเว็บ ช่วยให้นักพัฒนาสร้างและบริหารเส้นทางเดินหน้าจอผ่านโครงสร้างโฟลเดอร์ได้อย่างสะดวก รวดเร็ว และลื่นไหล

---

## 6.1 แนวคิดการจัดเส้นทางแบบอิงโครงสร้างไฟล์ (File-based Routing)

File-based Routing คือการแปลงตำแหน่งเส้นทางของไฟล์ (File Paths) ในโฟลเดอร์พิเศษที่ตั้งชื่อว่า **`app/`** ให้กลายมาเป็นเส้นทางการนำทาง (Route Paths) ของแอปพลิเคชันโดยอัตโนมัติ:

```text
โครงสร้างในโฟลเดอร์ app/               URL / เส้นทางเข้าถึง
app/
├── index.tsx                         =>  "/" (หน้าแรกสุดของแอป)
├── profile.tsx                       =>  "/profile" (หน้าโปรไฟล์)
└── settings/
    └── index.tsx                     =>  "/settings" (หน้าตั้งค่า)
```

เมื่อคุณเพิ่มไฟล์ใหม่เข้าไปในโฟลเดอร์ `app/` ตัวระบบรวบรวมของ Expo (Metro Bundler) จะดักตรวจและเปิดใช้แผนที่นำทางนั้น ๆ ขึ้นมาโดยที่คุณไม่จำเป็นต้องมาเขียนโค้ดเพิ่มหน้าลงในอาเรย์การลงทะเบียนแต่อย่างใด

---

## 6.2 การสร้าง Layout และการจัดระเบียบโครงสร้างด้วย _layout.tsx

ไฟล์ที่ชื่อว่า **`_layout.tsx`** ถือเป็นชิ้นส่วนควบคุมพิเศษใน Expo Router มีบทบาทสำคัญในการ:
1. กำหนดรูปแบบเลย์เอาต์หลักของแอป เช่น หน้าจอเรียงซ้อน (Stack) หรือ หน้าจอแบบแท็บบาร์ (Tabs)
2. ห่อหุ้มและแชร์ส่วนหน้าตาร่วมกัน (Shared UI) เช่น แถบสถานะ หรือแถบนำทางหลัก
3. จัดการพฤติกรรมความปลอดภัยและการปกป้องการเข้าถึงหน้าจอ (เช่น ระบบ Auth Guards)

ถ้าเราบันทึกไฟล์ `_layout.tsx` ไว้ที่ระดับบนสุดของโฟลเดอร์ `app/` สไตล์ของเลย์เอาต์นั้นจะคลุมทุกไฟล์ย่อยที่อยู่ภายใต้โฟลเดอร์นั้นทั้งหมด

---

## 6.3 ระบบนำทางแบบสะสมประวัติ (Stack Navigation)

เลย์เอาต์แบบ **`Stack`** คือระบบจัดการนำหน้าจอที่จำลองการวางซ้อนข้อมูลแผ่นการ์ดจากล่างขึ้นบน (Push/Pop Screen):
* เมื่อเปิดหน้าใหม่ หน้าจอใหม่จะถูกดันซ้อนทับอยู่ด้านบนสุดของหน้าเก่า (Push)
* เมื่อกดปุ่มย้อนกลับ (Back) หน้าบนสุดจะถูกดึงทิ้งออกไปเพื่อกลับมาโชว์หน้าจอด้านล่าง (Pop)

### 1. วิธีประกาศเลย์เอาต์ Stack ใน `_layout.tsx`
เราเรียกใช้คอมโพเนนต์ `<Stack>` เพื่อสร้างโครงสร้างการนำทางแบบซ้อนทับ:

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router';

export default function Layout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: { backgroundColor: '#0f172a' }, // แต่งสีแถบหัวข้อเข้ม
        headerTintColor: '#ffffff', // สีตัวหนังสือปุ่มย้อนกลับ
        headerTitleStyle: { fontWeight: 'bold' },
      }}
    >
      {/* ระบุตั้งค่าสไตล์เฉพาะหน้าจอผ่าน Stack.Screen */}
      <Stack.Screen name="index" options={{ title: 'หน้าหลักเดสก์ท็อป' }} />
      <Stack.Screen name="profile" options={{ title: 'โปรไฟล์ของคุณ' }} />
    </Stack>
  );
}
```

---

## 6.4 ระบบนำทางแบบแท็บบาร์ล่าง (Tab Navigation)

เลย์เอาต์แบบ **`Tabs`** จัดสรรความสามารถยอดนิยมในการควบคุมเปลี่ยนโหมดหลักของแอปพลิเคชันผ่านเมนูปุ่มกดสัมผัสด้านล่างสุดของจอ:

### 1. วิธีสร้างเลย์เอาต์ Tabs ใน `app/_layout.tsx`
ใช้คำสั่งนำเข้าจาก `expo-router` และจัดวางไอคอนสไตล์:

```tsx
// app/_layout.tsx
import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons'; // โหลดไอคอนมาตรฐาน

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#38bdf8', // สีเมนูขณะถูกคลิกเลือก
        tabBarInactiveTintColor: '#94a3b8',
        tabBarStyle: { backgroundColor: '#0f172a' },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'หน้าหลัก',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="home" color={color} size={size} />
          ),
        }}
      />
      <Tabs.Screen
        name="settings"
        options={{
          title: 'ตั้งค่า',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="settings" color={color} size={size} />
          ),
        }}
      />
    </Tabs>
  );
}
```

---

## 6.5 การเชื่อมโยงลิงก์และเปลี่ยนหน้าจอ (Link & Router Object)

ใน Expo Router มี 2 วิธีหลักในการสั่งนำทางเปลี่ยนหน้าจอ:

### 1. การนำทางแบบประกาศผ่านคอมโพเนนต์ `<Link>` (Declarative Navigation)
เหมาะอย่างยิ่งสำหรับข้อความ ตัวหนังสือ หรือปุ่มสัมผัสสเตติกทั่วไป โดยส่งพาธปลายทางผ่านพร็อพส์ `href`:
```tsx
import { Link } from 'expo-router';

export default function HomeScreen() {
  return (
    <View>
      <Link href="/profile" asChild>
        {/* asChild สั่งให้ Link ไปคุมคุณสมบัติสัมผัสของคอมโพเนนต์ลูกย่อย */}
        <Pressable><Text>เข้าหน้าโปรไฟล์</Text></Pressable>
      </Link>
    </View>
  );
}
```

### 2. การสั่งการนำทางด้วยเหตุการณ์ JavaScript ผ่าน `router` (Imperative Navigation)
กรณีต้องการประมวลผลโลจิกสำเร็จก่อนนำทาง เช่น เช็คว่าผู้ใช้กรอกฟอร์มเสร็จแล้ว หรือดึงบันทึกสำเร็จ จึงค่อยย้ายหน้า:
* **`router.push('/path')`**: ผลักหน้าจอใหม่ทับซ้อนบนสแต็ค (ผู้ใช้ย้อนกลับได้)
* **`router.replace('/path')`**: ล้างหน้าจอปัจจุบันออกและสวมทับหน้าใหม่ (ใช้บ่อยในระบบ Auth ล็อกอินสำเร็จแล้วไม่ให้กดย้อนกลับมาหน้ารับค่าอีก)
* **`router.back()`**: ย้อนกลับหน้าจอก่อนหน้า 1 ระดับ

```tsx
import { router } from 'expo-router';
import { Pressable, Text } from 'react-native';

export default function LoginButton() {
  const handleLogin = () => {
    // สมมติล็อกอินสำเร็จแล้ว
    router.replace('/dashboard'); // เปลี่ยนแบบแทนที่หน้าเดิมทันที
  };

  return (
    <Pressable onPress={handleLogin}>
      <Text>ยืนยันการเข้าสู่ระบบ</Text>
    </Pressable>
  );
}
```

---

## 6.6 เส้นทางนำทางแบบไดนามิกและการอ่านค่าพารามิเตอร์ (Dynamic Routes & useLocalSearchParams)

ในกรณีที่หน้าจอต้องการรับตัวแปร ID เพื่อไปยิงต่อค้นหารายละเอียดสินค้าเฉพาะชิ้น (เช่น หน้ารายละเอียดข่าว ID 125) เราใช้เทคนิคการตั้งชื่อไฟล์แบบใส่เครื่องหมายวงเล็บเหลี่ยม **`[id].tsx`** เพื่อกำหนดเป็น Dynamic Route

### 1. วิธีจัดเก็บโครงสร้างไฟล์ไดนามิก
```text
app/
├── index.tsx                         (หน้ารวมข่าวสาร)
└── news/
    └── [id].tsx                      (หน้าอ่านข่าวเฉพาะชิ้น)
```

### 2. วิธีสั่งลิงก์นำทางส่งตัวแปร (Navigation with Parameters)
เราส่งพาธไดนามิกแนบข้อมูลพารามิเตอร์ไปได้โดยตรง:
```tsx
// นำทางไปยังแอปหน้าอ่านข่าวรหัส 45
router.push('/news/45');

// หรือส่งผ่านพารามิเตอร์สไตล์ Query String เพิ่มเติม
router.push('/news/45?author=Somchai');
```

### 3. วิธีการดักจับค่าตัวแปรในหน้าปลายทางด้วย `useLocalSearchParams`
ภายในไฟล์ย่อย `app/news/[id].tsx` เราจะดึงข้อมูลตัวแปรจากพารามิเตอร์ทรานสิทผ่านมาด้วย `useLocalSearchParams` Hook:

```tsx
// app/news/[id].tsx
import { useLocalSearchParams, router } from 'expo-router';
import { View, Text, Button, StyleSheet } from 'react-native';

export default function NewsDetailScreen() {
  // ดักจับค่า id และพารามิเตอร์ author ที่ส่งผ่านเส้นทาง URL
  const { id, author } = useLocalSearchParams<{ id: string; author?: string }>();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>รายละเอียดข่าวสารรหัส: #{id}</Text>
      {author && <Text style={styles.authorText}>ผู้เขียน: {author}</Text>}
      
      <Button title="กลับหน้าแรก" onPress={() => router.back()} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#0f172a',
  },
  title: {
    fontSize: 20,
    color: '#ffffff',
    fontWeight: 'bold',
    marginBottom: 8,
  },
  authorText: {
    fontSize: 14,
    color: '#38bdf8',
    marginBottom: 20,
  },
});
```

## 6.7 สรุปท้ายบทเรียน

**แนวคิดการจัดเส้นทางแบบอิงโครงสร้างไฟล์:** ระบบนำทางยุคใหม่ใน Expo SDK 54 ใช้สถาปัตยกรรมแบบ File-based Routing ผ่าน Expo Router v6 โดยความสะดวกคือระบบจะแปลงพาธตำแหน่งโครงสร้างไฟล์ภายใต้โฟลเดอร์ app/ ให้กลายเป็นเส้นทางการเปลี่ยนหน้าตาแอปพลิเคชัน (URL Routes) โดยอัตโนมัติ ช่วยลดความยุ่งยากในการลงทะเบียนโค้ดแบบดั้งเดิม

**การสร้าง Layout และการจัดระเบียบโครงสร้างด้วย _layout.tsx:** ไฟล์ _layout.tsx เป็นกลไกศูนย์กลางเฉพาะของระบบมีประโยชน์ในด้านการควบคุมหน้าตาหลักของแอป เช่น หน้าจอ Stack หรือ หน้าจอแท็บบาร์ (Tabs) โดยทำหน้าที่เป็นโครงสร้างห่อหุ้มอินเทอร์เฟซส่วนกลาง (Shared UI) และช่วยจัดระเบียบความปลอดภัยในการกรองผู้เข้าใช้งานหน้าจอต่าง ๆ ได้อย่างเป็นระบบ

**ระบบนำทางแบบสะสมประวัติ (Stack Navigation):** โครงสร้าง Stack Navigation จำลองการนำทางในรูปแบบการวางแผ่นการ์ดซ้อนทับกัน (Push/Pop Screen) เมื่อเปิดหน้าจอใหม่จะนำหน้าต่างใหม่ไปทับแผ่นเก่า และเมื่อกดย้อนกลับหน้าจอด้านบนจะถูกดึงออกเพื่อกลับลงไปแสดงแผ่นถัดลงไป โดยเราเรียกนำเข้าคอมโพเนนต์ `<Stack>` และปรับแต่งคุณสมบัติต่าง ๆ ในหน้า _layout.tsx

**ระบบนำทางแบบแท็บบาร์ล่าง (Tab Navigation):** เลย์เอาต์แบบ Tabs เป็นการสร้างเมนูนำทางหลักสัมผัสด้านล่างสุดของสมาร์ทโฟนสำหรับสลับหมวดหลักของแอปพลิเคชันอย่างรวดเร็ว โดยสร้าง _layout.tsx แยกตามโฟลเดอร์ของกลุ่มงานและเรียกใช้คอมโพเนนต์ `<Tabs>` ร่วมกับ `<Tabs.Screen>` เพื่อระบุไอคอนและสไตล์สีเมื่อปุ่มทำงานหรือว่างเปล่าได้ตามที่ออกแบบไว้

**การเชื่อมโยงลิงก์และเปลี่ยนหน้าจอ:** การเปลี่ยนหน้าทำได้ 2 แนวทาง ได้แก่ การใช้คอมโพเนนต์ `<Link>` ร่วมกับพร็อพส์ href สำหรับการกดเชื่อมโยงทั่วไป และการใช้คำสั่ง JavaScript สั่งเปลี่ยนหน้าผ่านออบเจกต์ router (เช่น router.push สำหรับผลักหน้าจอขึ้นสแต็ค, router.replace เพื่อการข้ามหน้าแบบลบหน้าเดิมทิ้ง และ router.back สำหรับย้อนกลับหน้าเดิม)

**เส้นทางนำทางแบบไดนามิกและการอ่านค่าพารามิเตอร์:** สำหรับหน้าที่ต้องการรับตัวแปรระบุ ID เฉพาะ เราจะใช้การตั้งชื่อไฟล์แบบใส่เครื่องหมายวงเล็บเหลี่ยม เช่น [id].tsx เพื่อกำหนดเป็น Dynamic Route ซึ่งสามารถส่งผ่านพารามิเตอร์และตัวแปรผ่านเส้นทาง URL ได้อย่างอิสระ และฝั่งหน้าปลายทางจะดักจับข้อมูลเหล่านั้นมาใช้งานได้สะดวกผ่าน useLocalSearchParams Hook

---

← [ย้อนกลับแผนการสอน: 01-lesson-plan.md](./01-lesson-plan.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ทำแบบทดสอบถัดไป: 03-quiz.md](./03-quiz.md) →
