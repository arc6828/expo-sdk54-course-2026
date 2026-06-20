# บทที่ 9: พิกัดตำแหน่ง แผนที่ และเซนเซอร์อุปกรณ์ (Content)

การพัฒนาแอปพลิเคชันให้สามารถโต้ตอบกับโลกกายภาพภายนอก จำเป็นต้องอาศัยกลไกการเชื่อมโยงระบบพิกัดดาวเทียม (GPS) การจัดแสดงกราฟิกแผนที่เชิงภูมิศาสตร์ และการดักรับสัญญาณเซนเซอร์ของมือถือ ในบทเรียนนี้เราจะศึกษาการจัดการระบบขออนุญาตสิทธิ์ตำแหน่งทางภูมิศาสตร์ (Location Permissions) การเข้าถึงพิกัดด้วย `expo-location`, การเรนเดอร์แผนที่ด้วย `react-native-maps` และการใช้งานเซนเซอร์วัดแรงเร่ง `expo-sensors` (Accelerometer) ในระดับมาตรฐานสากล

---

## 9.1 ระบบสิทธิ์การเข้าถึงอุปกรณ์ (Runtime Permissions)

ในการเข้าถึงทรัพยากรที่มีความปลอดภัยและข้อมูลส่วนบุคคลของผู้ใช้งาน (เช่น พิกัดแผนที่ตำแหน่ง GPS) ระบบปฏิบัติการทั้ง iOS และ Android บังคับใช้ระบบ **สิทธิ์การเข้าถึงเวลาทำงาน (Runtime Permissions)** ซึ่งหมายความว่าแอปพลิเคชันไม่สามารถดึงข้อมูลได้ทันทีเมื่อเปิดใช้งาน แต่ต้องแสดงหน้าต่างขออนุมัติสิทธิ์ (Permission Request Pop-up) จากผู้ใช้เสียก่อน

### ประเภทของสิทธิ์เข้าถึงพิกัดตำแหน่ง (Location Permission Types):
1. **Foreground Location (ตำแหน่งเบื้องหน้า):** อนุญาตให้เข้าถึงข้อมูล GPS เฉพาะในขณะที่ผู้ใช้กำลังเปิดเปิดหน้าจอแอปพลิเคชันทำงานอยู่เท่านั้น (เป็นสิทธิ์หลักที่เรามักร้องขอ)
2. **Background Location (ตำแหน่งเบื้องหลัง):** อนุญาตให้แอปพลิเคชันคอยติดตามข้อมูล GPS ตลอดเวลาแม้แอปพลิเคชันจะถูกพับปิดหน้าต่างไปแล้ว (ต้องขอสิทธิ์ Foreground สำเร็จก่อนและผ่านเกณฑ์พิจารณาพิเศษจากสโตร์)

สำหรับระบบ Expo SDK 54 การขอสิทธิ์และตรวจสอบสถานะจะถูกควบคุมอย่างเป็นระบบผ่านคำสั่งสัญญา Asynchronous (Promise-based) ซึ่งส่งคืนค่าสถานะเป็นออบเจกต์ที่มีพร็อพส์ `status` บ่งชี้ผลลัพธ์:
* `'granted'`: ได้รับอนุมัติสิทธิ์สำเร็จ ดึงข้อมูลฮาร์ดแวร์ได้
* `'denied'`: ถูกปฏิเสธสิทธิ์ ไม่สามารถเข้าใช้ฮาร์ดแวร์ได้
* `'undetermined'`: ยังไม่เคยร้องขอสิทธิ์ (ผู้ใช้เปิดแอปครั้งแรก)

---

## 9.2 การเข้าถึงพิกัดตำแหน่งอุปกรณ์ด้วย expo-location

เพื่อดึงพิกัดตำแหน่งละติจูดและลองจิจูดจากอุปกรณ์เนทีฟ เราจะใช้งานไลบรารีอย่างเป็นทางการของ Expo คือ **`expo-location`**

### การติดตั้งไลบรารี:
```bash
npx expo install expo-location
```

### การตั้งค่าขออนุญาตใน `app.json` (สำหรับ Android & iOS):
```json
{
  "expo": {
    "plugins": [
      [
        "expo-location",
        {
          "locationAlwaysPermission": "อนุญาตให้แอปเข้าถึงตำแหน่งของคุณได้ตลอดเวลาเพื่อซิงก์แผนที่",
          "locationWhenInUsePermission": "อนุญาตให้เข้าถึงตำแหน่งในขณะเปิดใช้งานแอปเพื่อปักหมุดพิกัด"
        }
      ]
    ]
  }
}
```

