# ปฏิบัติการ บทที่ 11: การพัฒนาแอปเลือกรูปโปรไฟล์อวาตาร์บันทึก 3 ระบบ (Lab)

ปฏิบัติการนี้จะฝึกทักษะระดับสูงในการทำโมดูลอวาตาร์ โดยเชื่อมประสานกล้องพรีวิวสดของระบบเนทีฟและการกักเก็บไฟล์ 3 ระบบ ได้แก่ **Private Sandbox** (ในดิสก์จำกัดเฉพาะแอป), **Shared Media Library** (ในดิสก์สาธารณะแชร์ข้ามแอป) และ **Cloud Network Storage** (อัปโหลดเซิร์ฟเวอร์ Supabase Storage)

---

## 1. วัตถุประสงค์การเรียนรู้
1. สามารถเขียนขอยื่นสิทธิ์ความปลอดภัยเข้าใช้กล้องถ่ายรูป อัลบั้มส่วนตัว และการเขียนสื่อลงแกลเลอรีสาธารณะได้สำเร็จ
2. สามารถควบคุมกล้องเซลฟี่สดผ่าน `CameraView` และสลับกล้องหน้าหลังรวมถึงสั่งชัตเตอร์ Asynchronous
3. สามารถเรียกใช้ `expo-file-system` ย้ายไฟล์ภาพจาก Cache Folder ไปฝากถาวรใน `documentDirectory` ภายใน Sandbox
4. สามารถประยุกต์ใช้งาน `expo-media-library` ส่งออกไฟล์ภาพไปเก็บบันทึกในคลังภาพสาธารณะของระบบเครื่องเพื่อแชร์ข้ามแอปพลิเคชัน
5. สามารถเขียนตรรกะการแปลงสตริง Base64 และ ArrayBuffer เพื่อยิงภาพอัปโหลดตรงขึ้นระบบฝากไฟล์ Supabase Storage Bucket และดึง URL ลิงก์ตรงมาจัดแสดงผล

---

## 2. โจทย์และข้อกำหนดปฏิบัติการ (Requirements)

ผู้เรียนต้องจัดสร้างโปรเจกต์ React Native Expo โดยมีโครงสร้างดังนี้:

```text
โครงสร้างไฟล์ปฏิบัติการ:
├── .env                              => บรรจุคีย์โครงการ EXPO_PUBLIC_SUPABASE_URL และ EXPO_PUBLIC_SUPABASE_ANON_KEY
├── app.json                          => ลงทะเบียนคำอนุญาตสิทธิ์ใช้งานกล้อง อัลบั้มภาพ และคลังภาพส่วนกลาง
├── lib/
│   └── supabase.ts                   => สร้างอินสแตนซ์ Supabase Client
└── app/
    └── index.tsx                     => หน้าจอจัดแสดงโปรไฟล์ แผงกล้อง Modal และฟังก์ชันการเขียนไฟล์ 3 ระบบ
```

### การตั้งค่าตารางจัดเก็บไฟล์ฝากคลาวด์บน Supabase (Supabase Storage Setup):
1. ให้ผู้เรียนไปที่คอนโซลของ Supabase เข้าหัวข้อ **Storage**
2. กดสร้าง Bucket ใหม่ขึ้นมาชื่อว่า **`avatars`**
3. ปรับเปลี่ยนนโยบายความปลอดภัย (RLS Policies) ของบัคเก็ต `avatars` นี้โดยกดเพิ่มกฎใหม่ (New Policy) -> เลือกเทมเพลต **"Enable read access to everyone"** (เพื่อให้บุคคลภายนอกสามารถดึงภาพจาก URL สาธารณะได้) และกฎ **"Enable insert/upload access for authenticated and anonymous users"** (สำหรับการเปิดให้อัปโหลดไฟล์ส่งขึ้นไป)

---

## 3. ขั้นตอนการลงมือปฏิบัติ (Step-by-Step Tutorial)

### ขั้นตอนที่ 1: ติดตั้งคลังไลบรารีทั้งหมด
เปิดใช้งานเทอร์มินัลในโฟลเดอร์โปรเจกต์ของคุณแล้วสั่งรันบรรทัดต่อไปนี้:
```bash
npx expo install expo-camera expo-image-picker expo-file-system expo-media-library @react-native-async-storage/async-storage base64-js
```

