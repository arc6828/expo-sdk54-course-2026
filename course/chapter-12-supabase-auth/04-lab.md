# ปฏิบัติการ บทที่ 12: การสร้างระบบยืนยันตัวตน Email/Password ด้วย Supabase Auth และ Secure Store (Lab)

ปฏิบัติการนี้จะฝึกทักษะการสร้างระบบสมัครสมาชิก (Sign Up) และระบบเข้าสู่ระบบ (Sign In) ผ่านคลาวด์ **Supabase Auth** บนโทรศัพท์มือถือ โดยผู้เรียนจะได้ออกแบบแอปพลิเคชัน **"สมุดบันทึกรับล็อกสิทธิ์ความปลอดภัยส่วนตัว (Secure Personal Diary)"** ผู้ใช้จะกรอกอีเมลและพาสเวิร์ดที่ผ่านการ Validation ปลายทางเครื่องเพื่อล็อกอินรับโทเค็นความปลอดภัยที่จะถูกเข้ารหัสปกป้องถาวรในฮาร์ดแวร์เก็บข้อมูลลับด้วย `expo-secure-store` และปิดท้ายปฏิบัติการด้วย **แนวเนื้อหาพิเศษ (Bonus Section)** เพื่อทดลองเรียนรู้วิธีการรีแฟกเตอร์แยกส่วนตรรกะไปเป็นระบบจัดเก็บข้อมูลส่วนกลางแบบแชร์ข้ามจอด้วย `useContext`

---

## 1. วัตถุประสงค์การเรียนรู้
1. สามารถติดตั้งและตั้งค่าโปรเจกต์ Expo SDK 54 ให้จัดเก็บโทเค็นของ Supabase Auth ลงในระดับฮาร์ดแวร์ด้วย `expo-secure-store` ได้สำเร็จ
2. สามารถเขียนฟอร์มรับอินพุต พร้อมการกรองตรวจสอบอีเมลและรหัสผ่าน (Form Validation) ได้ถูกต้องตามมาตรฐาน
3. สามารถเรียกใช้ API `signUp` และ `signInWithPassword` ในการจัดการสมัครและยืนยันตนผู้ใช้กับระบบคลาวด์ได้สำเร็จ
4. สามารถใช้งาน `onAuthStateChange` ร่วมกับสเตตภายใน Component เพื่อสลับสลับสิทธิ์หน้าจอระหว่าง Login และ Dashboard (Conditional Rendering) ได้สำเร็จ
5. สามารถทำความเข้าใจและอธิบายสถาปัตยกรรมของการยกระดับระบบความปลอดภัยล็อกอินไปใช้โครงสร้างแชร์สเตตกลางแบบ `useContext`

---

## 2. โจทย์และข้อกำหนดปฏิบัติการ (Requirements)

ผู้เรียนต้องจัดวางโครงสร้างระบบไฟล์ดังต่อไปนี้:

```text
โครงสร้างไฟล์หลักปฏิบัติการ:
├── .env                              => คีย์ความปลอดภัย EXPO_PUBLIC_SUPABASE_URL และ EXPO_PUBLIC_SUPABASE_ANON_KEY
├── lib/
│   └── supabase.ts                   => กำหนดค่า Supabase Client เชื่อมต่อผ่าน Secure Store Adapter
└── app/
    └── index.tsx                     => หน้าควบคุมฟังก์ชัน สมัคร/ล็อกอิน และ Dashboard จัดการข้อมูลสมุดบันทึกส่วนตัว
```

### รายละเอียดเงื่อนไขการทำงาน (Logics):
1. **การยืนยันความถูกต้องฟอร์ม (Form Validation):**
   * ฟิลด์ Password ต้องกำหนดเงื่อนไขบังคับป้อนไม่น้อยกว่า 6 ตัวอักษร
   * ฟิลด์ Email ต้องกรอกอิงตามรูปแบบ Regular Expression ของอีเมลมาตรฐาน หากไม่ผ่านเกณฑ์ ให้ป้ายปุ่มบันทึกเป็นสีเทาและแสดงข้อความแจ้งเตือนสีแดงด้านล่าง