### การเขียนโค้ดดึงตำแหน่ง GPS ล่าสุด:
```tsx
import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ActivityIndicator } from 'react-native';
import * as Location from 'expo-location';

export default function CurrentLocationApp() {
  const [location, setLocation] = useState<Location.LocationObject | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    const requestLocation = async () => {
      // 1. ส่งคำขออนุมัติสิทธิ์เข้าถึงพิกัดตำแหน่งเบื้องหน้า (Foreground)
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setErrorMsg('การเข้าถึงตำแหน่งของคุณถูกปฏิเสธ');
        return;
      }

      // 2. เมื่อได้รับอนุญาต ให้ทำการดึงพิกัดตำแหน่งละติจูดลองจิจูดปัจจุบัน
      let currentLocation = await Location.getCurrentPositionAsync({});
      setLocation(currentLocation);
    };

    requestLocation();
  }, []);

  return (
    <View style={styles.container}>
      {errorMsg ? (
        <Text style={styles.errorText}>{errorMsg}</Text>
      ) : location ? (
        <View>
          <Text style={styles.text}>Latitude: {location.coords.latitude}</Text>
          <Text style={styles.text}>Longitude: {location.coords.longitude}</Text>
          <Text style={styles.subText}>ระดับความแม่นยำ: {location.coords.accuracy} เมตร</Text>
        </View>
      ) : (
        <ActivityIndicator size="large" color="#38bdf8" />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#0f172a' },
  text: { fontSize: 18, color: '#ffffff', fontWeight: 'bold', marginBottom: 8 },
  subText: { fontSize: 13, color: '#94a3b8' },
  errorText: { color: '#ef4444', fontSize: 15 },
});
```

---

## 9.3 การแปลงพิกัดกลับเป็นที่อยู่ (Reverse Geocoding)

ข้อมูลละติจูดและลองจิจูด (เช่น `13.7367`, `100.5231`) เป็นข้อมูลที่ยากต่อการทำความเข้าใจของผู้ใช้ทั่วไป ไลบรารี `expo-location` จึงได้นำเสนอคุณสมบัติ **Reverse Geocoding** ซึ่งทำหน้าที่แปลงพิกัดทางภูมิศาสตร์ตัวเลขให้กลายเป็นออบเจกต์ที่อยู่จริงของที่ตั้งปลายทาง เช่น ชื่ออาคาร, เลขที่ถนน, อำเภอ, จังหวัด และรหัสไปรษณีย์

### ตัวอย่างคำสั่งแปลงพิกัด:
```tsx
const getAddressFromCoords = async (latitude: number, longitude: number) => {
  try {
    // ส่งละติจูดและลองจิจูดไปถอดข้อมูลภูมิภาค
    const addressResponse = await Location.reverseGeocodeAsync({
      latitude: latitude,
      longitude: longitude,
    });

    if (addressResponse.length > 0) {
      const address = addressResponse[0];
      // ตัวอย่างการดึงฟิลด์ข้อมูลที่อยู่
      console.log(`ที่อยู่: ถนน ${address.street}, อำเภอ ${address.district}, จังหวัด ${address.region}`);
    }
  } catch (error) {
    console.error('การแปลงที่อยู่ล้มเหลว:', error);
  }
};
```

---

## 9.4 การติดตั้งและจัดแสดงแผนที่ด้วย react-native-maps

ในการเรนเดอร์ภาพแผนที่เชิงโต้ตอบ (Interactive Maps) ที่ผู้ใช้งานสามารถย่อขยาย ดึงแผนที่ และมองเห็นความตื้นลึกของระดับสิ่งปลูกสร้างอย่างไหลลื่น เราจะติดตั้งใช้งานไลบรารีภายนอกยอดนิยมคือ **`react-native-maps`**

### การติดตั้ง:
```bash
npx expo install react-native-maps
```

