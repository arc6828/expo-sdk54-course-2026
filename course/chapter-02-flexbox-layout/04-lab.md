# ปฏิบัติการ บทที่ 2: การจัดเลย์เอาต์หน้าจอแดชบอร์ดจำลองด้วย Flexbox (Lab)

ปฏิบัติการนี้จะฝึกทักษะการประยุกต์ใช้ระบบ Flexbox ในการออกแบบโครงสร้างส่วนจัดตำแหน่งต่าง ๆ บนหน้าจอจริง โดยจำลองหน้าอินเทอร์เฟซของ **แอปพลิเคชันแดชบอร์ดควบคุมสมาร์ทโฮม (Smart Home Dashboard Mockup)** ผ่านคอมโพเนนต์พื้นฐาน `View` และ `Text`

---

## 1. วัตถุประสงค์การเรียนรู้
1. สามารถใช้คุณสมบัติ `flexDirection` ในการวางวัตถุทั้งในแนวแกนตั้งและแนวนอนได้ตามโจทย์กำหนด
2. สามารถใช้คุณสมบัติ `justifyContent` และ `alignItems` ในการกระจายบล็อกสีและจัดวัตถุกึ่งกลางหน้าจอได้อย่างถูกต้อง
3. สามารถใช้งานคุณสมบัติ `flexWrap` และ `gap` เพื่อสร้างรูปแบบ Grid ตารางเมนู 2x2 ได้สำเร็จ
4. มีความเข้าใจหลักการจัดลำดับการเขียนและประกอบสไตล์ชีทภายนอกด้วย `StyleSheet.create`

---

## 2. โจทย์และข้อกำหนดปฏิบัติการ (Requirements)
ผู้เรียนจะต้องเขียนโค้ดเพื่อสร้างหน้าจอแดชบอร์ดจำลองในไฟล์ `app/index.tsx` (หลังจากรัน `npm run reset-project` จากบทที่ 1 แล้ว) โดยมีรายละเอียดเลย์เอาต์ 4 ส่วนย่อยหลัก ดังนี้:

```text
+------------------------------------------+
|  [Header Bar] (Title & Notification Dot) |
+------------------------------------------+
|  [Status Summary Card] (Full Width)      |
+------------------------------------------+
|  [2x2 Menu Grid Block]                  |
|  - [Menu 1 (47%)]    - [Menu 2 (47%)]    |
|  - [Menu 3 (47%)]    - [Menu 4 (47%)]    |
+------------------------------------------+
|  [Footer Navigation Bar]                 |
+------------------------------------------+
```

### รายละเอียดเงื่อนไขการจัดสไตล์:
1. **ธีมพื้นหลังแอปพลิเคชัน:** กำหนดเป็นสีเทาดำหรูหรา (`#0f172a`)
2. **ส่วนหัว (Header Bar):**
   * จัดเรียงแบบแนวนอน (`flexDirection: 'row'`) 
   * แบ่งตัวหนังสือชิดซ้ายและขวาสุดริมขอบ (`justifyContent: 'space-between'`)
   * มีชื่อแอป "HOME CONTROL" และฝั่งขวาแสดงจุดไอคอนกลมสีเขียวนีออนแสดงสถานะ Online
3. **การ์ดสรุปสถานะ (Status Summary Card):**
   * กำหนดความกว้างเต็มจอ และมีมุมโค้งมน
   * กำหนดสีพื้นหลังการ์ดเป็นสี Slate กึ่งโปร่งใส (`#1e293b`)
   * ภายในประกอบด้วยข้อความบอกค่าอุณหภูมิ เช่น "24°C - ปกติ"
4. **ตารางบล็อกเมนูย่อย (2x2 Grid):**
   * บล็อกปุ่มเมนูทั้ง 4 ปุ่มมีขนาดความกว้างบล็อกละ `47%` ของพื้นที่ เพื่อให้เรียงตัวคู่กันสองข้างได้พอดี
   * จัดการล้นของวัตถุด้วย `flexWrap: 'wrap'` และมีช่องไฟเว้นระหว่างบล็อกสีเท่ากับ `16` พิกเซล
   * แต่ละบล็อกสีมีพื้นหลังคนละสีกันเพื่อแสดงความเป็นเมนูเฉพาะด้าน
5. **แถบส่วนท้าย (Footer Navigation Bar):**
   * ลอยตัวชิดด้านล่างสุดของหน้าจอ
   * แสดงแท็บจำลอง 3 เมนู (เช่น "Home", "Devices", "Settings") เรียงแนวนอน กระจายระยะห่างสเปซเท่ากันทั้งหมด (`justifyContent: 'space-evenly'`)

---

## 3. ขั้นตอนการลงมือปฏิบัติ (Step-by-Step Tutorial)

