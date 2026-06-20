# บทที่ 7: การตกแต่งอินเทอร์เฟซ ไอคอน และรูปภาพประสิทธิภาพสูง (Content)

การออกแบบประสบการณ์ผู้ใช้งาน (User Experience - UX) ที่ดีไม่ได้ขึ้นอยู่กับฟังก์ชันการทำงานที่ครบถ้วนเพียงอย่างเดียว แต่ยังขึ้นอยู่กับความลื่นไหล ความเร็วในการจัดแสดงรูปภาพ และความกลมกลืนของการออกแบบดีไซน์ ในบทเรียนนี้เราจะศึกษาเชิงลึกเกี่ยวกับการควบคุมสไตล์ขั้นสูงด้วยระบบจัดตำแหน่ง `absolute`, การโหลดแบบอักษรพิเศษ (Custom Fonts), การเรียกใช้งานชุดเวกเตอร์ไอคอน และการเพิ่มประสิทธิภาพการแสดงภาพด้วย `expo-image` รวมถึงระบบปรับสีตามธีมของตัวเครื่อง (Dark Mode)

---

## 7.1 ระบบพิกัดตำแหน่งสัมพัทธ์และสัมบูรณ์ (Relative and Absolute Positioning)

ในการจัดองค์ประกอบหน้าจอบน React Native ค่าเริ่มต้นของสไตล์ `position` จะเป็น `'relative'` (พิกัดตำแหน่งสัมพัทธ์) ซึ่งสอดคล้องกับการวางตัวตนต่อท้ายกันตามทิศทางของ Flexbox แต่สำหรับการออกแบบ UI ยุคใหม่ เช่น การทำเครื่องหมายแจ้งเตือน (Notification Badge) ทับบนไอคอน หรือการวางปุ่มลอย (Floating Action Button) ค้างไว้ที่มุมขวาล่าง เราจำเป็นต้องเลือกใช้ `'absolute'` (พิกัดตำแหน่งสัมบูรณ์)

### ข้อแตกต่างและการประยุกต์ใช้งาน
* **`relative` (Default):** คอมโพเนนต์จะจัดวางพื้นที่และขยับตำแหน่งโดยอ้างอิงจากตำแหน่งที่มันควรจะอยู่ปกติในระบบ Flow โดยที่ยังคงจองพื้นที่ของตัวเองไว้ ไม่ให้ชิ้นงานอื่นมาเบียดทับ
* **`absolute`:** คอมโพเนนต์จะหลุดออกจากระเบียบการจัดแถวของ Flexbox ทันที โดยพิกัดจะถูกระบุด้วยทิศทาง `top`, `bottom`, `left`, `right` สัมพันธ์กับพื้นที่ของ **"คอนเทนเนอร์แม่ตัวแรกสุดที่มีระดับชั้นอยู่เหนือมันและทำตัวเป็นจุดอ้างอิง"** (มักจะตั้งค่าแม่เป็น `position: 'relative'` หรือปล่อยไว้เป็นดีฟอลต์)

```tsx
import { StyleSheet, View, Text } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function BadgeExample() {
  return (
    <View style={styles.container}>
      {/* 1. ปุ่มกระดิ่งแจ้งเตือน */}
      <View style={styles.iconButton}>
        <Ionicons name="notifications" size={32} color="#ffffff" />
        
        {/* 2. ตัวเลขสีแดงแจ้งเตือนวางทับซ้อนมุมขวาบน */}
        <View style={styles.badge}>
          <Text style={styles.badgeText}>3</Text>
        </View>
      </View>
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
  iconButton: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#1e293b',
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative', // เป็นหลักแหล่งพิกัดอ้างอิงให้ลูกสะกดตำแหน่ง
    borderWidth: 1,
    borderColor: '#334155',
  },
  badge: {
    position: 'absolute', // หลุดออกจากโฟลว์เพื่อทับซ้อนอิสระ
    top: -4,              // ดันขึ้นไปด้านบน 4px เหนือขอบกระดิ่ง
    right: -4,            // ขยับเยื้องขวา 4px เลยขอบกระดิ่ง
    backgroundColor: '#ef4444', // สีแดงเตือนภัย
    minWidth: 20,
    height: 20,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 4,
  },
  badgeText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: 'bold',
  },
});
```

---

## 7.2 การใช้งาน Custom Fonts ด้วย expo-font

