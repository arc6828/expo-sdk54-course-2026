# บทที่ 4: การจัดการสถานะ พร็อพส์ และแบบฟอร์มรับข้อมูล (Content)

อินเทอร์เฟซของโมบายแอปพลิเคชันที่มีการตอบโต้ที่ดีจำเป็นต้องประมวลผลการเปลี่ยนแปลงข้อมูลตามพฤติกรรมของผู้ใช้ เช่น การพิมพ์ข้อความ การสลับหน้าจอปุ่มตัวเลือก หรือการกดส่งฟอร์ม ใน React Native เราใช้แนวคิดของ **State (สถานะ)** ร่วมกับ **Props (คุณสมบัติ)** ในการเป็นตัวควบคุมโครงสร้างข้อมูลและการเรนเดอร์เนื้อหาใหม่ (Re-render) เพื่ออัปเดตหน้าจอให้ทันสมัยโดยอัตโนมัติ

---

## 4.1 แนวคิดของสถานะ (State) ใน React Native และการใช้งาน useState Hook

### 1. State คืออะไร?
**State** คือ ข้อมูลภายในคอมโพเนนต์ที่สามารถเปลี่ยนแปลงค่าได้ตลอดเวลา (Mutable) ในแต่ละรอบอายุการทำงาน (Lifecycle) ของคอมโพเนนต์ เมื่อค่าของ State ถูกแก้ไขด้วยฟังก์ชันเฉพาะ React จะทำการวาดคอมโพเนนต์ย่อยชิ้นนั้น ๆ ใหม่บนหน้าจอ (Re-render) ทันที เพื่อสะท้อนการเปลี่ยนแปลงให้ผู้ใช้งานเห็นหน้าจอใหม่

### 2. การเรียกใช้งาน useState Hook
ใน Functional Components เราประกาศสถานะเริ่มต้นและฟังก์ชันในการเปลี่ยนแปลงค่าสเตตผ่าน `useState` Hook:
```tsx
import { useState } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

export default function CounterApp() {
  // ประกาศ State ชื่อ count มีค่าเริ่มต้นเป็น 0 และมีฟังก์ชัน setCount ในการแก้ไขค่า
  const [count, setCount] = useState<number>(0);

  return (
    <View style={styles.container}>
      <Text style={styles.text}>จำนวนคลิกปัจจุบัน: {count}</Text>
      {/* เมื่อคลิกปุ่ม ให้เพิ่มค่า count ขึ้นทีละ 1 */}
      <Button title="กดเพิ่มจำนวน" onPress={() => setCount(count + 1)} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    fontSize: 20,
    marginBottom: 20,
  },
});
```

---

## 4.2 ข้อแตกต่างและการทำงานร่วมกันระหว่าง State และ Props

การทำความเข้าใจข้อแตกต่างระหว่าง State และ Props ถือเป็นรากฐานสำคัญของการจัดสถาปัตยกรรมข้อมูลใน React Native:

| คุณลักษณะ | State (สถานะภายใน) | Props (คุณสมบัติภายนอก) |
| :--- | :--- | :--- |
| **ที่มา (Source)** | กำหนดและสร้างขึ้นภายในคอมโพเนนต์ตัวเอง | ส่งผ่านมาจากคอมโพเนนต์แม่ (Parent) |
| **การแก้ไขค่า (Mutability)** | เปลี่ยนแปลงได้อิสระโดยเรียกใช้ฟังก์ชัน Setter (เช่น `setCount`) | เปลี่ยนแปลงค่าไม่ได้จากภายในลูก (ใช้อ่านอย่างเดียว - Read-Only) |
| **ตัวเหนี่ยวนำให้เกิดการวาดหน้าจอใหม่ (Re-render Trigger)** | ส่งผลให้เรนเดอร์ใหม่ทันทีเมื่อเรียกฟังก์ชันอัปเดตค่า | ส่งผลให้คอมโพเนนต์ลูกเรนเดอร์ใหม่ทันทีเมื่อแม่เปลี่ยนค่า Props |
| **บทบาทหน้าที่หลัก** | เก็บข้อมูลประวัติย่อย ความชอบ หรืออินพุตที่ผู้ใช้กำลังพิมพ์ | ส่งผ่านการตั้งค่า หน้าตา หรือสั่งทำเหตุการณ์กลับไปหาแม่ |