คอมโพเนนต์หลักที่ใช้งาน:
* **`<MapView>`**: คอนเทนเนอร์หลักที่ใช้สำหรับจำลองเรนเดอร์แผนที่ภูมิศาสตร์ลงบนหน้าจออุปกรณ์
* **`<Marker>`**: คอมโพเนนต์ลูกย่อยที่ถูกเรนเดอร์ไว้ข้างใน MapView เพื่อแสดงสัญลักษณ์หมุดปัก (Map Pin) ณ จุดพิกัดใดพิกัดหนึ่งโดยเฉพาะ

---

## 9.5 การควบคุมแผนที่ (Region) และการใช้งาน Marker

การกำหนดมุมกล้องและพิกัดซูมบนคอมโพเนนต์ `<MapView>` จะถูกควบคุมผ่านพร็อพส์ **`region`** ซึ่งจะรับออบเจกต์ประกอบด้วยข้อมูล 4 ส่วนหลัก:

1. **`latitude`**: ละติจูดของพิกัดที่จะให้เป็นกึ่งกลางหน้าจอแผนที่
2. **`longitude`**: ลองจิจูดของพิกัดที่จะให้เป็นกึ่งกลางหน้าจอแผนที่
3. **`latitudeDelta`**: ระยะการซูมในแนวตั้ง (ค่ายิ่งน้อย ยิ่งซูมเข้าลึก มองเห็นรายละเอียดถนนและซอยชัดเจน)
4. **`longitudeDelta`**: ระยะการซูมในแนวนอน (ค่ายิ่งน้อย ยิ่งซูมเข้าลึก)

```tsx
import React from 'react';
import { StyleSheet, View } from 'react-native';
import MapView, { Marker } from 'react-native-maps';

export default function SimpleMap() {
  return (
    <View style={styles.container}>
      <MapView
        style={styles.map}
        // กำหนดตำแหน่งศูนย์กลางกล้องแผนที่เริ่มต้น (กรุงเทพมหานคร)
        initialRegion={{
          latitude: 13.7563,
          longitude: 100.5018,
          latitudeDelta: 0.05,
          longitudeDelta: 0.05,
        }}
      >
        {/* ปักหมุดตำแหน่ง ณ เสาชิงช้า */}
        <Marker
          coordinate={{ latitude: 13.7519, longitude: 100.5012 }}
          title="เสาชิงช้า"
          description="จุดเช็คอินใจกลางกรุงเทพมหานคร"
        />
      </MapView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  map: { width: '100%', height: '100%' },
});
```

---

## 9.6 การใช้งานเซนเซอร์ตรวจความเร่งด้วย expo-sensors (Accelerometer)

อุปกรณ์สมาร์ทโฟนสมัยใหม่ทุกเครื่องจะมีชิปเซนเซอร์ภายในเครื่องสำหรับวัดมุม การหมุน และความเร่ง ไลบรารี **`expo-sensors`** ช่วยให้ผู้พัฒนาสามารถอ่านค่าพฤติกรรมกายภาพของมือถือได้ง่าย

### การดาวน์โหลดแพ็คเกจ:
```bash
npx expo install expo-sensors
```

### การใช้งาน Accelerometer (เซนเซอร์วัดแรงเร่ง):
เซนเซอร์นี้จะคอยส่งชุดตัวเลขตามแกนพิกัดสามมิติ (x, y, z) อิงตามแรงโน้มถ่วงและการเคลื่อนที่จริงของตัวเครื่อง:
* **แกน x:** เอียงเครื่องไปซ้าย/ขวา
* **แกน y:** เอียงเครื่องไปหน้า/หลัง
* **แกน z:** แรงดึงแนวตั้งของการถือเครื่อง

```tsx
import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { Accelerometer } from 'expo-sensors';

export default function MotionSensorApp() {
  const [data, setData] = useState({ x: 0, y: 0, z: 0 });
  const [subscription, setSubscription] = useState<any>(null);

  // 1. สั่งเปิดรับฟังการเปลี่ยนแปลงข้อมูลจากชิปเซนเซอร์
  const subscribe = () => {
    setSubscription(
      Accelerometer.addListener((accelerometerData) => {
        setData(accelerometerData);
      })
    );
    // ตั้งรอบเวลาตรวจรับข้อมูลทุก ๆ 200 มิลลิวินาที
    Accelerometer.setUpdateInterval(200);
  };

  // 2. ยกเลิกการดักฟลักซ์ข้อมูลเพื่อเซฟแบตเตอรี่เครื่อง
  const unsubscribe = () => {
    subscription && subscription.remove();
    setSubscription(null);
  };

  useEffect(() => {
    subscribe();
    // คืนค่าฟังก์ชัน Unsubscribe สำหรับ Cleanup ตอนปิดหน้าจอป้องกัน RAM รั่ว
    return () => unsubscribe();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>ค่าความเร่ง Accelerometer</Text>
      <Text style={styles.coord}>X: {data.x.toFixed(3)}</Text>
      <Text style={styles.coord}>Y: {data.y.toFixed(3)}</Text>
      <Text style={styles.coord}>Z: {data.z.toFixed(3)}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#0f172a' },
  title: { fontSize: 18, color: '#38bdf8', fontWeight: 'bold', marginBottom: 12 },
  coord: { fontSize: 24, color: '#ffffff', fontFamily: 'monospace', marginVertical: 4 },
});
```

