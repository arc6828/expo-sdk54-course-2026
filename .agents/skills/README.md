# สรุปรายการ Skills ประจำโปรเจกต์ (Workspace Skills Catalog)

เอกสารนี้รวบรวมรายชื่อ **Skills** ทั้งหมดที่สร้างไว้ในโปรเจกต์ (`d:\react-native\expo-sdk54-course-2026\.agents\skills\`) เพื่อให้สามารถตรวจสอบ เรียกใช้งานซ้ำ หรือคัดลอกไปใช้ในรายวิชา/โปรเจกต์อื่นได้ทันที

---

## 📊 สรุปภาพรวม (Skills Summary)

ปัจจุบันในโปรเจกต์มี Custom Skills ทั้งหมด **2 Skills** (และ Built-in Skills ของระบบอีก 7 รายการ):

| ลำดับ | ชื่อ Skill (`name`) | โฟลเดอร์ที่เก็บ | หน้าที่หลัก |
| :---: | :--- | :--- | :--- |
| **1** | [`generate-course-docx`](./generate-course-docx/SKILL.md) | `.agents/skills/generate-course-docx/` | สร้างและกรอกข้อมูลเอกสารประกอบการสอน `.docx` ทั้ง 35 ไฟล์ (`01`–`35`) จากฟอร์มหาวิทยาลัย (`course/ฟอร์ม/*.doc`), `COURSE_METADATA.md` และไฟล์เนื้อหา Markdown ทั้ง 13 บท ด้วย Word COM |
| **2** | [`export-docx-to-pdf`](./export-docx-to-pdf/SKILL.md) | `.agents/skills/export-docx-to-pdf/` | แปลงไฟล์ `.docx` ใน `course/docx-v2/` ให้เป็นไฟล์ `.pdf` ใน `course/pdf/` (รองรับทั้งแบบคงไฮไลท์สีเหลืองไว้ตรวจทาน และแบบลบไฮไลท์สีเหลืองออกเพื่อส่งพิมพ์จริง) |

---

## 🛠️ รายละเอียดและการเรียกใช้งานแต่ละ Skill

### 1. `generate-course-docx` (สร้างเอกสารประกอบการสอน `.docx`)
- **ไฟล์คำสั่งหลัก:** [`.agents/skills/generate-course-docx/SKILL.md`](./generate-course-docx/SKILL.md)
- **สคริปต์ภายใน (`scripts/`):**
  - [`generate_01_03_com.py`](./generate-course-docx/scripts/generate_01_03_com.py) — สร้างปกนอก (`01`), ปกใน (`02`) และคำนำ (`03`)
  - [`generate_all_plans_com.py`](./generate-course-docx/scripts/generate_all_plans_com.py) — สร้างแผนบริหารการสอนประจำบทที่ 1–13 (`08`, `10`, ..., `32`)
  - [`generate_chapters_com.py`](./generate-course-docx/scripts/generate_chapters_com.py) — สร้างเนื้อหาบทเรียน ทฤษฎี บล็อกโค้ด แบบฝึกหัด ใบงาน Lab และอ้างอิง APA ท้ายบท (`09`, `11`, ..., `33`)
  - [`generate_34_35_com.py`](./generate-course-docx/scripts/generate_34_35_com.py) — สร้างบรรณานุกรมรวม (`34`) และภาคผนวก (`35`)
  - [`extract_exact_pages.py`](./generate-course-docx/scripts/extract_exact_pages.py) — อ่านเลขหน้าจริงของทุกหัวข้อและตารางจาก Word COM เพื่อนำไปทำสารบัญ
  - [`generate_07_com.py`](./generate-course-docx/scripts/generate_07_com.py) — สร้างแผนบริหารการสอนประจำวิชา (`07`)
  - [`generate_04_05_06_com.py`](./generate-course-docx/scripts/generate_04_05_06_com.py) — สร้างสารบัญเนื้อหา (`04`), สารบัญตาราง (`05`) และสารบัญภาพ (`06`) พร้อมเส้นจุดไข่ปลา (Dot Leaders)
- **ตัวอย่างคำสั่งแชทเรียกใช้:**
  - *"ช่วยอัปเดตเอกสาร .docx บทที่ 5 ใน docx-v2 จากไฟล์ Markdown ให้หน่อย"*
  - *"สร้างไฟล์สารบัญ 04-06 ใหม่ตามเลขหน้าล่าสุด"*

---

### 2. `export-docx-to-pdf` (ส่งออกไฟล์ `.docx` เป็น `.pdf`)
- **ไฟล์คำสั่งหลัก:** [`.agents/skills/export-docx-to-pdf/SKILL.md`](./export-docx-to-pdf/SKILL.md)
- **สคริปต์ภายใน (`scripts/`):**
  - [`export_docx_to_pdf.py`](./export-docx-to-pdf/scripts/export_docx_to_pdf.py) — แปลง `.docx` เป็น `.pdf` ผ่าน Word COM (`wdFormatPDF = 17`)
- **ตัวอย่างคำสั่งแชทเรียกใช้:**
  - *"ช่วย Export ไฟล์ใน docx-v2 ทั้งหมดเป็น PDF ให้หน่อย"*
  - *"Export ไฟล์ใน docx-v2 เป็น PDF แบบเอาไฮไลท์สีเหลืองออกทั้งหมด"*
- **ตัวอย่างการรันผ่าน Terminal:**
  ```powershell
  # แปลงทุกไฟล์ (คงไฮไลท์สีเหลืองไว้ตรวจทาน)
  python .agents/skills/export-docx-to-pdf/scripts/export_docx_to_pdf.py

  # แปลงทุกไฟล์แบบลบไฮไลท์สีเหลืองออก (โดยไม่แก้ไฟล์ .docx ต้นฉบับ)
  python .agents/skills/export-docx-to-pdf/scripts/export_docx_to_pdf.py --remove-highlights

  # แปลงเฉพาะไฟล์ที่ระบุ
  python .agents/skills/export-docx-to-pdf/scripts/export_docx_to_pdf.py --files 01-CoverOut.docx 04-Content.docx
  ```

---

## ♻️ วิธีการนำ Skills ไปใช้ซ้ำในโปรเจกต์อื่น (How to Reuse)

1. **ใช้เฉพาะในโปรเจกต์ใหม่ (Workspace Level):**
   - คัดลอกโฟลเดอร์ `.agents/skills/` ทั้งโฟลเดอร์ไปวางที่ Root ของโปรเจกต์รายวิชาใหม่ได้เลย
2. **ติดตั้งให้ใช้ได้ทุกโปรเจกต์ในเครื่อง (Global Level):**
   - คัดลอกโฟลเดอร์ `export-docx-to-pdf` และ `generate-course-docx` ไปวางไว้ที่:
     ```text
     C:\Users\User\.gemini\config\skills\
     ```
   - เมื่อวางไว้ที่ Global แล้ว ไม่ว่าจะเปิดโปรเจกต์วิชาไหนในเครื่องนี้ AI จะมองเห็นและเรียกใช้ทั้ง 2 Skills นี้ได้ทันทีโดยไม่ต้องก๊อปปี้ซ้ำ

