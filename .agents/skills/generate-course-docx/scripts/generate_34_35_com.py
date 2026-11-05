import os, re, glob, sys, win32com.client
sys.stdout.reconfigure(encoding='utf-8')

form_dir = r'd:\react-native\expo-sdk54-course-2026\course\ฟอร์ม'
out_dir = r'd:\react-native\expo-sdk54-course-2026\course\docx-v2'
ch_dirs = sorted(glob.glob(r'd:\react-native\expo-sdk54-course-2026\course\chapter-*'))

wdYellow = 7
wdAlignParagraphLeft = 0
wdAlignParagraphCenter = 1
wdAlignParagraphThaiJustify = 9
wdFormatXMLDocument = 16
wdThai = 1054

# Collect all unique references across 13 chapters
refs = set()
for ch_dir in ch_dirs:
    p = os.path.join(ch_dir, '02-content.md')
    with open(p, 'r', encoding='utf-8') as f:
        in_ref = False
        for line in f:
            s = line.strip()
            if s.startswith('## ') and 'แหล่งข้อมูลอ้างอิง' in s:
                in_ref = True
                continue
            if in_ref:
                if s.startswith('---') or s.startswith('←'):
                    break
                if s.startswith('* ') or s.startswith('- '):
                    refs.add(s[2:].strip())

sorted_refs = sorted(refs, key=lambda x: x.lower())

word = win32com.client.Dispatch('Word.Application')
word.Visible = False

def write_formatted_para(doc, text, style_name='Normal', font_size=16, bold=False, align=wdAlignParagraphThaiJustify, first_indent_pt=42.55, left_indent_pt=0, space_before_pt=0, space_after_pt=0, yellow=True):
    p = doc.Paragraphs(doc.Paragraphs.Count)
    p.Style = doc.Styles(style_name)
    p.Alignment = align
    p.LeftIndent = left_indent_pt
    p.FirstLineIndent = first_indent_pt
    p.SpaceBefore = space_before_pt
    p.SpaceAfter = space_after_pt
    p.LineSpacingRule = 0

    rng = p.Range
    rng.End = rng.End - 1

    if not text:
        rng.Text = ''
        rng.Font.Name = 'TH SarabunPSK'
        rng.Font.NameBi = 'TH SarabunPSK'
        rng.Font.Size = font_size
        rng.Font.SizeBi = font_size
        rng.HighlightColorIndex = 0
        doc.Paragraphs.Add()
        return

    pattern = re.compile(r'(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)')
    segments = []
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            segments.append(('plain', text[pos:m.start()]))
        tok = m.group(0)
        if tok.startswith('**') and tok.endswith('**'):
            segments.append(('bold', tok[2:-2]))
        elif tok.startswith('`') and tok.endswith('`'):
            segments.append(('code', tok[1:-1]))
        elif tok.startswith('*') and tok.endswith('*'):
            segments.append(('italic', tok[1:-1]))
        pos = m.end()
    if pos < len(text):
        segments.append(('plain', text[pos:]))

    full_plain = ''.join(s[1] for s in segments)
    rng.Text = full_plain
    rng.Font.Name = 'TH SarabunPSK'
    rng.Font.NameBi = 'TH SarabunPSK'
    rng.Font.Size = font_size
    rng.Font.SizeBi = font_size
    rng.Font.Bold = bold
    rng.Font.BoldBi = bold
    rng.Font.Italic = False
    rng.Font.ItalicBi = False
    rng.HighlightColorIndex = wdYellow if yellow else 0
    rng.LanguageID = wdThai
    rng.LanguageIDOther = wdThai

    p_start = p.Range.Start
    offset = 0
    for stype, stxt in segments:
        slen = len(stxt)
        if stype != 'plain' and slen > 0:
            srng = doc.Range(p_start + offset, p_start + offset + slen)
            if stype == 'bold':
                srng.Font.Bold = True
                srng.Font.BoldBi = True
            elif stype == 'italic':
                srng.Font.Italic = True
                srng.Font.ItalicBi = True
            elif stype == 'code':
                srng.Font.Name = 'Consolas'
                srng.Font.Size = 10.5
        offset += slen

    doc.Paragraphs.Add()

# =========================================================================
# 1. Generate 34-Reference.docx
# =========================================================================
src34 = os.path.join(form_dir, '34-Reference.doc')
dst34 = os.path.join(out_dir, '34-Reference.docx')
doc34 = word.Documents.Open(src34, ReadOnly=True)

# Keep up to P29 (empty line after second 'บรรณานุกรม' on Page 3) and P30 as working paragraph
while doc34.Paragraphs.Count > 30:
    doc34.Paragraphs(doc34.Paragraphs.Count).Range.Delete()

p30_rng = doc34.Paragraphs(30).Range
p30_rng.End = p30_rng.End - 1
p30_rng.Text = ''

