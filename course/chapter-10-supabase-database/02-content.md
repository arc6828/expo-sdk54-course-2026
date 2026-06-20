# บทที่ 10: การใช้งานคลาวด์ดาต้าเบสด้วย Supabase (Content)

การพัฒนาแอปพลิเคชันที่มีระบบฐานข้อมูลหลังบ้านแบบเรียลไทม์ โดยไม่ต้องเสียเวลาเขียนโค้ดและตั้งค่าเครื่องเซิร์ฟเวอร์เอง ถือเป็นความสะดวกที่ทำได้จริงผ่านระบบ **Backend-as-a-Service (BaaS)** ในบทเรียนนี้เราจะศึกษาขั้นตอนการเชื่อมโยงแอปพลิเคชัน Expo กับ **Supabase Cloud Database** ซึ่งขับเคลื่อนด้วย PostgreSQL และเรียนรู้วิธีจัดการฐานข้อมูลครบวงจร (CRUD Operations) ทั้งการเพิ่ม ดึง แก้ไข และลบข้อมูล

---

## 10.1 สถาปัตยกรรม BaaS และคลาวด์ดาต้าเบสของ Supabase

**Supabase** เป็นแพลตฟอร์มหลังบ้านสำเร็จรูปที่เป็นมิตรต่อผู้พัฒนาและเปิดใช้งานแบบ Open-source โดยมีโครงสร้างฐานข้อมูลหลักเป็น **PostgreSQL** ซึ่งมีความเสถียรและรองรับความสัมพันธ์ของข้อมูล (Relational Database)

### ทำไมต้องเลือก Supabase?
* **พร้อมใช้งานทันที:** มีระบบ Database, Auth, และ Storage มาให้พร้อมใช้โดยไม่ต้องติดตั้งและตั้งค่าระบบเครือข่ายเซิร์ฟเวอร์เอง
* **รองรับระบบ SQL แท้:** สามารถเขียน Query จัดความสัมพันธ์ข้อมูล หรือประกาศ Constraints ป้องกันตารางพังได้เหมือนฐานข้อมูลสากลทั่วไป
* **ประสิทธิภาพระดับเนทีฟ:** ไลบรารีพัฒนามาให้รองรับระบบ Asynchronous (Promise-based) ทำงานร่วมกับ React Native ได้อย่างไร้รอยต่อ

