---
name: export-docx-to-pdf
description: >-
  Use this skill when the user asks to export or convert Word (.docx) teaching material files
  (such as those in course/docx-v2/) into PDF files (such as in course/pdf/), either all files
  in batch or specific files, with or without yellow review highlights.
---

# Export DOCX to PDF Skill

This skill converts `.docx` files into `.pdf` files using Microsoft Word COM automation (`win32com.client`), preserving exact Thai typography (`TH SarabunPSK`), `thaiDistribute` paragraph justification, tables, and shaded `Consolas` code blocks.

## Steps

1. **Run the Export Script**
   Execute [export_docx_to_pdf.py](./scripts/export_docx_to_pdf.py) from the workspace root (`d:\react-native\expo-sdk54-course-2026`):

   - **Export all `.docx` files from `course/docx-v2` to `course/pdf` (default):**
     ```powershell
     python .agents/skills/export-docx-to-pdf/scripts/export_docx_to_pdf.py
     ```

   - **Export specific files or patterns only:**
     ```powershell
     python .agents/skills/export-docx-to-pdf/scripts/export_docx_to_pdf.py --files 01-CoverOut.docx 04-Content.docx
     ```

   - **Export clean PDFs without yellow review highlights (leaves `.docx` untouched):**
     ```powershell
     python .agents/skills/export-docx-to-pdf/scripts/export_docx_to_pdf.py --remove-highlights
     ```

   - **Custom source or destination directories:**
     ```powershell
     python .agents/skills/export-docx-to-pdf/scripts/export_docx_to_pdf.py --src "course/docx-v2" --dst "course/pdf"
     ```

2. **Verify the Output**
   Check that the target `.pdf` files were created in the destination directory and have non-zero file sizes:
   ```powershell
   Get-ChildItem "course/pdf/*.pdf" | Sort-Object Name | Select-Object Name, Length
   ```