---

## 4.3 การทำแบบฟอร์มด้วย Controlled Components ผ่าน TextInput

ในการพัฒนาเว็บหรือแอปแบบดั้งเดิม ตัวอัปเดตข้อความจะถูกผูกไว้ภายในระบบของแป้นพิมพ์หรือ DOM ดั้งเดิม แต่ใน React Native การพัฒนาแบบฟอร์มที่เป็นระเบียบจะใช้แนวคิด **Controlled Components** ซึ่งหมายถึงการนำ State ของ React มาเป็น "แหล่งข้อมูลที่ถูกต้องเพียงหนึ่งเดียว (Single Source of Truth)" สำหรับคอมโพเนนต์อินพุตนั้น ๆ

### 1. วิธีการสร้าง Controlled Input
เราจะสร้าง State คอยบันทึกตัวอักษร และผูกพร็อพส์ `value` เข้ากับสเตตนั้น พร้อมสั่งการผ่านเหตุการณ์ `onChangeText` ให้นำข้อความสตริงล่าสุดไปอัปเดตสเตตทันที:

```tsx
import { useState } from 'react';
import { View, TextInput, Text, StyleSheet } from 'react-native';

export default function ControlledInput() {
  const [username, setUsername] = useState<string>('');

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        value={username}
        onChangeText={setUsername} // มีค่าเท่ากับ (text) => setUsername(text)
        placeholder="กรอกชื่อผู้ใช้ของคุณ..."
      />
      <Text style={styles.previewText}>ค่าสเตตปัจจุบัน: {username}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: '#94a3b8',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },
  previewText: {
    marginTop: 10,
    color: '#64748b',
  },
});
```

---

## 4.4 การแบ่งปันข้อมูลย้อนกลับด้วยหลักการ Lifting State Up

ข้อมูลใน React จะไหลเวียนไปในทิศทางเดียวจากบนลงล่าง (Parent to Child) หากเราต้องการให้คอมโพเนนต์ลูกสลับกันเปลี่ยนแปลง หรือส่งข้อมูลอินพุตจากช่องกรอกในคอมโพเนนต์ลูกขึ้นไปเปลี่ยนค่าที่คอมโพเนนต์แม่ เราจำเป็นต้องประยุกต์ใช้เทคนิค **Lifting State Up (การยกสถานะขึ้น)**

### แนวปฏิบัติของการ Lifting State Up
1. **ยกตำแหน่งเก็บ State:** นำ State ไปเก็บไว้ในคอมโพเนนต์ที่เป็นบรรพบุรุษร่วมที่ใกล้ที่สุด (Common Ancestor)
2. **ส่งผ่านฟังก์ชันอัปเดตค่า:** ตัวคอมโพเนนต์แม่จะสร้างฟังก์ชันการประมวลผล แล้วจัดส่งฟังก์ชันนี้ไปเป็นหนึ่งใน Props ของคอมโพเนนต์ลูก
3. **การโทรกลับ (Callback):** เมื่อลูกสัมผัสหรือพิมพ์รับข้อความ จะทำการกระตุ้นฟังก์ชัน Props นั้น ส่งข้อมูลย้อนกลับขึ้นไปอัปเดตค่าสเตตบนคอมโพเนนต์แม่

