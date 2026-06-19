# ปฏิบัติการ บทที่ 4: การพัฒนาแบบฟอร์มประเมินความพึงพอใจพร้อมระบบแสดงผลเรียลไทม์ (Lab)

ปฏิบัติการนี้จะฝึกฝนทักษะการประยุกต์ใช้สถานะ (State) การเชื่อมโยงคอมโพเนนต์ลูกด้วยหลักการ Lifting State Up และการเขียนระบบฟอร์มลงทะเบียนประเมินคุณภาพสินค้าพร้อมตรวจเช็คเงื่อนไขความถูกต้อง (Form Validation) โดยจำลองหน้าจอ **ระบบประเมินความพึงพอใจของลูกค้า (Customer Feedback & Review Form)**

---

## 1. วัตถุประสงค์การเรียนรู้
1. สามารถใช้งาน `useState` Hook ในการควบคุมการทำงานของแบบฟอร์มที่มีหลายช่องกรอกข้อมูล (Multi-input Form)
2. สามารถเขียนฟังก์ชันตรวจสอบความถูกต้องของข้อมูลแบบเรียลไทม์ (Live Form Validation) และดักจับความยาวข้อความได้
3. สามารถส่งผ่านสเตตอัปเดตย้อนกลับจากชิ้นส่วนคอมโพเนนต์ย่อยแบบปุ่มตัวเลือกผ่านกลไก Lifting State Up
4. สามารถเชื่อมโยงข้อมูลสเตตไปแสดงผลบนการ์ดพรีวิวจำลอง (Live Card Preview) ได้อย่างสม่ำเสมอ
5. สามารถจำกัดการโต้ตอบของปุ่มสัมผัสด้วยพร็อพส์ `disabled` และปรับสไตล์อย่างสอดคล้อง

---

## 2. โจทย์และข้อกำหนดปฏิบัติการ (Requirements)
ผู้เรียนต้องเขียนโค้ดและโครงสร้างแอปประเมินความพึงพอใจลงในโฟลเดอร์ของตนเอง โดยมีองค์ประกอบการทำงานดังนี้:

### รายละเอียดเงื่อนไขและเลย์เอาต์แอป:
1. **ส่วนบน: การ์ดตัวอย่างแสดงผลการรีวิว (Live Review Card Preview)**
   * แสดงข้อความประเภทชื่อผู้รีวิว คะแนนดาวจำลอง (1-5 ดาว) และข้อเสนอแนะความพึงพอใจ
   * ข้อมูลบนการ์ดใบนี้จะเปลี่ยนแปลงสดทันทีเมื่อผู้เรียนพิมพ์ข้อความ หรือเลือกคะแนนดาวในกลุ่มแบบฟอร์ม
2. **ส่วนกลาง: แบบฟอร์มประเมิน (Feedback Form Container)**
   * **กล่องกรอกชื่อผู้รีวิว:** ตัวหนังสือความยาวขั้นต่ำ 2 ตัวอักษร หากไม่ถึงเกณฑ์ให้แสดงกรอบสีส้มแดงเตือน และปิดระบบเดาภาษาอังกฤษอัตโนมัติ
   * **ส่วนเลือกคะแนนประเมิน (Star Rating Selector):** 
     * เป็นคอมโพเนนต์ลูกย่อยชื่อ `components/RatingSelector.tsx`
     * มีปุ่มคะแนน 1 ถึง 5 เรียงกันแนวนอน
     * ปุ่มที่ถูกเลือกจะมีสีพื้นหลังสว่างเข้มกว่าปุ่มอื่น และเมื่อกดเลือกคะแนนใด ๆ จะต้องใช้หลักการ Lifting State Up เพื่อส่งสัญญาณตัวเลขคะแนนกลับไปบันทึกที่ State หลักในคอมโพเนนต์แม่
   * **กล่องคำแนะนำ (Comment Textarea):** รับคำบรรยายความพึงพอใจขั้นต่ำ 10 ตัวอักษร หากไม่ถึงเกณฑ์ให้แสดงข้อความคำแนะนำสีแดงด้านล่าง
3. **ส่วนล่าง: ปุ่มกดส่งข้อมูลประเมิน (Submit & Reset Layout)**
   * **ปุ่มกดส่ง (Submit):** ล็อกไม่ให้คลิกปุ่มสัมผัสทำงานได้หากกรอกข้อมูลชื่อไม่ครบ 2 อักษร ข้อคิดเห็นไม่ถึง 10 อักษร หรือยังไม่ได้เลือกกดคะแนนประเมิน
   * **ปุ่มล้างค่า (Reset):** กดสัมผัสเพื่อคืนสถานะสเตตฟอร์มทั้งหมดกลับเป็นค่าเริ่มต้นเดิม