for ref_txt in sorted_refs:
    write_formatted_para(doc34, ref_txt, font_size=16, bold=False, align=wdAlignParagraphLeft, first_indent_pt=-36, left_indent_pt=36, space_after_pt=3)

if doc34.Paragraphs.Count > 30 and not doc34.Paragraphs(doc34.Paragraphs.Count).Range.Text.strip():
    doc34.Paragraphs(doc34.Paragraphs.Count).Range.Delete()

doc34.Content.LanguageID = wdThai
doc34.Content.LanguageIDOther = wdThai
doc34.Repaginate()
pages34 = doc34.ComputeStatistics(2)
doc34.SaveAs2(dst34, FileFormat=wdFormatXMLDocument)
doc34.Close(False)
print(f'Generated 34-Reference.docx (Pages={pages34}, Refs={len(sorted_refs)})')

# =========================================================================
# 2. Generate 35-Appendix.docx
# =========================================================================
src35 = os.path.join(form_dir, '35-Appendix.doc')
dst35 = os.path.join(out_dir, '35-Appendix.docx')
doc35 = word.Documents.Open(src35, ReadOnly=True)

# Keep up to P19 (empty line after second 'ภาคผนวก' on Page 3) and P20 as working paragraph
while doc35.Paragraphs.Count > 20:
    doc35.Paragraphs(doc35.Paragraphs.Count).Range.Delete()

p20_rng = doc35.Paragraphs(20).Range
p20_rng.End = p20_rng.End - 1
p20_rng.Text = ''

appendix_items = [
    ('H', 'ภาคผนวก ก: สรุปคำสั่งสำคัญของ Expo CLI และ EAS CLI (Expo SDK 54)'),
    ('P', 'ในการพัฒนาแอปพลิเคชันด้วย React Native และ Expo SDK 54 ผู้เรียนสามารถใช้ชุดคำสั่งมาตรฐานผ่าน Terminal หรือ PowerShell สำหรับการสร้างโปรเจค การรันเซิร์ฟเวอร์นักพัฒนา การติดตั้งไลบรารี และการคอมไพล์แอปพลิเคชันขึ้นระบบคลาวด์ ดังต่อไปนี้'),
    ('B', '1. คำสั่งจัดการโปรเจคและการรันเซิร์ฟเวอร์นักพัฒนา (Expo CLI)'),
    ('L', '• `npx create-expo-app@latest <project-name>` : สร้างโปรเจค React Native Expo SDK 54 ใหม่จากเทมเพลตมาตรฐาน'),
    ('L', '• `npm run reset-project` : ล้างหน้าจอตัวอย่างเริ่มต้นและสร้างโฟลเดอร์ `app/` ใหม่ที่ว่างเปล่าสำหรับเริ่มต้นพัฒนาแอปพลิเคชัน'),
    ('L', '• `npx expo start` : เปิดเซิร์ฟเวอร์ Metro Bundler และแสดง QR Code สำหรับทดสอบผ่านแอปพลิเคชัน Expo Go'),
    ('L', '• `npx expo start --clear` : เปิดเซิร์ฟเวอร์นักพัฒนาพร้อมล้างหน่วยความจำแคช (Metro Cache) กรณีเกิดปัญหาการโหลดโมดูลไม่สมบูรณ์'),
    ('L', '• `npx expo install <package-name>` : ติดตั้งไลบรารีโดยตรวจสอบและเลือกเวอร์ชันที่เข้ากันได้กับ Expo SDK 54 โดยอัตโนมัติ'),
    ('L', '• `npx expo-doctor` : ตรวจสอบสุขภาพของโปรเจค ความเข้ากันได้ของไลบรารี และความถูกต้องของไฟล์ตั้งค่า `app.json`'),
    ('B', '2. คำสั่งคอมไพล์และเผยแพร่แอปพลิเคชัน (EAS CLI)'),
    ('L', '• `npm install -g eas-cli` : ติดตั้งเครื่องมือ EAS CLI แบบ Global ลงในเครื่องคอมพิวเตอร์'),
    ('L', '• `eas login` : เข้าสู่ระบบบัญชีผู้ใช้ Expo เพื่อเชื่อมต่อกับบริการคลาวด์ EAS'),
    ('L', '• `eas build:configure` : สร้างและตั้งค่าไฟล์ `eas.json` สำหรับกำหนดโปรไฟล์การคอมไพล์ (`development`, `preview`, `production`)'),
    ('L', '• `eas build --platform android --profile preview` : สั่งคอมไพล์ไฟล์ติดตั้ง `.apk` สำหรับทดสอบบนอุปกรณ์จริง Android'),
    ('L', '• `eas build --platform all --profile production` : สั่งคอมไพล์ไฟล์สำหรับเผยแพร่จริง (`.aab` สำหรับ Google Play และ `.ipa` สำหรับ App Store)'),
    ('L', '• `eas submit --platform all` : ส่งไฟล์แอปพลิเคชันที่คอมไพล์เสร็จแล้วขึ้นสู่ Google Play Console และ Apple App Store Connect'),
    ('H', 'ภาคผนวก ข: แนวทางการแก้ไขปัญหาที่พบบ่อย (Troubleshooting Guide)'),
    ('P', 'รวบรวมสาเหตุและแนวทางการแก้ไขข้อผิดพลาดที่ผู้เรียนมักพบบ่อยในระหว่างการฝึกปฏิบัติการพัฒนาแอปพลิเคชันมือถือ'),
    ('B', '1. สมาร์ทโฟนสแกน QR Code แล้วไม่สามารถเชื่อมต่อกับ Metro Bundler ได้'),
    ('P', '**สาเหตุ:** เครื่องคอมพิวเตอร์และสมาร์ทโฟนเชื่อมต่อเครือข่าย Wi-Fi คนละวงกัน หรือระบบ Firewall ของคอมพิวเตอร์บล็อกพอร์ต `8081` **วิธีแก้ไข:** ตรวจสอบให้ทั้งสองอุปกรณ์เชื่อมต่อ Wi-Fi วงเดียวกัน หรือรันคำสั่ง `npx expo start --tunnel` เพื่อสร้างการเชื่อมต่อผ่านเครือข่าย Tunnel'),
    ('B', '2. ข้อความแจ้งเตือน "Text strings must be rendered within a <Text> component"'),
    ('P', '**สาเหตุ:** ใน React Native ข้อความทุกชนิดไม่สามารถวางไว้ภายใต้ `<View>` ได้โดยตรงเหมือนภาษา HTML บนเว็บ **วิธีแก้ไข:** ตรวจสอบโค้ด JSX และครอบข้อความหรือตัวแปรที่แสดงผลด้วยคอมโพเนนต์ `<Text>` เสมอ รวมถึงระวังการเว้นช่องว่างหรือคอมเมนต์ที่อยู่นอกแท็ก'),
    ('B', '3. รายการ FlatList ไม่แสดงผลหรือมีความสูงเป็นศูนย์เมื่อวางซ้อนในหน้าจอ'),
    ('P', '**สาเหตุ:** คอนเทนเนอร์แม่ (`<View>` หรือ `<SafeAreaView>`) ไม่ได้กำหนดขนาดความยืดหยุ่นของพื้นที่หน้าจอ **วิธีแก้ไข:** กำหนดสไตล์ `flex: 1` ให้กับคอนเทนเนอร์หลักของหน้าจอเสมอ และหลีกเลี่ยงการนำ `<FlatList>` ไปวางซ้อนภายใน `<ScrollView>` ที่มีทิศทางการเลื่อนแนวเดียวกัน'),
    ('B', '4. การเรียกข้อมูลจาก Supabase คืนค่าว่างเปล่า (Empty Array `[]`) ทั้งที่มีข้อมูลในตาราง'),
    ('P', '**สาเหตุ:** ตารางในฐานข้อมูล PostgreSQL บน Supabase เปิดใช้งาน Row Level Security (RLS) อยู่ แต่ยังไม่ได้สร้างนโยบาย (Policy) อนุญาตให้อ่านข้อมูล **วิธีแก้ไข:** เข้าไปที่เมนู Authentication > Policies บนแดชบอร์ด Supabase แล้วเพิ่ม Policy สำหรับคำสั่ง `SELECT` ให้ตรงกับระดับสิทธิ์ที่ต้องการ'),
]

