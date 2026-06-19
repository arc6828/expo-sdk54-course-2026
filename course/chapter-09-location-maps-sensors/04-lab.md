# ปฏิบัติการ บทที่ 9: การพัฒนาแอปพลิเคชันปักหมุดแผนที่และสั่นสะเทือนจดจำตำแหน่ง (Lab)

ปฏิบัติการนี้จะฝึกทักษะการรวบรวมฟังก์ชันระดับฮาร์ดแวร์ของโทรศัพท์มือถือเข้าหากัน โดยผู้เรียนจะได้ออกแบบแอปพลิเคชัน **"ระบบแผนที่นำทางและสั่นสะเทือนจดจำพิกัด (Interactive Location Map Tracker)"** ซึ่งจะร้องขอสิทธิ์ดาวเทียม ดึงตำแหน่ง GPS ของเครื่องมาประมวลผล ถอดรหัสแปลงกลับเป็นชื่อสถานที่จริง แสดงผลแผนที่เชิงโต้ตอบแบบซูมลึก ปักหมุดตำแหน่งปัจจุบัน และผูกเซนเซอร์ความเร่งตรวจจับความเคลื่อนไหว (Accelerometer) เมื่อผู้ใช้ทำมุมเอียงหรือเขย่าเครื่อง เพื่อบังคับมุมกล้องแผนที่ให้ดีดสไลด์กลับมาโฟกัสพิกัดผู้ใช้ปัจจุบันแบบไดนามิก

---

## 1. วัตถุประสงค์การเรียนรู้
1. สามารถเขียนรหัสควบคุมระบบสิทธิ์การเข้าถึงพิกัดตำแหน่ง (Runtime Location Permission) และเขียนระบบป้องกันเมื่อผู้ใช้ปฏิเสธสิทธิ์
2. สามารถใช้คุณสมบัติ Geocoding แปลงละติจูดลองจิจูดให้ออกมาเป็นข้อมูลตำบลและอำเภอจริงเพื่อจัดแสดงผลบนหน้าจอ
3. สามารถกำหนดคอนเทนเนอร์แผนที่ `<MapView>` ร่วมกับสัญลักษณ์ `<Marker>` โดยตั้งค่าระยะซูม Delta ที่เหมาะสมคมชัด
4. สามารถเชื่อมโยงการทำงานร่วมกับเซนเซอร์ความเร่ง `Accelerometer` เพื่อสั่งขยับพิกัดกล้องแผนที่ตามการสั่นเครื่องได้สำเร็จ
5. สามารถเขียนโค้ดระงับสตรีมเซนเซอร์ (Cleanup listeners) ได้ถูกต้องเพื่อประสิทธิภาพของทรัพยากรระบบ

---

## 2. โจทย์และข้อกำหนดปฏิบัติการ (Requirements)

ผู้เรียนต้องพัฒนาแอปพลิเคชันระบบแผนที่และพิกัดตำแหน่งส่วนบุคคลตามเงื่อนไขต่อไปนี้:

1. **สิทธิ์และการเข้าถึงพิกัดตำแหน่ง (Permissions & GPS Tracking):**
   * ทันทีที่แอปเปิดทำงาน ต้องทำการขอสิทธิ์ Foreground Location
   * หากสิทธิ์ถูกปฏิเสธ (Denied) ให้แสดงหน้าต่างเตือนภัยปุ่มสีแดงระบุข้อความ "กรุณาเปิดรับสิทธิ์ตำแหน่งเพื่อแสดงแผนที่" พร้อมปุ่มกดดึงคำสั่ง `Linking.openSettings()` เพื่ออำนวยความสะดวกให้ผู้ใช้เข้าหน้าระบบควบคุมสิทธิ์เครื่องได้ทันที
   * หากสิทธิ์ได้รับอนุมัติ ให้ทำพิกัดละติจูดลองจิจูดปัจจุบัน แปลงที่อยู่อักษรย้อนกลับด้วย `reverseGeocodeAsync` และนำข้อมูลชื่อถนน/จังหวัด แสดงเป็นแผงป้ายชื่อด้านบนสุด
