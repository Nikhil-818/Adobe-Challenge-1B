"""
Main execution script for Round 1B - Persona Driven PDF Intelligence.
Reads input JSON + PDFs, extracts and ranks relevant sections, builds final output.
"""

import os
import json
from app import pdf_parser, section_chunker, ranker, subsection_refiner, json_builder

INPUT_JSON_PATH = "../data/input/input.json"
PDF_DIR = "../data/input/pdfs"
OUTPUT_JSON_PATH = "../data/output/output.json"
MODEL_PATH = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    # Load metadata (persona, task, document list)
    with open(INPUT_JSON_PATH, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    persona_role = input_data["persona"]["role"]
    job_task = input_data["job_to_be_done"]["task"]
    pdf_filenames = [doc["filename"] for doc in input_data["documents"]]

    all_sections = []

    for filename in pdf_filenames:
        pdf_path = os.path.join(PDF_DIR, filename)
        parsed_pages = pdf_parser.extract_text_from_pdf(pdf_path)
        sections = section_chunker.chunk_sections(parsed_pages, filename)
        all_sections.extend(sections)

    # Combine persona + job
    prompt_text = f"{persona_role}: {job_task}"

    model = ranker.load_model(MODEL_PATH)
    ranked_sections = ranker.rank_sections(all_sections, prompt_text, model, top_k=5)

    refined = []
    for section in ranked_sections:
        refined_text = subsection_refiner.extract_best_paragraphs(
            section["section_text"], prompt_text, model
        )
        refined.append({
            "document": section["document"],
            "refined_text": refined_text,
            "page_number": section["page_number"]
        })

    # Write final output
    json_builder.write_output(
        OUTPUT_JSON_PATH,
        input_data,
        ranked_sections,
        refined
    )


if __name__ == "__main__":
    main()