for kind, txt in appendix_items:
    if kind == 'H':
        write_formatted_para(doc35, '', font_size=16, first_indent_pt=0)
        write_formatted_para(doc35, txt, style_name='Heading 3', font_size=18, bold=True, align=wdAlignParagraphLeft, first_indent_pt=0, space_after_pt=4)
    elif kind == 'B':
        write_formatted_para(doc35, txt, font_size=16, bold=True, align=wdAlignParagraphLeft, first_indent_pt=0, space_before_pt=4, space_after_pt=2)
    elif kind == 'L':
        write_formatted_para(doc35, txt, font_size=16, bold=False, align=wdAlignParagraphLeft, first_indent_pt=28, space_after_pt=2)
    else:
        write_formatted_para(doc35, txt, font_size=16, bold=False, align=wdAlignParagraphThaiJustify, first_indent_pt=42.55, space_after_pt=3)

if doc35.Paragraphs.Count > 20 and not doc35.Paragraphs(doc35.Paragraphs.Count).Range.Text.strip():
    doc35.Paragraphs(doc35.Paragraphs.Count).Range.Delete()

doc35.Content.LanguageID = wdThai
doc35.Content.LanguageIDOther = wdThai
doc35.Repaginate()
pages35 = doc35.ComputeStatistics(2)
doc35.SaveAs2(dst35, FileFormat=wdFormatXMLDocument)
doc35.Close(False)
print(f'Generated 35-Appendix.docx (Pages={pages35})')

word.Quit()
