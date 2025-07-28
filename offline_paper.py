import os
import fitz  
import nltk
import json
from datetime import datetime
from nltk.tokenize import sent_tokenize


nltk.download('punkt')

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "summary.json")

PERSONA = "PhD Researcher in Computational Biology"
JOB = "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"

def extract_sections_from_pdf(file_path):
    doc = fitz.open(file_path)
    extracted = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        if any(keyword in text.lower() for keyword in ["method", "dataset", "benchmark"]):
            importance = 1 if "method" in text.lower() else 2
            extracted.append({
                "document": os.path.basename(file_path),
                "page": page_num,
                "section_title": f"Possible Relevant Section (Page {page_num})",
                "importance_rank": importance
            })
    return extracted

def get_refined_text(file_path, page_num):
    doc = fitz.open(file_path)
    page_text = doc[page_num - 1].get_text()
    sentences = sent_tokenize(page_text)
    return " ".join(sentences[:3])

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    input_pdfs = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]

    all_extracted_sections = []
    subsection_analysis = []

    for pdf in input_pdfs:
        extracted = extract_sections_from_pdf(pdf)
        all_extracted_sections.extend(extracted)

        for section in extracted:
            refined = get_refined_text(pdf, section["page"])
            subsection_analysis.append({
                "document": section["document"],
                "page_number": section["page"],
                "refined_text": refined
            })

    output = {
        "metadata": {
            "input_documents": [os.path.basename(p) for p in input_pdfs],
            "persona": PERSONA,
            "job_to_be_done": JOB,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": all_extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