2. **การสมัครสมาชิก (Sign Up Process):**
   * กดทริกเกอร์สร้างผู้ใช้และแสดงผล Alert ยืนยันความสำเร็จ
3. **การเข้าสู่ระบบและคงอยู่ (Sign In & Session Retention):**
   * ทันทีที่ล็อกอินผ่าน ให้นำผู้ใช้สลับหน้าไปที่หน้าจอบันทึกส่วนตัว (Secure Diary Dashboard)
   * เมื่อผู้ใช้ทำการปิดแอปพลิเคชันไป แล้วกดรันเปิดแอปกลับมาใหม่ ระบบต้องทำการดึงสถานะโทเค็นความปลอดภัยที่เก็บสะสมไว้ใน `expo-secure-store` และนำทางผู้ใช้งานตรงเข้ามาที่หน้า Dashboard ทันทีโดยไม่ต้องให้พิมพ์ล็อกอินซ้ำซ้อน
4. **ความประณีตในการรายงาน Error:**
   * ดักจับ Error จาก Supabase API (เช่น กรอกรหัสผิด หรืออีเมลเคยลงทะเบียนไปแล้ว) และแสดงผลเป็นป้ายกล่องแจ้งเตือนความปลอดภัยสีแดงสดที่เข้าใจง่าย

---

## 3. ขั้นตอนการลงมือปฏิบัติ (Step-by-Step Tutorial)

### ขั้นตอนที่ 1: ติดตั้งไลบรารีที่จำเป็น
เปิดใช้งานเทอร์มินัลพิมพ์รันการติดตั้งคำสั่งต่อไปนี้:
```bash
npx expo install expo-secure-store
```

### ขั้นตอนที่ 2: ติดตั้งและเชื่อม Supabase Client ผ่าน Secure Store
สร้างหรือปรับปรุงไฟล์ `lib/supabase.ts` เพื่อเปลี่ยนให้ Supabase Client บันทึกค่าเซสชันลงในหน่วยความจำเข้ารหัสระดับอุปกรณ์เนทีฟ:
```typescript
import 'react-native-url-polyfill/auto';
import { createClient } from '@supabase/supabase-js';
import * as SecureStore from 'expo-secure-store';

// คลาสตัวช่วยจัดการ Secure Store
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

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    storage: ExpoSecureStoreAdapter,
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: false,
  },
});
```

---

## 4. โค้ดเฉลยฉบับสมบูรณ์ (Complete Solution)

รหัสซอร์สโค้ดฉบับสมบูรณ์นี้ทำงานในไฟล์ **`app/index.tsx`** โดยจะจัดการระบบสมัครสมาชิก เข้าระบบ สลับหน้าจอ และบันทึกโทเค็นความปลอดภัยอย่างครบถ้วนจบในไฟล์เดียว:

```tsx
import React, { useState, useEffect } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  TextInput, 
  TouchableOpacity, 
  ActivityIndicator, 
  Alert, 
  SafeAreaView, 
  KeyboardAvoidingView, 
  Platform, 
  Keyboard, 
  TouchableWithoutFeedback 
} from 'react-native';
import { supabase } from '../lib/supabase';

export default function SecureDiaryAuthApp() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  const [session, setSession] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // 1. ตรวจสอบสแกนหาประวัติล็อกอินเดิมที่เก็บไว้ใน Secure Store
  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setIsLoading(false);
    });

    // ดักฟังการอัปเดตสเตตัสล็อกอิน/ล็อกเอาต์
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      setErrorMessage(null); // เคลียร์ข้อความแจ้งเตือนข้อผิดพลาดเก่า
    });

    return () => subscription.unsubscribe();
  }, []);

  // 2. ตรวจสอบความถูกต้องฟอร์ม (Validation Rules)
  const isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  const isPasswordValid = password.length >= 6;
  const isFormReady = isEmailValid && isPasswordValid;

  // 3. ฟังก์ชันลงทะเบียนสมัครสมาชิก (Sign Up)
  const handleSignUp = async () => {
    if (!isFormReady) return;
    try {
      setIsSubmitting(true);
      setErrorMessage(null);
      Keyboard.dismiss();

      const { data, error } = await supabase.auth.signUp({
        email: email.trim(),
        password: password,
      });

      if (error) throw error;

      Alert.alert(
        'สมัครสมาชิกสำเร็จ!',
        'ระบบส่งอีเมลยืนยันตัวตนไปยังที่อยู่ของท่านแล้ว (กรุณาเช็คอินบ็อกซ์หรือโฟลเดอร์สแปม)',
        [{ text: 'ตกลง' }]
      );
      // เคลียร์ฟิลด์รหัสผ่าน
      setPassword('');
    } catch (error: any) {
      setErrorMessage(error.message || 'เกิดข้อผิดพลาดในการลงทะเบียน');
    } finally {
      setIsSubmitting(false);
    }
  };

  // 4. ฟังก์ชันเข้าสู่ระบบ (Sign In)
  const handleSignIn = async () => {
    if (!isFormReady) return;
    try {
      setIsSubmitting(true);
      setErrorMessage(null);
      Keyboard.dismiss();

      const { error } = await supabase.auth.signInWithPassword({
        email: email.trim(),
        password: password,
      });

      if (error) throw error;
      
      // เมื่อล็อกอินผ่าน onAuthStateChange จะดักสลับหน้าจอให้อัตโนมัติ
    } catch (error: any) {
      setErrorMessage(error.message || 'รหัสผ่านหรืออีเมลไม่ถูกต้อง');
    } finally {
      setIsSubmitting(false);
    }
  };

  // 5. ออกจากระบบ (Sign Out)
  const handleSignOut = async () => {
    try {
      setIsLoading(true);
      await supabase.auth.signOut();
    } catch (error) {
      Alert.alert('ข้อผิดพลาด', 'ไม่สามารถลงชื่อออกจากระบบได้');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#38bdf8" />
        <Text style={styles.loadingText}>กำลังตรวจสอบสิทธิ์เข้าระบบ...</Text>
      </View>
    );
  }

  // --- แผงการเรนเดอร์สลับ UI (Conditional Rendering) ---
  if (session) {
    // 1. หน้าจอหลักเมื่อเข้าสู่ระบบได้สำเร็จ (Secure Diary Dashboard)
    return (
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.dashboardContainer}>
          <View style={styles.headerBlock}>
            <Text style={styles.dashboardTitle}>🔒 Secure Diary</Text>
            <Text style={styles.userEmailLabel}>ผู้ใช้: {session.user.email}</Text>
          </View>

          {/* กล่องบันทึกข้อมูลส่วนตัวจำลอง */}
          <View style={styles.diaryContentCard}>
            <Text style={styles.diaryCardHeader}>📝 บันทึกลับสุดยอดประจำวัน</Text>
            <Text style={styles.diaryCardBody}>
              "วันนี้เราได้ศึกษาความแตกต่างระหว่าง Authentication และ Authorization สำเร็จ รวมถึงการเปลี่ยนไปใช้ expo-secure-store แทนคีย์ plain text ข้อมูลทั้งหมดถูกป้องกันอย่างแน่นหนาแล้วบนระบบคลาวด์..."
            </Text>
            <Text style={styles.securityBadge}>🛡️ เข้ารหัสด้วย Keystore/Keychain</Text>
          </View>

          <TouchableOpacity style={styles.signOutBtn} onPress={handleSignOut}>
            <Text style={styles.signOutBtnText}>🚪 ลงชื่อออกจากระบบ</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  // 2. หน้าจอแบบฟอร์มยืนยันตนเมื่อยังไม่มีเซสชัน (Login & Register Interface)
  return (
    <SafeAreaView style={styles.safeArea}>
      <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        <KeyboardAvoidingView 
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'} 
          style={styles.keyboardAvoid}
        >
          <View style={styles.loginContainer}>
            
            {/* หัวข้อล็อกอิน */}
            <View style={styles.loginHeader}>
              <Text style={styles.loginTitle}>🗝️ Private Vault</Text>
              <Text style={styles.loginSubtitle}>กรุณาเข้าสู่ระบบด้วยอีเมลส่วนตัวเพื่อเปิดไดอารี่ลับ</Text>
            </View>

            {/* แผงแสดงข้อผิดพลาด */}
            {errorMessage && (
              <View style={styles.errorAlertBox}>
                <Text style={styles.errorAlertText}>⚠️ {errorMessage}</Text>
              </View>
            )}

            {/* ช่องกรอกข้อมูล */}
            <View style={styles.formCard}>
              <Text style={styles.inputTitle}>อีเมล (Email Address)</Text>
              <TextInput
                style={styles.input}
                placeholder="กรอกอีเมล (เช่น user@email.com)..."
                placeholderTextColor="#64748b"
                value={email}
                onChangeText={setEmail}
                keyboardType="email-address"
                autoCapitalize="none"
              />

              <Text style={styles.inputTitle}>รหัสผ่าน (Password - ขั้นต่ำ 6 ตัวอักษร)</Text>
              <TextInput
                style={styles.input}
                placeholder="กรอกรหัสผ่านปลอดภัย..."
                placeholderTextColor="#64748b"
                value={password}
                onChangeText={setPassword}
                secureTextEntry
                autoCapitalize="none"
              />

              {/* ข้อแนะนำการพิมพ์ฟอร์ม */}
              {!isFormReady && (email.length > 0 || password.length > 0) && (
                <Text style={styles.formWarningText}>
                  * รูปแบบอีเมลต้องถูกต้อง และรหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร
                </Text>
              )}

              {isSubmitting ? (
                <ActivityIndicator size="small" color="#38bdf8" style={styles.spinner} />
              ) : (
                <View style={styles.actionButtonGroup}>
                  <TouchableOpacity 
                    style={[styles.btn, styles.signInBtn, !isFormReady && styles.disabledBtn]} 
                    onPress={handleSignIn}
                    disabled={!isFormReady}
                  >
                    <Text style={styles.btnText}>🔑 เข้าสู่ระบบ</Text>
                  </TouchableOpacity>

                  <TouchableOpacity 
                    style={[styles.btn, styles.signUpBtn, !isFormReady && styles.disabledBtn]} 
                    onPress={handleSignUp}
                    disabled={!isFormReady}
                  >
                    <Text style={styles.signUpBtnText}>📝 สมัครสมาชิก</Text>
                  </TouchableOpacity>
                </View>
              )}
            </View>
          </View>
        </KeyboardAvoidingView>
      </TouchableWithoutFeedback>
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
    backgroundColor: '#0f172a',
  },
  loadingText: {
    color: '#94a3b8',
    marginTop: 12,
    fontSize: 14,
  },
  keyboardAvoid: {
    flex: 1,
  },
  loginContainer: {
    flex: 1,
    padding: 24,
    justifyContent: 'center',
  },
  loginHeader: {
    alignItems: 'center',
    marginBottom: 24,
  },
  loginTitle: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  loginSubtitle: {
    fontSize: 13,
    color: '#94a3b8',
    textAlign: 'center',
    marginTop: 8,
    lineHeight: 18,
  },
  errorAlertBox: {
    backgroundColor: '#ef444422',
    borderWidth: 1,
    borderColor: '#ef4444',
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
  },
  errorAlertText: {
    color: '#f87171',
    fontSize: 12,
    fontWeight: '600',
  },
  formCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    borderWidth: 1,
    borderColor: '#334155',
  },
  inputTitle: {
    color: '#cbd5e1',
    fontSize: 12,
    fontWeight: '600',
    marginBottom: 6,
    marginTop: 10,
  },
  input: {
    backgroundColor: '#0f172a',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#334155',
    color: '#ffffff',
    padding: 12,
    fontSize: 14,
    marginBottom: 10,
  },
  formWarningText: {
    color: '#fbbf24',
    fontSize: 11,
    marginTop: 4,
    marginBottom: 10,
    lineHeight: 16,
  },
  actionButtonGroup: {
    marginTop: 14,
  },
  btn: {
    borderRadius: 8,
    height: 44,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
  },
  signInBtn: {
    backgroundColor: '#38bdf8',
  },
  signUpBtn: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#38bdf8',
  },
  disabledBtn: {
    backgroundColor: '#475569',
    borderColor: '#475569',
    opacity: 0.4,
  },
  btnText: {
    color: '#0f172a',
    fontWeight: 'bold',
    fontSize: 14,
  },
  signUpBtnText: {
    color: '#38bdf8',
    fontWeight: 'bold',
    fontSize: 14,
  },
  spinner: {
    paddingVertical: 12,
  },
  // ส่วนสไตล์หน้าจอ Dashboard
  dashboardContainer: {
    flex: 1,
    padding: 24,
    justifyContent: 'space-between',
  },
  headerBlock: {
    alignItems: 'center',
    marginTop: 20,
  },
  dashboardTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  userEmailLabel: {
    fontSize: 13,
    color: '#10b981',
    marginTop: 6,
    fontWeight: '600',
    backgroundColor: '#065f4633',
    paddingVertical: 4,
    paddingHorizontal: 12,
    borderRadius: 12,
  },
  diaryContentCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    borderWidth: 1,
    borderColor: '#334155',
    marginVertical: 40,
  },
  diaryCardHeader: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 15,
    marginBottom: 10,
  },
  diaryCardBody: {
    color: '#94a3b8',
    fontSize: 13,
    lineHeight: 22,
  },
  securityBadge: {
    color: '#10b981',
    fontSize: 11,
    fontWeight: '600',
    marginTop: 15,
  },
  signOutBtn: {
    backgroundColor: '#ef4444',
    borderRadius: 8,
    height: 46,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
  },
  signOutBtnText: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 14,
  },
});
```