---

## 3. ขั้นตอนการลงมือปฏิบัติ (Step-by-Step Tutorial)

### ขั้นตอนที่ 1: สร้างชิ้นส่วนเลือกระดับคะแนนด้วยเทคนิค Lifting State Up
สร้างไฟล์คอมโพเนนต์ใหม่ชื่อ `components/RatingSelector.tsx` เพื่อเป็นชุดปุ่มเลือกคะแนน 1-5 โดยให้ลูกส่งค่าตัวเลขที่เลือกลับคืนไปให้แม่ผ่าน Props ฟังก์ชัน:

```tsx
import { View, Text, Pressable, StyleSheet } from 'react-native';

// ข้อกำหนด Props: รับระดับคะแนนปัจจุบัน และฟังก์ชัน Callback ส่งคะแนนใหม่กลับขึ้นไป
interface RatingSelectorProps {
  selectedRating: number;
  onSelectRating: (rating: number) => void;
}

export default function RatingSelector({ selectedRating, onSelectRating }: RatingSelectorProps) {
  const ratings = [1, 2, 3, 4, 5];

  return (
    <View style={styles.container}>
      <Text style={styles.label}>เลือกคะแนนความพึงพอใจ (1 - 5 ดาว)</Text>
      <View style={styles.starRow}>
        {ratings.map((num) => {
          const isSelected = num === selectedRating;
          return (
            <Pressable
              key={num}
              onPress={() => onSelectRating(num)} // ทริกเกอร์ฟังก์ชันส่งค่ากลับขึ้นด้านบน
              style={[
                styles.starButton,
                isSelected ? styles.starSelected : styles.starUnselected
              ]}
            >
              <Text style={[styles.starText, isSelected ? styles.starTextActive : null]}>
                ⭐ {num}
              </Text>
            </Pressable>
          );
        })}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 12,
  },
  label: {
    fontSize: 14,
    color: '#cbd5e1',
    fontWeight: '500',
    marginBottom: 8,
  },
  starRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 8,
  },
  starButton: {
    flex: 1,
    height: 44,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
  },
  starSelected: {
    backgroundColor: '#f59e0b',
    borderColor: '#d97706',
  },
  starUnselected: {
    backgroundColor: '#0f172a',
    borderColor: '#334155',
  },
  starText: {
    color: '#94a3b8',
    fontWeight: 'bold',
    fontSize: 14,
  },
  starTextActive: {
    color: '#ffffff',
  },
});
```

---

### ขั้นตอนที่ 2: ผูกข้อมูล สเตต และการแสดงตัวอย่างการ์ด ในหน้าจอหลัก `app/index.tsx`
เขียนแบบฟอร์มพร้อมเงื่อนไขการตรวจสอบคำเตือน UI ที่เปลี่ยนไปตามสเตตแบบเรียลไทม์:

```tsx
import { useState } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  TextInput, 
  Pressable, 
  SafeAreaView, 
  ScrollView, 
  Alert 
} from 'react-native';
import RatingSelector from '../components/RatingSelector'; // โหลดคอมโพเนนต์เลือกดาว

export default function App() {
  // สเตตเก็บข้อมูลช่องป้อนแบบฟอร์ม
  const [name, setName] = useState<string>('');
  const [rating, setRating] = useState<number>(0);
  const [comment, setComment] = useState<string>('');

  // สเตตเก็บแจ้งเตือนคำเตือน
  const [nameTouched, setNameTouched] = useState<boolean>(false);
  const [commentTouched, setCommentTouched] = useState<boolean>(false);

  // คำนวณความถูกต้องแบบเรียลไทม์
  const isNameInvalid = nameTouched && name.trim().length < 2;
  const isCommentInvalid = commentTouched && comment.trim().length < 10;
  
  // ตรวจสอบว่าปุ่มส่งข้อมูลควรถูกเปิดความต้องการใช้งานหรือไม่
  const isFormValid = name.trim().length >= 2 && comment.trim().length >= 10 && rating > 0;

  const handleSubmit = () => {
    if (isFormValid) {
      Alert.alert(
        'ขอบคุณสำหรับการประเมิน', 
        `ชื่อผู้ประเมิน: ${name}\nคะแนนความพอใจ: ${rating}/5 ดาว\nความคิดเห็น: ${comment}`
      );
    }
  };

  const handleReset = () => {
    setName('');
    setRating(0);
    setComment('');
    setNameTouched(false);
    setCommentTouched(false);
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Text style={styles.headerTitle}>ส่งแบบประเมินบริการ</Text>
        
        {/* 1. Live Card Preview Area */}
        <View style={styles.previewCard}>
          <Text style={styles.previewTitle}>แสดงผลตัวอย่างคำวิจารณ์ (Live Preview)</Text>
          <View style={styles.previewBody}>
            <Text style={styles.previewNameText}>
              👤 {name.trim() !== '' ? name : 'ยังไม่ได้ระบุชื่อผู้ประเมิน'}
            </Text>
            <Text style={styles.previewStarsText}>
              {rating > 0 ? '★'.repeat(rating) + '☆'.repeat(5 - rating) : '☆☆☆☆☆ (กรุณาเลือกคะแนน)'}
            </Text>
            <Text style={styles.previewCommentText}>
              📝 {comment.trim() !== '' ? comment : 'พิมพ์ความคิดเห็นของคุณที่ฟอร์มด้านล่าง...'}
            </Text>
          </View>
        </View>

        {/* 2. Feedback Form Input Control */}
        <View style={styles.formCard}>
          
          {/* ช่องป้อนชื่อผู้รีวิว */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>ชื่อและนามสกุลลูกค้า</Text>
            <TextInput
              style={[styles.input, isNameInvalid ? styles.inputInvalid : null]}
              placeholder="กรอกชื่อของคุณอย่างน้อย 2 ตัวอักษร"
              placeholderTextColor="#64748b"
              value={name}
              onChangeText={(text) => {
                setName(text);
                setNameTouched(true);
              }}
              autoCapitalize="none"
              autoCorrect={false}
            />
            {isNameInvalid && (
              <Text style={styles.errorText}>ข้อบกพร่อง: ชื่อต้องการอักขระอย่างน้อย 2 ตัวขึ้นไป</Text>
            )}
          </View>

          {/* เรียกใช้งาน Custom Selector ผ่าน Props ด้วยกลไก Lifting State Up */}
          <RatingSelector selectedRating={rating} onSelectRating={setRating} />

          {/* ช่องกรอกข้อคิดเห็นประเมินผล */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>รายละเอียดความพึงพอใจการใช้บริการ</Text>
            <TextInput
              style={[styles.input, styles.textArea, isCommentInvalid ? styles.inputInvalid : null]}
              placeholder="บรรยายสิ่งที่คุณอยากแนะนำอย่างน้อย 10 ตัวอักษร..."
              placeholderTextColor="#64748b"
              value={comment}
              onChangeText={(text) => {
                setComment(text);
                setCommentTouched(true);
              }}
              multiline={true}
              numberOfLines={4}
            />
            {isCommentInvalid && (
              <Text style={styles.errorText}>ข้อบกพร่อง: กรุณากรอกรายละเอียดอย่างน้อย 10 ตัวอักษร</Text>
            )}
          </View>

          {/* ปุ่มจัดรายการ Submit และ Reset */}
          <View style={styles.buttonRow}>
            <Pressable
              onPress={handleReset}
              style={({ pressed }) => [
                styles.resetButton,
                pressed ? styles.resetButtonPressed : null
              ]}
            >
              <Text style={styles.resetButtonText}>ล้างฟอร์ม</Text>
            </Pressable>

            <Pressable
              disabled={!isFormValid}
              onPress={handleSubmit}
              style={({ pressed }) => [
                styles.submitButton,
                !isFormValid ? styles.submitButtonDisabled : null,
                pressed && isFormValid ? styles.submitButtonPressed : null
              ]}
            >
              <Text style={styles.submitButtonText}>ส่งข้อมูลรีวิว</Text>
            </Pressable>
          </View>

        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  // รายละเอียด CSS Style จะรวมอยู่ในโครงสร้างเฉลยในส่วนถัดไป
});
```

---

## 4. โค้ดเฉลยฉบับสมบูรณ์ (Complete Solution)

ผู้เรียนสามารถเปิดดูซอร์สโค้ดที่ถูกต้องรวมการสไตล์ชีทครบถ้วน โดยคัดลอกไฟล์ต่อไปนี้ไปทดสอบการทำงานบนตัวเครื่อง:

### 4.1 ซอร์สโค้ดไฟล์ปุ่มคะแนน: `components/RatingSelector.tsx`
```tsx
import { View, Text, Pressable, StyleSheet } from 'react-native';

interface RatingSelectorProps {
  selectedRating: number;
  onSelectRating: (rating: number) => void;
}

export default function RatingSelector({ selectedRating, onSelectRating }: RatingSelectorProps) {
  const ratings = [1, 2, 3, 4, 5];

  return (
    <View style={styles.container}>
      <Text style={styles.label}>เลือกคะแนนความพึงพอใจ (1 - 5 ดาว)</Text>
      <View style={styles.starRow}>
        {ratings.map((num) => {
          const isSelected = num === selectedRating;
          return (
            <Pressable
              key={num}
              onPress={() => onSelectRating(num)}
              style={[
                styles.starButton,
                isSelected ? styles.starSelected : styles.starUnselected
              ]}
            >
              <Text style={[styles.starText, isSelected ? styles.starTextActive : null]}>
                ⭐ {num}
              </Text>
            </Pressable>
          );
        })}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 12,
  },
  label: {
    fontSize: 14,
    color: '#cbd5e1',
    fontWeight: '500',
    marginBottom: 8,
  },
  starRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 8,
  },
  starButton: {
    flex: 1,
    height: 44,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
  },
  starSelected: {
    backgroundColor: '#f59e0b',
    borderColor: '#d97706',
  },
  starUnselected: {
    backgroundColor: '#0f172a',
    borderColor: '#334155',
  },
  starText: {
    color: '#94a3b8',
    fontWeight: 'bold',
    fontSize: 14,
  },
  starTextActive: {
    color: '#ffffff',
  },
});
```

