# ปฏิบัติการ บทที่ 13: การดีบั๊กแอปพลิเคชันและการจัดทำไฟล์ติดตั้ง APK ผ่านระบบ EAS Build (Lab)

ปฏิบัติการในบทเรียนสุดท้ายนี้จะมุ่งเน้นกระบวนการปลายน้ำในการจัดเตรียมความพร้อมของแอปพลิเคชันสู่ระดับโปรดักชัน โดยผู้เรียนจะได้ร่วมกันปรับแต่งไฟล์โครงสร้างคุณลักษณะระบบของแอปพลิเคชัน (`app.json`), กำหนดเส้นทางคอมไพล์คลาวด์เพื่อรับไฟล์ติดตั้งด่วน Android Package (`eas.json`), รันการตรวจสอบและเตรียมปรับปรุงความขัดแย้งของแพ็คเกจสำหรับเตรียมตัวอัปเกรด SDK, ออกแบบหน้าจอแดชบอร์ดวินิจฉัยสำหรับกดจำลองบั๊กหาจุดเกิดเหตุด้วยดีบั๊กเกอร์ (Diagnostics & Debugging Client) และรันชุดคำสั่งถอดรหัสบิลด์ตัวแอปขึ้นไปบนระบบคลาวด์ของ Expo EAS Build

---

## 1. วัตถุประสงค์การเรียนรู้
1. สามารถแก้ไขไฟล์ `app.json` เพื่อลงทะเบียนชื่อแพ็คเกจที่เป็นเอกลักษณ์ (Android Package Name) และเวอร์ชันอิงตามหลักเกณฑ์สากลได้ถูกต้อง
2. สามารถจัดสรรและกำหนดค่าโปรไฟล์สำหรับประกอบไฟล์ APK ลงใน `eas.json` ได้ถูกต้อง
3. สามารถเรียกใช้ชุดคำสั่ง `npx expo install --fix` และเคลียร์ Metro cache เพื่อรับมือกับการขยับอัปเกรดรุ่น Expo SDK ได้สำเร็จ
4. สามารถใช้งาน Chrome Developer Tools ในการระบุจุดเกิดเหตุของบั๊กประเภท JavaScript Crash ในคอมโพเนนต์ได้สำเร็จ
5. สามารถใช้งาน EAS CLI ในการรันประมวลผลเซฟและส่งโค้ดขึ้นบิลด์บนคลาวด์จนได้รับลิงก์ดาวน์โหลดหรือรหัส QR Code ไฟล์ติดตั้งจริง

---

## 2. โจทย์และข้อกำหนดปฏิบัติการ (Requirements)

ผู้เรียนต้องจัดสร้างโปรเจกต์ React Native Expo โดยมีโครงสร้างดังนี้:

```text
โครงสร้างไฟล์ปฏิบัติการ:
├── app.json                          => ลงทะเบียนชื่อแอป คลังภาพไอคอน และรหัส com.yourdomain.diaryapp
├── eas.json                          => ปรับแต่ง Preview Profile ให้สั่ง Build สรุปประเภทไฟล์เป็น APK
└── app/
    └── index.tsx                     => หน้าแอปวินิจฉัย (Diagnostics Dashboard) พร้อมปุ่มทดสอบสกัดบั๊ก
```

### การตั้งค่าการจำลองบั๊กและวิเคราะห์ (Diagnostics Engine):
1. **หน้าจอวินิจฉัย (Diagnostics UI):** แสดงรายงานสเตตัสคุณสมบัติของแอป เช่น เวอร์ชัน และระบบปฏิบัติการ
2. **ปุ่มดีบั๊กจำลองข้อผิดพลาด (Trigger Simulation Crash):** เมื่อผู้ใช้กดคลิก ปุ่มนี้จะต้องรันฟังก์ชันที่จงใจให้เกิด Runtime Crash (เช่น พยายามเข้าถึงคุณสมบัติของอ็อบเจกต์ที่ไม่มีอยู่จริงหรือเป็น `undefined`) เพื่อทดลองเปิด Chrome DevTools ตรวจหาสาเหตุการเกิด Stack Trace
3. **ปุ่มทดสอบความเสถียร (Run Normal API Mock):** ปุ่มสำหรับทดสอบการทำงานปกติเพื่อเปรียบเทียบ

---

## 3. ขั้นตอนการลงมือปฏิบัติ (Step-by-Step Tutorial)

