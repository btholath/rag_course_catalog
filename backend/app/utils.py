### backend/app/utils.py
import fitz  # PyMuPDF
from sentence_splitter import SentenceSplitter

splitter = SentenceSplitter(language='en')

def extract_chunks_from_pdf(file_path, min_len=100):
    chunks = []
    doc = fitz.open(file_path)
    for page_num, page in enumerate(doc):
        text = page.get_text()
        if len(text.strip()) < min_len:
            continue
        sentences = splitter.split(text)
        for chunk in sentences:
            if chunk.strip():
                chunks.append((chunk, page_num + 1))
    return chunks