### ขั้นตอนการเตรียมคลาวด์โปรเจกต์:
1. ลงทะเบียนและล็อกอินเข้าใช้งานที่ [supabase.com](https://supabase.com)
2. สร้างโครงการใหม่ (Create New Project) และระบุรหัสผ่านฐานข้อมูล
3. ไปที่เมนู **Project Settings > API** ของแผงควบคุมหลังบ้าน เพื่อคัดลอกค่าความปลอดภัยหลัก 2 คีย์ ได้แก่:
   * **Project URL**: ที่อยู่โดเมนชี้เฉพาะสำหรับส่ง API รีเควส
   * **Anon Key (Public)**: คีย์สาธารณะสำหรับสแกนส่งสิทธิ์อนุญาตเข้าถึงตารางข้อมูล

---

## 10.2 การติดตั้งและตั้งค่า Supabase Client ใน Expo (SDK 54)

เพื่อเชื่อมแอปพลิเคชัน Expo เข้าหาตารางฐานข้อมูล เราจะติดตั้งชุดซอฟต์แวร์พัฒนาอย่างเป็นทางการร่วมกับตัวช่วยจัดระเบียบ URL สำหรับ React Native:

```bash
npm install @supabase/supabase-js react-native-url-polyfill
```
*หมายเหตุ: `react-native-url-polyfill` ทำหน้าที่เป็นสะพานเชื่อมฟังก์ชันการประมวลผลคำสั่ง URL ของตัวเนทีฟเครื่องให้สอดรับกับมาตรฐานเว็บ เนื่องจาก React Native รันไทม์ไม่มีฟังก์ชัน URL ดั้งเดิม*

### การตั้งค่าตัวแปรสภาพแวดล้อม (Environment Variables) ใน SDK 54:
เพื่อความปลอดภัย ห้ามนำเอาคีย์ความลับอย่าง Anon Key ไปแปะเขียนโค้ดลงไปตรง ๆ แต่ให้ใช้ไฟล์ **`.env`** ในโฟลเดอร์นอกสุดของโปรเจกต์:
```text
EXPO_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
*หมายเหตุ: ใน Expo SDK 54 ตัวแปรสภาพแวดล้อมที่ขึ้นต้นด้วย `EXPO_PUBLIC_` จะถูกแปลงและโหลดเข้าสู่ระบบรันไทม์จาวาสคริปต์อัตโนมัติ*

### การเขียนไฟล์ตั้งค่าเชื่อมโยง client (`lib/supabase.ts`):
```typescript
import 'react-native-url-polyfill/auto'; // นำเข้าเพื่อแก้บั๊กคำสั่ง URL ในระบบเนทีฟ
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY || '';

// สร้างและส่งออก supabase object ไปใช้งานข้ามไฟล์
export const supabase = createClient(supabaseUrl, supabaseAnonKey);
```

---

## 10.3 การอ่านข้อมูลจากตาราง (Read / Select Data)

การสืบค้นดึงข้อมูลแถวตารางจากฐานข้อมูล Supabase จะทำผ่านเมธอด **`.select()`** โดยสกัดผลลัพธ์ข้อมูลออกมาในคีย์ `data` และตรวจจับปัญหาการอ่านในคีย์ `error`

```tsx
import { supabase } from '../lib/supabase';

interface Task {
  id: number;
  title: string;
  is_completed: boolean;
  created_at: string;
}

const fetchTasks = async (): Promise<Task[]> => {
  const { data, error } = await supabase
    .from('tasks') // อ้างอิงชื่อตารางใน Supabase
    .select('*')   // ดึงฟิลด์ข้อมูลทุกคอลัมน์
    .order('created_at', { ascending: false }); // เรียงลำดับเอาโพสต์ใหม่ขึ้นก่อน

  if (error) {
    console.error('ดึงข้อมูลล้มเหลว:', error.message);
    return [];
  }
  
  return data as Task[];
};
```

### การใส่ตัวกรอง (Query Filters):
เราสามารถคัดกรองข้อมูลเฉพาะแถวที่ต้องการได้ด้วยการต่อเมธอด เช่น:
* `.eq('is_completed', true)`: แสดงเฉพาะโพสต์ที่เสร็จสมบูรณ์แล้ว (Equal)
* `.ilike('title', '%เรียน%')`: ค้นหาชื่อโพสต์ที่มีตัวอักษร "เรียน" ผสมอยู่โดยไม่สนใจตัวพิมพ์เล็กใหญ่

---

## 10.4 การเพิ่มข้อมูลแถวใหม่ (Create / Insert Data)

ในการสร้างแถวข้อมูลชุดใหม่ (เช่น การลงทะเบียนหรือบันทึกสินค้าเพิ่ม) จะส่งผ่านเมธอด **`.insert()`** โดยยอมรับข้อมูลในรูปแบบของอาร์เรย์ออบเจกต์ (Array of Objects)

```tsx
const createNewTask = async (taskTitle: string) => {
  const { data, error } = await supabase
    .from('tasks')
    .insert([
      { 
        title: taskTitle, 
        is_completed: false 
      }
    ])
    .select(); // บอกให้ Supabase ส่งข้อมูลแถวล่าสุดที่สร้างสำเร็จกลับคืนมาด้วย

  if (error) {
    console.error('บันทึกไม่สำเร็จ:', error.message);
    return null;
  }

  return data[0]; // คืนค่าออบเจกต์ข้อมูลชิ้นแรกที่พึ่งบันทึกสำเร็จ
};
```

---

## 10.5 การแก้ไขและปรับปรุงข้อมูล (Update Data)

เมื่อมีการคลิกทำเครื่องหมายติ๊กถูก หรือต้องการเปลี่ยนข้อความแถวข้อมูล เราจะใช้เมธอด **`.update()`** โดยต้องระบุเงื่อนไขเสมอด้วย **`.eq()`** เพื่อป้องกันไม่ให้คำสั่งเข้าไปทับข้อมูลของแถวอื่น ๆ ทั้งตาราง

```tsx
const toggleTaskCompletion = async (taskId: number, currentStatus: boolean) => {
  const { data, error } = await supabase
    .from('tasks')
    .update({ 
      is_completed: !currentStatus 
    }) // ระบุคอลัมน์และค่าใหม่ที่ต้องการแก้ไข
    .eq('id', taskId) // กรองอัปเดตเฉพาะแถวที่มี ID ตรงกัน
    .select();

  if (error) {
    console.error('อัปเดตข้อมูลล้มเหลว:', error.message);
    return null;
  }

  return data[0];
};
```

---

## 10.6 การลบข้อมูลออกจากตาราง (Delete Data)

การสั่งถอดถอนแถวข้อมูลออกจากสารระบบอย่างถาวร จะทำผ่านเมธอด **`.delete()`** โดยต้องผูกตัวกรอง `.eq()` ชี้เฉพาะเจาะจงเป้าหมาย

```tsx
const deleteTask = async (taskId: number): Promise<boolean> => {
  const { error } = await supabase
    .from('tasks')
    .delete()
    .eq('id', taskId); // ลบเฉพาะแถวที่มี ID ตรงกันเท่านั้น

  if (error) {
    console.error('ลบข้อมูลไม่สำเร็จ:', error.message);
    return false;
  }

  return true; // ส่งค่าความสำเร็จกลับไปอัปเดตสถานะลิสต์บนหน้าจอแอป
};
```

---

## 10.7 การจัดการสถานะการทำงานและประมวลผลข้อผิดพลาด (Loading & Error Handling)

จุดแตกต่างของการติดต่อฐานข้อมูลตรงบนคลาวด์เมื่อเทียบกับการเก็บตัวแปรบนเครื่อง คือความเร็วการตอบรับจะแปรผันตามระยะทางและคุณภาพของเครือข่ายอินเทอร์เน็ต ผู้พัฒนาต้องเตรียมกลไกแจ้งสถานะอย่างมีชั้นเชิง:

```tsx
import React, { useState, useEffect } from 'react';
import { View, Text, ActivityIndicator, Alert, Button } from 'react-native';
import { supabase } from '../lib/supabase';

export default function LoadingExample() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const { data, error } = await supabase.from('tasks').select('*');
      
      if (error) {
        throw error; // ดีดเข้าบล็อก catch เพื่อแยกส่วนจัดเตือน
      }
      
      setTasks(data || []);
    } catch (error: any) {
      Alert.alert('เชื่อมโยงฐานข้อมูลขัดข้อง', error.message || 'กรุณาลองใหม่อีกครั้ง');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#38bdf8" />
        <Text style={{ marginTop: 8, color: '#64748b' }}>กำลังเชื่อมต่อฐานข้อมูลระบบคลาวด์...</Text>
      </View>
    );
  }

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold' }}>จำนวนงานคงค้าง: {tasks.length} รายการ</Text>
      <Button title="🔄 ดึงข้อมูลสดใหม่" onPress={loadData} />
    </View>
  );
}
```

## 10.8 สรุปท้ายบทเรียน

**สถาปัตยกรรม BaaS และคลาวด์ดาต้าเบสของ Supabase:** Supabase เป็นระบบหลังบ้านสำเร็จรูปประเภท Backend-as-a-Service (BaaS) ที่ขับเคลื่อนด้วยฐานข้อมูล PostgreSQL ทำให้ประยุกต์จัดความสัมพันธ์ของข้อมูลแบบ SQL แท้ได้อย่างเต็มรูปแบบ โดยผู้พัฒนาสามารถเริ่มใช้งานได้ทันทีและเข้าถึงคีย์ความปลอดภัยอย่าง Project URL และ Anon Key เพื่อเข้าสิทธิ์เชื่อมต่อการทำงานต่าง ๆ

**การติดตั้งและตั้งค่า Supabase Client ใน Expo:** การนำ Supabase เข้าใช้งานในโครงการ Expo SDK 54 ต้องติดตั้งไลบรารี @supabase/supabase-js ร่วมกับ react-native-url-polyfill เพื่อแก้ปัญหาการจัดการโครงสร้างลิงก์ และควรเก็บคีย์ความลับทั้งหมดไว้ในรูปตัวแปรสภาพแวดล้อมที่ขึ้นต้นด้วย EXPO_PUBLIC_ ภายในไฟล์ .env นอกสุดของโปรเจกต์เพื่อยกระดับความปลอดภัยก่อนเปิดใช้งานจริง

**การอ่านข้อมูลจากตาราง (Read / Select Data):** เมธอด .select() ใช้สำหรับการเรียกค้นหาและดึงข้อมูลจากตารางฐานข้อมูล Supabase โดยเราสามารถสืบค้นคอลัมน์ทั้งหมดแบบเจาะจง หรือต่อคำสั่งคัดกรองผลลัพธ์ผ่านตัวกรองเฉพาะ เช่น .eq() สำหรับเทียบข้อมูลค่าเท่า และ .ilike() ในการค้นหาบางส่วนของคำเพื่อส่งผลข้อมูลที่จัดเรียงถูกต้องกลับไปที่แอป

**การเพิ่มข้อมูลแถวใหม่ (Create / Insert Data):** การบันทึกข้อมูลใหม่ลงในตารางใช้เมธอด .insert() โดยยอมรับข้อมูลรูปแาร์เรย์ของออบเจกต์ ซึ่งสามารถอัปเดตฟิลด์ข้อมูลที่ต้องการและเรียกใช้งานคำสั่งพ่วงต่ออย่าง .select() เพื่อร้องขอให้เซิร์ฟเวอร์ส่งข้อมูลบรรทัดที่บันทึกสำเร็จล่าสุดย้อนกลับมาหาตัวแปรบนแอปทันทีเพื่อประมวลผลในขั้นตอนถัดไป

**การแก้ไขและปรับปรุงข้อมูล (Update Data):** กระบวนการแก้ไขค่าของข้อมูลคอลัมน์ในแถวที่เลือกจะสั่งงานผ่านเมธอด .update() โดยข้อควรระวังหลักคือผู้พัฒนาจำเป็นต้องผูกตัวกรองอย่างเช่น .eq('id', taskId) ต่อท้ายเสมอ เพื่อระบุขอบเขตการแก้ไขให้ตรงตามแถวเป้าหมายและจำกัดไม่ให้คำสั่งเข้าไปเขียนทับแถวข้อมูลอื่น ๆ ทั้งตารางข้อมูล

**การลบข้อมูลออกจากตาราง (Delete Data):** การถอดถอนแถวข้อมูลออกจากตารางอย่างมั่นคงถาวรทำได้โดยใช้เมธอด .delete() ซึ่งต้องใช้ร่วมกับตัวกรอง .eq() ในการระบุค่าไอดีเอกลักษณ์เพื่อกำจัดการลบแถวข้อมูลที่ไม่พึงประสงค์ โดยคำสั่งจะคืนค่ารายงานความขัดข้องกลับมาในคีย์ error เพื่อให้เราวิเคราะห์และอัปเดตสถานะลิสต์บนหน้าจอได้อย่างถูกต้อง

**การจัดการสถานะการทำงานและประมวลผลข้อผิดพลาด:** เนื่องจากคุณภาพสัญญาณเน็ตเวิร์กส่งผลให้เวลาในการตอบสนองฐานข้อมูลคลาวด์มีความเร็วแตกต่างกัน การออกแบบระบบจึงจำเป็นต้องครอบคลุมการจัดการสเตต loading เพื่อเปิดปิดไอคอน ActivityIndicator รวมถึงการนำเข้าโครงสร้าง try-catch มาเขียนควบคุมและใช้ response.ok หรือคีย์ error ในการตรวจจับความล้มเหลวของเครือข่ายก่อนสลับการเรนเดอร์อินเตอร์เฟซเตือนผู้ใช้งาน

---

← [ย้อนกลับแผนการสอน: 01-lesson-plan.md](./01-lesson-plan.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ทำแบบทดสอบถัดไป: 03-quiz.md](./03-quiz.md) →