```tsx
// 1. ชิ้นส่วนลูก (Child) - ช่องป้อนข้อมูล
interface SearchInputProps {
  query: string;
  onQueryChange: (text: string) => void;
}

function SearchInput({ query, onQueryChange }: SearchInputProps) {
  return (
    <TextInput
      value={query}
      onChangeText={onQueryChange} // กระตุ้น Callback ส่งค่ากลับขึ้นด้านบน
      placeholder="พิมพ์ค้นหาชื่อสินค้า..."
      style={{ borderWidth: 1, padding: 8, borderRadius: 6 }}
    />
  );
}

// 2. ชิ้นส่วนแม่ (Parent) - เก็บสเตตหลัก
import { useState } from 'react';
import { View, Text } from 'react-native';

export default function ProductCatalog() {
  const [searchQuery, setSearchQuery] = useState<string>('');

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 18, marginBottom: 8 }}>แคตตาล็อกสินค้า</Text>
      {/* ส่งผ่านทั้งค่าสเตตและฟังก์ชันอัปเดตสเตตไปให้คอมโพเนนต์ลูก */}
      <SearchInput query={searchQuery} onQueryChange={setSearchQuery} />
      <Text style={{ marginTop: 10 }}>คุณกำลังค้นหาคำว่า: {searchQuery}</Text>
    </View>
  );
}
```

---

## 4.5 การจัดทำฟอร์มคำนวณค่าดัชนีมวลกาย (BMI Calculation Form)

นอกจากการพิมพ์เก็บข้อความธรรมดาแล้ว แบบฟอร์มในโมบายแอปพลิเคชันยังนิยมใช้ในการประมวลผลคำนวณทางคณิตศาสตร์จากตัวเลขอินพุตที่ผู้ใช้พิมพ์เข้ามา เช่น ยอดราคาสินค้ารวม หรือดัชนีสุขภาพ โดยข้อมูลอินพุตจาก `TextInput` จะถูกส่งคืนมาเป็นประเภทสตริง (`string`) เสมอ ดังนั้น ผู้พัฒนาจึงต้องแปลงค่าเป็นตัวเลขจริงก่อนเริ่มการคำนวณเพื่อป้องกันข้อผิดพลาดเชิงโปรแกรม (NaN)

### 1. วิธีการผูกและแปลงค่าตัวเลข (Numeric Binding & Parsing)
* **`keyboardType="numeric"`**: เปิดแป้นพิมพ์ตัวเลข
* **`parseFloat()` / `parseInt()`**: ใช้สำหรับแปลงข้อความที่พิมพ์เป็นตัวเลขจำนวนจริงหรือทศนิยม
* **การป้องกันความผิดพลาด (Defensive Programming):** ตรวจสอบว่าผู้ใช้กรอกข้อความว่างเปล่า หรือหารด้วยศูนย์ (Division by Zero) หรือไม่ ก่อนทำรายการคำนวณ

### 2. โค้ดตัวอย่างคอมโพเนนต์เครื่องคำนวณดัชนีมวลกาย (BMI Calculator)

