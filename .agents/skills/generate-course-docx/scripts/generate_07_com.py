import win32com.client
import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

form_dir = r'd:\react-native\expo-sdk54-course-2026\course\ฟอร์ม'
out_dir = r'd:\react-native\expo-sdk54-course-2026\course\docx-v2'
toc_json_path = r'C:\Users\User\.gemini\antigravity\brain\f24fdf29-f7b9-4b36-b7c4-17856ffda31d\scratch\toc_pages.json'

with open(toc_json_path, 'r', encoding='utf-8') as f:
    toc_data = json.load(f)

CHAPTER_TITLES = {
    1: "ความรู้เบื้องต้นเกี่ยวกับ React Native Expo และการเตรียมสภาพแวดล้อม",
    2: "การจัดเลย์เอาต์หน้าจอด้วย Flexbox",
    3: "คอมโพเนนต์พื้นฐานและการจัดการปฏิสัมพันธ์กับผู้ใช้",
    4: "การจัดการสถานะ พร็อพส์ และแบบฟอร์มรับข้อมูล",
    5: "การแสดงผลรายการข้อมูลและประสิทธิภาพการทำงาน",
    6: "ระบบนำทางและสถาปัตยกรรมการเปลี่ยนหน้าจอด้วย Expo Router",
    7: "การตกแต่งอินเทอร์เฟซ ไอคอน และรูปภาพประสิทธิภาพสูง",
    8: "การเก็บข้อมูลในเครื่องและการเชื่อมต่อเครือข่าย API",
    9: "พิกัดตำแหน่ง แผนที่ และเซนเซอร์อุปกรณ์",
    10: "การใช้งานคลาวด์ดาต้าเบสด้วย Supabase",
    11: "การใช้งานกล้อง อัลบั้มภาพ และระบบจัดเก็บไฟล์เนทีฟร่วมกับคลาวด์",
    12: "ระบบยืนยันตัวตนและการเข้าถึงข้อมูลด้วย Supabase Authentication",
    13: "การดีบั๊ก การสร้างแอปพลิเคชัน และการเผยแพร่ด้วย EAS Build",
}

COURSE_DESC = (
    "ศึกษาเทคโนโลยีเพื่อใช้พัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่ทั้งรูปแบบออนไลน์และออฟไลน์ "
    "ภาษาและซอฟต์แวร์ที่นิยมใช้ในปัจจุบัน และประยุกต์ใช้งานในการสร้างและออกแบบแอปพลิเคชัน "
    "การเขียนโปรแกรมเชิงฟังก์ชัน การทำระบบยืนยันตัวตน การอัปโหลดข้อมูล การจัดการข้อมูลบนอุปกรณ์เคลื่อนที่"
    "และเชื่อมต่อกับเซิร์ฟเวอร์ การทำงานเชื่อมต่อระหว่าง แอปพลิเคชันกับสื่อโซเชียลที่นิยมใช้ในปัจจุบัน"
    "ร่วมกับเซิร์ฟเวอร์ที่พัฒนาขึ้น เผยแพร่แอปพลิเคชันบนแพลตฟอร์มที่ได้รับความนิยมในปัจจุบัน"
)

COURSE_OBJECTIVES = [
    "เข้าใจหลักการและกระบวนการพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่อย่างเป็นระบบ",
    "ใช้เทคโนโลยี Expo, Expo Router และ Supabase ในการพัฒนาแอปพลิเคชันได้อย่างมีประสิทธิภาพ",
    "ออกแบบและพัฒนา ส่วนติดต่อผู้ใช้ (UI) และ ประสบการณ์ผู้ใช้ (UX) ที่เหมาะสมกับอุปกรณ์เคลื่อนที่",
    "เขียนโปรแกรมเชิงฟังก์ชันและจัดการข้อมูลระหว่างแอปพลิเคชันกับเซิร์ฟเวอร์หรือฐานข้อมูลได้",
    "สร้างระบบยืนยันตัวตน การอัปโหลดข้อมูล และการเชื่อมต่อกับบริการออนไลน์หรือโซเชียลมีเดียได้",
    "ทดสอบ แก้ไขข้อผิดพลาด และปรับปรุงประสิทธิภาพของแอปพลิเคชันให้เหมาะสมกับผู้ใช้จริง",
    "เผยแพร่และจัดการแอปพลิเคชันบนแพลตฟอร์มที่ได้รับความนิยม เช่น Google Play และ App Store",
    "ปฏิบัติงานอย่างมีจริยธรรม เคารพลิขสิทธิ์ และคำนึงถึงความปลอดภัยของข้อมูลผู้ใช้",
]

