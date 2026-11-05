import win32com.client, os, zipfile, xml.etree.ElementTree as ET, sys
sys.stdout.reconfigure(encoding='utf-8')

form_dir = r'd:\react-native\expo-sdk54-course-2026\course\ฟอร์ม'
out_dir = r'd:\react-native\expo-sdk54-course-2026\course\docx-v2'

word = win32com.client.Dispatch('Word.Application')
word.Visible = False

wdYellow = 7
wdAlignParagraphJustify = 3
wdFormatXMLDocument = 16
wdThai = 1054

def fill_form_fields(doc, values):
    count = doc.FormFields.Count
    assert count == len(values), f"Expected {len(values)} fields, got {count}"
    for idx in range(count, 0, -1):
        ff = doc.FormFields(idx)
        rng = ff.Range
        val = values[idx - 1]
        rng.Text = val
        rng.HighlightColorIndex = wdYellow
        rng.Font.Name = "TH SarabunPSK"
        rng.Font.NameBi = "TH SarabunPSK"
        rng.LanguageID = wdThai
        rng.LanguageIDOther = wdThai
    doc.Content.LanguageID = wdThai
    doc.Content.LanguageIDOther = wdThai

# 1. 01-CoverOut.doc -> 01-CoverOut.docx
doc1 = word.Documents.Open(os.path.join(form_dir, '01-CoverOut.doc'), ReadOnly=True)
fill_form_fields(doc1, [
    'ประกอบการสอน',
    'การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่',
    'ชวลิต โควีระวงศ์',
    'วิทยาศาสตร์และเทคโนโลยี',
    '2568'
])
dst1 = os.path.join(out_dir, '01-CoverOut.docx')
doc1.SaveAs2(dst1, FileFormat=wdFormatXMLDocument)
doc1.Close(False)
print('Saved:', dst1)

# 2. 02-CoverIn.doc -> 02-CoverIn.docx
doc2 = word.Documents.Open(os.path.join(form_dir, '02-CoverIn.doc'), ReadOnly=True)
fill_form_fields(doc2, [
    'ประกอบการสอน',
    'การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่',
    'ชวลิต โควีระวงศ์',
    'M.Eng.',
    'Information and communication technology for Embedded Systems',
    'วิทยาศาสตร์และเทคโนโลยี',
    '2568'
])
dst2 = os.path.join(out_dir, '02-CoverIn.docx')
doc2.SaveAs2(dst2, FileFormat=wdFormatXMLDocument)
doc2.Close(False)
print('Saved:', dst2)

# 3. 03-Intro2.doc -> 03-Intro2.docx
doc3 = word.Documents.Open(os.path.join(form_dir, '03-Intro2.doc'), ReadOnly=True)
fill_form_fields(doc3, [
    'ประกอบการสอน',
    'การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่',
    'SCS337',
    '2',
    '2568',
    '10',
    '1-2',
    'ในการเข้าใจหลักการและกระบวนการพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่อย่างเป็นระบบ ทั้งรูปแบบออนไลน์และออฟไลน์ การใช้เทคโนโลยี React Native, Expo, Expo Router และ Supabase ในการพัฒนาแอปพลิเคชัน การออกแบบและพัฒนาส่วนติดต่อผู้ใช้ (UI) และประสบการณ์ผู้ใช้ (UX) การเขียนโปรแกรมเชิงฟังก์ชัน การจัดการข้อมูลในเครื่องและฐานข้อมูลคลาวด์ การทำระบบยืนยันตัวตน การอัปโหลดข้อมูล การทำงานร่วมกับพิกัดตำแหน่ง แผนที่ และเซนเซอร์อุปกรณ์ ตลอดจนการทดสอบ แก้ไขข้อผิดพลาด และการเผยแพร่แอปพลิเคชันบนแพลตฟอร์มมาตรฐานอย่างมีจริยธรรม',
    'ประกอบการสอน',
    'การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่',
    'ประกอบการสอน',
    'ชวลิต โควีระวงศ์',
    '28 ตุลาคม 2568'
])
for p_idx in [3, 4, 5]:
    doc3.Paragraphs(p_idx).Alignment = wdAlignParagraphJustify

dst3 = os.path.join(out_dir, '03-Intro2.docx')
doc3.SaveAs2(dst3, FileFormat=wdFormatXMLDocument)
doc3.Close(False)
print('Saved:', dst3)

word.Quit()
