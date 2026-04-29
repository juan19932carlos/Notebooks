#!/Users/juangama/workspace/personal/Notebooks/.venv/bin/python3
try:
    import Crypto
except ImportError:
    print("PyCryptodome is required for AES-encrypted PDFs. Install it with: pip install pycryptodome")
    exit(1)

import sys
import os
from pypdf import PdfReader, PdfWriter

def remove_pdf_password(pdf_path, password):
    # Read the encrypted PDF
    with open(pdf_path, "rb") as infile:
        reader = PdfReader(infile)
        if reader.is_encrypted:
            try:
                reader.decrypt(password)
            except Exception as e:
                print(f"Failed to decrypt PDF: {e}")
                return

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        # Output file name
        base, ext = os.path.splitext(pdf_path)
        output_path = f"{base}-no-pass{ext}"

        with open(output_path, "wb") as outfile:
            writer.write(outfile)
        print(f"Decrypted PDF saved as: {output_path}")

def process_folder(folder_path, password):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            answer = input(f"Process '{filename}'? [Y/n]: ").strip().lower()
            if answer in ("", "y", "yes"):
                remove_pdf_password(pdf_path, password)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python remove-pdf-password.py <pdf_path|folder_path> <password>")
        sys.exit(1)
    path = sys.argv[1]
    password = sys.argv[2]
    if os.path.isdir(path):
        process_folder(path, password)
    else:
        remove_pdf_password(path, password)