### 4.2 ซอร์สโค้ดหน้าหลักฟอร์มโต้ตอบ: `app/index.tsx`
```tsx
import { useState } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  TextInput, 
  Pressable, 
  SafeAreaView, 
  ScrollView, 
  Alert 
} from 'react-native';
import RatingSelector from '../components/RatingSelector';

export default function App() {
  const [name, setName] = useState<string>('');
  const [rating, setRating] = useState<number>(0);
  const [comment, setComment] = useState<string>('');

  const [nameTouched, setNameTouched] = useState<boolean>(false);
  const [commentTouched, setCommentTouched] = useState<boolean>(false);

  const isNameInvalid = nameTouched && name.trim().length < 2;
  const isCommentInvalid = commentTouched && comment.trim().length < 10;
  
  const isFormValid = name.trim().length >= 2 && comment.trim().length >= 10 && rating > 0;

  const handleSubmit = () => {
    if (isFormValid) {
      Alert.alert(
        'ส่งข้อมูลรีวิวสำเร็จ', 
        `ขอบคุณสำหรับข้อแนะนำที่มีค่า!\n\nผู้รีวิว: ${name}\nคะแนน: ${rating}/5 ดาว\nเนื้อหา: ${comment}`
      );
      handleReset();
    }
  };

  const handleReset = () => {
    setName('');
    setRating(0);
    setComment('');
    setNameTouched(false);
    setCommentTouched(false);
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Text style={styles.headerTitle}>แบบประเมินการให้บริการ</Text>
        
        {/* 1. Live Preview Card */}
        <View style={styles.previewCard}>
          <Text style={styles.previewTitle}>ตัวอย่างรีวิวสด (Live Preview)</Text>
          <View style={styles.previewBody}>
            <Text style={styles.previewNameText}>
              👤 {name.trim() !== '' ? name : 'ยังไม่ได้ป้อนชื่อของคุณ'}
            </Text>
            <Text style={styles.previewStarsText}>
              {rating > 0 
                ? '★'.repeat(rating) + '☆'.repeat(5 - rating) 
                : '☆☆☆☆☆ (กรุณาเลือกคะแนนให้คะแนนดาว)'}
            </Text>
            <Text style={styles.previewCommentText}>
              📝 {comment.trim() !== '' ? comment : 'รายละเอียดความคิดเห็นของคุณจะปรากฏที่นี่...'}
            </Text>
          </View>
        </View>

        {/* 2. Interaction Inputs Form */}
        <View style={styles.formCard}>
          
          <View style={styles.inputGroup}>
            <Text style={styles.label}>ชื่อ-นามสกุลผู้รีวิว</Text>
            <TextInput
              style={[styles.input, isNameInvalid ? styles.inputInvalid : null]}
              placeholder="กรอกชื่อ-สกุลจริงของคุณ"
              placeholderTextColor="#64748b"
              value={name}
              onChangeText={(text) => {
                setName(text);
                setNameTouched(true);
              }}
              autoCapitalize="none"
              autoCorrect={false}
            />
            {isNameInvalid && (
              <Text style={styles.errorText}>* กรุณากรอกชื่อจริงอย่างน้อย 2 ตัวอักษร</Text>
            )}
          </View>

          <RatingSelector selectedRating={rating} onSelectRating={setRating} />

          <View style={styles.inputGroup}>
            <Text style={styles.label}>ข้อแนะนำและระดับข้อเสนอแนะ</Text>
            <TextInput
              style={[styles.input, styles.textArea, isCommentInvalid ? styles.inputInvalid : null]}
              placeholder="บอกเหตุผลหรือสิ่งที่ระบบควรปรับปรุง (อย่างน้อย 10 ตัวอักษร)..."
              placeholderTextColor="#64748b"
              value={comment}
              onChangeText={(text) => {
                setComment(text);
                setCommentTouched(true);
              }}
              multiline={true}
              numberOfLines={4}
            />
            {isCommentInvalid && (
              <Text style={styles.errorText}>* ข้อความยาวไม่เพียงพอ (ต้องการขั้นต่ำ 10 อักษร)</Text>
            )}
          </View>

          <View style={styles.buttonRow}>
            <Pressable
              onPress={handleReset}
              style={({ pressed }) => [
                styles.resetButton,
                pressed ? styles.resetButtonPressed : null
              ]}
            >
              <Text style={styles.resetButtonText}>ล้างแบบฟอร์ม</Text>
            </Pressable>

            <Pressable
              disabled={!isFormValid}
              onPress={handleSubmit}
              style={({ pressed }) => [
                styles.submitButton,
                !isFormValid ? styles.submitButtonDisabled : null,
                pressed && isFormValid ? styles.submitButtonPressed : null
              ]}
            >
              <Text style={styles.submitButtonText}>บันทึกความคิดเห็น</Text>
            </Pressable>
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
  scrollContainer: {
    padding: 20,
    paddingBottom: 40,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: 16,
  },
  previewCard: {
    backgroundColor: '#1e293b',
    borderColor: '#334155',
    borderWidth: 1,
    borderRadius: 16,
    padding: 16,
    marginBottom: 20,
  },
  previewTitle: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#38bdf8',
    textTransform: 'uppercase',
    marginBottom: 10,
    letterSpacing: 0.5,
  },
  previewBody: {
    backgroundColor: '#0f172a',
    padding: 14,
    borderRadius: 8,
    gap: 8,
  },
  previewNameText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  previewStarsText: {
    color: '#fbbf24',
    fontSize: 18,
    letterSpacing: 2,
  },
  previewCommentText: {
    color: '#cbd5e1',
    fontSize: 14,
    fontStyle: 'italic',
    lineHeight: 20,
  },
  formCard: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    borderColor: '#334155',
    borderWidth: 1,
  },
  inputGroup: {
    marginBottom: 12,
  },
  label: {
    fontSize: 14,
    color: '#cbd5e1',
    fontWeight: '500',
    marginBottom: 6,
  },
  input: {
    backgroundColor: '#0f172a',
    borderWidth: 1,
    borderColor: '#334155',
    borderRadius: 8,
    height: 46,
    paddingHorizontal: 12,
    color: '#ffffff',
    fontSize: 14,
  },
  inputInvalid: {
    borderColor: '#f43f5e',
  },
  textArea: {
    height: 90,
    paddingTop: 10,
    textAlignVertical: 'top',
  },
  errorText: {
    color: '#f43f5e',
    fontSize: 12,
    marginTop: 4,
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 16,
    gap: 12,
  },
  resetButton: {
    flex: 1,
    height: 48,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#334155',
    backgroundColor: '#1e293b',
    justifyContent: 'center',
    alignItems: 'center',
  },
  resetButtonPressed: {
    backgroundColor: '#334155',
  },
  resetButtonText: {
    color: '#cbd5e1',
    fontSize: 15,
    fontWeight: 'bold',
  },
  submitButton: {
    flex: 2,
    height: 48,
    borderRadius: 8,
    backgroundColor: '#3b82f6',
    justifyContent: 'center',
    alignItems: 'center',
  },
  submitButtonDisabled: {
    backgroundColor: '#1e293b',
    borderColor: '#334155',
    borderWidth: 1,
    opacity: 0.4,
  },
  submitButtonPressed: {
    backgroundColor: '#2563eb',
  },
  submitButtonText: {
    color: '#ffffff',
    fontSize: 15,
    fontWeight: 'bold',
  },
});
```

---

← [ย้อนกลับแบบทดสอบ: 03-quiz.md](./03-quiz.md) | [กลับหน้าสารบัญหลัก (Course Index)](../README.md) | [ศึกษาบทเรียนถัดไป: บทที่ 5](../chapter-05-lists-flatlist/) →