ฟอนต์ดั้งเดิมของระบบปฏิบัติการ (System Fonts) มักจะขาดเอกลักษณ์เฉพาะตัวของแบรนด์ โครงการ Expo SDK 54 สนับสนุนการดาวน์โหลดชุดฟอนต์จากภายนอกมาติดตั้งใช้งานในระดับเนทีฟอย่างสะดวก ผ่านไลบรารี `expo-font` และจัดการความสมบูรณ์ในการโหลดฟอนต์พร้อมกับระบบ Splash Screen เพื่อป้องกันปัญหาสัญลักษณ์เบี้ยวหรือกระตุก (Flash of Unstyled Text)

### การดาวน์โหลดและติดตั้งคอมโพเนนต์
ขั้นตอนแรกในการทำงานคือการติดตั้งไลบรารีที่จำเป็น:
```bash
npx expo install expo-font expo-splash-screen
```

### การเขียนโค้ดผูกฟอนต์และหน่วงเวลา Splash Screen
เราต้องสั่งหยุดไม่ให้ Splash Screen ปิดตัวเองก่อนที่ฟอนต์จะถูกโหลดเสร็จลงในหน่วยความจำ RAM ของเครื่อง โดยเรียกใช้ `SplashScreen.preventAutoHideAsync()` และสั่งซ่อนด้วย `SplashScreen.hideAsync()` หลังจากผลลัพธ์การโหลดพร้อมรัน:

```tsx
import { useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';

// 1. ตรึงภาพ Splash Screen ไว้ไม่ให้หน้าจอดับลงก่อนการโหลด
SplashScreen.preventAutoHideAsync();

export default function FontLoaderApp() {
  // 2. เรียกใช้ useFonts โหลดแบบอักษรพิเศษจากโฟลเดอร์ assets
  const [fontsLoaded, error] = useFonts({
    'Prompt-Regular': require('../../assets/fonts/Prompt-Regular.ttf'),
    'Prompt-Bold': require('../../assets/fonts/Prompt-Bold.ttf'),
  });

  useEffect(() => {
    // 3. เมื่อดาวน์โหลดเสร็จสมบูรณ์หรือมีข้อผิดพลาด ให้ทำการซ่อน Splash Screen
    if (fontsLoaded || error) {
      SplashScreen.hideAsync();
    }
  }, [fontsLoaded, error]);

  // 4. หากฟอนต์ยังไม่พร้อมและไม่พบข้อผิดพลาด ให้คืนค่าว่างเปล่า (null) เพื่อป้องกันการเรนเดอร์พัง
  if (!fontsLoaded && !error) {
    return null;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.textRegular}>สวัสดีภาษาไทยด้วยแบบอักษร Prompt (Regular)</Text>
      <Text style={styles.textBold}>หัวข้อสำคัญด้วย Prompt (Bold)</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
    backgroundColor: '#0f172a',
  },
  textRegular: {
    fontFamily: 'Prompt-Regular', // อ้างอิงตรงตามชื่อคีย์ที่ลงทะเบียนใน useFonts
    fontSize: 18,
    color: '#cbd5e1',
    marginBottom: 12,
  },
  textBold: {
    fontFamily: 'Prompt-Bold',
    fontSize: 24,
    color: '#ffffff',
  },
});
```

---

## 7.3 การใช้งานระบบเวกเตอร์ไอคอนด้วย @expo/vector-icons

ไลบรารี `@expo/vector-icons` ติดตั้งมาพร้อมใช้งานในแม่แบบโครงการของ Expo ช่วยลดภาระการโหลดไฟล์ PNG ของไอคอน ซึ่งทำให้ขนาดไฟล์แอปพลิเคชันใหญ่โดยไม่จำเป็น โดยชุดแพ็คเกจนี้จะรวมไอคอนเวกเตอร์ชื่อดังไว้เพียบ เช่น Ionicons, AntDesign, FontAwesome, MaterialIcons, Feather และ Octicons