```tsx
import { useState } from 'react';
import { View, Text, TextInput, Pressable, StyleSheet } from 'react-native';

export default function BMICalculator() {
  const [weight, setWeight] = useState<string>(''); // เก็บน้ำหนัก (กิโลกรัม) เป็นข้อความ
  const [height, setHeight] = useState<string>(''); // เก็บส่วนสูง (เซนติเมตร) เป็นข้อความ
  const [bmi, setBmi] = useState<number | null>(null); // เก็บคะแนน BMI คำนวณเสร็จ
  const [category, setCategory] = useState<string>(''); // เก็บเกณฑ์สุขภาพ

  const handleCalculate = () => {
    const w = parseFloat(weight);
    const h = parseFloat(height) / 100; // แปลงหน่วยเซนติเมตรเป็นเมตร

    if (w > 0 && h > 0) {
      const calculatedBmi = w / (h * h);
      setBmi(calculatedBmi);

      // แปลผลเกณฑ์ BMI (อ้างอิงตามเกณฑ์เอเชียแปซิฟิก)
      if (calculatedBmi < 18.5) {
        setCategory('น้ำหนักน้อยกว่าเกณฑ์ (ผอม)');
      } else if (calculatedBmi < 23) {
        setCategory('น้ำหนักปกติ (สุขภาพดี)');
      } else if (calculatedBmi < 25) {
        setCategory('น้ำหนักเกิน (ท้วม)');
      } else {
        setCategory('ภาวะอ้วน (Obese)');
      }
    } else {
      setBmi(null);
      setCategory('กรุณากรอกข้อมูลส่วนสูงและน้ำหนักให้ครบถ้วนถูกต้อง');
    }
  };

  return (
    <View style={styles.card}>
      <Text style={styles.cardTitle}>เครื่องคำนวณหาค่า BMI</Text>

      {/* ช่องกรอกน้ำหนัก */}
      <Text style={styles.label}>น้ำหนักตัว (กิโลกรัม)</Text>
      <TextInput
        style={styles.input}
        placeholder="ตัวอย่าง 65"
        placeholderTextColor="#64748b"
        keyboardType="numeric"
        value={weight}
        onChangeText={setWeight}
      />

      {/* ช่องกรอกส่วนสูง */}
      <Text style={styles.label}>ส่วนสูง (เซนติเมตร)</Text>
      <TextInput
        style={styles.input}
        placeholder="ตัวอย่าง 170"
        placeholderTextColor="#64748b"
        keyboardType="numeric"
        value={height}
        onChangeText={setHeight}
      />

      {/* ปุ่มสั่งคำนวณจัดด้วย Pressable */}
      <Pressable 
        onPress={handleCalculate} 
        style={({ pressed }) => [
          styles.button, 
          pressed ? styles.buttonPressed : null
        ]}
      >
        <Text style={styles.buttonText}>ประมวลผลดัชนีมวลกาย</Text>
      </Pressable>

      {/* พื้นที่แสดงผลการคำนวณแบบมีเงื่อนไข (Conditional Rendering) */}
      {bmi !== null && (
        <View style={styles.resultBox}>
          <Text style={styles.resultBmiText}>ค่า BMI ของคุณ: {bmi.toFixed(1)}</Text>
          <Text style={styles.resultCatText}>เกณฑ์ของคุณ: {category}</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#1e293b',
    padding: 16,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#334155',
    marginVertical: 16,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 12,
  },
  label: {
    color: '#cbd5e1',
    fontSize: 13,
    marginBottom: 6,
  },
  input: {
    backgroundColor: '#0f172a',
    borderWidth: 1,
    borderColor: '#334155',
    borderRadius: 8,
    height: 44,
    paddingHorizontal: 12,
    color: '#ffffff',
    marginBottom: 12,
  },
  button: {
    backgroundColor: '#10b981', // สีเขียวนีออนสำหรับคำนวณสุขภาพ
    height: 44,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonPressed: {
    backgroundColor: '#059669',
  },
  buttonText: {
    color: '#ffffff',
    fontWeight: 'bold',
  },
  resultBox: {
    marginTop: 16,
    padding: 12,
    backgroundColor: '#0f172a',
    borderRadius: 8,
    alignItems: 'center',
  },
  resultBmiText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  resultCatText: {
    color: '#38bdf8',
    fontSize: 14,
    marginTop: 4,
  },
});
```

---

## 4.6 การตรวจสอบความถูกต้องของฟอร์ม (Form Validation) และการแจ้งเตือนข้อผิดพลาด (Error Feedback)

แอปพลิเคชันคุณภาพสูงต้องช่วยป้องกันไม่ให้ผู้ใช้ส่งข้อมูลที่ผิดรูปแบบไปยังเซิร์ฟเวอร์ โดยระบบควรทำการตรวจสอบข้อผิดพลาด (Validation) ทันทีบนตัวเครื่อง (Client-side) และแสดงคำเตือนอย่างเด่นชัด

### 1. วิธีตรวจสอบข้อมูลแบบเรียลไทม์ (Real-time Validation)
เราสามารถตรวจสอบค่าของตัวแปรสเตตในแต่ละจังหวะการพิมพ์ และเก็บข้อความผิดพลาดลงในสถานะ `errors` หรือคำนวณจากสถานะปัจจุบันได้โดยตรง:

```tsx
// ตรวจสอบว่ารูปแบบอีเมลถูกต้องหรือไม่โดยใช้ Regular Expression (Regex)
const validateEmail = (emailText: string) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(emailText)) {
    return 'รูปแบบอีเมลไม่ถูกต้อง';
  }
  return '';
};
```

### 2. การจัดการสถานะปุ่มกดสัมผัสและ Error UI
* **กล่องรับข้อความสีส้ม/แดง:** กำหนดสไตล์ขอบช่องพิมพ์ให้แดงขึ้นเมื่อสเตตข้อผิดพลาดไม่มีค่าว่าง
* **การสั่งปิดความสามารถของปุ่มสัมผัส (Disable Button):** นำค่าความถูกต้องของข้อมูล (เช่น `isFormValid`) มาเป็นตัวกำหนดค่าการตอบสนองของ `Pressable` หากฟอร์มยังกรอกไม่สมบูรณ์ ปุ่มจะจางลงและไม่รับคำสั่งนิ้วสัมผัส

---

## 4.7 โค้ดตัวอย่างการประกอบฟอร์มลงทะเบียนพร้อมระบบตรวจสอบแบบเรียลไทม์

โค้ดเต็มด้านล่างนี้แสดงวิธีการรวบรวมสถานะหลายช่องรับอินพุต การทำ Validation ข้อมูล และการปรับแต่งปุ่มสัมผัสอย่างลื่นไหลเมื่อเงื่อนไขถูกต้องสมบูรณ์:

```tsx
import { useState } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  TextInput, 
  Pressable, 
  SafeAreaView, 
  Alert 
} from 'react-native';

export default function RegisterForm() {
  // 1. ประกาศตัวแปรสำหรับผูกฟอร์มรับอินพุต
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  
  // 2. ประกาศตัวแปรเก็บสถานะขอบบกพร่อง
  const [emailError, setEmailError] = useState<string>('');
  const [passwordError, setPasswordError] = useState<string>('');

  // 3. ฟังก์ชันดักจับความถูกต้องของอีเมล
  const handleEmailChange = (text: string) => {
    setEmail(text);
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (text.trim() === '') {
      setEmailError('กรุณากรอกอีเมลของคุณ');
    } else if (!emailRegex.test(text)) {
      setEmailError('อีเมลต้องเป็นรูปแบบที่ถูกต้อง เช่น name@domain.com');
    } else {
      setEmailError('');
    }
  };

  // 4. ฟังก์ชันดักจับความยาวรหัสผ่าน
  const handlePasswordChange = (text: string) => {
    setPassword(text);
    if (text.trim() === '') {
      setPasswordError('กรุณากรอกรหัสผ่าน');
    } else if (text.length < 6) {
      setPasswordError('รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร');
    } else {
      setPasswordError('');
    }
  };

  // 5. ประเมินสัญญานว่าฟอร์มโดยรวมสมบูรณ์พร้อมส่งหรือไม่
  const isFormValid = 
    email.trim() !== '' && 
    password.trim() !== '' && 
    emailError === '' && 
    passwordError === '';

  const handleSubmit = () => {
    if (isFormValid) {
      Alert.alert('ลงทะเบียนสำเร็จ', `อีเมล: ${email}\nรหัสผ่านของคุณปลอดภัยเรียบร้อย`);
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <Text style={styles.title}>สร้างบัญชีสมาชิก</Text>
        
        {/* ฟอร์มรับอีเมล */}
        <View style={styles.inputGroup}>
          <Text style={styles.label}>ที่อยู่อีเมล</Text>
          <TextInput
            style={[
              styles.input, 
              emailError ? styles.inputInvalid : null
            ]}
            placeholder="ตัวอย่าง user@email.com"
            placeholderTextColor="#64748b"
            value={email}
            onChangeText={handleEmailChange}
            keyboardType="email-address"
            autoCapitalize="none"
          />
          {emailError ? <Text style={styles.errorText}>{emailError}</Text> : null}
        </View>

        {/* ฟอร์มรับรหัสผ่าน */}
        <View style={styles.inputGroup}>
          <Text style={styles.label}>รหัสผ่าน (Password)</Text>
          <TextInput
            style={[
              styles.input, 
              passwordError ? styles.inputInvalid : null
            ]}
            placeholder="ตั้งรหัสผ่านอย่างน้อย 6 ตัว"
            placeholderTextColor="#64748b"
            value={password}
            onChangeText={handlePasswordChange}
            secureTextEntry={true}
            autoCapitalize="none"
          />
          {passwordError ? <Text style={styles.errorText}>{passwordError}</Text> : null}
        </View>

        {/* ปุ่มบันทึกข้อมูลโต้ตอบตามความถูกต้องของข้อมูล */}
        <Pressable
          disabled={!isFormValid} // ล็อกไม่ให้คลิกปุ่มหากฟอร์มไม่สมบูรณ์
          onPress={handleSubmit}
          style={({ pressed }) => [
            styles.submitButton,
            !isFormValid ? styles.submitButtonDisabled : null,
            pressed && isFormValid ? styles.submitButtonPressed : null
          ]}
        >
          <Text style={styles.submitButtonText}>ลงทะเบียนบัญชีใหม่</Text>
        </Pressable>

      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#0f172a',
    justifyContent: 'center',
  },
  container: {
    padding: 24,
    marginHorizontal: 16,
    backgroundColor: '#1e293b',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#334155',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: 24,
  },
  inputGroup: {
    marginBottom: 16,
  },
  label: {
    fontSize: 14,
    color: '#cbd5e1',
    marginBottom: 6,
    fontWeight: '500',
  },
  input: {
    height: 48,
    backgroundColor: '#0f172a',
    borderWidth: 1,
    borderColor: '#334155',
    borderRadius: 8,
    paddingHorizontal: 12,
    color: '#ffffff',
    fontSize: 15,
  },
  inputInvalid: {
    borderColor: '#f43f5e', // เปลี่ยนกรอบเป็นสีส้มแดงเตือนภัย
  },
  errorText: {
    fontSize: 12,
    color: '#f43f5e',
    marginTop: 6,
  },
  submitButton: {
    backgroundColor: '#3b82f6',
    height: 48,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 10,
  },
  submitButtonDisabled: {
    backgroundColor: '#1e293b',
    borderColor: '#334155',
    borderWidth: 1,
    opacity: 0.5,
  },
  submitButtonPressed: {
    backgroundColor: '#2563eb',
  },
  submitButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
```

