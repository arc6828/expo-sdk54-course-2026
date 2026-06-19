# ปฏิบัติการ บทที่ 7: การสร้างการ์ดโปรไฟล์พรีเมียมรองรับระบบสลับธีม (Lab)

ปฏิบัติการนี้จะฝึกทักษะการประยุกต์ใช้งานสไตล์ระดับสูงในระบบ React Native โดยผู้เรียนจะได้ออกแบบแอปพลิเคชันหน้า **แดชบอร์ดการ์ดโปรไฟล์ระดับพรีเมียม (Premium Profile Card Dashboard)** ที่โหลดฟอนต์พิเศษมาใช้งาน ตกแต่งจุดทับซ้อนไอคอนแบบสไตล์สัมบูรณ์ (`absolute`) โหลดรูปภาพโปรไฟล์ผ่านไลบรารี `expo-image` พร้อมรองรับการแสดงเฉดสีพรีวิวด้วยรหัส Blurhash และการรองรับโหมดมืด (Dark Mode) ตามเครื่องปลายทาง

---

## 1. วัตถุประสงค์การเรียนรู้
1. สามารถประยุกต์ใช้พิกัดตำแหน่งสัมบูรณ์ `position: 'absolute'` ในการวางเครื่องหมายออนไลน์ (Online Status Badge) บนรูปภาพโปรไฟล์
2. สามารถติดตั้ง โหลด และใช้งานแบบอักษรพิเศษ (Custom Fonts) ผ่านระบบของ `expo-font` ร่วมกับการใช้ `expo-splash-screen`
3. สามารถดึงและจัดสไตล์สัญลักษณ์เวกเตอร์ไอคอนด้วยไลบรารี `@expo/vector-icons`
4. สามารถเพิ่มประสิทธิภาพและความลื่นไหลการโหลดภาพโปรไฟล์ด้วย `expo-image` พร้อมกำหนดค่า `placeholder` (Blurhash) และการเฟดภาพด้วย `transition`
5. สามารถดักเช็คและประยุกต์ใช้โทนสีกราฟิกตามธีมสว่างหรือธีมมืด (Dark Mode) ด้วย `useColorScheme` Hook

---

## 2. โจทย์และข้อกำหนดปฏิบัติการ (Requirements)

ผู้เรียนต้องสร้างโครงสร้างคอมโพเนนต์การ์ดโปรไฟล์ส่วนตัว (Profile Dashboard Screen) ที่มีเงื่อนไขดังต่อไปนี้:

1. **การโหลดทรัพยากรระบบ (Assets Loading):**
   * โหลดฟอนต์จำนวน 2 รูปแบบ ได้แก่ `Prompt-Regular` (สำหรับเนื้อหาทั่วไป) และ `Prompt-Bold` (สำหรับชื่อโปรไฟล์และหัวข้อสำคัญ)
   * แสดงหน้า Splash Screen ค้างไว้ และสั่งเปิดเผยหน้าแอปเมื่อโหลดฟอนต์เสร็จเท่านั้น หากเกิดข้อผิดพลาดในการโหลดไฟล์ฟอนต์ ต้องยกเลิกหน้า Splash เพื่อป้องกันหน้าจอค้างตลอดกาล
2. **การจัดอินเทอร์เฟซโปรไฟล์พรีเมียม (Premium Interface Layout):**
   * **กรอบภาพโปรไฟล์ (Avatar Container):** รันรูปวงกลมด้วย `expo-image` ดึงภาพจากลิงก์เน็ตเวิร์ก โดยตั้งค่า `placeholder` เป็นรหัส Blurhash และใช้ความเร็ว `transition` เท่ากับ 500 มิลลิวินาที
   * **เครื่องหมายบอกสถานะการใช้งาน (Status Badge):** วางวงกลมสีเขียวนีออน (`#22c55e`) ขนาดเล็กระบุ "Online" ทับซ้อนลงบนมุมขวาล่างของรูปภาพวงกลมโปรไฟล์หลักด้วย `position: 'absolute'`
   * **ข้อมูลส่วนตัว:** แสดงชื่อจริง ยศตำแหน่งงาน และประวัติสั้น ๆ โดยเรียกใช้ตระกูลอักษร `Prompt-Bold` และ `Prompt-Regular`
3. **ตารางชุดปุ่มคำสั่งด่วน (Action Grid):**
   * แสดงชุดปุ่มแบบการ์ดขนาดเล็ก 3 ช่อง ได้แก่ "ส่งอีเมล", "ส่งข้อความ" และ "แชร์ข้อมูล"
   * ในการ์ดย่อยแต่ละตัวให้เรียกสัญลักษณ์เวกเตอร์มาจาก `@expo/vector-icons` เช่น `mail`, `message-square`, `share-2`