---

## 9.7 แนวทางการเขียนดักจับเหตุการณ์ปฏิเสธสิทธิ์และคืนค่าทรัพยากร (Permission Denied & Memory Cleanups)

กฎเหล็กสำคัญสองประการในการป้องกันไม่ให้โมบายแอปพลิเคชันเกิดอาการค้างหรือกินหน่วยความจำมหาศาลจนแอปเด้งดับ มีดังนี้:

### 1. การจัดการกรณีสิทธิ์การเข้าถึงถูกปฏิเสธ (Permission Rejection Fallback)
หากผู้ใช้งานไม่ยินยอมเปิด GPS ให้แอปพลิเคชัน ผู้พัฒนาไม่ควรปล่อยให้แอปพลิเคชันเรนเดอร์แผนที่ว่างเปล่าหรือค้างหน้าจอขาว แต่ต้องสลับ UI มาแสดงกล่องข้อความอธิบายความจำเป็นของการใช้พิกัด พร้อมดีไซน์ปุ่มกด "ตั้งค่าอุปกรณ์ (Open Settings)" เพื่อนำทางด่วนไปหน้าตั้งค่าระบบปฏิบัติการของเครื่อง:
```tsx
import * as Linking from 'expo-linking';
import { Button, View, Text } from 'react-native';

const handleOpenSettings = () => {
  // สั่งสั่งระบบทางตรงไปที่แอปพลิเคชันตั้งค่าสิทธิ์บนโทรศัพท์
  Linking.openSettings();
};
```

### 2. การล้างและปิดสตรีมเซนเซอร์ (Memory Cleanups)
เซนเซอร์ต่าง ๆ (เช่น Accelerometer, Gyroscope) ทำการสตรีมฟีดค่าพารามิเตอร์ขึ้นมาอัปเดตตลอดเวลา หากเปิดทริกเกอร์ฟังข้อมูลไว้แต่มีการเปลี่ยนไปหน้าอื่น สตรีมนี้จะยังทำงานค้างอยู่เบื้องหลัง ดึงแรมและกินแบตเตอรี่จนเครื่องร้อนจัด ผู้พัฒนาจำเป็นต้องคืนค่าและระงับการทำงาน (Unsubscribe) ใน Cleanup Function ของ React `useEffect` เสมอ

## 9.8 สรุปท้ายบทเรียน

**ระบบสิทธิ์การเข้าถึงอุปกรณ์ (Runtime Permissions):** การรักษาความปลอดภัยด้านความเป็นส่วนตัวบังคับให้แอปพลิเคชันต้องขอสิทธิ์เข้าถึงพิกัด GPS ระหว่างรันแอปผ่านระบบ Runtime Permissions ซึ่งสามารถขอสิทธิ์แบบเบื้องหน้า (Foreground) หรือเบื้องหลัง (Background) โดยระบบ Expo SDK 54 จัดการสถานะสิทธิ์การเข้าถึงส่งคืนค่าเป็นสัญญา Asynchronous ที่ส่งผลลัพธ์หลักเป็น granted (ได้รับสิทธิ์), denied (ถูกปฏิเสธ) หรือ undetermined (ยังไม่ร้องขอ)

**การเข้าถึงพิกัดตำแหน่งอุปกรณ์ด้วย expo-location:** การค้นหาพิกัดละติจูดและลองจิจูดของโทรศัพท์ใช้ไลบรารี expo-location ซึ่งต้องลงทะเบียนขออนุญาตในไฟล์ตั้งค่าโครงการ app.json ก่อน และใช้คำสั่ง requestForegroundPermissionsAsync ร่วมกับ getCurrentPositionAsync ในการดักจับพิกัดละติจูดและลองจิจูดปัจจุบัน รวมถึงระดับค่าความแม่นยำของจุดปักพิกัดสัญญาณดาวเทียมเพื่อนำไปใช้แสดงผลต่อ