2. **การจัดแสดงภาพแผนที่แบบลึกซูม (Map Rendering):**
   * แสดงแผงแผนที่แบบเต็มจอในบริเวณด้านล่าง โดยมีศูนย์กลางอยู่ที่ตำแหน่งละติจูดและลองจิจูดของผู้ใช้ปัจจุบัน
   * ตั้งค่าระยะซูมเข้าลึก `latitudeDelta: 0.01` และ `longitudeDelta: 0.01` เพื่อให้เห็นรายละเอียดหมู่บ้านและตรอกซอย
   * เรนเดอร์คอมโพเนนต์ `<Marker>` ปักหมุดเข็มสีสว่างไว้ที่จุดพิกัดปัจจุบัน พร้อมเขียนป้ายทูลทิป (Tooltip) ระบุข้อความ "ตำแหน่งของคุณในขณะนี้"
3. **ระบบสั่นสะเทือนจัดศูนย์กลาง (Motion Sensor Integration):**
   * สมัครสตรีมสัญญาณข้อมูลเซนเซอร์จากเครื่องมือ `Accelerometer` โดยอัปเดตแกนความเร่ง x, y, z
   * กำหนดให้หากผู้ใช้งานเขย่าตัวเครื่องจำลอง หรือเอียงเครื่องทำมุมความเร่ง (เช่น ค่าสัมบูรณ์แกน `x` หรือ `y` มีค่าความแรงเกินกว่า 1.8) ให้แผนที่สไลด์ (Animate) นำศูนย์กลางกล้องแผนที่วิ่งกลับมาโฟกัสพิกัดเริ่มต้นปัจจุบันของผู้ใช้โดยอัตโนมัติ (เสมือนการสั่ง Center Map ด้วยการเขย่า)
4. **ความมั่นคงในการล้างทรัพยากร (Memory Safety Cleanup):**
   * ผู้เรียนต้องเขียนส่งมอบฟังก์ชัน Unsubscribe เพื่อยกเลิกลบผู้ฟังค่า Accelerometer ออกจาก RAM ของเครื่องเมื่อคอมโพเนนต์ถูกปิดตัวลง

---

## 3. ขั้นตอนการลงมือปฏิบัติ (Step-by-Step Tutorial)

### ขั้นตอนที่ 1: ติดตั้งไลบรารีตำแหน่ง แผนที่ และเซนเซอร์
รันคำสั่งติดตั้งคลังฮาร์ดแวร์ของ Expo และ React Native เพื่อใช้งานในโครงการ:
```bash
npx expo install expo-location react-native-maps expo-sensors
```

### ขั้นตอนที่ 2: ตั้งค่าสิทธิ์และขอบเขตใน `app.json`
เปิดไฟล์ `app.json` และเขียนเพิ่มค่าสิทธิ์ความปลอดภัยลงในคีย์ `plugins`:
```json
{
  "expo": {
    "plugins": [
      [
        "expo-location",
        {
          "locationWhenInUsePermission": "เราจำเป็นต้องเข้าถึงพิกัด GPS เพื่อแสดงจุดสีน้ำเงินบนแผนที่ของคุณ"
        }
      ]
    ]
  }
}
```

### ขั้นตอนที่ 3: ออกแบบระบบตรวจสอบสิทธิ์และดักจับการตั้งค่าเครื่อง
เขียนโค้ดตรวจสอบเงื่อนไขและส่งลิงก์ Settings ด้วยคำสั่ง Linking:
```tsx
import * as Linking from 'expo-linking';

// ปุ่มกดนำทางข้ามระบบ Sandbox
<TouchableOpacity 
  style={styles.settingsButton} 
  onPress={() => Linking.openSettings()}
>
  <Text style={styles.buttonText}>เปิดตั้งค่าสิทธิ์สิทธิ์บนระบบเครื่อง</Text>
</TouchableOpacity>
```

### ขั้นตอนที่ 4: เชื่อมโยง Accelerometer เข้าหา MapView อ้างอิงด้วย Ref
เพื่อสั่งสั่งกล้องของแผนที่เลื่อนไปมาอย่างนุ่มนวล เราจะสร้างตัวแปรอ้างอิง `mapRef` และสั่งการผ่านคำสั่ง `animateToRegion`:
```tsx
const mapRef = React.useRef<MapView | null>(null);

// หากแรงเหวี่ยงเซนเซอร์เขย่าเกินพิกัด ให้เลื่อนศูนย์กลางกลับมา
if (Math.abs(x) > 1.8 || Math.abs(y) > 1.8) {
  mapRef.current?.animateToRegion({
    latitude: currentCoords.latitude,
    longitude: currentCoords.longitude,
    latitudeDelta: 0.01,
    longitudeDelta: 0.01,
  }, 1000); // ดีดกล้องสไลด์นุ่มนวลในเวลา 1 วินาที
}
```

