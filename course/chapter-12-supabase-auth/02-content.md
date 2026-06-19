# บทที่ 12: ระบบยืนยันตัวตนและการเข้าถึงข้อมูลด้วย Supabase Authentication (Content)

การสร้างแอปพลิเคชันที่มีการระบุตัวตน เช่น การรักษาความปลอดภัยสมุดจดบันทึก หรือการจำกัดสิทธิ์ให้เฉพาะเจ้าของบัญชีเข้าถึงข้อมูล จำเป็นต้องใช้ระบบยืนยันตัวตน (Authentication) ในบทเรียนนี้เราจะศึกษาการเชื่อมโยงระบบหลังบ้านของ **Supabase Auth** เข้ากับหน้าจออินเทอร์เฟซในแอปพลิเคชัน React Native Expo SDK 54 ตั้งแต่การจัดการเซสชันผู้ใช้แบบตรงไปตรงมาในจุดเดียว ไปจนถึงการเก็บรักษาความปลอดภัยของโทเค็นด้วยฮาร์ดแวร์เก็บข้อมูลลับ (`expo-secure-store`) และการต่อยอดไปสู่ระบบแชร์สเตตัสระดับสากลด้วย `useContext`

---

## 12.1 แนวคิดระบบยืนยันตัวตนและการจัดการสิทธิ์ (Authentication vs Authorization)

ในการเขียนโปรแกรมระบบความปลอดภัย มีสองแนวคิดที่เราต้องทำความเข้าใจแยกจากกัน:

1. **การยืนยันตัวตน (Authentication - AuthN):** คือกระบวนการพิสูจน์ทราบว่า *"ผู้ใช้งานคือใครจริงหรือไม่"* เช่น การกรอกอีเมลและรหัสผ่าน จากนั้นหลังบ้านจะส่งโทเค็นระบุตัวตนยืนยันกลับมา (เช่น JWT - JSON Web Tokens)
2. **การอนุญาตสิทธิ์ (Authorization - AuthZ):** คือกระบวนการดักกรองว่า *"ผู้ใช้งานที่ยืนยันตนเข้ามาแล้วนั้น มีสิทธิ์ทำอะไรได้บ้าง"* เช่น ผู้ใช้งานทั่วไปเข้าถึงได้เฉพาะตารางของตัวเอง ส่วนผู้ใช้ที่เป็นแอดมินสามารถเข้าดูและลบแถวข้อมูลของทุกคนได้ (ทำงานร่วมกับระบบ RLS ของ PostgreSQL ใน Supabase)

ในการทำระบบล็อกอินบนโทรศัพท์มือถือ อุปกรณ์ไคลเอนต์จะได้รับ Access Token และ Refresh Token จากระบบคลาวด์หลังบ้านมาเก็บรักษาไว้ และต้องส่งแนบโทเค็นนี้ไปกับ API Request ทุกครั้งเพื่อยืนยันตัวตน

---

## 12.2 สถาปัตยกรรมระบบของ Supabase Auth (GoTrue Service)

Supabase มีระบบที่พัฒนาขึ้นจากบริการหลังบ้านแบบ Open Source ชื่อ **GoTrue API** ซึ่งคอยจัดสรรและประมวลผลข้อมูลผู้ใช้อยู่เบื้องหลัง โดยมีฟังก์ชันการยืนยันตัวตนที่หลากหลาย เช่น Email/Password, Magic Link, และ OAuth (เช่น Sign in with Google หรือ Apple)

ในบทเรียนนี้เราจะมุ่งเน้นไปที่การระบุตัวตนที่คลาสสิกและสำคัญที่สุดคือ **Email and Password Authentication** ซึ่งแอปจะคุยตรงกับเซิร์ฟเวอร์ GoTrue ผ่าน Supabase Client SDK

---

## 12.3 การสร้างฟังก์ชันสมัครสมาชิกและเข้าสู่ระบบ (Sign Up & Sign In)

ฟังก์ชันการทำงานพื้นฐานประกอบด้วยการลงทะเบียนบัญชีใหม่ และการล็อกอินเข้าใช้งานผ่านชุดคำสั่ง Asynchronous ต่อไปนี้:

### 1. การสมัครสมาชิกใหม่ (Sign Up)
เมธอด `signUp` จะรับค่าเป็นออบเจกต์ที่มีคีย์ `email` และ `password` เพื่อนำไปจัดสร้างแถวบัญชีใหม่บน Supabase:

```typescript
const handleSignUp = async () => {
  const { data, error } = await supabase.auth.signUp({
    email: 'user@example.com',
    password: 'securepassword123',
  });
  
  if (error) {
    console.error('สมัครสมาชิกขัดข้อง:', error.message);
  } else {
    console.log('สร้างบัญชีสำเร็จแล้ว:', data.user);
  }
};
```

### 2. การลงชื่อเข้าใช้งาน (Sign In)
เมธอด `signInWithPassword` จะระบุค่าอินพุตเพื่อกู้คืนสเตตัสการเชื่อมต่อและดึงสิทธิ์โทเค็นกลับมา:

```typescript
const handleSignIn = async () => {
  const { data, error } = await supabase.auth.signInWithPassword({
    email: 'user@example.com',
    password: 'securepassword123',
  });

  if (error) {
    console.error('ล็อกอินไม่ผ่าน:', error.message);
  } else {
    console.log('ยินดีต้อนรับ เข้าสู่ระบบสำเร็จ:', data.session);
  }
};
```

---

## 12.4 การจัดการเซสชันผู้ใช้และตัวดักจับสถานะ (Session State & onAuthStateChange)

เพื่อให้ตัวแอปพลิเคชันทราบความเคลื่อนไหวตลอดเวลาว่าปัจจุบันผู้ใช้กำลังเชื่อมต่ออยู่ หรือล็อกเอาต์หลุดระบบไปแล้ว เราจะใช้เครื่องมือดักฟังความเคลื่อนไหวเซสชันของ Supabase ที่ชื่อว่า **`onAuthStateChange()`** 

คำสั่งนี้เสมือนเป็นสตรีมข้อมูล (Subscription Stream) ที่จะคอยส่งสัญญาณทริกเกอร์เรียกฟังก์ชัน Callback ทำงานทุกครั้งเมื่อสเตตมีการขยับเปลี่ยน (เช่น `INITIAL_SESSION`, `SIGNED_IN`, `SIGNED_OUT`, `TOKEN_REFRESHED`)

### ตัวอย่างการคุมสเตตแบบง่ายในระดับ Component (Direct State Monitoring):
เราสามารถใช้ `useState` บันทึกค่าเซสชันไว้ในหน้าจอหลัก และใช้ `useEffect` ดักฟังเหตุการณ์เพื่อสลับ UI ในหน้าเดียวได้อย่างง่ายดาย:

```tsx
import React, { useState, useEffect } from 'react';
import { View, Text, ActivityIndicator } from 'react-native';
import { supabase } from '../lib/supabase';

export default function RootScreen() {
  const [session, setSession] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // 1. ดึงเซสชันเริ่มต้นที่อาจค้างอยู่ออกมาดูก่อน
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setIsLoading(false);
    });

    // 2. สมัครรับสัญญาณคอยฟังเมื่อสเตตล็อกอินขยับเปลี่ยน
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    // 3. คืนค่าแรมยกเลิกสมัครสตรีมเมื่อคอมโพเนนต์ถูกถอดถอน
    return () => {
      subscription.unsubscribe();
    };
  }, []);

  if (isLoading) {
    return <ActivityIndicator size="large" />;
  }

  // ทำ Conditional Rendering สลับหน้าแบบตรงไปตรงมา
  return session ? <Dashboard session={session} /> : <LoginForm />;
}
```

---

## 12.5 การรักษาความปลอดภัยระดับอุปกรณ์ด้วย expo-secure-store

ตามค่าเริ่มต้นของ Supabase JS Client ในโปรเจกต์ทั่วไปมักจะเก็บโทเค็นของระบบลงใน `AsyncStorage` ของเครื่องมือถือ แต่มีข้อเสียร้ายแรงด้านความปลอดภัยคือ **AsyncStorage เก็บข้อมูลไว้เป็นเพียงไฟล์ข้อความ Plaintext JSON ธรรมดาบนเครื่อง** ซึ่งไม่มีการเข้ารหัสข้อมูล (Encryption) ทำให้โทรศัพท์ที่ผ่านการ Root หรือ Jailbreak สามารถแอบแกะโทเค็นไปสวมสิทธิ์แทนเจ้าของได้

