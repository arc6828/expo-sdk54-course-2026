import os, re, glob, json, sys, win32com.client
sys.stdout.reconfigure(encoding='utf-8')

form_dir = r'd:\react-native\expo-sdk54-course-2026\course\ฟอร์ม'
out_dir = r'd:\react-native\expo-sdk54-course-2026\course\docx-v2'
ch_dirs = sorted(glob.glob(r'd:\react-native\expo-sdk54-course-2026\course\chapter-*'))

roman_map = {
    1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII',
    8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII', 13: 'XIII'
}

chapter_titles = {
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

table_captions = {
    1: "การเปรียบเทียบแนวทางการพัฒนาแอปพลิเคชันด้วย React Native และ Expo",
    2: "ค่าคงที่และทิศทางการจัดวางของ flexDirection",
    3: "การเปรียบเทียบคุณสมบัติระหว่าง View และ ScrollView",
    4: "การเปรียบเทียบคุณลักษณะระหว่าง State และ Props",
    11: "สรุปเปรียบเทียบระบบจัดเก็บไฟล์ทั้ง 3 รูปแบบ",
}

wdYellow = 7
wdAlignParagraphLeft = 0
wdAlignParagraphCenter = 1
wdAlignParagraphThaiJustify = 9
wdFormatXMLDocument = 16
wdThai = 1054

def generate_chapter_docx(word, ch_num):
    ch_dir = ch_dirs[ch_num - 1]
    file_num = 7 + ch_num * 2
    roman = roman_map[ch_num]
    src_name = f'{file_num:02d}-Chater-{roman}.doc'
    dst_name = f'{file_num:02d}-Chater-{roman}.docx'
    src_path = os.path.join(form_dir, src_name)
    dst_path = os.path.join(out_dir, dst_name)

    doc = word.Documents.Open(src_path, ReadOnly=True)

    # Keep Paragraph 1 ('บทที่  X') and Paragraph 2 (working paragraph)
    while doc.Paragraphs.Count > 2:
        doc.Paragraphs(doc.Paragraphs.Count).Range.Delete()

    p1_rng = doc.Paragraphs(1).Range
    p1_rng.End = p1_rng.End - 1
    p1_rng.Text = f'บทที่  {ch_num}'

    p2_rng = doc.Paragraphs(2).Range
    p2_rng.End = p2_rng.End - 1
    p2_rng.Text = ''

    def write_para(text, style_name='Normal', font_size=16, bold=False, align=wdAlignParagraphThaiJustify, first_indent_pt=42.55, left_indent_pt=0, space_before_pt=0, space_after_pt=0, yellow=True):
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

        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

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
                    srng.Font.Size = 10.5 if font_size == 16 else font_size - 4
            offset += slen

        doc.Paragraphs.Add()

    def write_code_box(code_lines):
        p = doc.Paragraphs(doc.Paragraphs.Count)
        p.Style = doc.Styles('Normal')
        p.Alignment = wdAlignParagraphLeft
        p.FirstLineIndent = 0
        p.LeftIndent = 20
        p.SpaceBefore = 4
        p.SpaceAfter = 4
        rng = p.Range
        rng.End = rng.End - 1
        tbl = doc.Tables.Add(rng, 1, 1)
        tbl.Borders.Enable = True
        cell = tbl.Cell(1, 1)
        cell.Shading.BackgroundPatternColor = 0xFAF8F5
        c_rng = cell.Range
        c_rng.End = c_rng.End - 1
        c_rng.Text = '\r'.join(code_lines)
        c_rng.Font.Name = 'Consolas'
        c_rng.Font.NameBi = 'TH SarabunPSK'
        c_rng.Font.Size = 10
        c_rng.Font.SizeBi = 12
        c_rng.Font.Bold = False
        c_rng.Font.BoldBi = False
        c_rng.HighlightColorIndex = wdYellow
        c_rng.LanguageID = wdThai
        c_rng.LanguageIDOther = wdThai
        for cp in cell.Range.Paragraphs:
            cp.Alignment = wdAlignParagraphLeft
            cp.FirstLineIndent = 0
            cp.LeftIndent = 4
            cp.SpaceBefore = 0
            cp.SpaceAfter = 0
        doc.Paragraphs.Add()

    def write_md_table(rows_data):
        p = doc.Paragraphs(doc.Paragraphs.Count)
        p.Style = doc.Styles('Normal')
        p.Alignment = wdAlignParagraphLeft
        p.FirstLineIndent = 0
        p.LeftIndent = 0
        rng = p.Range
        rng.End = rng.End - 1
        num_rows = len(rows_data)
        num_cols = len(rows_data[0])
        tbl = doc.Tables.Add(rng, num_rows, num_cols)
        tbl.Borders.Enable = True
        for r_i, r_cells in enumerate(rows_data, start=1):
            is_hdr = (r_i == 1)
            for c_i, c_txt in enumerate(r_cells, start=1):
                cell = tbl.Cell(r_i, c_i)
                if is_hdr:
                    cell.Shading.BackgroundPatternColor = 0xEDE8E2
                cr = cell.Range
                cr.End = cr.End - 1
                clean_txt = re.sub(r'\*\*([^*]+)\*\*', r'\1', c_txt.strip())
                clean_txt = clean_txt.replace('`', '')
                cr.Text = clean_txt
                cr.Font.Name = 'TH SarabunPSK'
                cr.Font.NameBi = 'TH SarabunPSK'
                cr.Font.Size = 16
                cr.Font.SizeBi = 16
                cr.Font.Bold = is_hdr or ('**' in c_txt)
                cr.Font.BoldBi = is_hdr or ('**' in c_txt)
                cr.HighlightColorIndex = wdYellow
                cr.LanguageID = wdThai
                cr.LanguageIDOther = wdThai
                cell.Range.Paragraphs(1).Alignment = wdAlignParagraphCenter if is_hdr else wdAlignParagraphLeft
                cell.Range.Paragraphs(1).FirstLineIndent = 0
                cell.Range.Paragraphs(1).LeftIndent = 0
        doc.Paragraphs.Add()

    def render_md_lines(lines, is_quiz=False, is_lab=False):
        i = 0
        n = len(lines)
        is_ref = False
        while i < n:
            line = lines[i].rstrip('\r\n')
            stripped = line.strip()

            if not stripped or stripped == '---' or stripped.startswith('← [') or stripped.startswith('[กลับหน้าสารบัญ'):
                i += 1
                continue

            if stripped.startswith('```'):
                code_lines = []
                i += 1
                while i < n and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i].rstrip('\r\n'))
                    i += 1
                i += 1
                write_code_box(code_lines)
                continue

            if stripped.startswith('|') and stripped.endswith('|'):
                table_rows = []
                while i < n and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
                    row_str = lines[i].strip()[1:-1]
                    cells = [c.strip() for c in row_str.split('|')]
                    if not all(re.match(r'^:?-+:?$', c) for c in cells):
                        table_rows.append(cells)
                    i += 1
                if table_rows:
                    cap_txt = table_captions.get(ch_num, f'ข้อมูลเปรียบเทียบประจำบทที่ {ch_num}')
                    write_para(f'**ตารางที่ {ch_num}.1** {cap_txt}', font_size=16, bold=False, align=wdAlignParagraphLeft, first_indent_pt=0, space_before_pt=6, space_after_pt=2)
                    write_md_table(table_rows)
                continue

            if stripped.startswith('>'):
                bq_lines = []
                alert_type = None
                while i < n and lines[i].strip().startswith('>'):
                    bql = re.sub(r'^>\s*', '', lines[i].strip())
                    m_alert = re.match(r'^\[!(NOTE|IMPORTANT|TIP|WARNING|CAUTION)\]', bql)
                    if m_alert:
                        alert_type = m_alert.group(1)
                    elif bql:
                        bq_lines.append(bql)
                    i += 1
                if bq_lines:
                    label_map = {
                        'NOTE': 'หมายเหตุ (Note): ',
                        'IMPORTANT': 'ข้อควรจำ (Important): ',
                        'TIP': 'เคล็ดลับ (Tip): ',
                        'WARNING': 'คำเตือน (Warning): ',
                        'CAUTION': 'ข้อควรระวัง (Caution): ',
                    }
                    prefix = f"**{label_map.get(alert_type, '')}**" if alert_type else ''
                    write_para(prefix + ' '.join(bq_lines), font_size=16, bold=False, align=wdAlignParagraphThaiJustify, first_indent_pt=42.55)
                continue

            if stripped.startswith('# '):
                if is_quiz:
                    write_para('', font_size=16, first_indent_pt=0)
                    write_para('แบบฝึกหัดท้ายบทเรียน', style_name='Heading 3', font_size=18, bold=True, align=wdAlignParagraphLeft, first_indent_pt=0)
                elif is_lab:
                    write_para('', font_size=16, first_indent_pt=0)
                    lab_title = re.sub(r'^#\s*ปฏิบัติการ\s*บทที่\s*\d+\s*:\s*', '', stripped)
                    lab_title = re.sub(r'\s*\(Lab\)\s*$', '', lab_title)
                    write_para(f'ปฏิบัติการท้ายบทเรียน: {lab_title}', style_name='Heading 3', font_size=18, bold=True, align=wdAlignParagraphLeft, first_indent_pt=0)
                i += 1
                continue

            if stripped.startswith('## '):
                h2_txt = stripped[3:].strip()
                is_ref = False
                if 'สรุปท้ายบทเรียน' in h2_txt:
                    h2_txt = 'สรุปท้ายบทเรียน'
                elif 'แหล่งข้อมูลอ้างอิง' in h2_txt:
                    h2_txt = 'เอกสารอ้างอิง'
                    is_ref = True
                elif ch_num == 11 and 'สรุปเปรียบเทียบระบบจัดเก็บไฟล์' in h2_txt:
                    # Render as a subsection heading inside 11.7 so TOC stays clean
                    write_para(h2_txt, font_size=16, bold=True, align=wdAlignParagraphLeft, first_indent_pt=42.55, space_before_pt=3)
                    i += 1
                    continue
                elif ch_num == 12 and '[เนื้อหาพิเศษตอนท้าย (Bonus Section)]:' in h2_txt:
                    h2_txt = h2_txt.replace('[เนื้อหาพิเศษตอนท้าย (Bonus Section)]: ', '')
                write_para('', font_size=16, first_indent_pt=0)
                sz_pt = 18 if not (is_quiz or is_lab) else 16
                write_para(h2_txt, style_name='Heading 3', font_size=sz_pt, bold=True, align=wdAlignParagraphLeft, first_indent_pt=0)
                i += 1
                continue

            if stripped.startswith('### '):
                h3_txt = stripped[4:].strip()
                write_para(h3_txt, font_size=16, bold=True, align=wdAlignParagraphLeft, first_indent_pt=42.55, space_before_pt=3)
                i += 1
                continue

            if stripped.startswith('#### '):
                h4_txt = stripped[5:].strip()
                write_para(h4_txt, font_size=16, bold=True, align=wdAlignParagraphLeft, first_indent_pt=42.55, space_before_pt=2)
                i += 1
                continue

            if is_ref and stripped.startswith('* '):
                ref_txt = stripped[2:].strip()
                write_para(ref_txt, font_size=16, bold=False, align=wdAlignParagraphLeft, first_indent_pt=-36, left_indent_pt=36)
                i += 1
                continue

            m_bul = re.match(r'^(\s*)([*-])\s+(.*)$', line)
            if m_bul:
                indent_spaces = len(m_bul.group(1))
                bul_txt = m_bul.group(3).strip()
                f_ind = 58.5 if indent_spaces >= 2 else 42.55
                write_para('• ' + bul_txt, font_size=16, bold=False, align=wdAlignParagraphThaiJustify, first_indent_pt=f_ind)
                i += 1
                continue

            m_num = re.match(r'^(\s*)(\d+\.)\s+(.*)$', line)
            if m_num:
                num_prefix = m_num.group(2) + ' '
                num_txt = m_num.group(3).strip()
                write_para(num_prefix + num_txt, font_size=16, bold=False, align=wdAlignParagraphThaiJustify, first_indent_pt=42.55)
                i += 1
                continue

            m_opt = re.match(r'^([กขคง]\.)\s+(.*)$', stripped)
            if m_opt:
                write_para(stripped, font_size=16, bold=False, align=wdAlignParagraphLeft, first_indent_pt=58.5)
                i += 1
                continue

            write_para(stripped, font_size=16, bold=False, align=wdAlignParagraphThaiJustify, first_indent_pt=42.55)
            i += 1

    write_para(chapter_titles[ch_num], style_name='Heading 2', font_size=20, bold=True, align=wdAlignParagraphCenter, first_indent_pt=0, space_after_pt=0)
    write_para('', font_size=16, first_indent_pt=0)

    with open(os.path.join(ch_dir, '02-content.md'), 'r', encoding='utf-8') as f:
        content_lines = f.readlines()

    ref_start_idx = None
    for idx, l in enumerate(content_lines):
        if 'แหล่งข้อมูลอ้างอิง' in l and l.startswith('## '):
            ref_start_idx = idx
            break

    main_content_lines = content_lines[:ref_start_idx] if ref_start_idx else content_lines
    ref_content_lines = content_lines[ref_start_idx:] if ref_start_idx else []

    render_md_lines(main_content_lines)

    with open(os.path.join(ch_dir, '03-quiz.md'), 'r', encoding='utf-8') as f:
        quiz_lines = f.readlines()
    render_md_lines(quiz_lines, is_quiz=True)

    with open(os.path.join(ch_dir, '04-lab.md'), 'r', encoding='utf-8') as f:
        lab_lines = f.readlines()
    render_md_lines(lab_lines, is_lab=True)

    if ref_content_lines:
        render_md_lines(ref_content_lines)

    if doc.Paragraphs.Count > 1 and not doc.Paragraphs(doc.Paragraphs.Count).Range.Text.strip():
        doc.Paragraphs(doc.Paragraphs.Count).Range.Delete()

    doc.Content.LanguageID = wdThai
    doc.Content.LanguageIDOther = wdThai

    doc.Repaginate()
    pages = doc.ComputeStatistics(2)
    doc.SaveAs2(dst_path, FileFormat=wdFormatXMLDocument)
    doc.Close(False)
    print(f'Generated {dst_name} (Pages={pages})')
    return pages

if __name__ == '__main__':
    start_ch = int(sys.argv[1])
    end_ch = int(sys.argv[2])
    word = win32com.client.Dispatch('Word.Application')
    for ch in range(start_ch, end_ch + 1):
        generate_chapter_docx(word, ch)
    word.Quit()
