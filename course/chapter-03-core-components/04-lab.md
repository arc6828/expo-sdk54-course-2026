# ปฏิบัติการ บทที่ 3: การสร้างหน้าจอโปรไฟล์และฟอร์มตอบรับข้อมูลผู้ใช้งาน (Lab)

ปฏิบัติการนี้จะฝึกฝนทักษะการประยุกต์ใช้คอมโพเนนต์พื้นฐานหลักของ React Native และแนวคิดการสร้างคอมโพเนนต์ย่อยที่กำหนดขึ้นเอง (Custom Component) ที่สนับสนุนโดยกลไก Type-safety ด้วย TypeScript Interface โดยมีเป้าหมายคือการพัฒนาหน้าจอ **ระบบข้อมูลโปรไฟล์พร้อมฟอร์มกรอกข้อมูลแบบโต้ตอบ (Profile Form with Live Preview Card)**

---

## 1. วัตถุประสงค์การเรียนรู้
1. สามารถใช้คอมโพเนนต์ `SafeAreaView` และ `ScrollView` เพื่อรองรับการทำงานของหน้าจอที่เนื้อหายาวโดยไม่ทับซ้อนขอบจอ
2. สามารถใช้คอมโพเนนต์ `Image` ในการแสดงผลภาพจากเน็ตเวิร์กได้อย่างถูกวิธี
3. สามารถประยุกต์ใช้ `TextInput` ในการรับข้อมูลรูปแบบต่าง ๆ พร้อมจัดการการทำงานของแป้นพิมพ์ (Keyboard Control)
4. สามารถควบคุมสไตล์ชีทแบบตอบสนองเมื่อผู้ใช้กดสัมผัสด้วย `Pressable` และพารามิเตอร์ `{ pressed }`
5. เข้าใจและลงมือสร้าง Custom Component พร้อมเขียน TypeScript Interface เพื่อกำกับประเภทตัวแปรของ Props ได้อย่างมีหลักการ

---

## 2. โจทย์และข้อกำหนดปฏิบัติการ (Requirements)
ผู้เรียนจะต้องแก้ไขไฟล์ภายในบทเรียนโดยสร้างโฟลเดอร์สำหรับ Custom Component และเขียนโค้ดประสานงานกันบนหน้าหลัก `app/index.tsx` ดังนี้:

### โครงสร้างการจัดแสดงข้อมูลเลย์เอาต์:
1. **พื้นที่ปลอดภัย (`SafeAreaView`):** คลุมรอบนอกสุดเพื่อป้องกันเนื้อหาทับซ้อนช่องบากบน iOS
2. **พื้นที่เลื่อนข้อความ (`ScrollView`):** ครอบเนื้อหาทั้งหมดเพื่อเปิดโอกาสให้เลื่อนสไลด์หน้าจอด้านล่างขึ้นมาได้ยามป้อนข้อมูลผ่านแป้นพิมพ์
3. **การ์ดโปรไฟล์แสดงผล (Live Preview Card):** 
   * สร้างเป็น Custom Component ชื่อ `ProfileCard` ไว้ในไฟล์แยกต่างหากคือ `components/ProfileCard.tsx`
   * มีคุณสมบัติ Props ใน TypeScript กำกับ ได้แก่ `avatarUrl: string`, `name: string`, `role: string`, `statusText?: string`, และ `onPressCard?: () => void`
   * แสดงรูปภาพด้วย `Image` (สไตล์ทรงกลมโค้งมน สมมาตร) พร้อมแสดงชื่อ ตำแหน่งงาน และสเตตัสข้อความ
4. **แบบฟอร์มแก้ไขข้อมูลโปรไฟล์ (Profile Form Editor):**
   * ช่องพิมพ์รับค่า URL รูปภาพ (`TextInput` กำหนดคีย์บอร์ดประเภทอีเมล/เว็บและปิดระบบตัวพิมพ์ใหญ่)
   * ช่องพิมพ์รับชื่อ (`TextInput` ทั่วไป)
   * ช่องพิมพ์รับตำแหน่งงาน (`TextInput` ทั่วไป)
   * ช่องพิมพ์รับข้อความสเตตัส (`TextInput` ทั่วไป)