## 4.8 สรุปท้ายบทเรียน

**แนวคิดของสถานะ (State) ใน React Native และการใช้งาน useState Hook:** สถานะ (State) คือข้อมูลภายในคอมโพเนนต์ที่เปลี่ยนค่าได้ โดยการอัปเดตสเตตผ่านฟังก์ชันแก้ไขของ useState Hook จะกระตุ้นให้ React ทำการวาดอินเตอร์เฟซบนหน้าจอใหม่ (Re-render) โดยอัตโนมัติ เพื่อนำผลลัพธ์ของข้อมูลล่าสุดไปแสดงผลให้กับผู้ใช้ได้อย่างถูกต้องทันที

**ข้อแตกต่างและการทำงานร่วมกันระหว่าง State และ Props:** State ทำหน้าที่เก็บและจัดการข้อมูลที่มีการเคลื่อนไหวอยู่ภายในคอมโพเนนต์ชิ้นนั้น ๆ ในขณะที่ Props เป็นคุณสมบัติภายนอกที่ส่งผ่านจากคอมโพเนนต์แม่ลงมายังคอมโพเนนต์ลูกแบบอ่านได้อย่างเดียว (Read-Only) ซึ่งการประสานงานระหว่างสองอย่างนี้จะเหนี่ยวนำให้คอมโพเนนต์ลูกเรนเดอร์ใหม่โดยอัตโนมัติเมื่อข้อมูลมีการเปลี่ยนแปลง

