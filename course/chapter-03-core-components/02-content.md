# บทที่ 3: คอมโพเนนต์พื้นฐานและการจัดการปฏิสัมพันธ์กับผู้ใช้ (Content)

ในสภาพแวดล้อมการพัฒนาแอปพลิเคชันด้วย React Native คอมโพเนนต์พื้นฐาน (Core Components) ทำหน้าที่เป็นตัวเชื่อมต่อ (Bridge) ไปยังมุมมองดั้งเดิม (Native UI Views) ของระบบปฏิบัติการ iOS (เช่น `UIView`, `UIImageView`, `UITextField`) และ Android (เช่น `View`, `ImageView`, `EditText`) ส่งผลให้แอปพลิเคชันสามารถประมวลผลอินเทอร์เฟซด้วยประสิทธิภาพระดับเนทีฟอย่างแท้จริง

---

## 3.1 คอมโพเนนต์แสดงผลรูปภาพ Image (Local และ Network Assets)

คอมโพเนนต์ `Image` ใช้สำหรับการแสดงผลรูปภาพในแอปพลิเคชัน ทั้งภาพประเภทสเตติกภายในเครื่อง (Static Local Assets) และภาพที่ดาวน์โหลดผ่านอินเทอร์เน็ต (Network Images)

### 1. การแสดงผลรูปภาพจาก Local Assets
เป็นการดึงภาพที่เก็บรวมอยู่ในโฟลเดอร์ของโปรเจกต์ โดยเรียกใช้ฟังก์ชัน `require()` ในการอ้างอิงตำแหน่งไฟล์ ซึ่งระบบจะประมวลผลขนาดของรูปภาพให้โดยอัตโนมัติตอนทำการบิลด์ (Build Time):
```tsx
import { Image, StyleSheet, View } from 'react-native';

export default function LocalImageExample() {
  return (
    <View style={styles.container}>
      <Image 
        source={require('../../assets/images/react-logo.png')} 
        style={styles.localImage}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  localImage: {
    width: 100,
    height: 100,
  },
});
```

### 2. การแสดงผลรูปภาพจากเครือข่ายอินเทอร์เน็ต (Network Images)
เป็นการโหลดรูปภาพผ่านโปรโตคอล HTTP/HTTPS โดยกำหนดค่า `source` เป็นออบเจกต์ที่มีพร็อพส์ `uri`:
> [!IMPORTANT]
> **กฎเหล็กของ Network Images:** หากเป็นการโหลดภาพผ่าน `uri` ผู้พัฒนา **จำเป็นต้องระบุความกว้าง (width) และความสูง (height) ในสไตล์เสมอ** มิฉะนั้นคอมโพเนนต์จะไม่ทราบขนาดพื้นที่จำลองและไม่แสดงผลภาพขึ้นมา (ขนาดเริ่มต้นจะเป็น 0x0 พิกเซล)

```tsx
<Image 
  source={{ uri: 'https://reactnative.dev/img/tiny_logo.png' }} 
  style={{ width: 50, height: 50 }}
/>
```

### 3. การปรับขนาดสัดส่วนด้วย resizeMode
คุณสมบัติ `resizeMode` ทำหน้าที่กำหนดทิศทางว่ารูปภาพจะจัดสัดส่วนอย่างไรเมื่อกรอบของรูปภาพ (สไตล์กว้าง/สูง) มีขนาดต่างจากภาพจริง:
* **`cover`** (ค่าเริ่มต้น): ยืด/ขยายรูปภาพให้ครอบคลุมเต็มพื้นที่กรอบ โดยรักษาอัตราส่วนภาพไว้ (ทำให้บางส่วนของภาพอาจถูกตัดออก)
* **`contain`**: ยืด/หดรูปภาพให้อยู่ภายในพื้นที่กรอบได้ครบถ้วนทั้งหมด โดยรักษาอัตราส่วนภาพไว้ (อาจเกิดพื้นที่ว่างซ้าย-ขวา หรือบน-ล่าง)
* **`stretch`**: ยืดขยายรูปภาพให้เต็มกรอบโดยตรง โดยละทิ้งการรักษาอัตราส่วนเดิม (ภาพจะบิดเบี้ยวได้)
* **`center`**: จัดกึ่งกลางรูปภาพในเฟรมโดยรักษาขนาดดั้งเดิมไว้ (ไม่มีการยืดขยาย)

