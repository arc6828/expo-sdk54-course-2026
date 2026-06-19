# ปฏิบัติการ บทที่ 1: การเตรียมสภาพแวดล้อมและการสร้างแอปพลิเคชันแรก (Lab)

ปฏิบัติการนี้จะช่วยให้ผู้เรียนได้ลงมือทำจริงตั้งแต่ขั้นตอนการติดตั้งโปรแกรมพื้นฐาน การสร้างโปรเจค React Native Expo SDK 54 การรีเซ็ตโครงสร้างตัวอย่างจากเทมเพลตเริ่มต้น การเขียนโค้ดภาษา TypeScript/JSX ตัวแรก และทดลองรันแอปพลิเคชันจริงผ่านเซิร์ฟเวอร์นักพัฒนา

---

## 1. วัตถุประสงค์การเรียนรู้
1. สามารถติดตั้งเครื่องมือพัฒนาแอปพลิเคชันมือถือ (Node.js, VS Code) และกำหนดสภาพแวดล้อมการรันได้อย่างถูกต้อง
2. สามารถสร้างโปรเจค React Native Expo ตัวใหม่ผ่านเทมเพลต TypeScript ได้สำเร็จ
3. สามารถใช้สคริปต์ `reset-project` เพื่อล้างโค้ดเทมเพลตตัวอย่างและจัดโครงสร้างโปรเจคเริ่มต้นใหม่ได้
4. สามารถเขียนคอมโพเนนต์พื้นฐานเพื่อสร้างหน้าจออินเทอร์เฟซต้อนรับอย่างง่ายได้ด้วยตนเอง
5. สามารถใช้งาน Metro Bundler และเปิดทดสอบหน้าจอแอปพลิเคชันจริงผ่านสมาร์ทโฟน (Expo Go) หรืออุปกรณ์จำลองได้

---

## 2. โจทย์และข้อกำหนดปฏิบัติการ (Requirements)
ผู้เรียนจะต้องดำเนินการเตรียมเครื่องมือและเขียนหน้าต้อนรับ (Welcome Screen) ลงในโปรเจคตามเงื่อนไขดังนี้:
1. ติดตั้ง Node.js และ VS Code พร้อมขยายระบบตัวช่วยโค้ด (Extensions) ที่กำหนด
2. สร้างโปรเจค Expo ใหม่ด้วยชื่อโฟลเดอร์ `my-first-app`
3. ล้างตัวอย่างโปรเจคดั้งเดิมให้เหลือเฉพาะโครงสร้างไฟล์เริ่มต้นเพื่อรอเขียนโปรแกรม
4. หน้าจอหลักต้องแสดงกล่องข้อมูลต้อนรับผู้เรียนซึ่งกึ่งกลางของหน้าจอ (Center alignment)
5. ปรับเปลี่ยนโทนสีพื้นหลังเป็นสไตล์ Slate เข้ม (`#0f172a`) และข้อความทั้งหมดต้องจัดสไตล์ให้อ่านง่าย มีสีสันสอดคล้องกับธีม (สไตล์ Dark Mode)
6. มีส่วนแสดงผล **ชื่อ-นามสกุล** และ **รหัสนักศึกษา/ชื่อผู้เรียน** รวมถึงแสดงสถานะการเชื่อมต่อว่า "Expo SDK 54 - Active"

---

## 3. ขั้นตอนการลงมือปฏิบัติ (Step-by-Step Tutorial)

