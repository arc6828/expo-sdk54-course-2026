import argparse
import glob
import os
import re
import sys
import win32com.client

sys.stdout.reconfigure(encoding="utf-8")

WD_STORY = 6
WD_SECTION_BREAK_NEXT_PAGE = 2
WD_HEADER_FOOTER_PRIMARY = 1
WD_HEADER_FOOTER_FIRST_PAGE = 2
WD_FIELD_PAGE = 33
WD_ALIGN_RIGHT = 2
WD_FORMAT_DOCX = 16
WD_FORMAT_PDF = 17
WD_NO_HIGHLIGHT = 0


def set_header_page_field(header_obj, parenthesized=False):
    """Set right-aligned PAGE field in TH SarabunPSK 16pt (optionally wrapped in parentheses)."""
    rng = header_obj.Range
    rng.Text = ""
    rng.ParagraphFormat.Alignment = WD_ALIGN_RIGHT
    if parenthesized:
        rng.InsertAfter("(")
        rng.Collapse(0)  # wdCollapseEnd
        rng.Fields.Add(Range=rng, Type=WD_FIELD_PAGE, PreserveFormatting=False)
        rng = header_obj.Range
        rng.InsertAfter(")")
    else:
        rng.Fields.Add(Range=rng, Type=WD_FIELD_PAGE, PreserveFormatting=False)

    full_rng = header_obj.Range
    full_rng.Font.Name = "TH SarabunPSK"
    full_rng.Font.NameBi = "TH SarabunPSK"
    full_rng.Font.NameOther = "TH SarabunPSK"
    full_rng.Font.Size = 16
    full_rng.Font.SizeBi = 16
    full_rng.Font.Bold = 0
    full_rng.Font.BoldBi = 0
    full_rng.HighlightColorIndex = WD_NO_HIGHLIGHT


def clear_all_highlights(doc):
    """Remove all yellow highlights in document body and tables."""
    doc.Content.HighlightColorIndex = WD_NO_HIGHLIGHT
    for tbl in doc.Tables:
        tbl.Range.HighlightColorIndex = WD_NO_HIGHLIGHT


def get_sorted_chapter_files(src_dir):
    """Return sorted list of (file_num, abs_path) for 01-*.docx through 35-*.docx."""
    all_files = glob.glob(os.path.join(src_dir, "*.docx"))
    matched = []
    for f in all_files:
        base = os.path.basename(f)
        if base.startswith("~$") or base.startswith("00-"):
            continue
        m = re.match(r"^(\d{2})-", base)
        if m:
            num = int(m.group(1))
            if 1 <= num <= 99:
                matched.append((num, os.path.abspath(f)))
    matched.sort(key=lambda x: x[0])
    return matched


