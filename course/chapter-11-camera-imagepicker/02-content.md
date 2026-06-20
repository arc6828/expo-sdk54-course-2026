# บทที่ 11: การใช้งานกล้อง อัลบั้มภาพ และระบบจัดเก็บไฟล์เนทีฟร่วมกับคลาวด์ (Content)

การสร้างสรรค์โมบายแอปพลิเคชันที่ต้องทำงานกับรูปภาพ ไม่เพียงแค่การถ่ายรูปหรือดึงภาพมาแสดงบนหน้าจอเท่านั้น แต่นักพัฒนาจำเป็นต้องมีความเข้าใจอย่างลึกซึ้งเกี่ยวกับการจัดการพื้นที่จัดเก็บไฟล์ (File Storage) เพื่อให้ภาพที่ได้ไม่สูญหายและถูกเผยแพร่ในระดับสิทธิ์ที่เหมาะสม ในบทเรียนนี้เราจะเรียนรู้ตั้งแต่การเข้าถึงกล้องและอัลบั้มภาพเนทีฟ ไปจนถึงระบบการจัดการไฟล์ 3 รูปแบบหลัก ได้แก่ ไฟล์เฉพาะแอป (Sandbox), ไฟล์แชร์ร่วมกับแอปอื่น (Shared Gallery) และไฟล์บนคลาวด์ (Supabase Cloud Storage)

---

## 11.1 กลไกการจัดการสิทธิ์กล้องถ่ายรูปและคลังภาพ (Camera & Media Permissions)

การเข้าถึงกล้องถ่ายรูปและการสืบค้นรูปภาพเก่าในเครื่องถือเป็นเรื่องละเอียดอ่อนต่อความเป็นส่วนตัว (Privacy) ระบบปฏิบัติการ iOS และ Android จึงมีระบบความปลอดภัยและบังคับร้องขอสิทธิ์แยกประเภทกันอย่างชัดเจน:

### 1. สิทธิ์การเปิดเลนส์กล้อง (Camera Permission)
สำหรับการใช้ถ่ายรูปสด ๆ ในแอป เราสามารถใช้ Hook `useCameraPermissions()` ของแพ็คเกจ `expo-camera` เพื่อตรวจสอบสถานะสิทธิ์และยื่นขอสิทธิ์ได้โดยตรง:

```tsx
import { useCameraPermissions } from 'expo-camera';

const [permission, requestPermission] = useCameraPermissions();

// ตรวจสอบสถานะการได้รับสิทธิ์
if (!permission) {
  // สถานะยังคงกำลังโหลดเช็ค
}
if (!permission.granted) {
  // สิทธิ์ยังไม่ได้เปิดอนุมัติ ต้องกดเรียก requestPermission()
}
```

### 2. สิทธิ์การเข้าถึงคลังสื่อเพื่อเลือกรูปภาพ (Media Library / Photos Permission)
สำหรับการดึงภาพถ่ายเดิมจากคลังภาพมาใช้งานผ่าน `expo-image-picker` จะต้องมีการร้องขอสิทธิ์แยกออกต่างหาก:

```tsx
import * as ImagePicker from 'expo-image-picker';

const requestGalleryPermission = async () => {
  const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
  if (status !== 'granted') {
    alert('จำเป็นต้องขอสิทธิ์เข้าถึงคลังภาพเพื่อเลือกรูปอวาตาร์');
  }
};
```

---

## 11.2 การใช้งาน CameraView เพื่อพรีวิวภาพสด (Camera Live Preview)

ใน Expo SDK 54 คอมโพเนนต์หลักที่ใช้เปิดช่องเลนส์รับภาพสดคือ **`CameraView`** (ถูกพัฒนามาทดแทนคอมโพเนนต์ `Camera` ตัวเดิม) 

### พร็อพส์หลักที่ใช้ควบคุม `<CameraView>`:
* **`facing`**: กำหนดประเภทเลนส์ที่จะใช้เปิด รับค่า `'front'` (กล้องหน้า) หรือ `'back'` (กล้องหลัง)
* **`autofocus`**: เปิดหรือปิดระบบดักจับโฟกัสภาพอัตโนมัติ (`'on'` หรือ `'off'`)
* **`ref`**: ตัวเชื่อมโยง (Reference) เพื่อเรียกคำสั่งลั่นชัตเตอร์ถ่ายภาพนิ่ง

