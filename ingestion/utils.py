# ingestion/utils.py

import fitz  # PyMuPDF
from sentence_splitter import SentenceSplitter

splitter = SentenceSplitter(language='en')

def extract_text_chunks_from_pdf(file_path, min_length=100):
    """Extracts and splits meaningful text chunks from each page of a PDF."""
    chunks = []
    doc = fitz.open(file_path)
    for page_num, page in enumerate(doc):
        text = page.get_text()
        if len(text.strip()) < min_length:
            continue
        sentences = splitter.split(text)
        for chunk in sentences:
            if chunk.strip():
                chunks.append((chunk, page_num + 1))
    return chunks