TEACHING_METHODS = [
    "การบรรยายและสาธิต (Lecture & Demonstration) อธิบายหลักการทำงานและสาธิตการเขียนโปรแกรมแบบ Step-by-Step",
    "การเรียนรู้แบบลงมือปฏิบัติ (Hands-on Practice / Learning by Doing) ปฏิบัติการเขียนโค้ดจริงผ่านใบงานท้ายบทเรียน",
    "การทำงานกลุ่มและโครงงาน (Group Work & Project-based Learning) พัฒนา Mini-Project ประยุกต์ใช้งานจริง",
    "การนำเสนอและแลกเปลี่ยนความคิดเห็น (Presentation & Peer Review) นำเสนอแนวคิด ผลงาน และอภิปรายร่วมกัน",
    "การเรียนรู้แบบผสมผสาน (Blended Learning) เสริมการเรียนรู้ผ่านระบบคลาวด์ GitHub และ Google Classroom",
]

INSTRUCTIONAL_MEDIA = [
    "เอกสารประกอบการสอนรายวิชา การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่ (รหัสวิชา SCS337)",
    "สไลด์นำเสนอเนื้อหาประจำบทเรียน (Presentation Slides) และคู่มือปฏิบัติการ (Lab Sheets)",
    "ซอฟต์แวร์และเครื่องมือพัฒนา ได้แก่ Node.js, Visual Studio Code, Expo SDK 54, Git และแอปพลิเคชัน Expo Go",
    "ระบบฐานข้อมูลและบริการคลาวด์ Supabase (Database, Authentication และ Storage)",
    "ระบบจัดการเรียนการสอนออนไลน์ (Google Classroom) และคลังโค้ดตัวอย่างบน GitHub Repository",
]

EVAL_ITEMS = {
    "1.1.1": "งานปฏิบัติการและแบบฝึกหัดท้ายบทเรียน 20%",
    "1.1.2": "การสอบกลางภาคเรียน 20%",
    "1.1.3": "รายงานและโครงงานพัฒนาระบบ (Mini-Project) 10%",
    "1.1.4": "การมีส่วนร่วม กิจกรรมในชั้นเรียน และจิตพิสัย 10%",
}

def set_font(rng, size=16, bold=False, highlight=False):
    rng.Font.Name = "TH SarabunPSK"
    rng.Font.NameBi = "TH SarabunPSK"
    rng.Font.NameOther = "TH SarabunPSK"
    rng.Font.Size = size
    rng.Font.SizeBi = size
    rng.Font.Bold = -1 if bold else 0
    rng.Font.BoldBi = -1 if bold else 0
    rng.HighlightColorIndex = 7 if highlight else 0
    rng.LanguageID = 1054

word = win32com.client.Dispatch("Word.Application")
try:
    word.Visible = False
except Exception:
    pass

src_path = os.path.join(form_dir, "07-PlanT.doc")
dst_path = os.path.join(out_dir, "07-PlanT.docx")

doc = word.Documents.Open(src_path, ReadOnly=True)

# Remove all FormFields first by replacing their Range.Text so gray shading disappears
for i in range(doc.FormFields.Count, 0, -1):
    try:
        ff = doc.FormFields(i)
        ff.Range.Text = ff.Result
    except Exception:
        pass

# 1. Replace paragraphs outside tables
for i in range(1, doc.Paragraphs.Count + 1):
    pr = doc.Paragraphs(i)
    if pr.Range.Information(12):  # inside table
        continue
    rng = pr.Range
    rng.End -= 1
    t = rng.Text.strip()
    if t.startswith("รหัสวิชา"):
        rng.Text = "รหัสวิชา SCS337"
        set_font(rng, size=16, bold=True, highlight=False)
        # highlight SCS337
        f_rng = pr.Range
        if f_rng.Find.Execute(FindText="SCS337"):
            f_rng.HighlightColorIndex = 7
    elif t.startswith("รายวิชา"):
        rng.Text = "รายวิชา การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่  3(2-2-5) หน่วยกิต"
        set_font(rng, size=16, bold=True, highlight=False)
        for sub in ["การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่", "3(2-2-5)"]:
            f_rng = pr.Range
            if f_rng.Find.Execute(FindText=sub):
                f_rng.HighlightColorIndex = 7
    elif t == "[ชื่อภาษาอังกฤษ]":
        rng.Text = "Mobile Application Development"
        set_font(rng, size=16, bold=True, highlight=True)
    elif t.startswith("[พิมพ์เนื้อหาที่ตำแหน่งนี้"):
        rng.Text = COURSE_DESC
        set_font(rng, size=16, bold=False, highlight=True)
        pr.Alignment = 9  # wdAlignParagraphThaiJustify
    elif t == "1. [วัตถุประสงค์]":
        rng.Text = f"1. {COURSE_OBJECTIVES[0]}"
        set_font(rng, size=16, bold=False, highlight=False)
        f_rng = pr.Range
        if f_rng.Find.Execute(FindText=COURSE_OBJECTIVES[0]):
            f_rng.HighlightColorIndex = 7
    elif t == "2. [วัตถุประสงค์]":
        lines = [f"{idx}. {obj}" for idx, obj in enumerate(COURSE_OBJECTIVES[1:], start=2)]
        rng.Text = "\r".join(lines)
        set_font(rng, size=16, bold=False, highlight=False)
        for obj in COURSE_OBJECTIVES[1:]:
            f_rng = doc.Range(rng.Start, rng.End)
            if f_rng.Find.Execute(FindText=obj):
                f_rng.HighlightColorIndex = 7

