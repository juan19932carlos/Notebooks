#!/Users/juangama/workspace/personal/Notebooks/.venv/bin/python3
import sys
import os
from pypdf import PdfReader, PdfWriter


def parse_page_ranges(range_str, total_pages):
    pages = []
    for token in range_str.split(","):
        token = token.strip()
        if not token:
            continue
        if "-" in token:
            parts = token.split("-", 1)
            try:
                start, end = int(parts[0]), int(parts[1])
            except ValueError:
                print(f"Invalid range: '{token}'")
                sys.exit(1)
            if start < 1 or end < 1:
                print(f"Page numbers must be >= 1, got '{token}'")
                sys.exit(1)
            if start > end:
                print(f"Range start must be <= end, got '{token}'")
                sys.exit(1)
            if end > total_pages:
                print(f"Page {end} exceeds total page count ({total_pages})")
                sys.exit(1)
            for p in range(start, end + 1):
                if p not in pages:
                    pages.append(p)
        else:
            try:
                p = int(token)
            except ValueError:
                print(f"Invalid page number: '{token}'")
                sys.exit(1)
            if p < 1:
                print(f"Page numbers must be >= 1, got '{token}'")
                sys.exit(1)
            if p > total_pages:
                print(f"Page {p} exceeds total page count ({total_pages})")
                sys.exit(1)
            if p not in pages:
                pages.append(p)
    return pages


def cut_pdf(pdf_path, range_str):
    if not os.path.isfile(pdf_path):
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)

    selected = parse_page_ranges(range_str, total_pages)
    if not selected:
        print("No pages selected.")
        sys.exit(1)

    writer = PdfWriter()
    for p in selected:
        writer.add_page(reader.pages[p - 1])

    base, ext = os.path.splitext(pdf_path)
    output_path = f"{base}-cut{ext}"

    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"Saved {len(selected)} page(s) to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python cut-pdf.py <pdf_path> <pages>")
        print("  pages: comma-separated ranges, e.g. 1-4,7-9")
        sys.exit(1)
    cut_pdf(sys.argv[1], sys.argv[2])