### ขั้นตอนที่ 2: ตั้งค่าระบบขอสิทธิ์ในไฟล์ `app.json`
เปิดไฟล์ `app.json` แล้วระบุ Plugins สิทธิ์เข้าใช้งานของอุปกรณ์ให้เรียบร้อย:
```json
{
  "expo": {
    "name": "MultiAvatarApp",
    "slug": "multi-avatar-app",
    "version": "1.0.0",
    "plugins": [
      [
        "expo-camera",
        {
          "cameraPermission": "แอปต้องการขอสิทธิ์เข้าใช้งานกล้องเพื่อใช้ในการถ่ายภาพโปรไฟล์"
        }
      ],
      [
        "expo-image-picker",
        {
          "photosPermission": "แอปต้องการขอสิทธิ์เข้าถึงคลังสื่อภาพเพื่อดึงภาพมาอัปเกรดโปรไฟล์"
        }
      ],
      [
        "expo-media-library",
        {
          "photosPermission": "แอปต้องการขอสิทธิ์เขียนบันทึกไฟล์ภาพถ่ายของแอปเพื่อนำไปบันทึกลงคลังแกลเลอรีเครื่อง"
        }
      ]
    ]
  }
}
```

### ขั้นตอนที่ 3: จัดการระบุคีย์ลับเซิร์ฟเวอร์ใน `lib/supabase.ts`
สร้างไฟล์ `.env` ไว้ที่โฟลเดอร์ชั้นนอกสุดของโปรเจกต์เพื่อนำส่งคีย์ลับ:
```text
EXPO_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-anon-public-key-here
```
และสร้างไฟล์เชื่อมโยง `lib/supabase.ts`:
```typescript
import 'react-native-url-polyfill/auto';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY || '';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
```

---

## 4. โค้ดเฉลยฉบับสมบูรณ์ (Complete Solution)

ผู้เรียนสามารถนำโค้ดสำหรับควบคุม จัดการรูปโปรไฟล์และประมวลผลเซฟและอัปโหลดส่งไฟล์ 3 ระบบนี้ บันทึกลงในไฟล์ **`app/index.tsx`** เพื่อรันระบบทดสอบระดับเนทีฟ:

```tsx
import React, { useState, useEffect, useRef } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  Image, 
  TouchableOpacity, 
  Modal, 
  ActivityIndicator, 
  Alert, 
  SafeAreaView, 
  ScrollView 
} from 'react-native';
import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system';
import * as MediaLibrary from 'expo-media-library';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { decode } from 'base64-js';
import { supabase } from '../lib/supabase';

const LOCAL_STORAGE_KEY = '@local_avatar_path';
const CLOUD_STORAGE_KEY = '@cloud_avatar_url';

export default function App() {
  const [tempImageUri, setTempImageUri] = useState<string | null>(null);
  
  // สถานะพาธและผลลัพธ์จัดเก็บรูปภาพในระบบต่าง ๆ
  const [sandboxPath, setSandboxPath] = useState<string | null>(null);
  const [sharedGalleryStatus, setSharedGalleryStatus] = useState<string | null>(null);
  const [cloudUrl, setCloudUrl] = useState<string | null>(null);

  const [isCameraVisible, setIsCameraVisible] = useState(false);
  const [facing, setFacing] = useState<CameraType>('front');
  const [isProcessing, setIsProcessing] = useState(false);

  const [cameraPermission, requestCameraPermission] = useCameraPermissions();
  const [mediaLibraryPermission, requestMediaLibraryPermission] = MediaLibrary.usePermissions();
  const cameraRef = useRef<CameraView | null>(null);

  // 1. โหลดข้อมูลที่เคยเก็บจำไว้ตอนเปิดเข้าแอป
  useEffect(() => {
    loadSavedSettings();
  }, []);

  const loadSavedSettings = async () => {
    try {
      const savedLocal = await AsyncStorage.getItem(LOCAL_STORAGE_KEY);
      const savedCloud = await AsyncStorage.getItem(CLOUD_STORAGE_KEY);
      
      if (savedLocal) {
        const info = await FileSystem.getInfoAsync(savedLocal);
        if (info.exists) {
          setSandboxPath(savedLocal);
        }
      }
      if (savedCloud) {
        setCloudUrl(savedCloud);
      }
    } catch (e) {
      console.error(e);
    }
  };

  // 2. ดึงภาพถ่ายจากอัลบั้มเครื่อง
  const handlePickImage = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('คำเตือน', 'กรุณาเปิดสิทธิ์เข้าใช้คลังภาพในการตั้งค่าเครื่อง');
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 0.8
    });

    if (!result.canceled && result.assets && result.assets.length > 0) {
      setTempImageUri(result.assets[0].uri);
      // เคลียร์ผลลัพธ์การเซฟรอบเก่า
      setSandboxPath(null);
      setSharedGalleryStatus(null);
      setCloudUrl(null);
    }
  };

  // 3. เริ่มเปิดใช้งานเลนส์กล้องพรีวิวสด
  const handleStartCamera = async () => {
    if (!cameraPermission || !cameraPermission.granted) {
      const response = await requestCameraPermission();
      if (!response.granted) {
        Alert.alert('สิทธิ์ถูกปฏิเสธ', 'กรุณายอมรับสิทธิ์ใช้งานเลนส์ถ่ายรูป');
        return;
      }
    }
    setIsCameraVisible(true);
  };

  const handleCapturePhoto = async () => {
    if (cameraRef.current) {
      try {
        const photo = await cameraRef.current.takePictureAsync({
          quality: 0.8,
          skipProcessing: false
        });
        if (photo && photo.uri) {
          setTempImageUri(photo.uri);
          setIsCameraVisible(false);
          setSandboxPath(null);
          setSharedGalleryStatus(null);
          setCloudUrl(null);
        }
      } catch (e) {
        Alert.alert('ผิดพลาด', 'ไม่สามารถบันทึกรูปภาพจากตัวเลนส์ได้');
      }
    }
  };

  // 4. บูรณาการระบบบันทึกรูปโปรไฟล์ 3 ระดับพร้อมกัน (Multi-Destination Process)
  const handleSaveAndSyncAll = async () => {
    if (!tempImageUri) {
      Alert.alert('แจ้งเตือน', 'กรุณาถ่ายรูปหรือเลือกภาพจากแกลเลอรีก่อนกดบันทึก');
      return;
    }

    try {
      setIsProcessing(true);

      // --- ระบบที่ 1: บันทึกเฉพาะตัวใน Private Sandbox (Document Directory) ---
      const filename = `avatar_${Date.now()}.jpg`;
      const destinationSandboxUri = `${FileSystem.documentDirectory}${filename}`;
      await FileSystem.copyAsync({
        from: tempImageUri,
        to: destinationSandboxUri
      });
      setSandboxPath(destinationSandboxUri);
      await AsyncStorage.setItem(LOCAL_STORAGE_KEY, destinationSandboxUri);

      // --- ระบบที่ 2: บันทึกลง Shared Media Gallery (แชร์ข้ามแอปในเครื่อง) ---
      let sharedAssetId = 'ปฏิเสธสิทธิ์เข้าใช้คลังสื่อ';
      if (!mediaLibraryPermission || !mediaLibraryPermission.granted) {
        const mediaPerm = await requestMediaLibraryPermission();
        if (mediaPerm.granted) {
          const asset = await MediaLibrary.createAssetAsync(tempImageUri);
          sharedAssetId = `สำเร็จ (Asset ID: ${asset.id})`;
        }
      } else {
        const asset = await MediaLibrary.createAssetAsync(tempImageUri);
        sharedAssetId = `สำเร็จ (Asset ID: ${asset.id})`;
      }
      setSharedGalleryStatus(sharedAssetId);

      // --- ระบบที่ 3: อัปโหลดขึ้น Cloud Storage ของ Supabase (ซิงก์เน็ตเวิร์ก) ---
      // อ่านข้อมูลไฟล์เป็น Base64
      const base64Data = await FileSystem.readAsStringAsync(tempImageUri, {
        encoding: FileSystem.EncodingType.Base64
      });
      // แปลง Base64 เป็น ArrayBuffer
      const arrayBuffer = decode(base64Data);
      
      const cloudFilePath = `profile_pics/${filename}`;
      const { data, error } = await supabase.storage
        .from('avatars')
        .upload(cloudFilePath, arrayBuffer, {
          contentType: 'image/jpeg',
          upsert: true
        });

      if (error) {
        throw error;
      }

      // ดึงลิงก์รูปภาพสาธารณะจาก Supabase
      const { data: publicUrlData } = supabase.storage
        .from('avatars')
        .getPublicUrl(cloudFilePath);

      const publicLink = publicUrlData.publicUrl;
      setCloudUrl(publicLink);
      await AsyncStorage.setItem(CLOUD_STORAGE_KEY, publicLink);

      Alert.alert('บันทึก 3 ระบบเสร็จสิ้น!', 'ภาพถูกจัดเก็บลงดิสก์ส่วนตัว แกลเลอรีเครื่อง และอัปโหลดขึ้นคลาวด์เรียบร้อย');
    } catch (err: any) {
      Alert.alert('เกิดข้อผิดพลาดในการรันระบบบันทึก', err.message || err);
      console.error(err);
    } finally {
      setIsProcessing(false);
    }
  };

  // 5. ล้างประวัติลบรูปภาพทั้งหมดออก
  const handleClearEverything = async () => {
    Alert.alert(
      'ยืนยันการเคลียร์ข้อมูล',
      'ล้างประวัติที่อยู่และลบไฟล์ภาพในแซนด์บ็อกซ์ดิสก์ทั้งหมดหรือไม่?',
      [
        { text: 'ยกเลิก', style: 'cancel' },
        {
          text: 'ล้างข้อมูล',
          style: 'destructive',
          onPress: async () => {
            try {
              // ลบรูปภาพใน Sandbox เครื่อง
              if (sandboxPath) {
                await FileSystem.deleteAsync(sandboxPath, { idempotent: true });
              }
              await AsyncStorage.removeItem(LOCAL_STORAGE_KEY);
              await AsyncStorage.removeItem(CLOUD_STORAGE_KEY);

              setTempImageUri(null);
              setSandboxPath(null);
              setSharedGalleryStatus(null);
              setCloudUrl(null);
              Alert.alert('ล้างค่าเรียบร้อยแล้ว');
            } catch (e) {
              console.error(e);
            }
          }
        }
      ]
    );
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        
        {/* หัวเรื่องแอป */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>📸 Profile Avatar Pro</Text>
          <Text style={styles.headerSubtitle}>ทบทวนการจัดการไฟล์ภาพถ่ายเนทีฟและคลาวด์ 3 ระบบ</Text>
        </View>

        {/* แผงเปรียบเทียบรูปภาพพรีวิว */}
        <View style={styles.avatarCard}>
          <Text style={styles.cardLabel}>อวาตาร์โปรไฟล์ปัจจุบัน</Text>
          <View style={styles.avatarWrapper}>
            {/* ดึงภาพแสดงตามลำดับความคงทน: 1. ลิงก์ตรงคลาวด์ 2. Sandbox 3. ภาพชั่วคราวดึงสด 4. ภาพว่างเปล่า */}
            {cloudUrl ? (
              <Image source={{ uri: cloudUrl }} style={styles.avatarImage} />
            ) : sandboxPath ? (
              <Image source={{ uri: sandboxPath }} style={styles.avatarImage} />
            ) : tempImageUri ? (
              <Image source={{ uri: tempImageUri }} style={styles.avatarImage} />
            ) : (
              <View style={styles.avatarPlaceholder}>
                <Text style={styles.placeholderText}>No Pic</Text>
              </View>
            )}
          </View>
          <Text style={styles.imageSourceIndicator}>
            {cloudUrl ? '☁️ แสดงจาก Cloud Storage' : sandboxPath ? '💾 แสดงจาก Local Sandbox' : tempImageUri ? '⏳ ภาพรอการบันทึก' : '⚙️ พร้อมรับข้อมูลภาพ'}
          </Text>
        </View>

        {/* แผงคำสั่งทริกเกอร์เลือกภาพ */}
        <View style={styles.buttonGroupCard}>
          <Text style={styles.cardHeaderTitle}>1. นำเข้าสื่อถ่ายภาพโปรไฟล์</Text>
          <View style={styles.rowButtons}>
            <TouchableOpacity style={styles.primaryButton} onPress={handleStartCamera}>
              <Text style={styles.buttonText}>📷 เปิดกล้องถ่ายภาพ</Text>
            </TouchableOpacity>
            <TouchableOpacity style={[styles.primaryButton, styles.darkBlueButton]} onPress={handlePickImage}>
              <Text style={styles.buttonText}>🖼️ ดึงจากอัลบั้มเครื่อง</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* แผงประมวลผลบันทึก 3 รูปแบบ */}
        <View style={styles.actionCard}>
          <Text style={styles.cardHeaderTitle}>2. ประมวลผลและทดสอบจัดเก็บไฟล์ 3 ทิศทาง</Text>
          
          {isProcessing ? (
            <View style={styles.spinnerBlock}>
              <ActivityIndicator size="small" color="#38bdf8" />
              <Text style={styles.processingText}>กำลังย้าย Sandbox / คัดลงอัลบั้ม / อัปโหลดส่งคลาวด์...</Text>
            </View>
          ) : (
            <TouchableOpacity 
              style={[styles.actionTriggerButton, !tempImageUri && styles.disabledButton]} 
              onPress={handleSaveAndSyncAll}
              disabled={!tempImageUri}
            >
              <Text style={styles.actionTriggerText}>💾 กดรันบันทึก 3 ระบบพร้อมกัน</Text>
            </TouchableOpacity>
          )}

          {/* รายงานสถานะ Log การบันทึก */}
          <View style={styles.logBox}>
            <Text style={styles.logHeader}>📌 บันทึกผลสำเร็จ (Storage Logs):</Text>
            <View style={styles.logLine}>
              <Text style={styles.logTitle}>1. Local Sandbox (Private):</Text>
              <Text style={styles.logValue} numberOfLines={2}>
                {sandboxPath ? sandboxPath : 'ยังไม่ได้จัดเก็บลงดิสก์เอกสารแอป'}
              </Text>
            </View>
            <View style={styles.logLine}>
              <Text style={styles.logTitle}>2. Shared Library (Public):</Text>
              <Text style={styles.logValue}>
                {sharedGalleryStatus ? sharedGalleryStatus : 'ยังไม่ได้ส่งเขียนแกลเลอรีกล้องหลัก'}
              </Text>
            </View>
            <View style={styles.logLine}>
              <Text style={styles.logTitle}>3. Cloud Storage (Supabase):</Text>
              <Text style={styles.logValueCloud} numberOfLines={2}>
                {cloudUrl ? cloudUrl : 'ยังไม่ได้ส่งอัปโหลดขึ้นเครือข่าย'}
              </Text>
            </View>
          </View>

          {/* ปุ่มลบประวัติ */}
          {(sandboxPath || cloudUrl || tempImageUri) && (
            <TouchableOpacity style={styles.clearButton} onPress={handleClearEverything}>
              <Text style={styles.clearButtonText}>🗑️ ล้างภาพและไฟล์ Sandbox ทั้งหมด</Text>
            </TouchableOpacity>
          )}
        </View>

      </ScrollView>

      {/* โมดูลเต็มจอสำหรับเปิดกล้องถ่ายภาพ */}
      <Modal visible={isCameraVisible} animationType="slide" transparent={false}>
        <View style={styles.cameraContainer}>
          <CameraView 
            ref={cameraRef} 
            style={styles.cameraViewport} 
            facing={facing}
          >
            {/* ส่วนควบคุมกล้องด้านบน */}
            <View style={styles.cameraHeader}>
              <TouchableOpacity 
                style={styles.cameraCircleBtn}
                onPress={() => setIsCameraVisible(false)}
              >
                <Text style={styles.cameraCloseIcon}>✕</Text>
              </TouchableOpacity>
              <TouchableOpacity 
                style={styles.cameraCircleBtn}
                onPress={() => setFacing(curr => curr === 'back' ? 'front' : 'back')}
              >
                <Text style={styles.cameraCloseIcon}>🔄</Text>
              </TouchableOpacity>
            </View>

            {/* ส่วนลั่นชัตเตอร์ด้านล่าง */}
            <View style={styles.cameraFooter}>
              <TouchableOpacity 
                style={styles.shutterRing}
                onPress={handleCapturePhoto}
              >
                <View style={styles.shutterDot} />
              </TouchableOpacity>
              <Text style={styles.cameraTip}>เลนส์พรีวิวสด: {facing === 'front' ? 'กล้องหน้า' : 'กล้องหลัง'}</Text>
            </View>
          </CameraView>
        </View>
      </Modal>
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
  },
  header: {
    alignItems: 'center',
    marginVertical: 10,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  headerSubtitle: {
    fontSize: 12,
    color: '#64748b',
    textAlign: 'center',
    marginTop: 6,
    lineHeight: 18,
  },
  avatarCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#334155',
    marginVertical: 15,
  },
  cardLabel: {
    color: '#94a3b8',
    fontSize: 13,
    fontWeight: '600',
    marginBottom: 12,
  },
  avatarWrapper: {
    width: 150,
    height: 150,
    borderRadius: 75,
    borderWidth: 4,
    borderColor: '#38bdf8',
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
    backgroundColor: '#0f172a',
  },
  avatarImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  avatarPlaceholder: {
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
  },
  placeholderText: {
    color: '#475569',
    fontWeight: 'bold',
    fontSize: 16,
  },
  imageSourceIndicator: {
    color: '#10b981',
    fontSize: 12,
    fontWeight: '600',
    marginTop: 12,
  },
  buttonGroupCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 15,
  },
  cardHeaderTitle: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 12,
  },
  rowButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  primaryButton: {
    flex: 0.48,
    backgroundColor: '#0284c7',
    borderRadius: 10,
    height: 44,
    justifyContent: 'center',
    alignItems: 'center',
  },
  darkBlueButton: {
    backgroundColor: '#334155',
  },
  buttonText: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 13,
  },
  actionCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 20,
  },
  actionTriggerButton: {
    backgroundColor: '#10b981',
    borderRadius: 10,
    height: 48,
    justifyContent: 'center',
    alignItems: 'center',
  },
  disabledButton: {
    backgroundColor: '#475569',
    opacity: 0.5,
  },
  actionTriggerText: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 14,
  },
  spinnerBlock: {
    alignItems: 'center',
    marginVertical: 10,
  },
  processingText: {
    color: '#94a3b8',
    fontSize: 11,
    marginTop: 6,
  },
  logBox: {
    backgroundColor: '#0f172a',
    borderRadius: 10,
    padding: 12,
    borderWidth: 1,
    borderColor: '#334155',
    marginTop: 15,
  },
  logHeader: {
    color: '#f8fafc',
    fontSize: 12,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  logLine: {
    marginBottom: 10,
  },
  logTitle: {
    color: '#38bdf8',
    fontSize: 11,
    fontWeight: '600',
  },
  logValue: {
    color: '#e2e8f0',
    fontSize: 10,
    fontFamily: 'monospace',
    marginTop: 2,
  },
  logValueCloud: {
    color: '#a7f3d0',
    fontSize: 10,
    fontFamily: 'monospace',
    marginTop: 2,
  },
  clearButton: {
    borderWidth: 1,
    borderColor: '#ef4444',
    borderRadius: 10,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 15,
  },
  clearButtonText: {
    color: '#ef4444',
    fontSize: 12,
    fontWeight: 'bold',
  },
  // ส่วนประกอบกล้อง Modal
  cameraContainer: {
    flex: 1,
    backgroundColor: '#000000',
  },
  cameraViewport: {
    flex: 1,
    justifyContent: 'space-between',
  },
  cameraHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingTop: 50,
    paddingHorizontal: 20,
  },
  cameraCircleBtn: {
    width: 42,
    height: 42,
    borderRadius: 21,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  cameraCloseIcon: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  cameraFooter: {
    alignItems: 'center',
    paddingBottom: 40,
    backgroundColor: 'rgba(0,0,0,0.3)',
    paddingTop: 15,
  },
  shutterRing: {
    width: 74,
    height: 74,
    borderRadius: 37,
    borderWidth: 4,
    borderColor: '#ffffff',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  shutterDot: {
    width: 58,
    height: 58,
    borderRadius: 29,
    backgroundColor: '#ffffff',
  },
  cameraTip: {
    color: '#cbd5e1',
    fontSize: 11,
    fontWeight: '500',
  },
});
```

---

← [ย้อนกลับแบบทดสอบ: 03-quiz.md](./03-quiz.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ศึกษาบทเรียนถัดไป: บทที่ 12](../chapter-12-animations-reanimated/) →