5. **ปุ่มอัปเดตข้อมูล (Pressable Button):**
   * จัดสไตล์ด้วย `Pressable` 
   * มีเอฟเฟกต์ตอบสนองอย่างรวดเร็ว (ย่อขนาดลงและสีเข้มขึ้น) ขณะกดปุ่มสัมผัส

---

## 3. ขั้นตอนการลงมือปฏิบัติ (Step-by-Step Tutorial)

### ขั้นตอนที่ 1: การสร้าง Custom Component พร้อมระบุโครงสร้าง TypeScript Props Interface
สร้างไฟล์ใหม่ในโฟลเดอร์โครงการตามเส้นทาง `components/ProfileCard.tsx` (หากไม่มีโฟลเดอร์ `components` ให้สร้างโฟลเดอร์นี้ขึ้นมาใหม่ก่อน) และใส่รหัสด้านล่างนี้ลงไป:

```tsx
import { View, Text, Image, StyleSheet, Pressable } from 'react-native';

// 1. ระบุข้อกำหนดประเภทข้อมูล Props ด้วย TypeScript Interface
export interface ProfileCardProps {
  avatarUrl: string;
  name: string;
  role: string;
  statusText?: string;       // เครื่องหมาย ? แสดงว่าเป็นคุณสมบัติทางเลือก (Optional)
  onPressCard?: () => void;  // เหตุการณ์ฟังก์ชันส่งสัญญาณเมื่อกดการ์ด
}

// 2. นำฟังก์ชันคอมโพเนนต์มาแมปตัวแปร Props
export default function ProfileCard({
  avatarUrl,
  name,
  role,
  statusText = 'ไม่มีข้อความอัปเดตสเตตัสในขณะนี้', // ค่าเริ่มต้นหากไม่มีการส่งมา
  onPressCard
}: ProfileCardProps) {
  
  // กำหนดรูปภาพสำรองหาก URL ถูกส่งมาเป็นข้อความว่างเปล่า
  const validAvatar = avatarUrl.trim() !== '' 
    ? avatarUrl 
    : 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150';

  return (
    <Pressable 
      onPress={onPressCard}
      style={({ pressed }) => [
        styles.card,
        { opacity: pressed ? 0.95 : 1.0, transform: [{ scale: pressed ? 0.99 : 1.0 }] }
      ]}
    >
      {/* แสดงภาพโปรไฟล์จาก URL เครือข่าย */}
      <Image source={{ uri: validAvatar }} style={styles.avatar} />
      
      <View style={styles.infoContainer}>
        <Text style={styles.nameText}>{name}</Text>
        <Text style={styles.roleText}>{role}</Text>
        <View style={styles.statusBox}>
          <Text style={styles.statusLabelText}>สเตตัสปัจจุบัน:</Text>
          <Text style={styles.statusText}>{statusText}</Text>
        </View>
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#334155',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 4,
    marginVertical: 12,
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40, // ครึ่งหนึ่งของขนาดภาพดึงมุมกลมสมบูรณ์
    backgroundColor: '#334155',
  },
  infoContainer: {
    flex: 1,
    marginLeft: 16,
  },
  nameText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  roleText: {
    fontSize: 14,
    color: '#38bdf8',
    marginTop: 2,
  },
  statusBox: {
    marginTop: 8,
    borderTopWidth: 1,
    borderTopColor: '#334155',
    paddingTop: 6,
  },
  statusLabelText: {
    fontSize: 10,
    color: '#94a3b8',
    textTransform: 'uppercase',
  },
  statusText: {
    fontSize: 12,
    color: '#cbd5e1',
    fontStyle: 'italic',
    marginTop: 2,
  },
});
```

---

### ขั้นตอนที่ 2: วางหน้าจอและเก็บสถานะฟอร์มในคอมโพเนนต์หลัก `app/index.tsx`
เขียนโครงสร้างการรับข้อมูล และการแสดงตัวอย่างการ์ดร่วมกับแบบฟอร์มการพิมพ์ โดยใช้ State ในการสะท้อนข้อมูลแบบ Real-time:

```tsx
import { useState } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  TextInput, 
  Pressable, 
  SafeAreaView, 
  ScrollView, 
  Alert 
} from 'react-native';
import ProfileCard from '../components/ProfileCard'; // เรียกใช้ออบเจกต์ Custom Component

export default function App() {
  // ประกาศ State เพื่อผูกเข้ากับฟอร์ม TextInput
  const [name, setName] = useState('สมชาย ใจดี');
  const [role, setRole] = useState('Full Stack Developer');
  const [avatar, setAvatar] = useState('https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150');
  const [status, setStatus] = useState('กำลังเรียนรู้ React Native Expo SDK 54');

  // สเตตสำหรับการบันทึกจริงตอนกดปุ่ม
  const [savedData, setSavedData] = useState({
    name: 'สมชาย ใจดี',
    role: 'Full Stack Developer',
    avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150',
    status: 'กำลังเรียนรู้ React Native Expo SDK 54'
  });

  const handleUpdate = () => {
    setSavedData({ name, role, avatar, status });
    Alert.alert('อัปเดตสำเร็จ', 'ข้อมูลโปรไฟล์ได้รับการบันทึกบนเครื่องสมบูรณ์');
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        
        <Text style={styles.pageTitle}>ระบบจัดการโปรไฟล์ผู้ใช้</Text>
        <Text style={styles.sectionTitle}>การ์ดแสดงผลปัจจุบัน (Preview)</Text>
        
        {/* เรียกใช้งาน Custom Component และส่งผ่านข้อมูลผ่านโครงสร้าง Props */}
        <ProfileCard
          name={savedData.name}
          role={savedData.role}
          avatarUrl={savedData.avatar}
          statusText={savedData.status}
          onPressCard={() => Alert.alert('ข้อความสเตตัส', savedData.status)}
        />

        <View style={styles.formContainer}>
          <Text style={styles.sectionTitle}>ฟอร์มกรอกข้อมูลการแก้ไข</Text>
          
          {/* ช่องกรอกรูปภาพ Avatar URL */}
          <Text style={styles.label}>URL รูปภาพโปรไฟล์</Text>
          <TextInput
            style={styles.input}
            value={avatar}
            onChangeText={setAvatar}
            placeholder="ใส่ URL รูปภาพโปรไฟล์..."
            keyboardType="url"
            autoCapitalize="none"
            autoCorrect={false}
          />

          {/* ช่องกรอกชื่อ */}
          <Text style={styles.label}>ชื่อ-นามสกุล</Text>
          <TextInput
            style={styles.input}
            value={name}
            onChangeText={setName}
            placeholder="ป้อนชื่อและนามสกุล..."
          />

          {/* ช่องกรอกตำแหน่งงาน */}
          <Text style={styles.label}>ตำแหน่งงาน/บทบาท</Text>
          <TextInput
            style={styles.input}
            value={role}
            onChangeText={setRole}
            placeholder="เช่น UI/UX Designer..."
          />

          {/* ช่องกรอกสเตตัส */}
          <Text style={styles.label}>ข้อความสถานะ (Status Message)</Text>
          <TextInput
            style={[styles.input, styles.textArea]}
            value={status}
            onChangeText={setStatus}
            placeholder="ใส่ข้อความทักทายของคุณ..."
            multiline={true}
            numberOfLines={3}
          />

          {/* ปุ่มบันทึกจัดสไตล์ด้วย Pressable */}
          <Pressable 
            onPress={handleUpdate}
            style={({ pressed }) => [
              styles.submitButton,
              { 
                backgroundColor: pressed ? '#0369a1' : '#0284c7',
                transform: [{ scale: pressed ? 0.98 : 1.0 }]
              }
            ]}
          >
            <Text style={styles.submitButtonText}>อัปเดตโปรไฟล์</Text>
          </Pressable>

        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#0f172a', // คลุมธีมสีกึ่งน้ำเงินเข้ม
  },
  scrollContainer: {
    padding: 20,
    paddingBottom: 40,
  },
  pageTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: 8,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#94a3b8',
    marginTop: 12,
    marginBottom: 4,
  },
  formContainer: {
    marginTop: 16,
    backgroundColor: '#1e293b',
    padding: 20,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#334155',
  },
  label: {
    color: '#cbd5e1',
    fontSize: 14,
    fontWeight: '500',
    marginTop: 12,
    marginBottom: 6,
  },
  input: {
    backgroundColor: '#0f172a',
    borderWidth: 1,
    borderColor: '#334155',
    borderRadius: 8,
    height: 46,
    paddingHorizontal: 12,
    color: '#ffffff',
    fontSize: 14,
  },
  textArea: {
    height: 80,
    paddingTop: 10,
    textAlignVertical: 'top', // ป้องกันข้อความเด้งไปกึ่งกลางแนวแกนตั้งในระบบ Android
  },
  submitButton: {
    borderRadius: 8,
    height: 48,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 20,
  },
  submitButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
```

