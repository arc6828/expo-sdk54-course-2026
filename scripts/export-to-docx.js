const fs = require('fs');
const path = require('path');

// ตรวจสอบการโหลดไลบรารีแปลงเอกสาร
let convertMarkdownToDocx;
try {
  const mdToDocx = require('@mohtasham/md-to-docx');
  convertMarkdownToDocx = mdToDocx.convertMarkdownToDocx;
} catch (error) {
  console.error('\n❌ เกิดข้อผิดพลาด: ไม่พบไลบรารี @mohtasham/md-to-docx');
  console.error('กรุณาติดตั้งไลบรารีเสริมโดยใช้คำสั่งนี้ก่อนรันสคริปต์:');
  console.error('👉 npm install @mohtasham/md-to-docx\n');
  process.exit(1);
}

const COURSE_DIR = path.join(__dirname, '..', 'course');
const EXPORT_DIR = path.join(COURSE_DIR, 'docx-exports');

async function run() {
  console.log('==================================================');
  console.log(' เริ่มต้นกระบวนการแปลงไฟล์ Markdown (.md) เป็น Word (.docx)...');
  console.log('==================================================');

  // สร้างโฟลเดอร์สำหรับเก็บผลลัพธ์ถ้ายังไม่มี
  if (!fs.existsSync(EXPORT_DIR)) {
    fs.mkdirSync(EXPORT_DIR, { recursive: true });
    console.log(`📁 สร้างโฟลเดอร์สำหรับเก็บไฟล์ผลลัพธ์: ${EXPORT_DIR}`);
  }

  // อ่านรายการโฟลเดอร์ใน course/
  const files = fs.readdirSync(COURSE_DIR);
  
  // คัดเลือกเฉพาะโฟลเดอร์ที่เป็นบทเรียน (เริ่มต้นด้วย chapter-)
  const chapters = files
    .filter(file => {
      const fullPath = path.join(COURSE_DIR, file);
      return fs.statSync(fullPath).isDirectory() && file.startsWith('chapter-');
    })
    .sort(); // เรียงลำดับโฟลเดอร์ตามหมายเลขบทเรียน (01, 02, ... 13)

  console.log(`🔍 พบไฟล์เนื้อหาทั้งหมด ${chapters.length} บทเรียน`);

  for (const chapter of chapters) {
    const chapterPath = path.join(COURSE_DIR, chapter);
    const mdFiles = [
      '01-lesson-plan.md',
      '02-content.md',
      '03-quiz.md',
      '04-lab.md'
    ];

    let combinedMarkdown = '';
    let filesFound = 0;

    for (const mdFile of mdFiles) {
      const filePath = path.join(chapterPath, mdFile);
      if (fs.existsSync(filePath)) {
        let content = fs.readFileSync(filePath, 'utf-8');

        // ตรวจสอบและแทรกหน้าว่าง (Page Break) ก่อนหัวข้อถัดไป
        if (combinedMarkdown !== '') {
          combinedMarkdown += '\n\n\\pagebreak\n\n';
        }
        
        combinedMarkdown += content;
        filesFound++;
      }
    }

    if (filesFound === 0) {
      console.log(`[-] ข้ามโฟลเดอร์ ${chapter} (ไม่พบไฟล์ .md สำหรับแปลงเนื้อหา)`);
      continue;
    }

    console.log(`[+] กำลังรวบรวมข้อมูลของ ${chapter} (พบเอกสาร ${filesFound}/4 ไฟล์)...`);

    try {
      // แปลงเนื้อหาที่รวบรวมเป็น DOCX Buffer
      const docxBuffer = await convertMarkdownToDocx(combinedMarkdown, {
        font: 'TH Sarabun PSK', // กำหนดรูปแบบฟอนต์เป็น TH Sarabun PSK
        fontSize: 16,           // กำหนดขนาดตัวอักษรเริ่มต้น (16pt เป็นขนาดมาตรฐานของ TH Sarabun)
      });

      // บันทึกไฟล์ผลลัพธ์เป็น .docx
      const outputFileName = `${chapter}.docx`;
      const outputPath = path.join(EXPORT_DIR, outputFileName);
      const arrayBuffer = await docxBuffer.arrayBuffer();
      const buffer = Buffer.from(arrayBuffer);
      fs.writeFileSync(outputPath, buffer);
      console.log(`  └─ [✓] บันทึกไฟล์สำเร็จ: ${outputPath}`);
    } catch (err) {
      console.error(`  └─ [✗] เกิดข้อผิดพลาดในการแปลงบทเรียน ${chapter}:`, err.stack || err.message);
    }
    break;
  }

  console.log('==================================================');
  console.log(' 🎉 สิ้นสุดกระบวนการทำงานไฟล์ทั้งหมดเรียบร้อยแล้ว!');
  console.log('==================================================');
}

run().catch(console.error);