### ขั้นตอนที่ 1: ติดตั้งโปรแกรมที่จำเป็น (Software Installation)
1. **ติดตั้ง Node.js:** ไปที่เว็บไซต์ [Node.js](https://nodejs.org/) ดาวน์โหลดรุ่น **LTS** ล่าสุดมาติดตั้งให้เรียบร้อย จากนั้นเช็กความถูกต้องผ่าน Terminal/PowerShell ด้วยคำสั่ง:
   ```bash
   node -v
   npm -v
   ```
2. **ติดตั้ง Visual Studio Code (VS Code):** ดาวน์โหลดที่ [VS Code](https://code.visualstudio.com/) และเข้าไปที่เมนู Extensions (ไอคอนสี่เหลี่ยมด้านซ้าย) ค้นหาและติดตั้งตัวช่วยต่อไปนี้:
   * *ES7+ React/Redux/React-Native snippets*
   * *Prettier - Code formatter*
   * *Expo Tools*

---

### ขั้นตอนที่ 2: การสร้างโปรเจคใหม่ด้วย create-expo-app
1. เปิด Command Prompt หรือ PowerShell (ใน Windows) หรือ Terminal (ใน macOS/Linux)
2. เปลี่ยนตำแหน่งไดเรกทอรีไปยังโฟลเดอร์ที่คุณต้องการบันทึกงาน เช่น:
   ```bash
   cd Documents
   ```
3. รันคำสั่งสร้างโปรเจคใหม่ด้วยคำสั่ง Expo CLI เวอร์ชันล่าสุด:
   ```bash
   npx create-expo-app@latest my-first-app
   ```
4. เมื่อสร้างโปรเจคเรียบร้อยแล้ว ให้ย้ายเข้าสู่โฟลเดอร์โปรเจค:
   ```bash
   cd my-first-app
   ```
5. เปิดหน้าต่างโปรเจคขึ้นมาบนโปรแกรม VS Code:
   ```bash
   code .
   ```

---

### ขั้นตอนที่ 3: ล้างไฟล์เทมเพลตเริ่มต้น (Reset Project Layout)
ในหน้าต่าง VS Code เปิด Terminal ขึ้นมา (กดปุ่มคีย์บอร์ด `Ctrl + ~`) จากนั้นพิมพ์รันสคริปต์เคลียร์โค้ดเริ่มต้น:

```bash
npm run reset-project
```

*สังเกตผลลัพธ์:* โฟลเดอร์ `app/` จะถูกล้างส่วนประกอบตัวอย่างออกทั้งหมดและสร้างโครงสร้างที่สะอาดขึ้นมาใหม่ทันที ส่วนโค้ดตัวอย่างเดิมจะถูกสำรองไว้ที่ `app-example/`

---

### ขั้นตอนที่ 4: เขียนโค้ดปรับปรุงหน้าแรก (app/index.tsx)
ให้เปิดไฟล์ `app/index.tsx` ใน VS Code แล้วเขียนโค้ดทับด้วยคอมโพเนนต์หน้าต้อนรับดังต่อไปนี้:

```tsx
import { StyleSheet, Text, View } from 'react-native';

export default function WelcomeScreen() {
  return (
    <View style={styles.container}>
      {/* ส่วนหัวแสดงไอคอนหรือรูปจำลองด้วยอิโมจิ */}
      <Text style={styles.emoji}>🚀</Text>
      
      {/* หัวข้อหลัก */}
      <Text style={styles.title}>ยินดีต้อนรับเข้าสู่ชั้นเรียน Mobile App</Text>
      <Text style={styles.subtitle}>React Native Expo (SDK 54)</Text>

      {/* การ์ดข้อมูลผู้เรียน */}
      <View style={styles.card}>
        <Text style={styles.cardLabel}>ผู้พัฒนาแอปพลิเคชัน:</Text>
        <Text style={styles.cardName}>สมชาย ยอดรักดี (นายทะเบียน)</Text>
        <Text style={styles.cardId}>รหัสนักศึกษา: 66-12345-6789</Text>
      </View>

      {/* แถบสถานะระบบ */}
      <View style={styles.statusBadge}>
        <Text style={styles.statusText}>● Status: Running on Expo Go</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a', // สีพื้นหลังเทาดำ Slate เข้ม
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
  },
  emoji: {
    fontSize: 64,
    marginBottom: 16,
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#38bdf8', // สีฟ้านีออนโดดเด่นสว่างตา
    textAlign: 'center',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    color: '#94a3b8', // สีเทาอ่อน สบายตา
    textAlign: 'center',
    marginBottom: 32,
  },
  card: {
    backgroundColor: '#1e293b', // พื้นหลังการ์ดสีเทา Slate
    borderRadius: 16,
    padding: 20,
    width: '100%',
    maxWidth: 320,
    borderWidth: 1,
    borderColor: '#334155', // เส้นขอบสี Slate จาง ๆ
    alignItems: 'flex-start',
    marginBottom: 24,
  },
  cardLabel: {
    fontSize: 12,
    color: '#64748b',
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: 6,
  },
  cardName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#f8fafc',
    marginBottom: 4,
  },
  cardId: {
    fontSize: 14,
    color: '#94a3b8',
  },
  statusBadge: {
    backgroundColor: '#064e3b', // พื้นหลังสีเขียวเข้ม
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 20,
  },
  statusText: {
    color: '#34d399', // ข้อความสีเขียวพาสเทล
    fontSize: 12,
    fontWeight: '600',
  },
});
```

---

### ขั้นตอนที่ 5: เปิดเซิร์ฟเวอร์ Metro Bundler
บันทึกไฟล์โค้ด จากนั้นใน Terminal ของ VS Code ให้รันคำสั่งเริ่มทำงานระบบเซิร์ฟเวอร์นักพัฒนา:

```bash
npx expo start
```

---

### ขั้นตอนที่ 6: สแกนทดสอบบนอุปกรณ์จริง (Expo Go) หรืออุปกรณ์จำลอง
1. เปิดแอปพลิเคชัน **Expo Go** บนมือถือของคุณ (ดาวน์โหลดติดตั้งผ่าน App Store/Play Store ก่อนหน้านี้)
2. **สำหรับ iOS:** เปิดกล้องมือถือสแกน QR Code บนหน้าจอคอมพิวเตอร์เพื่อสลับเปิดรันด้วย Expo Go
3. **สำหรับ Android:** เปิดแอป Expo Go แล้วกดสแกน QR Code ผ่านแอปโดยตรง
4. หากต้องการทดสอบบนเครื่องจำลอง: กดปุ่ม `i` สำหรับ iOS Simulator (สำหรับเครื่อง macOS) หรือกดปุ่ม `a` สำหรับ Android Emulator (ต้องเปิดโปรแกรม Android Virtual Device ก่อนรันคีย์)

---

### ขั้นตอนที่ 7: ทดสอบฟีเจอร์ Fast Refresh
1. เปิดแสดงผลหน้าจอแอปพลิเคชันควบคู่ไปกับหน้าต่างแก้ไขโค้ด VS Code
2. ให้แก้ไขคำว่า `"สมชาย ยอดรักดี"` ในโค้ด `app/index.tsx` บรรทัดที่ 16 ให้เปลี่ยนเป็น **"ชื่อและนามสกุลจริงของคุณ"**
3. กดปุ่มบันทึกไฟล์ (`Ctrl + S` หรือ `Cmd + S`)
4. สังเกตหน้าจอทดสอบ จะพบว่าข้อความอัปเดตเป็นชื่อของคุณทันทีภายในไม่กี่วินาทีโดยไม่ต้องปิดและรันแอปใหม่

---

## 4. โค้ดเฉลยฉบับสมบูรณ์ (Complete Solution)
โค้ดเฉลยฉบับสมบูรณ์สำหรับปฏิบัติการนี้ถูกระบุไว้เป็นตัวอย่างโครงสร้างใน **ขั้นตอนที่ 4** ผู้เรียนสามารถคัดลอกและบันทึกไฟล์เพื่อรันตรวจสอบความถูกต้องของระบบได้ทันที

---

← [ย้อนกลับแบบทดสอบ: 03-quiz.md](./03-quiz.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ศึกษาบทเรียนถัดไป: บทที่ 2](../chapter-02-flexbox-layout/) →