### ขั้นตอนที่ 1: การลงทะเบียนติดตั้งคลังคำสั่ง EAS CLI
สั่งรันคำสั่งติดตั้งตัวเชื่อมต่อในระบบส่วนกลาง (Global Node) ของคอมพิวเตอร์ของคุณ:
```bash
npm install -g eas-cli
```
จากนั้นสั่งล็อกอินเข้าระบบบัญชีผู้พัฒนาของ Expo:
```bash
eas login
```

### ขั้นตอนที่ 2: ตั้งรหัสโดเมนกลับใน `app.json`
ไปที่ไฟล์ `app.json` และระบุรหัส package ของฝั่ง Android (และ bundleIdentifier สำหรับ iOS) ให้ถูกต้อง:
```json
"android": {
  "package": "com.student.diaryapp",
  "versionCode": 1
}
```

### ขั้นตอนที่ 3: ตั้งค่าโปรไฟล์บิลด์ APK ใน `eas.json`
รันคำสั่ง `eas build:configure` เพื่อให้ระบบสร้างไฟล์ `eas.json` ขึ้นมา จากนั้นให้เข้าแก้ไขในส่วนโปรไฟล์ `"preview"` ให้ระบุการบิลด์เป็นประเภทไฟล์ APK (เนื่องจากสเปกเริ่มต้นของ EAS จะบิลด์เป็นไฟล์ AAB สำหรับขึ้นสโตร์อย่างเดียว ซึ่งไม่สามารถติดตั้งลงมือถือตรง ๆ ได้):
```json
"preview": {
  "distribution": "internal",
  "android": {
    "buildType": "apk"
  }
}
```

### ขั้นตอนที่ 4: ฝึกทักษะการตรวจสอบความเข้ากันได้และการเคลียร์แคชกรณีอัปเกรด SDK
ก่อนทำการส่งมอบโค้ดขึ้นระบบคลาวด์ หากมีการขยับรุ่นของ SDK หลัก เราต้องดึงไลบรารีอื่น ๆ ที่มีรุ่นขัดแย้งกันใน `package.json` ให้มาเชื่อมโยงกันอย่างมั่นคงด้วยการใช้คำสั่ง:
```bash
npx expo install --fix
```
และสั่งเคลียร์แคชของตัว Metro Bundler ที่ค้างสะสมไว้จากการรันแอปข้ามรุ่นด้วยการเรียกใช้:
```bash
npx expo start -c
```

### ขั้นตอนที่ 5: การเปิดเครื่องมือส่องความลับดีบั๊กเกอร์ (Chrome DevTools)
สั่งรันแอปพลิเคชันในโหมดพัฒนาปกติ:
```bash
npx expo start
```
ขณะที่รันโปรแกรม ให้กดปุ่ม **`j`** ในหน้าจอคอมพิวเตอร์ หรือเปิดเบราว์เซอร์ Chrome ขึ้นมาแล้วพิมพ์ค้นหา Debugger เพื่อเชื่อมประสาน Console เข้ากับโทรศัพท์มือถือในการปัก Breakpoints

### ขั้นตอนที่ 6: สั่งบิลด์แอปพลิเคชันบน EAS Cloud
เปิดเทอร์มินัลใหม่ยิงคำสั่งบิลด์ส่งขึ้นเซิร์ฟเวอร์ Expo เพื่อรับลิงก์ดาวน์โหลด APK:
```bash
eas build --platform android --profile preview
```

---

## 4. โค้ดเฉลยฉบับสมบูรณ์ (Complete Solution)

ผู้เรียนสามารถกำหนดค่าไฟล์สำคัญทั้ง 3 ไฟล์ตามซอร์สโค้ดเฉลยฉบับสมบูรณ์ต่อไปนี้:

### ไฟล์ที่ 1: รหัสคอนฟิก `app.json`
```json
{
  "expo": {
    "name": "SecureDiary",
    "slug": "secure-diary",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "dark",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#0f172a"
    },
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.student.securediary"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#0f172a"
      },
      "package": "com.student.securediary",
      "versionCode": 1
    },
    "web": {
      "favicon": "./assets/favicon.png"
    }
  }
}
```

### ไฟล์ที่ 2: รหัสคอนฟิก `eas.json`
```json
{
  "cli": {
    "version": ">= 10.0.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "android": {
        "buildType": "apk"
      }
    },
    "production": {
      "distribution": "store"
    }
  },
  "submit": {
    "production": {}
  }
}
```

