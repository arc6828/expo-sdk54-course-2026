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

# Calculate cumulative page numbers across the book
cur_page = 1
chap_plan_start = {}
chap_body_start = {}

for ch in range(1, 14):
    ch_info = toc_data["toc"][str(ch)]
    chap_plan_start[ch] = cur_page
    cur_page += ch_info["plan_pages"]
    chap_body_start[ch] = cur_page
    cur_page += ch_info["chap_pages"]

bib_start_page = cur_page
cur_page += 5  # 34-Reference.docx is 5 pages
appendix_start_page = cur_page

FIGURES_LIST = [
    ("1.1", "โครงสร้างโปรเจค React Native Expo SDK 54 และระบบไฟล์หลัก", 1, 4),
    ("2.1", "แผนผังแกนหลัก (Main Axis) และแกนตัด (Cross Axis) ใน Flexbox", 2, 2),
    ("3.1", "โครงสร้างลำดับชั้นของคอมโพเนนต์พื้นฐานและการส่งผ่าน Props", 3, 7),
    ("4.1", "แผนผังการไหลของข้อมูลแบบทิศทางเดียวและการทำ Lifting State Up", 4, 3),
    ("5.1", "กลไกการทำ Virtualization และ Windowing ของคอมโพเนนต์ FlatList", 5, 2),
    ("6.1", "โครงสร้างไดเรกทอรี app/ และการจับคู่เส้นทางของ Expo Router", 6, 1),
    ("7.1", "การจัดวางเลเยอร์แบบสัมบูรณ์ (Absolute Positioning) และการสลับธีม", 7, 1),
    ("8.1", "วงจรการดึงข้อมูล REST API ร่วมกับการแคชด้วย AsyncStorage", 8, 3),
    ("9.1", "สถาปัตยกรรมการขอสิทธิ์เข้าถึงพิกัดตำแหน่งและเซนเซอร์อุปกรณ์", 9, 1),
    ("10.1", "สถาปัตยกรรม Backend-as-a-Service (BaaS) ของระบบฐานข้อมูล Supabase", 10, 1),
    ("11.1", "แผนผังระบบจัดเก็บไฟล์ 3 รูปแบบ (Sandbox, Shared Media และ Cloud Storage)", 11, 5),
    ("12.1", "กระบวนการยืนยันตัวตนด้วย JWT Token และการจัดเก็บผ่าน SecureStore", 12, 1),
    ("13.1", "กระบวนการบิลด์และเผยแพร่แอปพลิเคชันบนคลาวด์ด้วย EAS Build", 13, 2),
]

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

def fill_toc_row(tbl, r_idx, prefix_plain, highlight_part, page_str, hl_page=True, indent_pt=0):
    c1 = tbl.Cell(r_idx, 1).Range
    c1.End -= 1
    full_txt = f"{prefix_plain}{highlight_part}\t"
    c1.Text = full_txt
    set_font(c1, size=16, bold=False, highlight=False)
    p1 = c1.Paragraphs(1)
    p1.LeftIndent = 0
    p1.FirstLineIndent = indent_pt
    p1.Alignment = 0  # Left
    p1.TabStops.ClearAll()
    p1.TabStops.Add(Position=380, Alignment=2, Leader=1)  # right tab with dot leader

    if highlight_part:
        f_rng = tbl.Cell(r_idx, 1).Range
        if f_rng.Find.Execute(FindText=highlight_part):
            f_rng.HighlightColorIndex = 7

    c2 = tbl.Cell(r_idx, 2).Range
    c2.End -= 1
    c2.Text = str(page_str)
    set_font(c2, size=16, bold=False, highlight=hl_page)
    c2.Paragraphs(1).Alignment = 2  # Right