---

## 4. โค้ดเฉลยฉบับสมบูรณ์ (Complete Solution)

ด้านล่างนี้คือไฟล์โค้ดเฉลยฉบับรันได้จริง ประกอบด้วยโค้ดแยกตามโครงสร้างย่อย เพื่อให้ผู้เรียนสามารถประยุกต์ทำปฏิบัติการและนำโครงสร้างนี้ไปรันผลลัพธ์ผ่านหน้าจอจำลองได้ทันที:

### 4.1 ซอร์สโค้ดไฟล์คอมโพเนนต์: `components/ProfileCard.tsx`
```tsx
import { View, Text, Image, StyleSheet, Pressable } from 'react-native';

export interface ProfileCardProps {
  avatarUrl: string;
  name: string;
  role: string;
  statusText?: string;
  onPressCard?: () => void;
}

export default function ProfileCard({
  avatarUrl,
  name,
  role,
  statusText = 'ไม่มีข้อความอัปเดตสถานะ',
  onPressCard
}: ProfileCardProps) {
  
  const validAvatar = avatarUrl.trim() !== '' 
    ? avatarUrl 
    : 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150';

  return (
    <Pressable 
      onPress={onPressCard}
      style={({ pressed }) => [
        styles.card,
        { opacity: pressed ? 0.95 : 1.0, transform: [{ scale: pressed ? 0.99 : 1.0 }] }
      ]}
    >
      <Image source={{ uri: validAvatar }} style={styles.avatar} />
      <View style={styles.infoContainer}>
        <Text style={styles.nameText}>{name}</Text>
        <Text style={styles.roleText}>{role}</Text>
        <View style={styles.statusBox}>
          <Text style={styles.statusLabelText}>สเตตัสปัจจุบัน:</Text>
          <Text style={styles.statusText}>{statusText}</Text>
        </View>
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#334155',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 4,
    marginVertical: 12,
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#334155',
  },
  infoContainer: {
    flex: 1,
    marginLeft: 16,
  },
  nameText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  roleText: {
    fontSize: 14,
    color: '#38bdf8',
    marginTop: 2,
  },
  statusBox: {
    marginTop: 8,
    borderTopWidth: 1,
    borderTopColor: '#334155',
    paddingTop: 6,
  },
  statusLabelText: {
    fontSize: 10,
    color: '#94a3b8',
    textTransform: 'uppercase',
  },
  statusText: {
    fontSize: 12,
    color: '#cbd5e1',
    fontStyle: 'italic',
    marginTop: 2,
  },
});
```