---

## 4. โค้ดเฉลยฉบับสมบูรณ์ (Complete Solution)

ผู้เรียนสามารถคัดลอกรหัสต้นฉบับสมบูรณ์ด้านล่างนี้ บันทึกทับในไฟล์หลักของโครงการ (เช่น `app/index.tsx`) เพื่อรันสตรีมนำพิกัดดาวเทียมขึ้นระบบแผนที่พร้อมระบบสั่นตรวจจับการเขย่า:

```tsx
import React, { useState, useEffect, useRef } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  ActivityIndicator, 
  TouchableOpacity, 
  Alert, 
  SafeAreaView 
} from 'react-native';
import * as Location from 'expo-location';
import MapView, { Marker } from 'react-native-maps';
import { Accelerometer } from 'expo-sensors';
import * as Linking from 'expo-linking';

// โมเดลเก็บข้อมูลพิกัด
interface Coords {
  latitude: number;
  longitude: number;
}

export default function InteractiveLocationTracker() {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [currentCoords, setCurrentCoords] = useState<Coords | null>(null);
  const [address, setAddress] = useState<string>('กำลังค้นหาที่อยู่ของคุณ...');
  const [isLoading, setIsLoading] = useState<boolean>(true);
  
  // ตัวแปรเก็บค่าพิกัดความเร่งเซนเซอร์
  const [accelerometerData, setAccelerometerData] = useState({ x: 0, y: 0, z: 0 });
  const accelerometerSubscription = useRef<any>(null);
  
  // ตัวอ้างอิงออบเจกต์ MapView เพื่อส่งคำสั่งจัดเฟรมกล้อง
  const mapRef = useRef<MapView | null>(null);

  useEffect(() => {
    setupLocationAndSensors();

    // คืนค่าฟังก์ชัน Cleanup เมื่อถอนหน้าจอป้องกัน RAM รั่ว
    return () => {
      stopAccelerometerListening();
    };
  }, []);

  // 1. ฟังก์ชันจัดระเบียบสิทธิ์และการดึงพิกัดเริ่มต้น
  const setupLocationAndSensors = async () => {
    try {
      setIsLoading(true);
      
      // ขออนุมัติเข้าถึง Location
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setHasPermission(false);
        setIsLoading(false);
        return;
      }
      
      setHasPermission(true);
      
      // อ่านค่าพิกัดปัจจุบัน
      const location = await Location.getCurrentPositionAsync({
        accuracy: Location.Accuracy.Balanced,
      });
      
      const coordsObj = {
        latitude: location.coords.latitude,
        longitude: location.coords.longitude
      };
      
      setCurrentCoords(coordsObj);
      
      // ดึงที่อยู่ถนนจริงจากพิกัด GPS (Reverse Geocode)
      const reverseResponse = await Location.reverseGeocodeAsync(coordsObj);
      if (reverseResponse.length > 0) {
        const addr = reverseResponse[0];
        const streetName = addr.street || addr.name || 'ไม่มีระบุถนน';
        const districtName = addr.district || 'ไม่มีระบุอำเภอ';
        const regionName = addr.region || 'ไม่มีระบุจังหวัด';
        setAddress(`📍 ${streetName}, อ.${districtName}, จ.${regionName}`);
      }

      // เริ่มต้นดักฟังข้อมูลเซนเซอร์เขย่า
      startAccelerometerListening(coordsObj);
      
    } catch (error) {
      console.error(error);
      Alert.alert('ข้อผิดพลาด', 'ไม่สามารถเชื่อมต่อระบบ GPS หรือระบุพิกัดในเครื่องได้');
    } finally {
      setIsLoading(false);
    }
  };

  // 2. ฟังก์ชันจดจำสัญญาณ Accelerometer
  const startAccelerometerListening = (coords: Coords) => {
    // กำหนดรอบการดึงข้อมูลเซนเซอร์ถี่ขึ้น (200 มิลลิวินาที)
    Accelerometer.setUpdateInterval(200);
    
    accelerometerSubscription.current = Accelerometer.addListener((data) => {
      setAccelerometerData(data);
      
      // ตรวจสอบเงื่อนไขการเขย่าเครื่อง (เช็คความแรงขยับแกน x หรือ y เกิน 1.8)
      if (Math.abs(data.x) > 1.8 || Math.abs(data.y) > 1.8) {
        // บังคับเลื่อนแผนที่วิ่งกลับมาที่จุดพิกัดปัจจุบันของผู้ใช้
        mapRef.current?.animateToRegion({
          latitude: coords.latitude,
          longitude: coords.longitude,
          latitudeDelta: 0.01,
          longitudeDelta: 0.01,
        }, 1000); // สไลด์กล้องแผนที่ใน 1 วินาที
      }
    });
  };

  const stopAccelerometerListening = () => {
    if (accelerometerSubscription.current) {
      accelerometerSubscription.current.remove();
      accelerometerSubscription.current = null;
    }
  };

  // 3. ฟังก์ชันปุ่มกดสปอตไลท์ด่วน (Manual Refocus)
  const handleManualCenter = () => {
    if (currentCoords) {
      mapRef.current?.animateToRegion({
        latitude: currentCoords.latitude,
        longitude: currentCoords.longitude,
        latitudeDelta: 0.01,
        longitudeDelta: 0.01,
      }, 800);
    }
  };

  // 4. แสดงกรณีสิทธิ์เข้าใช้งานถูกระงับ
  if (hasPermission === false) {
    return (
      <SafeAreaView style={styles.errorContainer}>
        <View style={styles.errorCard}>
          <Text style={styles.errorEmoji}>🚫</Text>
          <Text style={styles.errorTitle}>ระบบสิทธิ์ตำแหน่งถูกปิดกั้น</Text>
          <Text style={styles.errorDesc}>
            แอปพลิเคชันจำเป็นต้องเข้าใช้งานพิกัด GPS เพื่อทำจัดเรนเดอร์ภาพแผนที่แสดงจุดพิกัดส่วนบุคคล กรุณาเปิดอนุมัติสิทธิ์ในแอปการตั้งค่า
          </Text>
          <TouchableOpacity 
            style={styles.settingsButton}
            onPress={() => Linking.openSettings()}
          >
            <Text style={styles.settingsButtonText}>เปิดหน้าต่างตั้งค่าสิทธิ์แอป</Text>
          </TouchableOpacity>
          <TouchableOpacity 
            style={styles.retryButton}
            onPress={setupLocationAndSensors}
          >
            <Text style={styles.retryButtonText}>🔄 ลองขอสิทธิ์ใหม่อีกครั้ง</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        
        {/* แผงควบคุมแสดงรายละเอียดที่อยู่ด้านบนสุด */}
        <View style={styles.addressPanel}>
          <Text style={styles.addressTitle}>พิกัดปัจจุบันของคุณ</Text>
          <Text style={styles.addressText} numberOfLines={2}>
            {isLoading ? '⏳ กำลังค้นหาข้อมูลตำแหน่งพิกัดดาวเทียม...' : address}
          </Text>
          {currentCoords && (
            <Text style={styles.coordsSub}>
              Lat: {currentCoords.latitude.toFixed(5)}, Lng: {currentCoords.longitude.toFixed(5)}
            </Text>
          )}
        </View>

        {/* ส่วนแสดงแผนที่ระบุพิกัดภูมิศาสตร์ */}
        <View style={styles.mapContainer}>
          {isLoading || !currentCoords ? (
            <View style={styles.loadingWrapper}>
              <ActivityIndicator size="large" color="#38bdf8" />
              <Text style={styles.loadingText}>กำลังจับคู่แผนที่กับสัญญาณดาวเทียม...</Text>
            </View>
          ) : (
            <>
              <MapView
                ref={mapRef}
                style={styles.map}
                initialRegion={{
                  latitude: currentCoords.latitude,
                  longitude: currentCoords.longitude,
                  latitudeDelta: 0.01,
                  longitudeDelta: 0.01,
                }}
                showsUserLocation={true}
              >
                {/* ปักเข็มหมุดแสดงพิกัดผู้ใช้ */}
                <Marker
                  coordinate={{
                    latitude: currentCoords.latitude,
                    longitude: currentCoords.longitude
                  }}
                  title="ตำแหน่งของคุณ"
                  description="ปักหมุดตรงพิกัดตาม GPS"
                />
              </MapView>

              {/* ปุ่มควบคุมแบบลอยตัว (Floating action buttons over map) */}
              <TouchableOpacity 
                style={styles.floatingButton} 
                onPress={handleManualCenter}
              >
                <Text style={styles.floatingButtonText}>🎯 ซิงก์กล้องที่จุดคุณ</Text>
              </TouchableOpacity>

              {/* แถบรายงานค่าเซนเซอร์ความเร่งด้านขวาล่าง */}
              <View style={styles.sensorInfoBox}>
                <Text style={styles.sensorText}>เขย่าเครื่องเบาๆ เพื่อจัดศูนย์กลาง</Text>
                <Text style={styles.sensorTextVal}>
                  X: {accelerometerData.x.toFixed(2)}, Y: {accelerometerData.y.toFixed(2)}
                </Text>
              </View>
            </>
          )}
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#0f172a',
  },
  container: {
    flex: 1,
  },
  addressPanel: {
    backgroundColor: '#1e293b',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#334155',
  },
  addressTitle: {
    color: '#38bdf8',
    fontWeight: 'bold',
    fontSize: 12,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  addressText: {
    color: '#ffffff',
    fontSize: 15,
    fontWeight: 'bold',
    marginTop: 4,
  },
  coordsSub: {
    color: '#94a3b8',
    fontFamily: 'monospace',
    fontSize: 11,
    marginTop: 4,
  },
  mapContainer: {
    flex: 1,
    position: 'relative',
  },
  map: {
    width: '100%',
    height: '100%',
  },
  loadingWrapper: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#0f172a',
  },
  loadingText: {
    color: '#94a3b8',
    marginTop: 12,
    fontSize: 14,
  },
  floatingButton: {
    position: 'absolute',
    bottom: 20,
    left: 20,
    backgroundColor: '#38bdf8',
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 6,
  },
  floatingButtonText: {
    color: '#0f172a',
    fontWeight: 'bold',
    fontSize: 14,
  },
  sensorInfoBox: {
    position: 'absolute',
    bottom: 20,
    right: 20,
    backgroundColor: 'rgba(15, 23, 42, 0.85)',
    padding: 10,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#334155',
    alignItems: 'flex-end',
  },
  sensorText: {
    color: '#94a3b8',
    fontSize: 10,
  },
  sensorTextVal: {
    color: '#38bdf8',
    fontFamily: 'monospace',
    fontSize: 11,
    fontWeight: 'bold',
    marginTop: 2,
  },
  errorContainer: {
    flex: 1,
    backgroundColor: '#0f172a',
    justifyContent: 'center',
    padding: 24,
  },
  errorCard: {
    backgroundColor: '#1e293b',
    borderRadius: 24,
    padding: 24,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#334155',
  },
  errorEmoji: {
    fontSize: 48,
    marginBottom: 16,
  },
  errorTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 10,
  },
  errorDesc: {
    fontSize: 14,
    color: '#cbd5e1',
    textAlign: 'center',
    lineHeight: 22,
    marginBottom: 24,
  },
  settingsButton: {
    backgroundColor: '#ef4444',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 12,
    width: '100%',
    alignItems: 'center',
    marginBottom: 12,
  },
  settingsButtonText: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 14,
  },
  retryButton: {
    backgroundColor: 'transparent',
    paddingVertical: 12,
    width: '100%',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#334155',
    borderRadius: 12,
  },
  retryButtonText: {
    color: '#94a3b8',
    fontWeight: 'bold',
    fontSize: 14,
  },
});
```