def build_chapter_toc_items(ch_list):
    items = []
    for ch in ch_list:
        ch_info = toc_data["toc"][str(ch)]
        plan_pg = chap_plan_start[ch]
        body_pg = chap_body_start[ch]
        # Plan row (if ch > 10, highlight chapter number too)
        if ch <= 10:
            items.append((f"แผนบริหารการสอนประจำบทที่ {ch}", "", str(plan_pg), True, 0))
        else:
            items.append(("แผนบริหารการสอนประจำบทที่ ", f"{ch}", str(plan_pg), True, 0))
        # Chapter title row
        items.append((f"บทที่ {ch} ", CHAPTER_TITLES[ch], str(body_pg), True, 0))
        # Section rows
        for sec_title, rel_pg in ch_info["sections"]:
            sec_pg = body_pg + rel_pg - 1
            items.append(("", sec_title, str(sec_pg), True, 24))
        # Summary, Quiz, Ref
        sum_pg = body_pg + ch_info["summary_page"] - 1
        qz_pg = body_pg + ch_info["quiz_page"] - 1
        rf_pg = body_pg + ch_info["ref_page"] - 1
        items.append(("สรุป", "", str(sum_pg), True, 24))
        items.append(("แบบฝึกหัด", "", str(qz_pg), True, 24))
        items.append(("เอกสารอ้างอิง", "", str(rf_pg), True, 24))
    return items

word = win32com.client.Dispatch("Word.Application")
try:
    word.Visible = False
except Exception:
    pass

# ==========================================
# 1. Generate 04-Content.docx
# ==========================================
doc04 = word.Documents.Open(os.path.join(form_dir, "04-Content.doc"), ReadOnly=True)
for i in range(doc04.FormFields.Count, 0, -1):
    try:
        ff = doc04.FormFields(i)
        ff.Range.Text = ff.Result
    except Exception:
        pass

t1_items = [
    ("คำนำ", "", "(1)", False, 0),
    ("สารบัญ", "", "(3)", False, 0),
    ("สารบัญตาราง", "", "(8)", True, 0),
    ("สารบัญภาพ", "", "(9)", True, 0),
    ("แผนบริหารการสอนประจำวิชา", "", "(11)", True, 0),
] + build_chapter_toc_items([1, 2, 3])

t2_items = build_chapter_toc_items([4, 5, 6])

t3_items = build_chapter_toc_items([7, 8, 9, 10, 11, 12, 13]) + [
    ("บรรณานุกรม", "", str(bib_start_page), True, 0),
    ("ภาคผนวก", "", str(appendix_start_page), True, 0),
]

for t_idx, items in enumerate([t1_items, t2_items, t3_items], start=1):
    tbl = doc04.Tables(t_idx)
    while tbl.Rows.Count < len(items):
        tbl.Rows.Add()
    while tbl.Rows.Count > len(items):
        tbl.Rows(tbl.Rows.Count).Delete()
    for r_idx, (pre, hl_txt, pg, hl_pg, ind) in enumerate(items, start=1):
        fill_toc_row(tbl, r_idx, pre, hl_txt, pg, hl_page=hl_pg, indent_pt=ind)

doc04.Repaginate()
p04_pages = doc04.ComputeStatistics(2)
doc04.SaveAs2(os.path.join(out_dir, "04-Content.docx"), FileFormat=16)
doc04.Close(False)
print(f"Saved 04-Content.docx! Pages={p04_pages}")

# ==========================================
# 2. Generate 05-Table.docx
# ==========================================
doc05 = word.Documents.Open(os.path.join(form_dir, "05-Table.doc"), ReadOnly=True)
for i in range(doc05.FormFields.Count, 0, -1):
    try:
        ff = doc05.FormFields(i)
        ff.Range.Text = ff.Result
    except Exception:
        pass

# Delete Table 2 and the trailing "สารบัญตาราง (ต่อ)" paragraphs since 5 tables fit on 1 page
if doc05.Tables.Count > 1:
    doc05.Tables(2).Delete()
for i in range(doc05.Paragraphs.Count, 0, -1):
    pr = doc05.Paragraphs(i)
    if not pr.Range.Information(12):
        txt = pr.Range.Text.strip()
        if "สารบัญตาราง (ต่อ)" in txt or (i > 10 and "ตารางที่" in txt):
            pr.Range.Delete()
        elif not txt and i > 6:
            pr.Range.Delete()

tbl05 = doc05.Tables(1)
tables_list = toc_data["tables"]
while tbl05.Rows.Count > len(tables_list):
    tbl05.Rows(tbl05.Rows.Count).Delete()
while tbl05.Rows.Count < len(tables_list):
    tbl05.Rows.Add()