**การแปลงพิกัดกลับเป็นที่อยู่ (Reverse Geocoding):** เนื่องจากพิกัดตัวเลขทางภูมิศาสตร์เข้าใจยากสำหรับผู้ใช้งานทั่วไป expo-location ได้จัดเตรียมความสามารถ Reverse Geocoding ผ่านฟังก์ชัน reverseGeocodeAsync ในการเปลี่ยนค่าละติจูดและลองจิจูดเป็นที่อยู่จริงของอุปกรณ์ เช่น ชื่อถนน ตำบล อำเภอ จังหวัด และรหัสไปรษณีย์ เพื่อแปลผลพิกัดเป็นข้อมูลที่แสดงผลแบบสื่อสารเข้าใจได้ง่ายบนอินเทอร์เฟซ

**การติดตั้งและจัดแสดงแผนที่ด้วย react-native-maps:** การแสดงแผนที่เชิงภูมิศาสตร์แบบโต้ตอบได้เต็มรูปแบบจะใช้ไลบรารี react-native-maps โดยประกอบไปด้วยคอมโพเนนต์หลัก ได้แก่ MapView ในการทำหน้าที่วาดหน้าต่างแผนที่ลงบนเฟรมหน้าต่างแอปพลิเคชัน และคอมโพเนนต์ย่อยอย่าง Marker เพื่อระบุพิกัดปักหมุดสีแดง (Map Pin) ณ ละติจูดและลองจิจูดเป้าหมายพร้อมเขียนบรรยายรายละเอียดกำกับ

**การควบคุมแผนที่ (Region) และการใช้งาน Marker:** การควบคุมการแสดงผลและปรับมุมกล้องแผนที่จะทำงานผ่านคุณสมบัติ Region ใน MapView ประกอบด้วยค่าศูนย์กลางละติจูด-ลองจิจูด และค่าความกว้างของการซูมอย่าง latitudeDelta และ longitudeDelta ซึ่งค่ายิ่งน้อยจะยิ่งซูมเข้าสู่ผิวถนนได้อย่างชัดเจน และเราสามารถปักหมุด Marker ระบุข้อมูล coordinate รวมถึงพิมพ์คำอธิบายหัวข้อจุดเช็คอินต่าง ๆ ได้อย่างอิสระ

**การใช้งานเซนเซอร์ตรวจความเร่งด้วย expo-sensors:** การเขียนรหัสรับรู้พฤติกรรมการเคลื่อนไหวจริงของโทรศัพท์ใช้ไลบรารี expo-sensors ในการอ่านค่าจากชิป Accelerometer เพื่อฟีดพารามิเตอร์ความเร่งสามแกน (x, y, z) สะท้อนแรงโน้มถ่วงเมื่อพลิก เอียง หรือขยับโทรศัพท์ โดยต้องระบุช่วงความถี่ในการตรวจสอบผ่าน setUpdateInterval เพื่อสตรีมข้อมูลความเคลื่อนไหวมาแสดงผลแบบเรียลไทม์

**แนวทางการเขียนดักจับเหตุการณ์ปฏิเสธสิทธิ์และคืนค่าทรัพยากร:** โครงสร้างความปลอดภัยของแอปพลิเคชันที่ดีต้องเตรียมระบบรองรับกรณีผู้ใช้ปฏิเสธสิทธิ์โดยใช้ Linking.openSettings() เพื่อพาลัดเข้าหน้าการตั้งค่าเครื่อง และที่สำคัญที่สุดคือการป้องกันปัญหาระบบเมมโมรี่รั่วไหล (Memory Leak) จากฟีดข้อมูลเซนเซอร์ โดยการสั่งยกเลิกติดตามเซนเซอร์ (Unsubscribe) ในส่วนของ Cleanup Function ของ React useEffect ก่อนเปิดหน้าจอแอปพลิเคชันถัดไป

---

← [ย้อนกลับแผนการสอน: 01-lesson-plan.md](./01-lesson-plan.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ทำแบบทดสอบถัดไป: 03-quiz.md](./03-quiz.md) →