```tsx
import React, { useState } from 'react';
import { StyleSheet, Text, View, Button, TouchableOpacity } from 'react-native';
import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';

export default function CameraPreviewApp() {
  const [facing, setFacing] = useState<CameraType>('front');
  const [permission, requestPermission] = useCameraPermissions();

  if (!permission) return <View />; // กำลังโหลดเช็คสิทธิ์

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={styles.text}>แอปต้องการสิทธิ์เข้าใช้กล้องถ่ายรูป</Text>
        <Button onPress={requestPermission} title="อนุมัติสิทธิ์การเข้าใช้งานกล้อง" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <CameraView style={styles.camera} facing={facing}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity 
            style={styles.button} 
            onPress={() => setFacing(curr => curr === 'back' ? 'front' : 'back')}
          >
            <Text style={styles.buttonText}>🔄 สลับมุมกล้อง</Text>
          </TouchableOpacity>
        </View>
      </CameraView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center' },
  camera: { flex: 1 },
  buttonContainer: { flex: 1, justifyContent: 'flex-end', margin: 40 },
  button: { backgroundColor: 'rgba(0,0,0,0.5)', padding: 12, borderRadius: 8, alignItems: 'center' },
  buttonText: { color: 'white', fontWeight: 'bold' },
  text: { textAlign: 'center', marginBottom: 10 }
});
```

---

## 11.3 การลั่นชัตเตอร์ถ่ายภาพนิ่ง (Taking Photos with takePictureAsync)

เพื่อบันทึกรูปภาพพรีวิวเป็นรูปนิ่ง (Snapshot) เราจะอ้างอิง Ref ไปยังคอมโพเนนต์ `<CameraView>` แล้วเรียกใช้เมธอด Asynchronous ชื่อ **`takePictureAsync()`**:

```tsx
import React, { useRef } from 'react';
import { CameraView } from 'expo-camera';
import { TouchableOpacity, Text } from 'react-native';

export default function CaptureComponent() {
  const cameraRef = useRef<CameraView | null>(null);

  const takePhoto = async () => {
    if (cameraRef.current) {
      const result = await cameraRef.current.takePictureAsync({
        quality: 0.8,         // คุณภาพการบีบอัดภาพ (0.0 ถึง 1.0)
        skipProcessing: false // จัดการหมุนทิศทางภาพถ่ายให้อัตโนมัติ
      });
      // ผลลัพธ์จะคืนค่าเป็นอ็อบเจกต์ที่มี URI ไฟล์ภาพชั่วคราวชี้ที่หน่วยความจำแคช
      console.log('ที่อยู่รูปถ่ายชั่วคราว:', result?.uri);
    }
  };

  return (
    <CameraView ref={cameraRef} style={{ flex: 1 }}>
      <TouchableOpacity onPress={takePhoto} style={{ alignSelf: 'center', margin: 40 }}>
        <Text style={{ color: 'white', fontSize: 18, fontWeight: 'bold' }}>📸 ลั่นชัตเตอร์</Text>
      </TouchableOpacity>
    </CameraView>
  );
}
```

---

## 11.4 การเลือกรูปภาพและสื่อผ่าน expo-image-picker (Image Library API)

ในการพัฒนาฟีเจอร์ดึงไฟล์ภาพที่มีอยู่แล้วในคลังอัลบั้มของเครื่องขึ้นมาจัดแสดง เราจะใช้ไลบรารีมาตรฐานยอดนิยมคือ **`expo-image-picker`** ผ่านคำสั่ง Asynchronous ชื่อ **`launchImageLibraryAsync()`**:

```tsx
import React, { useState } from 'react';
import { View, Button, Image, StyleSheet } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

export default function PickImageApp() {
  const [imageUri, setImageUri] = useState<string | null>(null);

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images, // คัดเฉพาะประเภทไฟล์ภาพนิ่ง
      allowsEditing: true, // เปิดกรอบแก้ไข/ตัดรูปภาพหน้าเนทีฟของอุปกรณ์
      aspect: [1, 1],      // บังคับครอปเป็นสัดส่วนจัตุรัส กว้าง:สูง
      quality: 0.8,        // กำหนดความละเอียดผลลัพธ์
    });

    if (!result.canceled && result.assets && result.assets.length > 0) {
      setImageUri(result.assets[0].uri);
    }
  };

  return (
    <View style={styles.container}>
      <Button title="เลือกรูปภาพจากอัลบั้ม" onPress={pickImage} />
      {imageUri && <Image source={{ uri: imageUri }} style={styles.image} />}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  image: { width: 150, height: 150, borderRadius: 75, marginTop: 15 }
});
```