---

## 5. การวิเคราะห์สรุปผลการประเมินปฏิบัติการ

เมื่อติดตั้งและทดลองเปิดแอปพลิเคชัน ให้ผู้เรียนประเมินความสมบูรณ์ดังนี้:
1. หากทำการยกเลิกไม่ยอมเปิด GPS แถบแสดงผลของแอปพลิเคชันต้องดีดสลับมาหน้ากล่องข้อความเตือนภัยสีแดง และกดปุ่ม Settings ได้ทันที
2. เมื่อเปิดบริการ GPS รายการแผนที่ต้องดึงศูนย์กลางกล้องมาโฟกัสพิกัดผู้ใช้และปักหมุดได้อย่างแม่นยำ
3. เมื่อใช้นิ้วเลื่อนแผนที่หนีขอบเขตไปไกล และออกแรงเขย่าตัวเครื่อง (หรือปรับจำลอง Accelerometer ในอุปกรณ์ Emulator) แผนที่ต้องดีดตัวอนิเมตกล้องกลับมาที่จุดพิกัดปัจจุบันโดยอัตโนมัติ

---

← [ย้อนกลับแบบทดสอบ: 03-quiz.md](./03-quiz.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ศึกษาบทเรียนถัดไป: บทที่ 10](../chapter-10-camera-imagepicker/) →