### เครื่องมือสำหรับค้นหาไอคอนอย่างเป็นทางการ
ผู้พัฒนาสามารถเลือกค้นหาชุดภาพและรายชื่อไอคอนที่ถูกต้องได้ผ่านเว็บไซต์ [icons.expo.fyi](https://icons.expo.fyi/) ซึ่งจะบอกคำสั่ง Import และรายชื่อไอคอนทั้งหมด

### ตัวอย่างการประยุกต์ใช้งาน
```tsx
import { View, StyleSheet, TouchableOpacity, Text } from 'react-native';
import { Ionicons, Feather } from '@expo/vector-icons';

export default function MenuGrid() {
  return (
    <View style={styles.grid}>
      {/* การใช้งาน Ionicons สำหรับปุ่มตั้งค่า */}
      <TouchableOpacity style={styles.card}>
        <Ionicons name="settings-outline" size={28} color="#38bdf8" />
        <Text style={styles.label}>ตั้งค่าระบบ</Text>
      </TouchableOpacity>

      {/* การใช้งาน Feather สำหรับปุ่มแผนที่ */}
      <TouchableOpacity style={styles.card}>
        <Feather name="map-pin" size={28} color="#f43f5e" />
        <Text style={styles.label}>สถานที่</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  grid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 20,
    backgroundColor: '#0f172a',
  },
  card: {
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    width: '40%',
    borderWidth: 1,
    borderColor: '#334155',
  },
  label: {
    color: '#ffffff',
    marginTop: 8,
    fontSize: 14,
  },
});
```

---

## 7.4 การจัดการรูปภาพประสิทธิภาพสูงด้วย expo-image

คอมโพเนนต์ `Image` ดั้งเดิมของ React Native ประสบปัญหาร้ายแรงหลายประการเมื่อต้องทำงานกับภาพจากเน็ตเวิร์กจำนวนมาก เช่น การกระพริบตา (Flickering) เวลาอัปเดตข้อมูล, ไม่มีระบบเซฟเก็บความจำสำรองบนความจุฮาร์ดดิสก์แบบเนทีฟ (Native Caching) ทำให้แอปเปลืองอินเทอร์เน็ต และการเปิดโหลดภาพขนาดใหญ่ก่อให้เกิดอาการค้างชั่วขณะบนโทรศัพท์ Android ระดับล่าง

เพื่อขจัดขีดจำกัดดังกล่าว Expo จึงพัฒนาคอมโพเนนต์ **`expo-image`** ขึ้นมาโดยขับเคลื่อนผ่านไลบรารีประสิทธิภาพสูงของภาษาเนทีฟอย่าง **SDWebImage (iOS)** และ **Glide (Android)**

### ความสำคัญของ expo-image
* **ระบบ Caching ชั้นเลิศ:** บันทึกภาพลงบนไดรฟ์เครื่องอัตโนมัติ เปิดซ้ำไม่ต้องโหลดเน็ตอีกครั้ง
* **ความเร็วในการประมวลผลสูง:** ป้องกันไม่ให้แอปพลิเคชันกระตุกขณะผู้ใช้ทำการปัดเลื่อนลิสต์ที่มีภาพประกอบ
* **สอดคล้องกับมาตรฐานเว็บ:** การใช้งานฟังก์ชันขยายสไตล์สอดรับกับคุณสมบัติของ CSS `object-fit` (เช่นการใช้ค่า `contentFit`)
* **รองรับหลากหลายไฟล์สมัยใหม่:** สามารถรันภาพเคลื่อนไหวอย่าง WebP, APNG, GIF รวมถึงไฟล์ความหนาแน่นสูงอย่าง AVIF

```bash
npx expo install expo-image
```

---

## 7.5 การใช้งาน Blurhash Placeholder และ Transition

สองกลยุทธ์สำคัญที่จะช่วยเปลี่ยนแอปที่ดูธรรมดาให้เป็นแอปเกรดพรีเมียม คือการจัดการรอยต่อของเวลาที่รูปภาพกำลังโหลด:

### 1. ระบบจำลองภาพแบบเลือนลาง (Blurhash Placeholder)
**Blurhash** คือเทคโนโลยีการแปลงภาพถ่ายขนาดใหญ่ให้กลายเป็นรหัสข้อความสั้น ๆ (เช่น `L6PZUpUR00-y_4V[00aeY5g2o1of`) ซึ่งสามารถวาดแสดงผลขึ้นมาเป็นภาพไล่เฉดสีเบลอ ๆ ได้ในเศษเสี้ยววินาทีโดยไม่ต้องรอเน็ตเวิร์ก ช่วยลดความอึดอัดของผู้ใช้เมื่อเปรียบเทียบกับวงล้อโหลดข้อมูลที่ว่างเปล่า

### 2. เอฟเฟกต์ Fade-in Transition
เมื่อระบบดาวน์โหลดภาพไฟล์จริงจากเซิร์ฟเวอร์เสร็จสิ้นแล้ว `expo-image` จะทำการเปลี่ยนผ่านจากภาพเบลอตัวพรีวิวไปสู่รูปจริงอย่างราบรื่นด้วยเอฟเฟกต์อนิเมชันแบบสลัวทีละนิด ช่วยลดความตระหนกสายตาของผู้ใช้ (No Flickering Jump)

```tsx
import { View, StyleSheet, Text } from 'react-native';
import { Image } from 'expo-image';

// ตัวอย่างสตริง Blurhash จำลองเฉดสีเพื่อรอโหลด
const sampleBlurhash = 'L6PZUpUR00-y_4V[00aeY5g2o1of';

export default function HighPerformanceImage() {
  return (
    <View style={styles.container}>
      <Text style={styles.header}>ตัวอย่างการแสดงผลรูปภาพผ่าน expo-image</Text>
      
      <Image
        style={styles.image}
        source="https://picsum.photos/id/237/800/600"
        placeholder={{ blurhash: sampleBlurhash }} // แสดงภาพพรีวิวเบลอตามรหัสชุดข้อความทันที
        contentFit="cover" // เทียบเท่า object-fit: cover ในระบบ CSS
        transition={600}   // เล่นเอฟเฟกต์เฟดภาพจริง 0.6 วินาทีเพื่อความนุ่มนวล
      />
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
  header: {
    color: '#94a3b8',
    marginBottom: 16,
    fontSize: 15,
  },
  image: {
    width: 300,
    height: 200,
    borderRadius: 16,
  },
});
```

---

## 7.6 การรองรับโหมดมืด (Dark Mode / Theme Support) ด้วย useColorScheme

ในโทรศัพท์มือถือยุคปัจจุบัน ระบบปฏิบัติการจะเปิดโอกาสให้ผู้ใช้อัปเกรดหน้าจอไปใช้โทนสีดำ (Dark Mode) เพื่อความปลอดภัยของสายตาและประหยัดพลังงาน แบตเตอรี่ สำหรับแอป React Native เราสามารถเขียนตรวจสอบสถานะสีเครื่องได้โดยตรงผ่าน `useColorScheme` Hook ของ `react-native`

### การประกาศตัวแปรสีและผูกใช้ในสไตล์
เมื่อตรวจพบการปรับระบบ โค้ดหน้าจอจะเข้าข่ายและแสดงธีมที่สลับค่าโทนสีอย่างไดนามิก:

```tsx
import { StyleSheet, Text, View, useColorScheme } from 'react-native';

export default function DynamicThemeScreen() {
  // 1. เรียกรับค่าสถานะโหมดระบบปฏิบัติการ ('light' หรือ 'dark')
  const colorScheme = useColorScheme();
  
  // 2. ตรวจเช็คเพื่อกำหนดธีมสีแบบ Dynamic
  const isDarkMode = colorScheme === 'dark';

  return (
    // 3. กำหนดสไตล์โดยสลับ Object สไตล์ตามสถานะ
    <View style={[styles.container, isDarkMode ? styles.darkContainer : styles.lightContainer]}>
      <Text style={[styles.title, isDarkMode ? styles.darkText : styles.lightText]}>
        {isDarkMode ? '🌙 ระบบของคุณเปิดโหมดมืดอยู่' : '☀️ ระบบของคุณเปิดโหมดสว่างอยู่'}
      </Text>
      <Text style={[styles.subtitle, isDarkMode ? styles.darkSub : styles.lightSub]}>
        สไตล์และโทนสีของแอปตัวนี้จะขยับสับเปลี่ยนตามค่าหน้าจอหลักของสมาร์ทโฟน
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  // ธีมสีพื้นหลังสว่าง/มืด
  lightContainer: {
    backgroundColor: '#f8fafc',
  },
  darkContainer: {
    backgroundColor: '#0f172a',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 10,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 15,
    textAlign: 'center',
    lineHeight: 22,
  },
  // ธีมตัวหนังสือ
  lightText: {
    color: '#0f172a',
  },
  darkText: {
    color: '#ffffff',
  },
  lightSub: {
    color: '#64748b',
  },
  darkSub: {
    color: '#94a3b8',
  },
});
```

## 7.7 สรุปท้ายบทเรียน

**ระบบพิกัดตำแหน่งสัมพัทธ์และสัมบูรณ์:** การจัดวางอินเทอร์เฟซใน React Native ใช้สไตล์ position ในการกำหนดระบบพิกัด โดยมี relative เป็นค่าเริ่มต้นที่จัดเรียงวัตถุตามระบบ Flexbox โดยยังจองพื้นที่ไว้ และ absolute สำหรับยกวัตถุออกจากโฟลว์เพื่อกำหนดทิศทางผ่าน top, bottom, left และ right สัมพันธ์กับพื้นที่ของคอมโพเนนต์แม่ที่ตั้งค่าเป็นหลักแหล่งอ้างอิง ซึ่งช่วยให้เราสามารถจัดทำส่วนทับซ้อนหรือปุ่มลอยต่าง ๆ ได้ตามต้องการ

**การใช้งาน Custom Fonts ด้วย expo-font:** การดาวน์โหลดและแสดงผลแบบอักษรแบรนด์เฉพาะตัวกระทำได้ผ่านชุดไลบรารี expo-font ร่วมกับ expo-splash-screen โดยเราจะต้องทำโครงสร้างการหน่วงเวลาเพื่อสั่งให้ระบบคงภาพ Splash Screen ค้างไว้ก่อนในขณะที่ตัวฟังก์ชัน useFonts กำลังโหลดชุดอักษรพิเศษ เพื่อป้องกันการแสดงผลแบบอักษรผิดพลาดหรือเกิดการกระตุกเปลี่ยนแบบอักษรหลังจากเข้าหน้าแอปพลิเคชัน

**การใช้งานระบบเวกเตอร์ไอคอนด้วย @expo/vector-icons:** เพื่อประหยัดขนาดพื้นที่และความสามารถในการตอบสนองสเกลภาพ เวกเตอร์ไอคอนจากไลบรารี @expo/vector-icons จึงเป็นทางเลือกหลักในการรวบรวมสัญลักษณ์สากลอย่าง Ionicons, Feather หรือ FontAwesome มาใช้งานในโปรเจกต์ ซึ่งสามารถนำรูปภาพที่ถูกต้องจากคู่มือค้นหารายชื่อไอคอน icons.expo.fyi มาใส่สีและกำหนดขนาดตามที่สไตล์ชีทกำหนดไว้ได้อย่างมีประสิทธิภาพ

**การจัดการรูปภาพประสิทธิภาพสูงด้วย expo-image:** คอมโพเนนต์ดั้งเดิมมีปัญหาด้านแคชข้อมูลภาพจากเน็ตเวิร์กและการกระตุกตอนปัดเลื่อนจอ ทำให้ Expo ได้พัฒนา expo-image ขึ้นมาทำงานทดแทนผ่านเทคโนโลยีฝั่งเนทีฟ (Glide และ SDWebImage) ซึ่งมอบฟีเจอร์การสร้างแคชจัดเก็บบนความจุไดรฟ์เครื่องอัตโนมัติ ทำให้ผู้พัฒนาสามารถจัดสรรการแสดงผลรูปภาพจำนวนมากได้อย่างรวดเร็วและประหยัดอินเทอร์เน็ตของผู้ใช้อย่างเด่นชัด

**การใช้งาน Blurhash Placeholder และ Transition:** การเสริมสร้างรอยต่อเวลาที่รูปภาพหลักกำลังอยู่ในกระบวนการดาวน์โหลดสามารถทำได้ผ่านสองกลยุทธ์หลัก คือการใช้รหัสข้อความจำลองเฉดสีขนาดเล็กอย่าง Blurhash แสดงผลขึ้นมาเป็นภาพเบลอตัวอย่างโดยไม่ต้องรอเน็ตเวิร์ก และระบบเล่นเอฟเฟกต์ Fade-in Transition ของ expo-image เพื่อทำการเปลี่ยนผ่านภาพจากแบบเบลอไปสู่ภาพจริงได้อย่างนุ่มนวลและลดอาการกระตุกทางสายตา

**การรองรับโหมดมืดด้วย useColorScheme:** โทรศัพท์มือถือยุคใหม่มักจะให้ผู้ใช้ปรับแต่งธีมสว่างหรือมืดตามใจชอบ ซึ่งเราสามารถดักฟังค่าระบบปฏิบัติการได้ผ่าน useColorScheme Hook ของ react-native เพื่อนำค่า light หรือ dark มาทำการสลับโทนสีของแอปพลิเคชันอย่างไดนามิกผ่านโครงสร้างออบเจกต์สไตล์ชีท ช่วยให้อินเทอร์เฟซมีความกลมกลืนตามความชอบของผู้ใช้งานเครื่องสมาร์ทโฟน

---

← [ย้อนกลับแผนการสอน: 01-lesson-plan.md](./01-lesson-plan.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ทำแบบทดสอบถัดไป: 03-quiz.md](./03-quiz.md) →