---

## 11.5 ระบบจัดการไฟล์แบบที่ 1: Private Sandbox Storage (แอปมองเห็นเฉพาะตัว)

รูปภาพที่ได้จากการสั่งถ่ายด้วยกล้องถ่ายรูป หรือได้จากการดึงภาพของ Image Picker จะได้รับการสร้างเป็นที่อยู่พาธชั่วคราวอยู่ใน **Cache Directory** เสมอ (เช่น `file:///.../Caches/xxx.jpg`)

ในระบบปฏิบัติการ iOS และ Android พื้นที่ความจำของแอปพลิเคชันจะถูกจำกัดอยู่ในเขตปลอดภัยที่เรียกว่า **Sandbox** โดยแบ่งออกเป็นสองระดับหลัก ๆ:

1. **Cache Folder (`cacheDirectory`)**: ใช้เก็บผลลัพธ์ชั่วคราว มีข้อเสียหลักคือ **OS สามารถกวาดล้างลบไฟล์ออกได้อัตโนมัติ** เมื่ออุปกรณ์ต้องการทวงคืนพื้นที่ดิสก์ว่างคืน หากเปิดแอปขึ้นมาอีกครั้ง ภาพโปรไฟล์ก็อาจชำรุดเสียหายได้
2. **Documents Folder (`documentDirectory`)**: เป็นโฟลเดอร์สำหรับเอกสารสำคัญของแอป **ไม่มีทางโดนระบบปฏิบัติการลบทิ้งอย่างเด็ดขาด** ยกเว้นตัวผู้ใช้งานจะเป็นคนกดถอนการติดตั้งแอปพลิเคชัน (Uninstall) ออกไปด้วยตัวเอง

ดังนั้น หากเราจำเป็นต้องทำระบบบันทึกรูปโปรไฟล์ออฟไลน์ให้อยู่ได้คงทนถาวร เราต้องคัดลอกไฟล์ย้ายออกจากห้องแคชด้วยไลบรารี **`expo-file-system`**:

```tsx
import * as FileSystem from 'expo-file-system';

const copyToPrivateStorage = async (temporaryUri: string): Promise<string | null> => {
  try {
    const filename = `profile_avatar_${Date.now()}.jpg`; // ตั้งชื่อใหม่ไม่ให้ชนกัน
    const destinationUri = `${FileSystem.documentDirectory}${filename}`;

    // ย้ายไฟล์จาก Cache ไปยังโฟลเดอร์ Document ส่วนตัวของแอป
    await FileSystem.copyAsync({
      from: temporaryUri,
      to: destinationUri,
    });

    console.log('ไฟล์ถูกเก็บไว้แบบถาวรเฉพาะตัวแอปที่:', destinationUri);
    return destinationUri; // คืนค่าที่อยู่ใหม่เพื่อนำไปเซฟลง AsyncStorage ต่อไป
  } catch (error) {
    console.error('คัดลอกไฟล์ Sandbox ล้มเหลว:', error);
    return null;
  }
};
```

---

## 11.6 ระบบจัดการไฟล์แบบที่ 2: Shared Media Storage (แอปอื่นมองเห็นและเข้าถึงข้อมูลร่วมกันได้)

หากแอปพลิเคชันของเราต้องการถ่ายรูปภาพ แล้วบันทึกส่งออกไปจัดแสดงอยู่ในแกลเลอรีหลักของโทรศัพท์มือถือ (Camera Roll / Photos App) เพื่อให้แอปพลิเคชันภายนอก (เช่น Facebook, Instagram, LINE) ค้นหาและหยิบภาพนั้นไปใช้งานต่อได้ เราจะไม่บันทึกใน Sandbox แต่จะต้องบันทึกเข้าสู่คลังภาพสาธารณะของระบบ โดยใช้ไลบรารี **`expo-media-library`**

### การติดตั้ง:
```bash
npx expo install expo-media-library
```

### การตั้งค่าการขอสิทธิ์เข้าใช้งานใน `app.json` (สำหรับสร้าง Asset):
```json
{
  "expo": {
    "plugins": [
      [
        "expo-media-library",
        {
          "photosPermission": "แอปต้องการขอสิทธิ์เข้าถึงเพื่อบันทึกไฟล์ภาพถ่ายลงสู่แกลเลอรีของคุณ"
        }
      ]
    ]
  }
}
```