### ไฟล์ที่ 3: โค้ดอินเทอร์เฟซวินิจฉัย `app/index.tsx`
```tsx
import React, { useState } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  TouchableOpacity, 
  ScrollView, 
  SafeAreaView, 
  Platform, 
  Alert 
} from 'react-native';

interface BugLog {
  id: number;
  time: string;
  type: 'info' | 'error';
  message: string;
}

export default function DiagnosticsDashboard() {
  const [logs, setLogs] = useState<BugLog[]>([]);
  const [triggerCrash, setTriggerCrash] = useState(false);

  const addLog = (type: 'info' | 'error', message: string) => {
    const newLog: BugLog = {
      id: Date.now(),
      time: new Date().toLocaleTimeString(),
      type,
      message
    };
    setLogs((prev) => [newLog, ...prev]);
  };

  // 1. จำลองการยิงเรียกใช้งาน API ปกติ
  const handleNormalOperation = () => {
    addLog('info', 'เรียกใช้งาน API ดึงข้อมูลตามปกติสำเร็จ');
  };

  // 2. จงใจทริกเกอร์ให้เกิด JavaScript Error เพื่อใช้ทดสอบกับ Chrome DevTools
  const handleTriggerMockError = () => {
    try {
      addLog('info', 'กำลังเตรียมทริกเกอร์ JavaScript Error...');
      
      // การทำงานที่ผิดพลาด: พยายามเข้าถึงคุณสมบัติจากตัวแปรที่เป็น undefined
      const mockUserData: any = undefined;
      const userProfileName = mockUserData.profile.name; // จุดนี้จะระเบิดและเด้ง Error ทันที!
      
      console.log(userProfileName);
    } catch (error: any) {
      // ดักข้อความส่งเข้าดีบั๊กเกอร์แอป
      addLog('error', `ดักจับข้อผิดพลาดสำเร็จ: ${error.message}`);
      console.error('พบข้อบกพร่องในระบบ (ดูรายละเอียดใน Console):', error);
      Alert.alert('ตรวจสอบพบคอขวดข้อผิดพลาด', error.message);
    }
  };

  // 3. จำลองพฤติกรรมการแอปค้างพังเฉียบพลัน (สำหรับจำลอง Native Crash ในดีบั๊กเกอร์)
  const handleSimulateNativeCrash = () => {
    addLog('info', 'สั่งเปิดใช้งานจำลอง Runtime Crash ใน 1 วินาที...');
    setTimeout(() => {
      setTriggerCrash(true); // จะสั่งพ่นตัวแปรคอมโพเนนต์พัง
    }, 1000);
  };

  // เมื่อตัวแปรเป็น true ระบบจะพังการเรนเดอร์ทิ้งจำลอง
  if (triggerCrash) {
    const brokenData: any = null;
    return (
      <View style={styles.center}>
        <Text>{brokenData.nonExistentField.crashApp}</Text>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.container}>
        
        {/* หัวข้อเรื่อง */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>⚙️ App Diagnostics</Text>
          <Text style={styles.headerSubtitle}>โมดูลวินิจฉัยและจำลองข้อผิดพลาดเพื่อทดสอบดีบั๊กเกอร์</Text>
        </View>

        {/* ข้อมูล Metadata แอป */}
        <View style={styles.metadataCard}>
          <Text style={styles.cardTitle}>📌 ข้อมูลจำเพาะของแอป (App Metadata)</Text>
          <View style={styles.metaRow}>
            <Text style={styles.metaLabel}>ชื่อแอป (App Name):</Text>
            <Text style={styles.metaValue}>SecureDiary</Text>
          </View>
          <View style={styles.metaRow}>
            <Text style={styles.metaLabel}>รุ่นเวอร์ชัน (Version):</Text>
            <Text style={styles.metaValue}>1.0.0 (android/versionCode: 1)</Text>
          </View>
          <View style={styles.metaRow}>
            <Text style={styles.metaLabel}>รหัสแพ็คเกจ (Package):</Text>
            <Text style={styles.metaValue}>com.student.securediary</Text>
          </View>
          <View style={styles.metaRow}>
            <Text style={styles.metaLabel}>แพลตฟอร์มที่รัน (OS):</Text>
            <Text style={styles.metaValue}>{Platform.OS === 'ios' ? 'iOS' : 'Android'}</Text>
          </View>
        </View>

        {/* ปุ่มทริกเกอร์ระบบ */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>🛠️ แผงควบคุมดีบั๊กเกอร์ (Debug Controls)</Text>
          <Text style={styles.cardDesc}>
            ทดลองเชื่อมต่อ Chrome Developer Tools (คีย์ลัด 'j' ใน CLI) จากนั้นกดปุ่มจำลองด้านล่างเพื่อหัดตรวจวิเคราะห์สาเหตุของบั๊ก
          </Text>

          <TouchableOpacity style={styles.btnNormal} onPress={handleNormalOperation}>
            <Text style={styles.btnText}>🟢 ทริกเกอร์ทำงานปกติ (API Success)</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.btnWarn} onPress={handleTriggerMockError}>
            <Text style={styles.btnText}>🟡 ทริกเกอร์ข้อผิดพลาด (Catchable Error)</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.btnDanger} onPress={handleSimulateNativeCrash}>
            <Text style={styles.btnText}>🔴 ทริกเกอร์แอปพลิเคชันระเบิด (Fatal Render Crash)</Text>
          </TouchableOpacity>
        </View>

        {/* รายงาน Log Realtime บนจอภาพ */}
        <View style={styles.logCard}>
          <View style={styles.logHeaderRow}>
            <Text style={styles.cardTitle}>📜 บันทึกสถานะหน้าจอ (On-Screen Logs)</Text>
            <TouchableOpacity onPress={() => setLogs([])}>
              <Text style={styles.clearLogsText}>ล้างสเตต</Text>
            </TouchableOpacity>
          </View>

          <View style={styles.logScrollWrapper}>
            {logs.length === 0 ? (
              <Text style={styles.emptyLogsText}>ยังไม่มีความเคลื่อนไหวเกิดขึ้นในดีบั๊กเกอร์ขณะนี้</Text>
            ) : (
              logs.map((log) => (
                <View key={log.id} style={styles.logLine}>
                  <Text style={styles.logTime}>[{log.time}]</Text>
                  <Text style={log.type === 'error' ? styles.logErrorText : styles.logInfoText}>
                    {log.message}
                  </Text>
                </View>
              ))
            )}
          </View>
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
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#7f1d1d',
  },
  container: {
    padding: 20,
  },
  header: {
    alignItems: 'center',
    marginVertical: 12,
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
  metadataCard: {
    backgroundColor: '#1e293b',
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 15,
  },
  cardTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 10,
  },
  cardDesc: {
    color: '#94a3b8',
    fontSize: 11,
    lineHeight: 16,
    marginBottom: 12,
  },
  metaRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 6,
    borderBottomWidth: 1,
    borderBottomColor: '#0f172a',
  },
  metaLabel: {
    color: '#94a3b8',
    fontSize: 12,
  },
  metaValue: {
    color: '#38bdf8',
    fontSize: 12,
    fontWeight: '600',
    fontFamily: 'monospace',
  },
  card: {
    backgroundColor: '#1e293b',
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 15,
  },
  btnNormal: {
    backgroundColor: '#10b981',
    borderRadius: 8,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
  },
  btnWarn: {
    backgroundColor: '#f59e0b',
    borderRadius: 8,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
  },
  btnDanger: {
    backgroundColor: '#ef4444',
    borderRadius: 8,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  btnText: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 13,
  },
  logCard: {
    backgroundColor: '#0f172a',
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    borderColor: '#334155',
    minHeight: 180,
  },
  logHeaderRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  clearLogsText: {
    color: '#38bdf8',
    fontSize: 12,
    fontWeight: '600',
  },
  logScrollWrapper: {
    maxHeight: 160,
  },
  emptyLogsText: {
    color: '#475569',
    fontSize: 12,
    textAlign: 'center',
    marginTop: 40,
  },
  logLine: {
    flexDirection: 'row',
    marginBottom: 6,
    alignItems: 'flex-start',
  },
  logTime: {
    color: '#64748b',
    fontSize: 11,
    fontFamily: 'monospace',
    marginRight: 6,
  },
  logInfoText: {
    color: '#e2e8f0',
    fontSize: 11,
    flex: 1,
  },
  logErrorText: {
    color: '#f87171',
    fontSize: 11,
    fontWeight: '600',
    flex: 1,
  },
});
```

---

← [ย้อนกลับแบบทดสอบ: 03-quiz.md](./03-quiz.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [สิ้นสุดหลักสูตรการเรียนรู้](../README.md) →