สำหรับโมบายแอปพลิเคชันยุคใหม่ จึงบังคับให้นำโทเค็นข้อมูลลับเหล่านี้ไปเก็บไว้ในช่องเก็บข้อมูลลับที่มีระบบเข้ารหัสความปลอดภัยระดับฮาร์ดแวร์ (Keychain สำหรับ iOS และ Keystore สำหรับ Android) โดยเราจะใช้ไลบรารี **`expo-secure-store`**

### 1. การติดตั้ง Secure Store:
```bash
npx expo install expo-secure-store
```

### 2. การสร้างคลาสเก็บข้อมูลความปลอดภัยเชื่อมต่อ Supabase Client:
เราสามารถดีไซน์อ็อบเจกต์ทำหน้าที่เป็น Storage Adapter เพื่อบังคับให้โมดูล Auth ของ Supabase เก็บโทเค็นลงใน Secure Store แทน AsyncStorage:

```typescript
import 'react-native-url-polyfill/auto';
import { createClient } from '@supabase/supabase-js';
import * as SecureStore from 'expo-secure-store';

// 1. สร้างคลาสจัดการ Secure Store Adapter
const ExpoSecureStoreAdapter = {
  getItem: (key: string) => {
    return SecureStore.getItemAsync(key);
  },
  setItem: (key: string, value: string) => {
    return SecureStore.setItemAsync(key, value);
  },
  removeItem: (key: string) => {
    return SecureStore.deleteItemAsync(key);
  },
};

const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY || '';

// 2. ประกาศเชื่อมโดยส่ง adapter เข้าไปใน config
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    storage: ExpoSecureStoreAdapter,
    autoRefreshToken: true,   // เปิดระบายโทเค็นใหม่ให้อัตโนมัติเบื้องหลัง
    persistSession: true,       // บังคับจำค่าเซสชันข้ามการเปิดปิดแอป
    detectSessionInUrl: false,
  },
});
```

---

## 12.6 [เนื้อหาพิเศษตอนท้าย (Bonus Section)]: การรีแฟกเตอร์ไปใช้ useContext และ AuthContext

แม้ว่าการจัดเก็บสเตตัสล็อกอินใน Component เดียวจะเข้าใจง่าย แต่หากเราขยายแอปพลิเคชันจนมีหลายหน้าจอ (เช่น หน้าโปรไฟล์, หน้าตั้งค่า, หน้าแก้ไขข้อมูล) ทุกหน้าจอจำเป็นต้องทราบค่า Session ล็อกอินปัจจุบัน ซึ่งการส่ง Prop ต่อกันไปเป็นทอด ๆ (Prop Drilling) จะสร้างความยุ่งยากอย่างมหาศาล

แนวทางปฏิบัติที่ดีที่สุดคือการยกระดับตรรกะมาเก็บไว้ใน **`AuthContext`** เพื่อแชร์ข้อมูล Session ให้กับทุกหน้าจอทั่วแอปพลิเคชัน

### ตัวอย่างการสร้าง `context/AuthContext.tsx`
```tsx
import React, { createContext, useState, useEffect, useContext } from 'react';
import { supabase } from '../lib/supabase';
import { Session, User } from '@supabase/supabase-js';

interface AuthContextType {
  session: Session | null;
  user: User | null;
  isLoading: boolean;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({
  session: null,
  user: null,
  isLoading: true,
  signOut: async () => {}
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [session, setSession] = useState<Session | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // เช็คเซสชันเริ่มต้น
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session ? session.user : null);
      setIsLoading(false);
    });

    // ดักฟังการอัปเดตสเตตัสเซสชัน
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      setUser(session ? session.user : null);
      setIsLoading(false);
    });

    return () => subscription.unsubscribe();
  }, []);

  const signOut = async () => {
    await supabase.auth.signOut();
  };

  return (
    <AuthContext.Provider value={{ session, user, isLoading, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

// สร้าง Custom Hook เพื่อความสะดวกในการดึงข้อมูล
export const useAuth = () => useContext(AuthContext);
```

เมื่อใช้แนวทางนี้ ในไฟล์หน้าจอ Layout หลัก (`app/_layout.tsx`) หรือคอมโพเนนต์อื่น ๆ เราจะเรียกใช้งานเพื่ออ่านและทริกเกอร์ล้างสเตตัสเพียงบรรทัดเดียวได้ทันที:
```tsx
const { user, signOut } = useAuth();
```

---

← [ย้อนกลับแผนการสอน: 01-lesson-plan.md](./01-lesson-plan.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ทำแบบทดสอบถัดไป: 03-quiz.md](./03-quiz.md) →
