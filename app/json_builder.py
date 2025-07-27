"""
Builds the output JSON structure with metadata, section ranking and refined analysis.
"""

import json
from datetime import datetime


def write_output(output_path, input_data, ranked_sections, refined_subsections):
    output = {
        "metadata": {
            "input_documents": [d["filename"] for d in input_data["documents"]],
            "persona": input_data["persona"]["role"],
            "job_to_be_done": input_data["job_to_be_done"]["task"],
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": [
            {
                "document": sec["document"],
                "section_title": sec["section_title"],
                "importance_rank": sec["importance_rank"],
                "page_number": sec["page_number"]
            }
            for sec in ranked_sections
        ],
        "subsection_analysis": refined_subsections
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