---

## 3.2 คอมโพเนนต์รับข้อมูลข้อความ TextInput และการควบคุมคีย์บอร์ด

คอมโพเนนต์ `TextInput` ใช้ในการเปิดพื้นที่รับข้อมูลตัวอักษรหรือข้อความจากผู้ใช้งานผ่านแป้นพิมพ์เสมือน (Virtual Keyboard)

### 1. พร็อพส์พื้นฐานที่จำเป็นสำหรับการสร้างฟอร์ม
* **`value`**: ตัวแปรสถานะที่เก็บค่าข้อความปัจจุบัน
* **`placeholder`**: ข้อความแนะนำแบบจางที่จะแสดงเมื่อไม่มีการพิมพ์ข้อความใด ๆ
* **`onChangeText`**: เหตุการณ์สัมผัสที่จะเรียกฟังก์ชันกลับคืน (Callback Function) ส่งสตริงค่าล่าสุดกลับมาทุกครั้งที่ปุ่มแป้นพิมพ์ถูกกดพิมพ์
* **`secureTextEntry`**: กำหนดให้เป็น `true` เพื่อจำลองการกรอกรหัสผ่าน (ตัวอักษรจะเปลี่ยนเป็นสัญลักษณ์จุดวงกลมบดบังสายตา)

```tsx
import { useState } from 'react';
import { TextInput, StyleSheet, View } from 'react-native';

export default function InputExample() {
  const [password, setPassword] = useState('');
  
  return (
    <View style={styles.container}>
      <TextInput
        placeholder="กรอกรหัสผ่านของคุณ"
        value={password}
        onChangeText={setPassword}
        secureTextEntry={true}
        style={styles.input}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  input: {
    height: 48,
    borderWidth: 1,
    borderColor: '#ccc',
    paddingHorizontal: 12,
    borderRadius: 8,
  },
});
```

### 2. การควบคุมพฤติกรรมคีย์บอร์ด (Keyboard Control)
ในอุปกรณ์เคลื่อนที่ การจัดเรียงประเภทปุ่มบนแป้นพิมพ์ให้ตรงกับบริบทของอินพุตเป็นสิ่งสำคัญอย่างยิ่งเพื่ออำนวยความสะดวกให้ผู้ใช้งาน:
* **`keyboardType`**: ระบุรูปแบบคีย์บอร์ดที่ทำงานขึ้นมา
  * `'default'`: คีย์บอร์ดข้อความปกติ
  * `'numeric'`: คีย์บอร์ดปุ่มตัวเลข (เหมาะสำหรับการป้อนยอดเงิน รหัส OTP)
  * `'email-address'`: คีย์บอร์ดที่มีปุ่ม `@` และ `.com` ขึ้นมาอำนวยความสะดวก
  * `'phone-pad'`: แป้นพิมพ์ปุ่มหมายเลขโทรศัพท์ที่มีเครื่องหมายบวก/ดอกจัน
* **`autoCapitalize`**: ควบคุมการขึ้นต้นด้วยอักษรตัวใหญ่ภาษาอังกฤษอัตโนมัติ (แนะนำให้ใช้ `'none'` สำหรับอีเมลและรหัสผ่าน)
* **`autoCorrect`**: เปิด/ปิดระบบเดาคำศัพท์และแก้ไขข้อความอัตโนมัติของตัวระบบปฏิบัติการ (`true` หรือ `false`)
* **`returnKeyType`**: เปลี่ยนรูปภาพปุ่มตกลง/ทำรายการที่มุมขวาด้านล่างของคีย์บอร์ด (เช่น `'done'`, `'next'`, `'search'`, `'go'`)

---

## 3.3 การสร้างพื้นที่เลื่อนดูข้อมูลด้วย ScrollView เปรียบเทียบกับ View