### ตัวอย่างการส่งออกไฟล์ไปที่คลังแกลเลอรีสาธารณะ:
เมื่อเรียกใช้งานคำสั่ง `createAssetAsync` รูปจะถูกนำไปบรรจุลงในคลังภาพส่วนกลางของตัวเครื่องทันที และเปิดโอกาสให้ระบบแอปอื่น ๆ สแกนตรวจพบภาพนี้ได้:

```tsx
import * as MediaLibrary from 'expo-media-library';
import { Alert } from 'react-native';

const saveToSharedGallery = async (localUri: string) => {
  try {
    // 1. ตรวจสอบสิทธิ์เข้าถึงคลังสื่อในเครื่องก่อนเขียนข้อมูล
    const { status } = await MediaLibrary.requestPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('สิทธิ์ถูกปฏิเสธ', 'กรุณาอนุมัติสิทธิ์เข้าถึงแกลเลอรีสาธารณะ');
      return;
    }

    // 2. สร้างสินทรัพย์ภาพ (Asset) บันทึกลงเครื่องภายนอกแซนด์บ็อกซ์
    const asset = await MediaLibrary.createAssetAsync(localUri);
    Alert.alert('บันทึกสำเร็จ!', 'รูปภาพของท่านถูกจัดเก็บลงแกลเลอรีส่วนกลางแล้ว');
    console.log('Asset ID:', asset.id);
  } catch (error) {
    console.error('เกิดข้อผิดพลาดในการบันทึกลงแกลเลอรีหลัก:', error);
  }
};
```

---

## 11.7 ระบบจัดการไฟล์แบบที่ 3: Cloud Storage Network (อัปโหลด/ดาวน์โหลดผ่าน Supabase Storage)

หากรูปโปรไฟล์นั้นต้องซิงก์แลกเปลี่ยนนำไปเปิดดูในสมาร์ทโฟนของเพื่อน หรือนำไปแสดงผลบนเว็บไซต์กลาง ข้อมูลภาพถ่ายจะไม่สามารถเก็บอยู่เพียงในเครื่องเครื่องเดียวได้ เราจึงจำเป็นต้องอัปโหลดส่งไฟล์ผ่านทางเครือข่ายเครือข่าย (Network System) ขึ้นไปเก็บไว้บนคลาวด์ เช่น บริการ **Supabase Storage Buckets**

### กลไกการอัปโหลดไฟล์รูปภาพใน React Native ไปยัง Supabase:
เนื่องจากสภาพแวดล้อมระบบ React Native ไม่มีฟังก์ชันจัดการ Blob หรือ File แบบมาตรฐานเดียวกันกับบราวเซอร์คอมพิวเตอร์ วิธีการส่งไฟล์ที่เสถียรที่สุดคือการอ่านไฟล์เป็นรูปแบบสตริงรหัส **Base64** จากดิสก์ด้วย `expo-file-system` แล้วทำการแกะถอดรหัสออกมาเป็นรหัสฐานข้อมูลแบบไบนารี **`ArrayBuffer`** ก่อนส่งยิงขึ้น API:

### 1. การติดตั้งไลบรารีแปลงข้อมูล Base64:
```bash
npm install base64-js
```

### 2. โค้ด Asynchronous สำหรับอัปโหลดขึ้น Supabase Storage:
ผู้พัฒนาต้องเข้าไปที่แดชบอร์ดของ Supabase แล้วเปิดสร้างโฟลเดอร์ฝากไฟล์ที่เรียกว่า **Bucket** (เช่นสร้างชื่อตารางฝากไฟล์ชื่อ `avatars`) และตั้งค่านโยบายสิทธิ์ (RLS Rules) ให้เป็น Public หรืออนุญาตสิทธิ์การอัปโหลดให้พร้อมใช้งาน:

```tsx
import { supabase } from '../lib/supabase';
import * as FileSystem from 'expo-file-system';
import { decode } from 'base64-js';

const uploadToSupabaseCloud = async (localFileUri: string): Promise<string | null> => {
  try {
    // 1. อ่านข้อมูลไฟล์ภาพจากเครื่องปลายทางออกมาเป็น Base64 String
    const base64Data = await FileSystem.readAsStringAsync(localFileUri, {
      encoding: FileSystem.EncodingType.Base64,
    });

    // 2. แปลงสตริงรหัส Base64 ให้กลายเป็น ArrayBuffer
    const arrayBuffer = decode(base64Data);

    // 3. กำหนดชื่อและพาธปลายทางที่จะบันทึกไว้ในระบบคลาวด์
    const fileName = `profile_${Date.now()}.jpg`;
    const filePath = `user_avatar/${fileName}`;

    // 4. สั่งส่งอัปโหลด (Upload) ข้อมูลขึ้นไปฝากที่คลาวด์บัคเก็ต 'avatars'
    const { data, error } = await supabase.storage
      .from('avatars') // ระบุชื่อ Bucket เป้าหมาย
      .upload(filePath, arrayBuffer, {
        contentType: 'image/jpeg',
        upsert: true // หากเจอพาธเดียวกันให้สั่งเขียนทับทันที
      });

    if (error) {
      throw error;
    }

    // 5. ดึงข้อมูลที่อยู่พาธ URL สาธารณะ (Public URL) สำหรับนำไปใช้เรนเดอร์แสดงผล
    const { data: publicUrlData } = supabase.storage
      .from('avatars')
      .getPublicUrl(filePath);

    console.log('อัปโหลดขึ้นคลาวด์สำเร็จ! ลิงก์รูปภาพสาธารณะคือ:', publicUrlData.publicUrl);
    return publicUrlData.publicUrl; // ลิงก์ตรงที่นำไปส่งต่อให้ API อื่นใช้งานได้ทั่วโลก

  } catch (error: any) {
    console.error('ไม่สามารถส่งข้อมูลขึ้นระบบคลาวด์ได้:', error.message || error);
    return null;
  }
};
```

---

## สรุปเปรียบเทียบระบบจัดเก็บไฟล์ทั้ง 3 รูปแบบ

| รูปแบบการจัดเก็บ | พื้นที่จัดเก็บ (Directory/Server) | การแบ่งปัน (Sharing) | ความคงทนถาวร (Persistence) |
| :--- | :--- | :--- | :--- |
| **1. Private Sandbox** | โฟลเดอร์เอกสารภายในแอป (`documentDirectory`) | **เฉพาะแอปตนเองเท่านั้น** แอปอื่นไม่มีสิทธิ์มาแตะต้อง | **ถาวรในเครื่อง** จนกว่าแอปพลิเคชันจะถูกถอนออก |
| **2. Shared Storage** | แกลเลอรีสื่อหลักของโทรศัพท์ (`expo-media-library`) | **แบ่งปันสาธารณะในเครื่อง** แอปอื่นเปิดแกลเลอรีก็สแกนค้นเจอ | **ถาวรตามสิทธิ์ผู้ใช้** ดำรงอยู่ตลอดไปจนกว่าจะกดยืนยันลบในคลังภาพ |
| **3. Cloud Storage** | บนเซิร์ฟเวอร์ฝากไฟล์คลาวด์ (`Supabase Storage`) | **เข้าถึงข้ามอุปกรณ์ทั่วโลก** ผ่านการกระจายตัวของ URL เครือข่าย | **ถาวรตามระบบเซิร์ฟเวอร์** ลบออกเมื่อมีคำสั่ง API Trigger ลบทิ้งเท่านั้น |

## 11.8 สรุปท้ายบทเรียน

**กลไกการจัดการสิทธิ์กล้องถ่ายรูปและคลังภาพ:** การเข้าถึงกล้องและภาพถ่ายในเครื่องผู้ใช้จำเป็นต้องทำตามมาตรการความปลอดภัยและได้รับอนุญาตจากระบบปฏิบัติการ โดยเราสามารถตรวจสอบและขอสิทธิ์ใช้งานเลนส์กล้องแยกด้วย useCameraPermissions Hook ของ expo-camera และขอสิทธิ์อ่านคลังรูปภาพแกลเลอรีด้วยฟังก์ชันขออนุญาตของ ImagePicker (Media Library Permissions) ก่อนที่จะเรียกเข้าใช้งาน

**การใช้งาน CameraView เพื่อพรีวิวภาพสด:** คอมโพเนนต์ CameraView เข้ามาทำหน้าที่เปิดช่องรับสัญญาณภาพและแสดงพรีวิวภาพเคลื่อนไหวสดจากกล้องบนหน้าจอมือถือใน Expo SDK 54 โดยเราสามารถส่งผ่านพร็อพส์ facing บ่งชี้เลนส์หน้าหรือหลัง และใช้ autofocus ในการสั่งจัดระเบียบความคมชัดอัตโนมัติ ซึ่งต้องเตรียมการดีไซน์ปุ่มสัมผัสในการเปิดปิดมุมกล้องให้ใช้งานได้อย่างสะดวกสบาย

