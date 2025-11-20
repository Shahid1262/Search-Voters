import os, shutil, pytesseract
from pdf2image import convert_from_path
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID

PDF_FOLDER = "pdfs"
INDEX_FOLDER = "index"

schema = Schema(
    file=ID(stored=True),
    page=ID(stored=True),
    content=TEXT(stored=True)
)

if os.path.exists(INDEX_FOLDER):
    shutil.rmtree(INDEX_FOLDER)

os.makedirs(INDEX_FOLDER, exist_ok=True)
ix = create_in(INDEX_FOLDER, schema)
writer = ix.writer()

print("Building OCR index…")

for pdf in sorted(os.listdir(PDF_FOLDER)):
    if not pdf.endswith(".pdf"):
        continue

    print("Processing:", pdf)
    path = os.path.join(PDF_FOLDER, pdf)

    pages = convert_from_path(path, dpi=250)

    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page, lang="hin+mar+eng")
        writer.add_document(
            file=pdf,
            page=str(i+1),
            content=text
        )

writer.commit()

print("Index building complete!")