def merge_course_files(src_dir, out_docx, out_pdf, out_clean_docx=None, out_clean_pdf=None):
    src_dir = os.path.abspath(src_dir)
    files = get_sorted_chapter_files(src_dir)
    if not files:
        print(f"[ERROR] No numbered .docx files (01..35) found in {src_dir}")
        sys.exit(1)

    print(f"Found {len(files)} files to merge from: {src_dir}")
    for num, p in files:
        print(f"  [{num:02d}] {os.path.basename(p)}")
    print("-" * 60)

    word = win32com.client.Dispatch("Word.Application")
    try:
        word.Visible = False
    except Exception:
        pass
    try:
        word.DisplayAlerts = 0
    except Exception:
        pass

    try:
        # Open the first file (01-CoverOut.docx) as the base document
        first_num, first_path = files[0]
        master_doc = word.Documents.Open(first_path, ReadOnly=True)
        sel = word.Selection

        for idx, (f_num, f_path) in enumerate(files[1:], start=2):
            sel.EndKey(WD_STORY)
            sel.InsertBreak(WD_SECTION_BREAK_NEXT_PAGE)
            sel.InsertFile(FileName=f_path)

            # Remove the 1 extra trailing empty paragraph created by InsertFile at the end of the section
            sec = master_doc.Sections(idx)
            sec_paras = sec.Range.Paragraphs
            if sec_paras.Count > 1:
                last_p = sec_paras(sec_paras.Count)
                if last_p.Range.Text.strip() == "":
                    try:
                        last_p.Range.Delete()
                    except Exception:
                        pass
            print(f"  Merged [{idx:02d}/{len(files):02d}]: {os.path.basename(f_path)}")

        print("-" * 60)
        print("Configuring section headers and continuous page numbering...")

        # Configure PageSetup, Headers, and Page Numbering per section
        for sec_idx in range(1, master_doc.Sections.Count + 1):
            f_num = files[sec_idx - 1][0]
            sec = master_doc.Sections(sec_idx)
            ps = sec.PageSetup
            ps.TopMargin = 108.0
            ps.BottomMargin = 72.0
            ps.LeftMargin = 108.0
            ps.RightMargin = 72.0

            h_primary = sec.Headers(WD_HEADER_FOOTER_PRIMARY)
            h_first = sec.Headers(WD_HEADER_FOOTER_FIRST_PAGE)
            f_primary = sec.Footers(WD_HEADER_FOOTER_PRIMARY)
            f_first = sec.Footers(WD_HEADER_FOOTER_FIRST_PAGE)

            h_primary.LinkToPrevious = False
            h_first.LinkToPrevious = False
            f_primary.LinkToPrevious = False
            f_first.LinkToPrevious = False

            f_primary.Range.Text = ""
            f_first.Range.Text = ""

            if f_num in (1, 2):
                # Covers: no page numbers
                ps.DifferentFirstPageHeaderFooter = 0
                h_primary.Range.Text = ""
                h_first.Range.Text = ""
            elif 3 <= f_num <= 7:
                # Frontmatter (03-Intro2 to 07-PlanT): parenthesized page numbers (1), (2), ...
                ps.DifferentFirstPageHeaderFooter = -1
                h_first.Range.Text = ""
                set_header_page_field(h_primary, parenthesized=True)
                if f_num == 3:
                    h_primary.PageNumbers.RestartNumberingAtSection = True
                    h_primary.PageNumbers.StartingNumber = 1
                else:
                    h_primary.PageNumbers.RestartNumberingAtSection = False
            else:
                # Main book content (08-Plan-I to 35-Appendix): Arabic page numbers 1..N
                ps.DifferentFirstPageHeaderFooter = -1
                h_first.Range.Text = ""
                set_header_page_field(h_primary, parenthesized=False)
                if f_num == 8:
                    h_primary.PageNumbers.RestartNumberingAtSection = True
                    h_primary.PageNumbers.StartingNumber = 1
                else:
                    h_primary.PageNumbers.RestartNumberingAtSection = False

        master_doc.Fields.Update()
        master_doc.Repaginate()
        total_pages = master_doc.ComputeStatistics(2)
        print(f"Total merged pages: {total_pages}")

        # 1. Save Highlighted Merged DOCX and PDF
        if out_docx:
            out_docx = os.path.abspath(out_docx)
            os.makedirs(os.path.dirname(out_docx), exist_ok=True)
            master_doc.SaveAs2(out_docx, FileFormat=WD_FORMAT_DOCX)
            print(f"[OK] Saved Highlighted DOCX : {out_docx}")

        if out_pdf:
            out_pdf = os.path.abspath(out_pdf)
            os.makedirs(os.path.dirname(out_pdf), exist_ok=True)
            master_doc.SaveAs2(out_pdf, FileFormat=WD_FORMAT_PDF)
            print(f"[OK] Saved Highlighted PDF  : {out_pdf}")

        # 2. Save Clean (No Highlight) Merged DOCX and PDF
        if out_clean_docx or out_clean_pdf:
            print("Removing yellow highlights for Clean version...")
            clear_all_highlights(master_doc)
            if out_clean_docx:
                out_clean_docx = os.path.abspath(out_clean_docx)
                os.makedirs(os.path.dirname(out_clean_docx), exist_ok=True)
                master_doc.SaveAs2(out_clean_docx, FileFormat=WD_FORMAT_DOCX)
                print(f"[OK] Saved Clean DOCX       : {out_clean_docx}")
            if out_clean_pdf:
                out_clean_pdf = os.path.abspath(out_clean_pdf)
                os.makedirs(os.path.dirname(out_clean_pdf), exist_ok=True)
                master_doc.SaveAs2(out_clean_pdf, FileFormat=WD_FORMAT_PDF)
                print(f"[OK] Saved Clean PDF        : {out_clean_pdf}")

        master_doc.Close(0)
    finally:
        try:
            word.Quit()
        except Exception:
            pass

    print("-" * 60)
    print("Merge completed successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Merge all numbered course .docx files (01..35) into a single master .docx and .pdf."
    )
    parser.add_argument(
        "--src",
        default=r"course\docx-v2",
        help="Source directory containing numbered .docx files (default: course/docx-v2)",
    )
    parser.add_argument(
        "--out-docx",
        default=r"course\docx-v2\00-All-Merged.docx",
        help="Output path for merged .docx with yellow highlights",
    )
    parser.add_argument(
        "--out-pdf",
        default=r"course\pdf\00-All-Merged.pdf",
        help="Output path for merged .pdf with yellow highlights",
    )
    parser.add_argument(
        "--out-clean-docx",
        default=r"course\docx-v2\00-All-Merged-Clean.docx",
        help="Output path for clean merged .docx (without yellow highlights)",
    )
    parser.add_argument(
        "--out-clean-pdf",
        default=r"course\pdf\00-All-Merged-Clean.pdf",
        help="Output path for clean merged .pdf (without yellow highlights)",
    )
    args = parser.parse_args()
    merge_course_files(
        src_dir=args.src,
        out_docx=args.out_docx,
        out_pdf=args.out_pdf,
        out_clean_docx=args.out_clean_docx,
        out_clean_pdf=args.out_clean_pdf,
    )

