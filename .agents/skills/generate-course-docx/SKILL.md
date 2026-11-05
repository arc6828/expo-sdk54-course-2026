---
name: generate-course-docx
description: >-
  Use this skill when the user asks to generate, populate, or update Word (.docx) teaching material
  files in course/docx-v2/ from the legacy .doc templates in course/ฟอร์ม/, COURSE_METADATA.md,
  and chapter Markdown files (01-lesson-plan.md, 02-content.md, 03-quiz.md, 04-lab.md).
---

# Generate Course DOCX Skill

This skill populates all 35 university teaching material Word files (`01` through `35`) from the `.doc` templates in `course/ฟอร์ม/` and the Markdown chapter content in `course/chapter-*` using Microsoft Word COM automation (`win32com.client`).

## Formatting Standards Enforced
- **Font:** `TH SarabunPSK` (24pt Cover, 20pt Chapter Title, 18pt Main Heading, 16pt Body)
- **Code Blocks:** `Consolas` 10pt inside a 1x1 light-gray shaded table (`#F5F5F5`) with border
- **Paragraph Alignment:** `thaiDistribute` (`wdAlignParagraphThaiJustify = 9`) with Thai language tag (`wdThai = 1054`)
- **Review Highlight:** Yellow (`wdYellow = 7`) on all newly populated/replaced content
- **Citations:** APA 6th Edition inline and end-of-chapter references

## Scripts & Workflow

Run these scripts from the workspace root in order when rebuilding or updating `.docx` files:

1. **Covers & Preface (`01-CoverOut.docx`, `02-CoverIn.docx`, `03-Intro2.docx`):**
   - [generate_01_03_com.py](./scripts/generate_01_03_com.py)
2. **Lesson Plans for Chapters 1–13 (`08-Plan-I.docx` .. `32-Plan-XIII.docx`):**
   - [generate_all_plans_com.py](./scripts/generate_all_plans_com.py)
3. **Chapter Contents for Chapters 1–13 (`09-Chater-I.docx` .. `33-Chater-XIII.docx`):**
   - [generate_chapters_com.py](./scripts/generate_chapters_com.py)
4. **Bibliography & Appendix (`34-Reference.docx`, `35-Appendix.docx`):**
   - [generate_34_35_com.py](./scripts/generate_34_35_com.py)
5. **Extract Exact Page Numbers for TOC (`toc_pages.json`):**
   - [extract_exact_pages.py](./scripts/extract_exact_pages.py)
6. **Overall Course Administration Plan (`07-PlanT.docx`):**
   - [generate_07_com.py](./scripts/generate_07_com.py)
7. **Table of Contents, List of Tables, List of Figures (`04-Content.docx`, `05-Table.docx`, `06-Figure.docx`):**
   - [generate_04_05_06_com.py](./scripts/generate_04_05_06_com.py)