โดยปกติแล้ว คอมโพเนนต์ `View` พื้นฐานจะไม่มีความสามารถในการตอบสนองคำสั่งเลื่อนหน้าจอ (Scrolling) หากเนื้อหาในหน้าจอนั้นมีความยาวเกินกว่าพื้นที่ขอบเขตจอแสดงผลจริง เนื้อหาด้านล่างจะถูกตัดทิ้งและไม่สามารถเลื่อนอ่านได้

### 1. พฤติกรรมของ ScrollView
`ScrollView` คือตู้คอนเทนเนอร์แบบเลื่อนดูเนื้อหาภายในได้ โดยจะทำการแสดงผลแถบแถบเลื่อน (Scrollbar) อัตโนมัติเมื่อเนื้อหาภายในขยายความยาวเกินกว่าขอบเขตหน้าจอ

```tsx
import { ScrollView, Text, StyleSheet } from 'react-native';

export default function LongContent() {
  return (
    <ScrollView style={styles.scroll}>
      <Text style={styles.text}>ย่อหน้าที่ 1...</Text>
      <Text style={styles.text}>ย่อหน้าที่ 2...</Text>
      {/* เพิ่มเนื้อหาจำลองที่มีความยาวลงไปได้เรื่อย ๆ */}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scroll: {
    flex: 1,
    backgroundColor: '#fff',
  },
  text: {
    fontSize: 18,
    marginVertical: 40,
  },
});
```

### 2. การเปรียบเทียบ View กับ ScrollView
| คุณสมบัติ | View | ScrollView |
| :--- | :--- | :--- |
| **การเลื่อนหน้าจอ (Scrolling)** | ไม่ทำตามการปัดสัมผัสเลื่อนหน้าจอ | รองรับการเลื่อนแนวตั้งและแนวนอน |
| **พื้นที่ยึดแกนเลย์เอาต์** | จัดตำแหน่ง Layout ด้วย Flexbox ได้ทันที | จัดเลย์เอาต์เฉพาะจุดผ่าน `contentContainerStyle` |
| **การเรนเดอร์หน่วยความจำ** | รวดเร็ว แสดงเฉพาะของภายในกล่อง | เรนเดอร์คอมโพเนนต์ลูกทั้งหมดในครั้งเดียวตอนโหลด |
| **กรณีการใช้งานที่เหมาะสม** | โครงสร้างบล็อกเลย์เอาต์, ป้าย, พื้นที่ที่ไม่ล้นจอ | หน้าจอกรอกข้อมูลแบบฟอร์ม, หน้าเนื้อหายาว ๆ เช่น ข้อตกลง |

> [!WARNING]
> **การใช้สไตล์กับ ScrollView:** หากคุณใช้ `style` บน `ScrollView` จะเป็นการจัดลักษณะทางกายภาพภายนอกของตัวเลื่อนเอง แต่หากคุณต้องการกำหนดช่องไฟ ระยะห่าง (Padding) หรือการจัดกึ่งกลางเนื้อหาลูกที่อยู่ข้างในพื้นที่เลื่อน **คุณต้องใช้งานผ่านพร็อพส์ `contentContainerStyle` เท่านั้น**

---

## 3.4 การจัดการเหตุการณ์การสัมผัสและการกดปุ่มด้วย Pressable

ในยุคแรกเริ่ม React Native ใช้กลุ่มคอมโพเนนต์ตระกูล Touchable (เช่น `TouchableOpacity`, `TouchableHighlight`) ในการสร้างปุ่ม แต่ในปัจจุบันเวอร์ชันใหม่ ๆ ได้นำเสนอคอมโพเนนต์ที่ยืดหยุ่นและก้าวหน้ากว่าคือ `Pressable` ซึ่งรองรับการตรวจจับระดับการกดสัมผัสในสภาพการใช้งานที่ซับซ้อนขึ้น

### 1. เหตุการณ์สัมผัสต่าง ๆ บน Pressable
* **`onPress`**: สัมผัสปุ่มและปล่อยตัวในเวลาปกติ (การคลิกปุ่มทั่วไป)
* **`onLongPress`**: กดปุ่มสัมผัสแช่ไว้เป็นเวลาอย่างน้อย 500 มิลลิวินาที
* **`onPressIn`**: สัมผัสเริ่มแรกเมื่อนิ้วเตะโดนปุ่ม
* **`onPressOut`**: จังหวะที่ยกนิ้วขึ้นจากพื้นที่สัมผัสปุ่ม