4. **การสลับสไตล์ตามระบบเครื่อง (Theme Support):**
   * ดึงสถานะธีมด้วย `useColorScheme()`
   * หากระบบปฏิบัติการเป็นโหมดสว่าง (Light Theme) ให้ใช้สีพื้นหลังเป็น `#f8fafc` ตัวการ์ดสี `#ffffff` ตัวหนังสือสีเข้ม `#0f172a`
   * หากระบบปฏิบัติการเป็นโหมดมืด (Dark Theme) ให้ใช้สีพื้นหลังเป็น `#0f172a` ตัวการ์ดสี `#1e293b` ตัวหนังสือสีขาว `#ffffff` และขอบสี `#334155`

---

## 3. ขั้นตอนการลงมือปฏิบัติ (Step-by-Step Tutorial)

### ขั้นตอนที่ 1: ติดตั้งไลบรารีและจัดสรรทรัพยากรฟอนต์
เรียกใช้คำสั่งเพื่อติดตั้งไลบรารีหลักทั้งหมดในโฟลเดอร์โปรเจกต์:
```bash
npx expo install expo-font expo-splash-screen expo-image
```
*หมายเหตุ: ตรวจสอบให้แน่ใจว่าได้จัดเตรียมไฟล์ฟอนต์ `Prompt-Regular.ttf` และ `Prompt-Bold.ttf` บันทึกเก็บไว้ที่ไดเรกทอรี `assets/fonts/` ของแอปพลิเคชัน*

### ขั้นตอนที่ 2: โครงสร้างนำเข้าโมดูลและเริ่มหน่วงเวลา Splash Screen
เขียนเริ่มการโหลดฟอนต์ในหน้าแรกสุด:
```tsx
import { useEffect } from 'react';
import { View, Text, StyleSheet, useColorScheme, Pressable } from 'react-native';
import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';
import { Image } from 'expo-image';
import { Feather } from '@expo/vector-icons';

// ตรึงหน้ารูปภาพโลโก้ไว้ก่อนรอข้อมูลแบบอักษรเสร็จสิ้น
SplashScreen.preventAutoHideAsync();
```

### ขั้นตอนที่ 3: ออกแบบสเตตัส Badge ลอยสัมบูรณ์ทับบน Avatar
กำหนดรูปสไตล์รูปภาพให้มีกรอบความกว้างและสูงเป็นวงกลม และใช้ `absolute` ปักหมุดลูกด้านล่าง:
```tsx
// กล่องครอบรูปวงกลมมีพิกัดเป็น relative
<View style={styles.avatarWrapper}>
  <Image
    source="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400"
    placeholder={{ blurhash: 'LKN]~^%hS$of9G-pB%-;U_RPn%s:' }}
    style={styles.avatar}
    transition={500}
  />
  {/* จุดวงกลมออนไลน์วางปักหมุดไว้ที่มุมขวาล่าง */}
  <View style={styles.onlineBadge} />
</View>
```

---

## 4. โค้ดเฉลยฉบับสมบูรณ์ (Complete Solution)

ผู้เรียนสามารถนำโค้ดเฉลยเต็มระบบชุดนี้ไปบันทึกทับในไฟล์หลักของแอปพลิเคชันเพื่อใช้ทดสอบ โดยสลับการตั้งค่าโหมดหน้าจอมือถือจำลอง (Simulator) ไปมาระหว่าง Light และ Dark Mode เพื่อตรวจผลลัพธ์:

```tsx
import { useEffect } from 'react';
import { StyleSheet, Text, View, useColorScheme, Pressable, ScrollView, SafeAreaView } from 'react-native';
import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';
import { Image } from 'expo-image';
import { Feather, Ionicons } from '@expo/vector-icons';

// 1. ตรึงหน้า Splash Screen ไม่ให้หายไปกะทันหันก่อนดาวน์โหลดฟอนต์เสร็จ
SplashScreen.preventAutoHideAsync();

export default function App() {
  // 2. เรียกใช้งานระบบโหลดฟอนต์ไทยยอดนิยม (Prompt)
  const [fontsLoaded, error] = useFonts({
    'Prompt-Regular': require('../../assets/fonts/Prompt-Regular.ttf'),
    'Prompt-Bold': require('../../assets/fonts/Prompt-Bold.ttf'),
  });

  useEffect(() => {
    // 3. ทันทีที่โหลดฟอนต์พร้อม (หรือตรวจพบ Error) ให้ทำการซ่อน Splash Screen
    if (fontsLoaded || error) {
      SplashScreen.hideAsync();
    }
  }, [fontsLoaded, error]);

  // 4. หากฟอนต์ยังเรนเดอร์ไม่เสร็จสิ้น ให้รอชั่วขณะ
  if (!fontsLoaded && !error) {
    return null;
  }

  // 5. ดักจับเฉดสีธีมเครื่องปลายทางด้วย Hook
  const colorScheme = useColorScheme();
  const isDark = colorScheme === 'dark';

  // 6. กำหนดชุดคู่สีให้ปรับเปลี่ยนตามสเตตัสเครื่อง
  const theme = {
    background: isDark ? '#0f172a' : '#f8fafc',
    cardBackground: isDark ? '#1e293b' : '#ffffff',
    textPrimary: isDark ? '#ffffff' : '#0f172a',
    textSecondary: isDark ? '#94a3b8' : '#64748b',
    borderColor: isDark ? '#334155' : '#e2e8f0',
    primaryColor: '#38bdf8',
  };

  return (
    <SafeAreaView style={[styles.safeArea, { backgroundColor: theme.background }]}>
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        {/* หัวข้อด้านบนสุด */}
        <View style={styles.header}>
          <Text style={[styles.headerTitle, { color: theme.textPrimary }]}>แดชบอร์ดส่วนตัว</Text>
          <Text style={[styles.headerSubtitle, { color: theme.textSecondary }]}>Premium Profile Card</Text>
        </View>

        {/* การ์ดโปรไฟล์หลัก */}
        <View style={[styles.profileCard, { backgroundColor: theme.cardBackground, borderColor: theme.borderColor }]}>
          
          {/* ส่วนกรอบตกแต่งรูปวงกลมด้วยสไตล์สัมบูรณ์ */}
          <View style={styles.avatarContainer}>
            <View style={styles.avatarWrapper}>
              <Image
                source="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400"
                placeholder={{ blurhash: 'LKN]~^%hS$of9G-pB%-;U_RPn%s:' }}
                style={styles.avatar}
                contentFit="cover"
                transition={500}
              />
              {/* สไตล์ Absolute วางทับมุมโปรไฟล์ด้านล่างขวา */}
              <View style={[styles.statusBadge, { borderColor: theme.cardBackground }]} />
            </View>
          </View>

          {/* รายละเอียดข้อความจำลองโปรไฟล์ */}
          <Text style={[styles.profileName, { color: theme.textPrimary }]}>ชนิดาภา รัตนพิมล</Text>
          <Text style={[styles.profileRole, { color: theme.primaryColor }]}>Lead UX/UI Designer</Text>
          <Text style={[styles.profileBio, { color: theme.textSecondary }]}>
            ชื่นชอบการออกแบบโมบายแอปพลิเคชันระดับพรีเมียม สนุกกับการพัฒนาอินเทอร์เฟซด้วยสไตล์อนิเมชันลื่นไหลและดีไซน์โหมดมืดแสนดึงดูดสายตา
          </Text>

          {/* แถบเส้นขีดคั่นกลางของการ์ด */}
          <View style={[styles.divider, { backgroundColor: theme.borderColor }]} />

          {/* สถิติตัวเลขย่อ */}
          <View style={styles.statsRow}>
            <View style={styles.statCol}>
              <Text style={[styles.statNumber, { color: theme.textPrimary }]}>48</Text>
              <Text style={[styles.statLabel, { color: theme.textSecondary }]}>โครงการ</Text>
            </View>
            <View style={styles.statCol}>
              <Text style={[styles.statNumber, { color: theme.textPrimary }]}>12.4K</Text>
              <Text style={[styles.statLabel, { color: theme.textSecondary }]}>ผู้ติดตาม</Text>
            </View>
            <View style={styles.statCol}>
              <Text style={[styles.statNumber, { color: theme.textPrimary }]}>150</Text>
              <Text style={[styles.statLabel, { color: theme.textSecondary }]}>รีวิวดีเยี่ยม</Text>
            </View>
          </View>
        </View>

        {/* เมนูการ์ดคำสั่งปุ่มสัมผัส (Action Grid) */}
        <View style={styles.actionGrid}>
          <Pressable style={[styles.actionCard, { backgroundColor: theme.cardBackground, borderColor: theme.borderColor }]}>
            <View style={[styles.iconCircle, { backgroundColor: '#e0f2fe' }]}>
              <Feather name="mail" size={20} color="#0284c7" />
            </View>
            <Text style={[styles.actionLabel, { color: theme.textPrimary }]}>ส่งอีเมล</Text>
          </Pressable>

          <Pressable style={[styles.actionCard, { backgroundColor: theme.cardBackground, borderColor: theme.borderColor }]}>
            <View style={[styles.iconCircle, { backgroundColor: '#f0fdf4' }]}>
              <Ionicons name="chatbubble-ellipses-outline" size={20} color="#16a34a" />
            </View>
            <Text style={[styles.actionLabel, { color: theme.textPrimary }]}>ส่งข้อความ</Text>
          </Pressable>

          <Pressable style={[styles.actionCard, { backgroundColor: theme.cardBackground, borderColor: theme.borderColor }]}>
            <View style={[styles.iconCircle, { backgroundColor: '#fdf2f8' }]}>
              <Feather name="share-2" size={20} color="#db2777" />
            </View>
            <Text style={[styles.actionLabel, { color: theme.textPrimary }]}>แชร์ข้อมูล</Text>
          </Pressable>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
  scrollContainer: {
    padding: 24,
  },
  header: {
    marginBottom: 24,
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 24,
    fontFamily: 'Prompt-Bold',
  },
  headerSubtitle: {
    fontSize: 14,
    fontFamily: 'Prompt-Regular',
    marginTop: 4,
  },
  profileCard: {
    borderRadius: 24,
    padding: 24,
    alignItems: 'center',
    borderWidth: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 10,
    elevation: 5,
  },
  avatarContainer: {
    marginBottom: 16,
  },
  avatarWrapper: {
    position: 'relative', // วางเพื่อรองรับพิกัด Absolute ของ Badge ลูก
  },
  avatar: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#cbd5e1',
  },
  statusBadge: {
    position: 'absolute', // หลุดออกจากโฟลว์เพื่อทับซ้อนมุมโปรไฟล์
    bottom: 2,
    right: 2,
    width: 22,
    height: 22,
    borderRadius: 11,
    backgroundColor: '#22c55e', // สีเขียวนีออนบอกสถานะ Online
    borderWidth: 3,            // เติมขอบตัดเพื่อป้องกันการกลืนสี
  },
  profileName: {
    fontSize: 20,
    fontFamily: 'Prompt-Bold',
    marginBottom: 4,
  },
  profileRole: {
    fontSize: 14,
    fontFamily: 'Prompt-Bold',
    marginBottom: 16,
  },
  profileBio: {
    fontSize: 14,
    fontFamily: 'Prompt-Regular',
    textAlign: 'center',
    lineHeight: 22,
    marginBottom: 20,
  },
  divider: {
    height: 1,
    width: '100%',
    marginBottom: 20,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
  },
  statCol: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 18,
    fontFamily: 'Prompt-Bold',
  },
  statLabel: {
    fontSize: 12,
    fontFamily: 'Prompt-Regular',
    marginTop: 2,
  },
  actionGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 20,
  },
  actionCard: {
    flex: 1,
    marginHorizontal: 4,
    borderRadius: 16,
    paddingVertical: 16,
    alignItems: 'center',
    borderWidth: 1,
  },
  iconCircle: {
    width: 44,
    height: 44,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  actionLabel: {
    fontSize: 13,
    fontFamily: 'Prompt-Regular',
  },
});
```

---

## 5. การวิเคราะห์สรุปผลการประเมินปฏิบัติการ

เมื่อรันโครงการสำเร็จ ให้ผู้เรียนประเมินตรวจสอบเกณฑ์การตรวจวัดดังนี้:
1. ฟอนต์ของตัวอักษรทั้งหมดในแอปพลิเคชันต้องใช้แบบอักษร `Prompt` และ Splash Screen ต้องซ่อนอย่างสมบูรณ์โดยที่ไม่มีการแจ้งพังหรือค้างหน้าจอขาว
2. รูปภาพแสดงผลโปรไฟล์คมชัด ลื่นไหลไม่กะพริบตา และเล่นเอฟเฟกต์เฟดตอนเริ่มหน้าจอ
3. เมื่อเข้าที่ส่วนตั้งค่าเปลี่ยนธีมของเครื่องให้เป็น Dark Mode องค์ประกอบหน้าจอทั้งหมดต้องสับสีดำสลัวโดยอัตโนมัติ

---

← [ย้อนกลับแบบทดสอบ: 03-quiz.md](./03-quiz.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ศึกษาบทเรียนถัดไป: บทที่ 8](../chapter-08-storage-api/) →