# Now re-iterate bottom paragraphs after objective insertion shifted indices
method_idx = 0
media_idx = 0
for i in range(1, doc.Paragraphs.Count + 1):
    pr = doc.Paragraphs(i)
    if pr.Range.Information(12):
        continue
    rng = pr.Range
    rng.End -= 1
    t = rng.Text.strip()
    if "[วิธีสอนและกิจกรรม]" in t and method_idx < len(TEACHING_METHODS):
        num = method_idx + 1
        val = TEACHING_METHODS[method_idx]
        method_idx += 1
        rng.Text = f"{num}. {val}"
        set_font(rng, size=16, bold=False, highlight=False)
        f_rng = pr.Range
        if f_rng.Find.Execute(FindText=val):
            f_rng.HighlightColorIndex = 7
    elif "[สื่อการเรียนการสอน]" in t and media_idx < len(INSTRUCTIONAL_MEDIA):
        num = media_idx + 1
        val = INSTRUCTIONAL_MEDIA[media_idx]
        media_idx += 1
        rng.Text = f"{num}. {val}"
        set_font(rng, size=16, bold=False, highlight=False)
        f_rng = pr.Range
        if f_rng.Find.Execute(FindText=val):
            f_rng.HighlightColorIndex = 7
    else:
        for k, val in EVAL_ITEMS.items():
            if t.startswith(k):
                rng.Text = f"{k} {val}"
                set_font(rng, size=16, bold=False, highlight=False)
                f_rng = pr.Range
                if f_rng.Find.Execute(FindText=val):
                    f_rng.HighlightColorIndex = 7

# 2. Populate Table 1 with all 13 chapters
desired_rows = [
    ("", "", "", False, False, False)  # R01 blank spacer row
]
for ch in range(1, 14):
    ch_str = str(ch)
    ch_title = CHAPTER_TITLES[ch]
    desired_rows.append((f"บทที่ {ch}", ch_title, "4 ชั่วโมง", True, True, True))
    for sec_title, _ in toc_data["toc"][ch_str]["sections"]:
        desired_rows.append(("", sec_title, "", False, True, False))
    desired_rows.append(("", "สรุป", "", False, False, False))
    desired_rows.append(("", "แบบฝึกหัด", "", False, False, False))
    desired_rows.append(("", "เอกสารอ้างอิง", "", False, False, False))
    if ch < 13:
        desired_rows.append(("", "", "", False, False, False))

tbl = doc.Tables(1)
while tbl.Rows.Count < len(desired_rows):
    tbl.Rows.Add()
while tbl.Rows.Count > len(desired_rows):
    tbl.Rows(tbl.Rows.Count).Delete()

for r_idx, (c1, c2, c3, is_bold, hl_c2, hl_c3) in enumerate(desired_rows, start=1):
    # Col 1
    r1 = tbl.Cell(r_idx, 1).Range
    r1.End -= 1
    r1.Text = c1
    set_font(r1, size=16, bold=is_bold, highlight=(is_bold and int(c1.split()[-1]) > 10 if c1 else False))
    # Col 2
    r2 = tbl.Cell(r_idx, 2).Range
    r2.End -= 1
    r2.Text = c2
    set_font(r2, size=16, bold=is_bold, highlight=hl_c2)
    # Col 3
    r3 = tbl.Cell(r_idx, 3).Range
    r3.End -= 1
    r3.Text = c3
    set_font(r3, size=16, bold=is_bold, highlight=False)
    if hl_c3 and c3:
        f_rng = tbl.Cell(r_idx, 3).Range
        if f_rng.Find.Execute(FindText="4"):
            f_rng.HighlightColorIndex = 7

doc.Repaginate()
pages = doc.ComputeStatistics(2)  # wdStatisticPages = 2
doc.SaveAs2(dst_path, FileFormat=16)
doc.Close(False)
word.Quit()

print(f"Saved 07-PlanT.docx successfully! Total rows={len(desired_rows)}, Pages={pages}")
