---
name: merge-course-docx
description: >-
  Use this skill when the user asks to merge or combine all numbered course Word (.docx) files
  (01 through 35 in course/docx-v2/) into a single master book (.docx and .pdf), either with
  yellow review highlights (00-All-Merged) or clean without highlights (00-All-Merged-Clean).
---

# Merge Course DOCX & PDF Skill

This skill combines all numbered `.docx` files (`01-CoverOut.docx` through `35-Appendix.docx`) in `course/docx-v2/` into a single complete book using Microsoft Word COM automation (`win32com.client`), separating each file with a `Section Break (Next Page)` and configuring continuous page numbering that matches `04-Content.docx`:
- **Sections 1–2 (`01`–`02`):** Outer & Inner Covers (no page numbers)
- **Sections 3–7 (`03`–`07`):** Frontmatter (`(1)`, `(2)`, ..., hidden on the first page of each section)
- **Sections 8–35 (`08`–`35`):** Main Content, Bibliography & Appendix (Arabic numerals `1`..`N`, starting at `1` on `08-Plan-I` and hidden on the first page of each chapter/plan)

## Steps

1. **Run the Merge Script**
   Execute [merge_course_docx.py](./scripts/merge_course_docx.py) from the workspace root (`d:\react-native\expo-sdk54-course-2026`):

   - **Generate both Highlighted (`00-All-Merged`) and Clean (`00-All-Merged-Clean`) `.docx` and `.pdf` files (default):**
     ```powershell
     python .agents/skills/merge-course-docx/scripts/merge_course_docx.py
     ```

2. **Verify the Output**
   Check that the merged `.docx` and `.pdf` files exist in `course/docx-v2/` and `course/pdf/`:
   ```powershell
   Get-ChildItem "course/docx-v2/00-All-Merged*.docx", "course/pdf/00-All-Merged*.pdf" | Select-Object FullName, Length
   ```