### ขั้นตอนที่ 1: เตรียมโปรเจคเริ่มต้น
ตรวจสอบความพร้อมของไฟล์ `app/index.tsx` หากมีโค้ดเก่าอยู่ให้ลบออก หรือเปิดเซิร์ฟเวอร์ด้วยคำสั่ง `npx expo start` เพื่อสแตนด์บายทดสอบผลลัพธ์ผ่านหน้าจออุปกรณ์จริงของคุณ

---

### ขั้นตอนที่ 2: เขียนโค้ดแบ่งโครงสร้างหลัก (Layout Partitioning)
คัดลอกตัวอย่างโครงสร้างโค้ดเริ่มต้นนี้ลงไปใน `app/index.tsx` เพื่อแบ่งโครงสร้างหลักทั้ง 4 ส่วน และทดลองวิเคราะห์ว่าแกนหลักแกนรองทำงานอย่างไร:

```tsx
import { StyleSheet, Text, View } from 'react-native';

export default function SmartHomeDashboard() {
  return (
    <View style={styles.container}>
      
      {/* 1. Header Bar */}
      <View style={styles.header}>
        <Text style={styles.headerText}>HOME CONTROL</Text>
        <View style={styles.statusContainer}>
          <View style={styles.statusDot} />
          <Text style={styles.statusDotText}>ONLINE</Text>
        </View>
      </View>

      {/* 2. Status Summary Card */}
      <View style={styles.statusCard}>
        <Text style={styles.cardTitle}>อุณหภูมิห้องโดยรวม</Text>
        <Text style={styles.cardValue}>24°C</Text>
        <Text style={styles.cardStatus}>ระบบปรับอากาศกำลังทำงานระดับปกติ</Text>
      </View>

      {/* 3. 2x2 Menu Grid Block */}
      <View style={styles.menuGrid}>
        
        {/* บล็อกเมนู 1 */}
        <View style={[styles.menuItem, { backgroundColor: '#ea580c' }]}>
          <Text style={styles.menuEmoji}>💡</Text>
          <Text style={styles.menuText}>ห้องนั่งเล่น</Text>
        </View>

        {/* บล็อกเมนู 2 */}
        <View style={[styles.menuItem, { backgroundColor: '#2563eb' }]}>
          <Text style={styles.menuEmoji}>🔒</Text>
          <Text style={styles.menuText}>ความปลอดภัย</Text>
        </View>

        {/* บล็อกเมนู 3 */}
        <View style={[styles.menuItem, { backgroundColor: '#16a34a' }]}>
          <Text style={styles.menuEmoji}>🔌</Text>
          <Text style={styles.menuText}>เครื่องใช้ไฟฟ้า</Text>
        </View>

        {/* บล็อกเมนู 4 */}
        <View style={[styles.menuItem, { backgroundColor: '#db2777' }]}>
          <Text style={styles.menuEmoji}>🎵</Text>
          <Text style={styles.menuText}>เครื่องเสียง</Text>
        </View>

      </View>

      {/* 4. Footer Navigation Bar */}
      <View style={styles.footer}>
        <Text style={styles.footerItemActive}>หน้าหลัก</Text>
        <Text style={styles.footerItem}>อุปกรณ์</Text>
        <Text style={styles.footerItem}>ตั้งค่า</Text>
      </View>

    </View>
  );
}

const styles = StyleSheet.create({
  // ให้ผู้เรียนระบุสไตล์ชีทสำหรับจัดแนวทาง Flexbox ที่ขั้นตอนถัดไป
});
```

---

### ขั้นตอนที่ 3: ระบุสไตล์และคลาสการจัดตำแหน่งด้วย Flexbox
เขียนข้อกำหนดสไตล์ลงในฟังก์ชัน `StyleSheet.create` ด้านล่างสุดของไฟล์ `app/index.tsx` ดังนี้ เพื่อจัดตำแหน่งกล่องตามโจทย์กำหนด:

```tsx
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a', // ธีมพื้นหลัง Dark Mode Slate
    paddingTop: 60,            // เว้นหลบหน้าจอด้านบน
    paddingHorizontal: 20,
    justifyContent: 'space-between', // ช่วยดึงส่วนหัว ตัวเนื้อหา และส่วนท้ายแยกชิดขอบห่างจากกัน
    paddingBottom: 20,
  },
  header: {
    flexDirection: 'row',        // เรียงแนวนอน
    justifyContent: 'space-between', // ดึงหัวหนังสือชิดซ้าย จุดเขียวชิดขวา
    alignItems: 'center',        // จัดวัตถุกึ่งกลางแนวแกนรอง (แนวตั้ง)
    borderBottomWidth: 1,
    borderColor: '#1e293b',
    paddingBottom: 12,
  },
  headerText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
    letterSpacing: 1,
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,             // ทำสัญลักษณ์วงกลมสมบูรณ์
    backgroundColor: '#22c55e',  // สีเขียวนีออน
  },
  statusDotText: {
    color: '#22c55e',
    fontSize: 12,
    fontWeight: 'bold',
  },
  statusCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    width: '100%',
    borderWidth: 1,
    borderColor: '#334155',
    marginVertical: 10,
  },
  cardTitle: {
    color: '#94a3b8',
    fontSize: 14,
    marginBottom: 4,
  },
  cardValue: {
    color: '#ffffff',
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  cardStatus: {
    color: '#38bdf8',
    fontSize: 12,
  },
  menuGrid: {
    flexDirection: 'row',        // จัดวัตถุลูกวางแนวนอน
    flexWrap: 'wrap',            // ถ้าวัตถุเกินความกว้าง ให้ตัดขึ้นแถวใหม่
    gap: 16,                     // เว้นระยะขอบรอบทุกด้าน
    justifyContent: 'space-between', // ผลักสัดส่วนเมนูสองฝั่งให้ออกชิดขอบ
    marginVertical: 10,
  },
  menuItem: {
    width: '47%',                // ความกว้างกล่องต่อชิ้น (แบ่งคู่ได้ 2 บล็อกพอดีและเหลือที่เว้น gap)
    height: 110,
    borderRadius: 16,
    padding: 16,
    justifyContent: 'space-between', // ช่วยดึง Emoji อยู่บน ชื่อข้อความอยู่ข้างล่าง
  },
  menuEmoji: {
    fontSize: 28,
  },
  menuText: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-evenly', // กระจายพื้นที่ว่างแบ่งเท่า ๆ กันระหว่าง 3 ปุ่มเมนู
    backgroundColor: '#1e293b',
    paddingVertical: 14,
    borderRadius: 24,
    borderWidth: 1,
    borderColor: '#334155',
  },
  footerItem: {
    color: '#64748b',
    fontWeight: 'bold',
  },
  footerItemActive: {
    color: '#38bdf8',            // ปรับสีเมนูแรกเป็นสีฟ้านีออนแสดงการแอ็คทีฟหน้าปัจจุบัน
    fontWeight: 'bold',
  },
});
```

---

### ขั้นตอนที่ 4: ทดสอบการทำงานและปรับเปลี่ยนพฤติกรรมเลย์เอาต์ (Experiment)
ให้ผู้เรียนบันทึกไฟล์และสังเกตแดชบอร์ดจำลองบนสมาร์ทโฟน จากนั้นให้ทดลองทดสอบพฤติกรรมสไตล์ดังนี้:
1. ทดลองเปลี่ยนค่า `flexDirection: 'row'` ในสไตล์ `menuGrid` ให้เป็น `'column'` สังเกตว่าเมนู 4 บล็อกถูกจัดเรียงอย่างไร
2. ลองแก้ไขค่า `gap: 16` ในเมนูตารางให้ลดลงเหลือ `8` หรือเปลี่ยนเป็น `rowGap` และ `columnGap` เพื่อเข้าใจความยืดหยุ่นของตัวแปร

---

## 4. โค้ดเฉลยฉบับสมบูรณ์ (Complete Solution)
ผู้เรียนสามารถคัดลอกโค้ดโครงสร้างที่รวมคอมโพเนนต์และสไตล์ชีทเข้าด้วยกันฉบับสมบูรณ์ด้านล่างนี้ ไปใส่แทนที่ในไฟล์ `app/index.tsx` เพื่อตรวจสอบการแสดงผลหน้าจอแดชบอร์ดควบคุมสมาร์ทโฮมที่ถูกต้อง:

```tsx
import { StyleSheet, Text, View } from 'react-native';

export default function SmartHomeDashboard() {
  return (
    <View style={styles.container}>
      
      {/* 1. Header Bar */}
      <View style={styles.header}>
        <Text style={styles.headerText}>HOME CONTROL</Text>
        <View style={styles.statusContainer}>
          <View style={styles.statusDot} />
          <Text style={styles.statusDotText}>ONLINE</Text>
        </View>
      </View>

      {/* 2. Status Summary Card */}
      <View style={styles.statusCard}>
        <Text style={styles.cardTitle}>อุณหภูมิห้องโดยรวม</Text>
        <Text style={styles.cardValue}>24°C</Text>
        <Text style={styles.cardStatus}>ระบบปรับอากาศกำลังทำงานระดับปกติ</Text>
      </View>

      {/* 3. 2x2 Menu Grid Block */}
      <View style={styles.menuGrid}>
        
        {/* บล็อกเมนู 1 */}
        <View style={[styles.menuItem, { backgroundColor: '#ea580c' }]}>
          <Text style={styles.menuEmoji}>💡</Text>
          <Text style={styles.menuText}>ห้องนั่งเล่น</Text>
        </View>

        {/* บล็อกเมนู 2 */}
        <View style={[styles.menuItem, { backgroundColor: '#2563eb' }]}>
          <Text style={styles.menuEmoji}>🔒</Text>
          <Text style={styles.menuText}>ความปลอดภัย</Text>
        </View>

        {/* บล็อกเมนู 3 */}
        <View style={[styles.menuItem, { backgroundColor: '#16a34a' }]}>
          <Text style={styles.menuEmoji}>🔌</Text>
          <Text style={styles.menuText}>เครื่องใช้ไฟฟ้า</Text>
        </View>

        {/* บล็อกเมนู 4 */}
        <View style={[styles.menuItem, { backgroundColor: '#db2777' }]}>
          <Text style={styles.menuEmoji}>🎵</Text>
          <Text style={styles.menuText}>เครื่องเสียง</Text>
        </View>

      </View>

      {/* 4. Footer Navigation Bar */}
      <View style={styles.footer}>
        <Text style={styles.footerItemActive}>หน้าหลัก</Text>
        <Text style={styles.footerItem}>อุปกรณ์</Text>
        <Text style={styles.footerItem}>ตั้งค่า</Text>
      </View>

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a', // ธีมพื้นหลัง Dark Mode Slate
    paddingTop: 60,            // เว้นหลบหน้าจอด้านบน
    paddingHorizontal: 20,
    justifyContent: 'space-between', // ช่วยดึงส่วนหัว ตัวเนื้อหา และส่วนท้ายแยกชิดขอบห่างจากกัน
    paddingBottom: 20,
  },
  header: {
    flexDirection: 'row',        // เรียงแนวนอน
    justifyContent: 'space-between', // ดึงหัวหนังสือชิดซ้าย จุดเขียวชิดขวา
    alignItems: 'center',        // จัดวัตถุกึ่งกลางแนวแกนรอง (แนวตั้ง)
    borderBottomWidth: 1,
    borderColor: '#1e293b',
    paddingBottom: 12,
  },
  headerText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
    letterSpacing: 1,
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,             // ทำสัญลักษณ์วงกลมสมบูรณ์
    backgroundColor: '#22c55e',  // สีเขียวนีออน
  },
  statusDotText: {
    color: '#22c55e',
    fontSize: 12,
    fontWeight: 'bold',
  },
  statusCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    width: '100%',
    borderWidth: 1,
    borderColor: '#334155',
    marginVertical: 10,
  },
  cardTitle: {
    color: '#94a3b8',
    fontSize: 14,
    marginBottom: 4,
  },
  cardValue: {
    color: '#ffffff',
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  cardStatus: {
    color: '#38bdf8',
    fontSize: 12,
  },
  menuGrid: {
    flexDirection: 'row',        // จัดวัตถุลูกวางแนวนอน
    flexWrap: 'wrap',            // ถ้าวัตถุเกินความกว้าง ให้ตัดขึ้นแถวใหม่
    gap: 16,                     // เว้นระยะขอบรอบทุกด้าน
    justifyContent: 'space-between', // ผลักสัดส่วนเมนูสองฝั่งให้ออกชิดขอบ
    marginVertical: 10,
  },
  menuItem: {
    width: '47%',                // ความกว้างกล่องต่อชิ้น (แบ่งคู่ได้ 2 บล็อกพอดีและเหลือที่เว้น gap)
    height: 110,
    borderRadius: 16,
    padding: 16,
    justifyContent: 'space-between', // ช่วยดึง Emoji อยู่บน ชื่อข้อความอยู่ข้างล่าง
  },
  menuEmoji: {
    fontSize: 28,
  },
  menuText: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-evenly', // กระจายพื้นที่ว่างแบ่งเท่า ๆ กันระหว่าง 3 ปุ่มเมนู
    backgroundColor: '#1e293b',
    paddingVertical: 14,
    borderRadius: 24,
    borderWidth: 1,
    borderColor: '#334155',
  },
  footerItem: {
    color: '#64748b',
    fontWeight: 'bold',
  },
  footerItemActive: {
    color: '#38bdf8',            // ปรับสีเมนูแรกเป็นสีฟ้านีออนแสดงการแอ็คทีฟหน้าปัจจุบัน
    fontWeight: 'bold',
  },
});
```

---

← [ย้อนกลับแบบทดสอบ: 03-quiz.md](./03-quiz.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ศึกษาบทเรียนถัดไป: บทที่ 3](../chapter-03-core-components/) →