**การทำแบบฟอร์มด้วย Controlled Components ผ่าน TextInput:** การจัดการอินพุตฟอร์มใน React Native ยึดหลัก Controlled Components โดยมีสเตตเป็นแหล่งข้อมูลที่ถูกต้องที่สุดเพียงแหล่งเดียว (Single Source of Truth) ซึ่งเป็นการผูกสเตตเข้ากับคุณสมบัติ value ของกล่องรับข้อมูลข้อความ TextInput และกระตุ้นฟังก์ชันเซ็ตเตอร์ผ่านเหตุการณ์ onChangeText เพื่อเก็บตัวอักษรทุกตัวลงในสเตตแบบเรียลไทม์

**การแบ่งปันข้อมูลย้อนกลับด้วยหลักการ Lifting State Up:** เพื่อรองรับทิศทางการไหลเวียนข้อมูลทางเดียวจากแม่ไปลูก (One-way Data Flow) การส่งผ่านข้อมูลย้อนกลับจากลูกขึ้นไปหาแม่จะใช้เทคนิค Lifting State Up โดยการย้ายสเตตหลักขึ้นไปไว้บนคอมโพเนนต์บรรพบุรุษร่วม แล้วส่งฟังก์ชันการจัดการ (Callback Function) ผ่าน Props ลงมาให้คอมโพเนนต์ลูกเรียกใช้งานเมื่อต้องการส่งสัญญาณการเปลี่ยนแปลง

**การจัดทำฟอร์มคำนวณค่าดัชนีมวลกาย (BMI Calculation Form):** การสร้างฟอร์มสำหรับคำนวณ เช่น เครื่องหาดัชนีมวลกาย (BMI) จะใช้ TextInput ควบคู่ไปกับแป้นพิมพ์ตัวเลข (keyboardType="numeric") และเมื่อสั่งทำงานจะต้องทำการแปลงประเภทข้อมูลจากข้อความสตริงเป็นตัวเลขจำนวนจริงผ่าน parseFloat() ก่อนเริ่มกระบวนการคำนวณ พร้อมทั้งจัดระบบป้องกันการคำนวณที่ผิดพลาดจากข้อมูลที่ว่างเปล่าหรือเป็นศูนย์

**การตรวจสอบความถูกต้องของฟอร์มและการแจ้งเตือนข้อผิดพลาด:** ระบบแบบฟอร์มที่ดีจำเป็นต้องมี Form Validation เพื่อตรวจสอบความถูกต้องของอีเมลหรือรหัสผ่านทันทีในระบบ Client-side ก่อนนำส่งข้อมูลจริง โดยผู้พัฒนาสามารถเก็บข้อมูลข้อผิดพลาดไว้ในสเตตและนำสัญญานตรวจสอบนั้นมาควบคุมการปิดฟังก์ชันปุ่มกด (disabled) รวมถึงเปลี่ยนดีไซน์สีของกรอบอินพุตให้สะดุดตาเพื่อสร้างการตอบสนองที่เข้าใจง่าย

**โค้ดตัวอย่างการประกอบฟอร์มลงทะเบียนพร้อมระบบตรวจสอบแบบเรียลไทม์:** ตัวอย่างการประกอบฟอร์มลงทะเบียนแสดงผลความสอดคล้องของการนำ TextInput มารับค่าอีเมลและรหัสผ่าน โดยใช้ฟังก์ชันประเมินความถูกต้องของตัวอักษรเพื่ออัปเดตสเตตความผิดพลาดแบบวินาทีต่อวินาที ซึ่งช่วยควบคุมการทำงานของปุ่ม Pressable และเปิดโอกาสให้ผู้ใช้งานกดยืนยันการทำธุรกรรมได้เฉพาะเมื่อข้อมูลในทุกช่องมีรูปแบบที่สมบูรณ์และปลอดภัย

---

← [ย้อนกลับแผนการสอน: 01-lesson-plan.md](./01-lesson-plan.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ทำแบบทดสอบถัดไป: 03-quiz.md](./03-quiz.md) →
