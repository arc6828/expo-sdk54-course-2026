import argparse
import glob
import os
import sys
import win32com.client

sys.stdout.reconfigure(encoding="utf-8")

WD_FORMAT_PDF = 17  # wdFormatPDF
WD_NO_HIGHLIGHT = 0  # wdNoHighlight


def clear_highlights_in_memory(doc):
    """Clear highlight colors in memory before exporting to PDF (does not save to .docx)."""
    rng = doc.Content
    rng.HighlightColorIndex = WD_NO_HIGHLIGHT
    for tbl in doc.Tables:
        tbl.Range.HighlightColorIndex = WD_NO_HIGHLIGHT


def export_docx_to_pdf(src_dir, dst_dir, file_patterns=None, remove_highlights=False):
    src_dir = os.path.abspath(src_dir)
    dst_dir = os.path.abspath(dst_dir)

    if not os.path.exists(src_dir):
        print(f"[ERROR] Source directory does not exist: {src_dir}")
        sys.exit(1)

    os.makedirs(dst_dir, exist_ok=True)

    # Collect target .docx files
    docx_files = []
    if file_patterns:
        for pat in file_patterns:
            matched = glob.glob(os.path.join(src_dir, pat))
            docx_files.extend(matched)
    else:
        docx_files = glob.glob(os.path.join(src_dir, "*.docx"))

    # Filter out Word lock files (~$*) and deduplicate sorted
    docx_files = sorted(
        list(
            {
                os.path.abspath(f)
                for f in docx_files
                if os.path.isfile(f)
                and f.lower().endswith(".docx")
                and not os.path.basename(f).startswith("~$")
            }
        )
    )

    if not docx_files:
        print(f"[WARN] No .docx files found in: {src_dir}")
        return

    print(f"Starting PDF export: {len(docx_files)} file(s)")
    print(f"  Source      : {src_dir}")
    print(f"  Destination : {dst_dir}")
    print(f"  Clear Yellow: {remove_highlights}")
    print("-" * 60)

    word = win32com.client.Dispatch("Word.Application")
    try:
        word.Visible = False
    except Exception:
        pass
    try:
        word.DisplayAlerts = 0  # wdAlertsNone
    except Exception:
        pass

    success_count = 0
    fail_count = 0

    try:
        for idx, docx_path in enumerate(docx_files, start=1):
            base_name = os.path.splitext(os.path.basename(docx_path))[0]
            pdf_path = os.path.join(dst_dir, f"{base_name}.pdf")
            try:
                doc = word.Documents.Open(docx_path, ReadOnly=True)
                if remove_highlights:
                    clear_highlights_in_memory(doc)
                doc.SaveAs2(pdf_path, FileFormat=WD_FORMAT_PDF)
                pages = doc.ComputeStatistics(2)  # wdStatisticPages = 2
                doc.Close(0)  # wdDoNotSaveChanges = 0
                success_count += 1
                print(f"[{idx:02d}/{len(docx_files):02d}] OK   : {base_name}.pdf ({pages} pages)")
            except Exception as e:
                fail_count += 1
                print(f"[{idx:02d}/{len(docx_files):02d}] FAIL : {base_name}.docx -> {e}")
    finally:
        try:
            word.Quit()
        except Exception:
            pass

    print("-" * 60)
    print(f"Completed: {success_count} succeeded, {fail_count} failed.")
    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Batch export Word (.docx) files to PDF using Microsoft Word COM automation."
    )
    parser.add_argument(
        "--src",
        default=r"course\docx-v2",
        help="Source directory containing .docx files (default: course/docx-v2)",
    )
    parser.add_argument(
        "--dst",
        default=r"course\pdf",
        help="Destination directory for exported .pdf files (default: course/pdf)",
    )
    parser.add_argument(
        "--files",
        nargs="*",
        default=None,
        help="Optional specific filenames or glob patterns (e.g. 01-CoverOut.docx 09-*.docx)",
    )
    parser.add_argument(
        "--remove-highlights",
        action="store_true",
        help="Remove yellow review highlights in memory before exporting to PDF (without modifying .docx)",
    )
    args = parser.parse_args()
    export_docx_to_pdf(
        src_dir=args.src,
        dst_dir=args.dst,
        file_patterns=args.files,
        remove_highlights=args.remove_highlights,
    )