for r_idx, t_item in enumerate(tables_list, start=1):
    t_num = t_item["num"]
    t_title = t_item["title"]
    t_pg = chap_body_start[t_item["ch_num"]] + t_item["rel_page"] - 1

    c1 = tbl05.Cell(r_idx, 1).Range
    c1.End -= 1
    c1.Text = t_num
    set_font(c1, size=16, bold=False, highlight=True)
    c1.Paragraphs(1).Alignment = 1  # Center

    c2 = tbl05.Cell(r_idx, 2).Range
    c2.End -= 1
    c2.Text = f"{t_title}\t"
    set_font(c2, size=16, bold=False, highlight=False)
    p2 = c2.Paragraphs(1)
    p2.Alignment = 0
    p2.TabStops.ClearAll()
    p2.TabStops.Add(Position=335, Alignment=2, Leader=1)
    f_rng = tbl05.Cell(r_idx, 2).Range
    if f_rng.Find.Execute(FindText=t_title):
        f_rng.HighlightColorIndex = 7

    c3 = tbl05.Cell(r_idx, 3).Range
    c3.End -= 1
    c3.Text = str(t_pg)
    set_font(c3, size=16, bold=False, highlight=True)
    c3.Paragraphs(1).Alignment = 2  # Right

doc05.Repaginate()
p05_pages = doc05.ComputeStatistics(2)
doc05.SaveAs2(os.path.join(out_dir, "05-Table.docx"), FileFormat=16)
doc05.Close(False)
print(f"Saved 05-Table.docx! Pages={p05_pages}")

# ==========================================
# 3. Generate 06-Figure.docx
# ==========================================
doc06 = word.Documents.Open(os.path.join(form_dir, "06-Figure.doc"), ReadOnly=True)
for i in range(doc06.FormFields.Count, 0, -1):
    try:
        ff = doc06.FormFields(i)
        ff.Range.Text = ff.Result
    except Exception:
        pass

if doc06.Tables.Count > 1:
    doc06.Tables(2).Delete()
for i in range(doc06.Paragraphs.Count, 0, -1):
    pr = doc06.Paragraphs(i)
    if not pr.Range.Information(12):
        txt = pr.Range.Text.strip()
        if "สารบัญภาพ (ต่อ)" in txt or (i > 10 and "ภาพที่" in txt):
            pr.Range.Delete()
        elif not txt and i > 6:
            pr.Range.Delete()

tbl06 = doc06.Tables(1)
while tbl06.Rows.Count > len(FIGURES_LIST):
    tbl06.Rows(tbl06.Rows.Count).Delete()
while tbl06.Rows.Count < len(FIGURES_LIST):
    tbl06.Rows.Add()

for r_idx, (f_num, f_title, ch_num, rel_pg) in enumerate(FIGURES_LIST, start=1):
    f_pg = chap_body_start[ch_num] + rel_pg - 1

    c1 = tbl06.Cell(r_idx, 1).Range
    c1.End -= 1
    c1.Text = f_num
    set_font(c1, size=16, bold=False, highlight=True)
    c1.Paragraphs(1).Alignment = 1  # Center

    c2 = tbl06.Cell(r_idx, 2).Range
    c2.End -= 1
    c2.Text = f"{f_title}\t"
    set_font(c2, size=16, bold=False, highlight=False)
    p2 = c2.Paragraphs(1)
    p2.Alignment = 0
    p2.TabStops.ClearAll()
    p2.TabStops.Add(Position=335, Alignment=2, Leader=1)
    f_rng = tbl06.Cell(r_idx, 2).Range
    if f_rng.Find.Execute(FindText=f_title):
        f_rng.HighlightColorIndex = 7

    c3 = tbl06.Cell(r_idx, 3).Range
    c3.End -= 1
    c3.Text = str(f_pg)
    set_font(c3, size=16, bold=False, highlight=True)
    c3.Paragraphs(1).Alignment = 2  # Right

doc06.Repaginate()
p06_pages = doc06.ComputeStatistics(2)
doc06.SaveAs2(os.path.join(out_dir, "06-Figure.docx"), FileFormat=16)
doc06.Close(False)
print(f"Saved 06-Figure.docx! Pages={p06_pages}")

word.Quit()