---

## 5. [เนื้อหาของแถมพิเศษ (Bonus Advanced Section)]

หลังจากผู้เรียนพัฒนาโค้ดแบบ Single-page สำเร็จเรียบร้อยแล้ว ในการสเกลหรือขยายแอปพลิเคชันสู่ระบบที่มีหลายหน้าจอในระบบ Expo Router เราจะประยุกต์ใช้แนวทาง **`useContext`** ในการแชร์เซสชันล็อกอินข้ามคอมโพเนนต์

ให้นักพัฒนาจัดสรรสร้างโครงสร้างไฟล์เพิ่มเติมดังนี้:

### ไฟล์ที่ 1: จัดทํา Provider ที่ `context/AuthContext.tsx`
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
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session ? session.user : null);
      setIsLoading(false);
    });

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

export const useAuth = () => useContext(AuthContext);
```

### ไฟล์ที่ 2: ดักจับความปลอดภัยหน้าจอที่ Root Layout `app/_layout.tsx`
นำเอา Provider เข้ามาครอบโครงหน้าของแอปพลิเคชัน เพื่อแบ่งกลุ่มเส้นทางและสกรีนด้วยตัวดัก Route Guard:
```tsx
import React, { useEffect } from 'react';
import { Slot, useRouter, useSegments } from 'expo-router';
import { AuthProvider, useAuth } from '../context/AuthContext';
import { ActivityIndicator, View } from 'react-native';

function InitialLayout() {
  const { session, isLoading } = useAuth();
  const segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    if (isLoading) return;

    // เช็คว่าหน้าจอที่จะเข้าอยู่ในกรอบกลุ่มล็อกอินหรือไม่
    const inAuthGroup = segments[0] === '(auth)';

    if (!session && !inAuthGroup) {
      // หากไม่มีเซสชันและไม่ได้อยู่หน้าล็อกอิน ให้ถีบผู้ใช้ไปหน้าล็อกอิน
      router.replace('/(auth)/login');
    } else if (session && inAuthGroup) {
      // หากมีเซสชันและคาอยู่หน้าล็อกอิน ให้กระโดดข้ามไปหน้าแดชบอร์ดหลัก
      router.replace('/(app)/dashboard');
    }
  }, [session, isLoading, segments]);

  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return <Slot />;
}

export default function RootLayout() {
  return (
    <AuthProvider>
      <InitialLayout />
    </AuthProvider>
  );
}
```

---

← [ย้อนกลับแบบทดสอบ: 03-quiz.md](./03-quiz.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ศึกษาบทเรียนถัดไป: บทที่ 13](../chapter-13-debugging-eas-build/) →