### 2. การจัดการสถานะ Active/Pressed สไตล์ไดนามิก
`Pressable` ยกระดับความสามารถโดยสามารถรับฟังก์ชันในคุณสมบัติ `style` หรือ `children` เพื่อรับทราบข้อมูลสถานะแอปพลิเคชันว่าผู้ใช้งานกำลังเอานิ้วกดคาไว้อยู่หรือไม่ผ่านตัวแปรบูเลียน `{ pressed }`:

```tsx
import { Pressable, Text, StyleSheet } from 'react-native';

export default function CustomButton() {
  return (
    <Pressable
      onPress={() => console.log('Button Pressed!')}
      style={({ pressed }) => [
        styles.button,
        {
          backgroundColor: pressed ? '#1d4ed8' : '#2563eb', // สีเข้มขึ้นเมื่อถูกกด
          transform: [{ scale: pressed ? 0.98 : 1.0 }],   // ย่อตัวลงเล็กน้อยจำลองน้ำหนักกด
        }
      ]}
    >
      <Text style={styles.text}>บันทึกข้อมูล</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: 'center',
  },
  text: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
});
```

---

## 3.5 การหลีกเลี่ยงพื้นที่ขอบจอด้วย SafeAreaView

อุปกรณ์สมาร์ทโฟนยุคใหม่มีดีไซน์ที่หลากหลาย เช่น หน้าจอไร้ขอบที่มีรอยบาก (Notch) มีกล้องทรงหยดน้ำ หรือแถบนำทางระบบปฏิบัติการอยู่ด้านล่างหน้าจอ หากเขียนวางคอมโพเนนต์ชิดขอบบนหรือขอบล่างเกินไป เนื้อหาอาจจะถูกกล้อง รอยบาก หรือแถบสถานะ (Status Bar) บดบัง

### การใช้งาน SafeAreaView
คอมโพเนนต์ `SafeAreaView` จะคำนวณและเว้นพื้นที่ระยะขอบปลอดภัยเฉพาะอุปกรณ์นั้น ๆ ให้อัตโนมัติ (มีผลเด่นชัดบนระบบ iOS) ทำให้ผู้พัฒนาไม่ต้องเขียนสไตล์ขยับความสูงด้วยค่าคงที่ตายตัว:

```tsx
import { SafeAreaView, View, Text, StyleSheet } from 'react-native';

export default function SafeLayout() {
  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.content}>
        <Text>เนื้อหาของแอปพลิเคชันที่ได้รับการปกป้องจากรอยบากหน้าจอ</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#f8fafc', // ให้พื้นที่ปลอดภัยเป็นสีเดียวกับแอป
  },
  content: {
    flex: 1,
    padding: 16,
  },
});
```

---

## 3.6 แนวคิดการสร้าง Custom Component และการกำหนด Props Interface ด้วย TypeScript

การพัฒนาแอปพลิเคชันที่มีขนาดใหญ่ขึ้นจำเป็นต้องคำนึงถึงความสะดวกในการบำรุงรักษาโค้ดและการนำชิ้นส่วนอินเตอร์เฟซกลับมาใช้ซ้ำ (Component Reusability) โดยสร้าง **Custom Components** และส่งผ่านค่าข้อมูลความต้องการผ่าน **Props**

### 1. แนวคิดการแยกสร้าง Custom Component
สมมติว่าเราต้องการสร้างการ์ดแนะนำข้อมูลผู้ใช้งานที่มีรูปโปรไฟล์ ชื่อ และปุ่มติดต่อ หากประกาศไว้ทั้งหมดบนหน้าหลัก โค้ดจะยาวและซ้ำซ้อน เราจึงควรแยกสร้างเป็นไฟล์ย่อยภายนอก