### 4.2 ซอร์สโค้ดหน้าจอแอปหลัก: `app/index.tsx`
```tsx
import { useState } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  TextInput, 
  Pressable, 
  SafeAreaView, 
  ScrollView, 
  Alert 
} from 'react-native';
import ProfileCard from '../components/ProfileCard';

export default function App() {
  const [name, setName] = useState('สมชาย ใจดี');
  const [role, setRole] = useState('Full Stack Developer');
  const [avatar, setAvatar] = useState('https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150');
  const [status, setStatus] = useState('กำลังเรียนรู้ React Native Expo SDK 54');

  const [savedData, setSavedData] = useState({
    name: 'สมชาย ใจดี',
    role: 'Full Stack Developer',
    avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150',
    status: 'กำลังเรียนรู้ React Native Expo SDK 54'
  });

  const handleUpdate = () => {
    setSavedData({ name, role, avatar, status });
    Alert.alert('อัปเดตสำเร็จ', 'ข้อมูลโปรไฟล์ได้รับการบันทึกบนเครื่องสมบูรณ์');
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        
        <Text style={styles.pageTitle}>ระบบจัดการโปรไฟล์ผู้ใช้</Text>
        <Text style={styles.sectionTitle}>การ์ดแสดงผลปัจจุบัน (Preview)</Text>
        
        <ProfileCard
          name={savedData.name}
          role={savedData.role}
          avatarUrl={savedData.avatar}
          statusText={savedData.status}
          onPressCard={() => Alert.alert('ข้อความสเตตัส', savedData.status)}
        />

        <View style={styles.formContainer}>
          <Text style={styles.sectionTitle}>ฟอร์มกรอกข้อมูลการแก้ไข</Text>
          
          <Text style={styles.label}>URL รูปภาพโปรไฟล์</Text>
          <TextInput
            style={styles.input}
            value={avatar}
            onChangeText={setAvatar}
            placeholder="ใส่ URL รูปภาพโปรไฟล์..."
            keyboardType="url"
            autoCapitalize="none"
            autoCorrect={false}
          />

          <Text style={styles.label}>ชื่อ-นามสกุล</Text>
          <TextInput
            style={styles.input}
            value={name}
            onChangeText={setName}
            placeholder="ป้อนชื่อและนามสกุล..."
          />

          <Text style={styles.label}>ตำแหน่งงาน/บทบาท</Text>
          <TextInput
            style={styles.input}
            value={role}
            onChangeText={setRole}
            placeholder="เช่น UI/UX Designer..."
          />

          <Text style={styles.label}>ข้อความสถานะ (Status Message)</Text>
          <TextInput
            style={[styles.input, styles.textArea]}
            value={status}
            onChangeText={setStatus}
            placeholder="ใส่ข้อความทักทายของคุณ..."
            multiline={true}
            numberOfLines={3}
          />

          <Pressable 
            onPress={handleUpdate}
            style={({ pressed }) => [
              styles.submitButton,
              { 
                backgroundColor: pressed ? '#0369a1' : '#0284c7',
                transform: [{ scale: pressed ? 0.98 : 1.0 }]
              }
            ]}
          >
            <Text style={styles.submitButtonText}>อัปเดตโปรไฟล์</Text>
          </Pressable>

        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#0f172a',
  },
  scrollContainer: {
    padding: 20,
    paddingBottom: 40,
  },
  pageTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: 8,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#94a3b8',
    marginTop: 12,
    marginBottom: 4,
  },
  formContainer: {
    marginTop: 16,
    backgroundColor: '#1e293b',
    padding: 20,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#334155',
  },
  label: {
    color: '#cbd5e1',
    fontSize: 14,
    fontWeight: '500',
    marginTop: 12,
    marginBottom: 6,
  },
  input: {
    backgroundColor: '#0f172a',
    borderWidth: 1,
    borderColor: '#334155',
    borderRadius: 8,
    height: 46,
    paddingHorizontal: 12,
    color: '#ffffff',
    fontSize: 14,
  },
  textArea: {
    height: 80,
    paddingTop: 10,
    textAlignVertical: 'top',
  },
  submitButton: {
    borderRadius: 8,
    height: 48,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 20,
  },
  submitButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
```

---

← [ย้อนกลับแบบทดสอบ: 03-quiz.md](./03-quiz.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ศึกษาบทเรียนถัดไป: บทที่ 4](../chapter-04-state-props-lists/) →
