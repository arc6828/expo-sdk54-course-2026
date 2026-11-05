import win32com.client, os, re, glob, json, sys
sys.stdout.reconfigure(encoding='utf-8')

out_dir = r'd:\react-native\expo-sdk54-course-2026\course\docx-v2'
ch_dirs = sorted(glob.glob(r'd:\react-native\expo-sdk54-course-2026\course\chapter-*'))

roman_map = {
    1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII',
    8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII', 13: 'XIII'
}

word = win32com.client.Dispatch('Word.Application')
word.Visible = False

wdActiveEndAdjustedPageNumber = 1
wdActiveEndPageNumber = 3

toc_data = {}
tables_data = []

for ch_num in range(1, 14):
    plan_fnum = 6 + ch_num * 2
    chap_fnum = 7 + ch_num * 2
    roman = roman_map[ch_num]
    plan_fname = f'{plan_fnum:02d}-Plan-{roman}.docx'
    chap_fname = f'{chap_fnum:02d}-Chater-{roman}.docx'

    # Open Plan to verify page count
    dp = word.Documents.Open(os.path.join(out_dir, plan_fname), ReadOnly=True)
    dp.Repaginate()
    plan_pages = dp.ComputeStatistics(2)
    dp.Close(False)

    # Open Chapter to extract exact page numbers of headings and tables
    dc = word.Documents.Open(os.path.join(out_dir, chap_fname), ReadOnly=True)
    dc.Repaginate()
    chap_pages = dc.ComputeStatistics(2)

    ch_info = {
        'plan_file': plan_fname,
        'plan_pages': plan_pages,
        'chap_file': chap_fname,
        'chap_pages': chap_pages,
        'sections': [],
        'summary_page': 1,
        'quiz_page': 1,
        'ref_page': 1,
    }

    for i in range(1, dc.Paragraphs.Count + 1):
        p = dc.Paragraphs(i)
        txt = p.Range.Text.strip().replace('\r', '').replace('\x07', '')
        if not txt:
            continue
        pg = p.Range.Information(wdActiveEndPageNumber)
        sname = p.Style.NameLocal
        if sname == 'Heading 3' or p.Range.Font.Size == 18:
            if re.match(rf'^{ch_num}\.\d+\s+', txt):
                if 'สรุปท้ายบทเรียน' in txt:
                    ch_info['summary_page'] = pg
                else:
                    ch_info['sections'].append((txt, pg))
            elif txt == 'สรุปท้ายบทเรียน' or txt == 'สรุป':
                ch_info['summary_page'] = pg
            elif txt == 'แบบฝึกหัดท้ายบทเรียน':
                ch_info['quiz_page'] = pg
            elif txt == 'เอกสารอ้างอิง':
                ch_info['ref_page'] = pg
        if txt.startswith(f'ตารางที่ {ch_num}.'):
            m_t = re.match(rf'^ตารางที่\s+({ch_num}\.\d+)\s+(.*)$', txt)
            if m_t:
                tables_data.append({
                    'num': m_t.group(1),
                    'title': m_t.group(2).strip(),
                    'rel_page': pg,
                    'ch_num': ch_num,
                })

    dc.Close(False)
    toc_data[ch_num] = ch_info
    print(f'Ch {ch_num:02d}: PlanPages={plan_pages}, ChapPages={chap_pages}, Secs={len(ch_info["sections"])}, SumPg={ch_info["summary_page"]}, QuizPg={ch_info["quiz_page"]}, RefPg={ch_info["ref_page"]}')

word.Quit()

with open(r'C:\Users\User\.gemini\antigravity\brain\f24fdf29-f7b9-4b36-b7c4-17856ffda31d\scratch\toc_pages.json', 'w', encoding='utf-8') as f:
    json.dump({'toc': toc_data, 'tables': tables_data}, f, ensure_ascii=False, indent=2)
print('Saved toc_pages.json!')