### 2. การประกาศคุณสมบัติและกำหนดโครงสร้างข้อมูลด้วย TypeScript Interface
ในระดับมืออาชีพการใช้ TypeScript ร่วมกับ React Native จะช่วยควบคุมคุณภาพการพัฒนาได้อย่างดีเยี่ยม โดยจะนำ `interface` มากำหนดเป็นตัวกรองข้อมูลว่าคอมโพเนนต์ย่อยนั้น ๆ ต้องการตัวแปรชนิดใดบ้าง และตัวแปรใดเป็นสิ่งจำเป็นหรือมีตัวเลือกอื่น ๆ:

```tsx
// 1. สร้างไฟล์ย่อยที่ตั้งชื่อว่า components/UserProfileCard.tsx
import { View, Text, Image, StyleSheet, Pressable } from 'react-native';

// กำหนดประเภทข้อมูล Props ด้วย TypeScript Interface
export interface UserProfileCardProps {
  name: string;
  avatarUrl: string;
  role: string;
  isActive?: boolean; // เครื่องหมาย ? แสดงว่าเป็นตัวเลือก (Optional) ไม่ส่งมาก็ไม่เกิดข้อผิดพลาด
  onPressDetails?: () => void; // ฟังก์ชัน Callback สำหรับส่งสัญญานเมื่อกดการ์ด
}

export default function UserProfileCard({
  name,
  avatarUrl,
  role,
  isActive = false, // กำหนดค่าเริ่มต้นให้กับพร็อพส์ที่เป็นตัวเลือก
  onPressDetails,
}: UserProfileCardProps) {
  return (
    <View style={styles.card}>
      <Image source={{ uri: avatarUrl }} style={styles.avatar} />
      <View style={styles.info}>
        <Text style={styles.nameText}>{name}</Text>
        <Text style={styles.roleText}>{role}</Text>
        <Text style={[styles.statusText, { color: isActive ? '#10b981' : '#ef4444' }]}>
          {isActive ? '● กำลังทำงาน' : '○ พักผ่อน'}
        </Text>
      </View>
      {onPressDetails && (
        <Pressable onPress={onPressDetails} style={styles.button}>
          <Text style={styles.buttonText}>ข้อมูลเพิ่มเติม</Text>
        </Pressable>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#fff',
    borderRadius: 12,
    marginVertical: 8,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  avatar: {
    width: 60,
    height: 60,
    borderRadius: 30,
  },
  info: {
    flex: 1,
    marginLeft: 16,
  },
  nameText: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  roleText: {
    color: '#64748b',
    fontSize: 14,
  },
  statusText: {
    fontSize: 12,
    marginTop: 4,
    fontWeight: '500',
  },
  button: {
    backgroundColor: '#0f172a',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 12,
  },
});
```

### 3. การเรียกใช้งานในหน้าจอหลัก (Parent Component)
เราสามารถเรียกนำเข้าและสร้างผู้ใช้หลาย ๆ คนได้โดยส่งข้อมูลที่ต้องการแตกต่างกันผ่านคุณสมบัติ Props:

```tsx
// 2. เรียกใช้ภายในไฟล์หลัก App.tsx หรือ index.tsx
import { View, StyleSheet, Alert } from 'react-native';
import UserProfileCard from './components/UserProfileCard';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      {/* ส่งข้อมูลครบสมบูรณ์ */}
      <UserProfileCard
        name="สมชาย ใจดี"
        avatarUrl="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde"
        role="ผู้พัฒนาโมบายแอป"
        isActive={true}
        onPressDetails={() => Alert.alert('ข้อมูลเพิ่มเติม', 'สมชายเป็นผู้พัฒนามานานกว่า 5 ปี')}
      />
      
      {/* ละตัวแปร isActive และ onPressDetails ที่เป็นออปชัน เสริมความยืดหยุ่น */}
      <UserProfileCard
        name="สมศรี รักเรียน"
        avatarUrl="https://images.unsplash.com/photo-1494790108377-be9c29b29330"
        role="นักออกแบบ UX/UI"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f1f5f9',
    padding: 16,
  },
});
```

---

← [ย้อนกลับแผนการสอน: 01-lesson-plan.md](./01-lesson-plan.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ทำแบบทดสอบถัดไป: 03-quiz.md](./03-quiz.md) →