**การลั่นชัตเตอร์ถ่ายภาพนิ่ง:** การถ่ายภาพนิ่งแบบ Snapshot จากตัวรับพรีวิวสดจะกระทำได้โดยการประกาศผูกตัวแปรอ้างอิง Ref เข้าหาคอมโพเนนต์ CameraView และเรียกฟังก์ชัน Asynchronous ยอดนิยมอย่าง takePictureAsync ซึ่งจะบันทึกรูปภาพนิ่งชั่วคราวลงในหน่วยความจำแคชของอุปกรณ์ และส่งคืนค่าพารามิเตอร์ของรูปภาพและที่อยู่ไฟล์ (URI) กลับมาประมวลผลต่อ

**การเลือกรูปภาพและสื่อผ่าน expo-image-picker:** เพื่ออำนวยความสะดวกให้ผู้ใช้งานสามารถดึงข้อมูลรูปภาพหรือสื่อที่มีการเก็บบันทึกไว้เดิมในเครื่องมาประยุกต์ใช้งาน (เช่น การเลือกภาพอวาตาร์) เราจะประยุกต์ใช้คำสั่ง launchImageLibraryAsync ของ expo-image-picker ในการเปิดหน้าต่างแกลเลอรีเนทีฟของโทรศัพท์เพื่อให้ผู้ใช้จัดแจงครอปภาพและส่งค่า URI รูปที่ถูกเลือกกลับมา

**ระบบจัดการไฟล์แบบที่ 1 (Private Sandbox Storage):** ไฟล์ที่ได้จากการถ่ายภาพหรือการดึงภาพจากแกลเลอรีจะได้รับการสร้างเป็นที่อยู่พาธชั่วคราวอยู่ใน cacheDirectory เสมอ ซึ่งเสี่ยงต่อการโดนระบบปฏิบัติการล้างข้อมูลทิ้งเมื่อพื้นที่เต็ม ผู้พัฒนาจึงต้องใช้ expo-file-system ในการคัดลอกไฟล์ย้ายเข้าไปจัดเก็บถาวรใน Sandbox ส่วนตัวของแอป หรือเรียกว่า documentDirectory ซึ่งมีความปลอดภัยและระบบจะไม่เข้ามากวนข้อมูล

**ระบบจัดการไฟล์แบบที่ 2 (Shared Media Storage):** กรณีที่รูปถ่ายจากแอปพลิเคชันของเราต้องการส่งต่อไปใช้งานร่วมกับแกลเลอรีหลักของโทรศัพท์ เพื่อเปิดโอกาสให้แอปภายนอก เช่น LINE หรือ Facebook สแกนดึงรูปนี้ไปใช้ได้ต่อ เราจะเปลี่ยนจากการเก็บข้อมูลในแซนด์บ็อกซ์ส่วนตัวมาส่งออกข้อมูลผ่านคำสั่ง createAssetAsync ของ expo-media-library เพื่อไปจดทะเบียนลงทะเบียนไฟล์ในคลังภาพสาธารณะของระบบ

**ระบบจัดการไฟล์แบบที่ 3 (Cloud Storage Network):** เพื่อให้รูปภาพถ่ายสามารถเผยแพร่ข้ามอุปกรณ์และส่งต่อขึ้นฝั่งเว็บไซต์ได้ ข้อมูลรูปภาพจำเป็นต้องอัปโหลดขึ้นฝั่งคลาวด์ เช่น Supabase Storage Buckets โดย React Native จะต้องใช้ expo-file-system ในการอ่านข้อมูลจากพิกัดไฟล์ออกมาเป็นสตริงรหัส Base64 จากนั้นใช้ไลบรารี base64-js ถอดรหัสเป็น ArrayBuffer และส่งยิงอัปโหลดขึ้นเซิร์ฟเวอร์เพื่อให้ได้ลิงก์ตรง (Public URL) สาธารณะ

---

← [ย้อนกลับแผนการสอน: 01-lesson-plan.md](./01-lesson-plan.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ทำแบบทดสอบถัดไป: 03-quiz.md](./03-quiz.md) →
