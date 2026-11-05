import win32com.client, os, glob, re, sys
sys.stdout.reconfigure(encoding='utf-8')

form_dir = r'd:\react-native\expo-sdk54-course-2026\course\ฟอร์ม'
out_dir = r'd:\react-native\expo-sdk54-course-2026\course\docx-v2'
ch_dirs = sorted(glob.glob(r'd:\react-native\expo-sdk54-course-2026\course\chapter-*'))

roman_map = {
    1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII',
    8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII', 13: 'XIII'
}

wdYellow = 7
wdAlignParagraphThaiJustify = 9
wdFormatXMLDocument = 16
wdThai = 1054

def strip_md_inline(s):
    s = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', s)
    s = s.replace('`', '')
    return s.strip()

def parse_lesson_plan(ch_dir):
    lp_file = os.path.join(ch_dir, '01-lesson-plan.md')
    ct_file = os.path.join(ch_dir, '02-content.md')

    # Topics from H2 headings of 02-content.md so they match the chapter numbering and TOC
    topics = []
    with open(ct_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('## '):
                t = line[3:].strip()
                if 'สรุปท้ายบทเรียน' in t or 'แหล่งข้อมูลอ้างอิง' in t:
                    continue
                topics.append(strip_md_inline(t))

    objectives = []
    methods = [] # list of (bold_prefix, rest_text)
    materials = []
    measurements = []
    evaluations = []

    curr = None
    with open(lp_file, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if s.startswith('## ') or s.startswith('### '):
                if 'วัตถุประสงค์เชิงพฤติกรรม' in s:
                    curr = 'obj'
                elif 'วิธีสอนและกิจกรรม' in s:
                    curr = 'met'
                elif 'สื่อการเรียนการสอน' in s:
                    curr = 'mat'
                elif '1. การวัดผล' in s:
                    curr = 'mea'
                elif '2. การประเมินผล' in s:
                    curr = 'eva'
                else:
                    curr = None
                continue
            if not curr or not s or s == '---' or s.startswith('['):
                continue
            m = re.match(r'^(\d+(?:\.\d+)?\.?)\s+(.*)$', s)
            if not m:
                continue
            body_txt = m.group(2).strip()
            if curr == 'obj':
                objectives.append(strip_md_inline(re.sub(r'\*\*([^*]+)\*\*', r'\1', body_txt)))
            elif curr == 'met':
                mb = re.match(r'^\*\*([^*]+)\*\*\s*(.*)$', body_txt)
                if mb:
                    b_pref = strip_md_inline(mb.group(1)) + ' '
                    rest = strip_md_inline(re.sub(r'\*\*([^*]+)\*\*', r'\1', mb.group(2)))
                    methods.append((b_pref, rest))
                else:
                    methods.append(('', strip_md_inline(body_txt)))
            elif curr == 'mat':
                materials.append(strip_md_inline(re.sub(r'\*\*([^*]+)\*\*', r'\1', body_txt)))
            elif curr == 'mea':
                measurements.append(strip_md_inline(re.sub(r'\*\*([^*]+)\*\*', r'\1', body_txt)))
            elif curr == 'eva':
                evaluations.append(strip_md_inline(re.sub(r'\*\*([^*]+)\*\*', r'\1', body_txt)))

    return topics, objectives, methods, materials, measurements, evaluations

def set_cell_text(tbl, row_idx, text, prefix='', bold_prefix='', align_thai=False):
    cell = tbl.Cell(row_idx, 1)
    rng = cell.Range
    rng.End = rng.End - 1
    rng.Text = prefix + bold_prefix + text

    full_rng = cell.Range
    full_rng.End = full_rng.End - 1
    full_rng.Font.Name = 'TH SarabunPSK'
    full_rng.Font.NameBi = 'TH SarabunPSK'
    full_rng.Font.Size = 16
    full_rng.Font.SizeBi = 16
    full_rng.Font.Bold = False
    full_rng.Font.BoldBi = False
    full_rng.LanguageID = wdThai
    full_rng.LanguageIDOther = wdThai

    if prefix:
        pref_rng = cell.Range
        pref_rng.End = pref_rng.Start + len(prefix)
        pref_rng.HighlightColorIndex = 0

    fill_rng = cell.Range
    fill_rng.Start = fill_rng.Start + len(prefix)
    fill_rng.End = fill_rng.End - 1
    fill_rng.HighlightColorIndex = wdYellow

    if bold_prefix:
        b_rng = cell.Range
        b_rng.Start = b_rng.Start + len(prefix)
        b_rng.End = b_rng.Start + len(bold_prefix)
        b_rng.Font.Bold = True
        b_rng.Font.BoldBi = True

    if align_thai:
        cell.Range.Paragraphs(1).Alignment = wdAlignParagraphThaiJustify

word = win32com.client.Dispatch('Word.Application')
word.Visible = False

for ch_num in range(2, 14):
    ch_dir = ch_dirs[ch_num - 1]
    topics, objectives, methods, materials, measurements, evaluations = parse_lesson_plan(ch_dir)

    file_num = 6 + ch_num * 2
    roman = roman_map[ch_num]
    src_name = f'{file_num:02d}-Plan-{roman}.doc'
    dst_name = f'{file_num:02d}-Plan-{roman}.docx'
    src_path = os.path.join(form_dir, src_name)
    dst_path = os.path.join(out_dir, dst_name)

    doc = word.Documents.Open(src_path, ReadOnly=True)
    tbl1 = doc.Tables(1)
    tbl2 = doc.Tables(2)

    # --- TABLE 1 (work bottom-to-top) ---
    # 4. สื่อการเรียนการสอน: template has 7 rows (23..29)
    diff_mat = len(materials) - 7
    if diff_mat < 0:
        for r in range(29, 29 + diff_mat, -1):
            tbl1.Rows(r).Delete()
    elif diff_mat > 0:
        for _ in range(diff_mat):
            tbl1.Rows.Add(tbl1.Rows(29))
    for i, m_txt in enumerate(materials):
        set_cell_text(tbl1, 23 + i, m_txt, align_thai=True)

    # 3. วิธีสอนและกิจกรรมการเรียนการสอนประจำบท: template has 5 rows (16..20)
    diff_met = len(methods) - 5
    if diff_met < 0:
        for r in range(20, 20 + diff_met, -1):
            tbl1.Rows(r).Delete()
    elif diff_met > 0:
        for _ in range(diff_met):
            tbl1.Rows.Add(tbl1.Rows(20))
    for i, (b_pref, m_txt) in enumerate(methods):
        set_cell_text(tbl1, 16 + i, m_txt, bold_prefix=b_pref, align_thai=True)

    # 2. วัตถุประสงค์เชิงพฤติกรรม: template has 5 rows (9..13)
    diff_obj = len(objectives) - 5
    if diff_obj < 0:
        for r in range(13, 13 + diff_obj, -1):
            tbl1.Rows(r).Delete()
    elif diff_obj > 0:
        for _ in range(diff_obj):
            tbl1.Rows.Add(tbl1.Rows(13))
    for i, obj_txt in enumerate(objectives):
        set_cell_text(tbl1, 9 + i, obj_txt, prefix=f'{i+1}. ', align_thai=True)

    # 1. หัวข้อเนื้อหาประจำบท: template has 2 rows (2..3)
    diff_top = len(topics) - 2
    if diff_top > 0:
        for _ in range(diff_top):
            tbl1.Rows.Add(tbl1.Rows(3))
    for i, top_txt in enumerate(topics):
        set_cell_text(tbl1, 2 + i, top_txt, align_thai=False)

    # --- TABLE 2 (work bottom-to-top) ---
    # 2. การประเมินผล: template has 4 rows (8..11)
    diff_eva = len(evaluations) - 4
    if diff_eva < 0:
        for r in range(11, 11 + diff_eva, -1):
            tbl2.Rows(r).Delete()
    elif diff_eva > 0:
        for _ in range(diff_eva):
            tbl2.Rows.Add(tbl2.Rows(11))
    for i, ev_txt in enumerate(evaluations):
        set_cell_text(tbl2, 8 + i, ev_txt, prefix=f'2.{i+1} ', align_thai=True)

    # 1. การวัดผล: template has 4 rows (3..6)
    diff_mea = len(measurements) - 4
    if diff_mea < 0:
        for r in range(6, 6 + diff_mea, -1):
            tbl2.Rows(r).Delete()
    elif diff_mea > 0:
        for _ in range(diff_mea):
            tbl2.Rows.Add(tbl2.Rows(6))
    for i, ms_txt in enumerate(measurements):
        set_cell_text(tbl2, 3 + i, ms_txt, prefix=f'1.{i+1} ', align_thai=True)

    doc.Content.LanguageID = wdThai
    doc.Content.LanguageIDOther = wdThai

    doc.SaveAs2(dst_path, FileFormat=wdFormatXMLDocument)
    doc.Close(False)
    print(f'Generated {dst_name} (Topics={len(topics)}, Obj={len(objectives)}, Met={len(methods)}, Mat={len(materials)})')

word.Quit()
print('All 12 lesson plan files (Ch 2 - Ch 13) generated successfully!')
