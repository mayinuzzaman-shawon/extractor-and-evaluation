# Home Inspection PDF Extraction and Evaluation Pipeline

## Overview

This project processes home inspection PDF reports to extract structured issue data using OpenAI’s GPT-4o model and evaluates the extraction quality against ground truth JSON annotations made with the help of another LLM namely Gemini.

---

## Project Structure

├── data/ # Input folder containing PDF files to process
├── output/ # Output folder where extracted JSON and images are saved
├── ground_truth/ # Folder with ground truth JSON files for evaluation
├── extract/ # Extraction pipeline code (PDF parsing and LLM parsing)
│ ├── llm_parser.py
│ └── pdf_parser.py
├── utils/ # Utility scripts (chunking text, file utils, JSON saving)
│ ├── chunk_text.py
│ ├── file_utils.py
│ └── save_json.py
├── config.py # Configuration for API keys, model name, and folders
├── evaluate.py # Evaluation pipeline using GPT-based quality assessment
├── main.py # Main script that executes PDF processing and extraction
├── requirements.txt # Python dependencies
└── README.md # documentation 

---

## Installation

1. Clone the repository:

```bash
git clone <repo-url>
cd <repo-folder>
Create and activate a Python virtual environment:

python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
Install dependencies:


pip install -r requirements.txt
Create a .env file in the root folder and add your OpenAI API key:

ini
Copy
Edit
OPENAI_API_KEY=your_openai_api_key_here
Configuration
config.py handles loading the API key from .env and sets constants for:

MODEL — OpenAI model to use (gpt-4o by default)

DATA_DIR — input PDF folder (data/)

OUTPUT_DIR — folder to save extracted JSON and images (output/)

Make sure your .env file contains a valid OpenAI API key.

Usage
1. Run the Extraction Pipeline
This reads PDFs from data/, extracts text and images, sends text to the GPT-4o model for issue extraction, and saves JSON and matched images to output/.


python main.py
Extracted JSON files will be saved as <pdf_filename>.json in output/.

Extracted images linked to issues will also be saved in output/.

2. Evaluate Extraction Quality
Compare the extracted JSON outputs against ground truth JSON files in ground_truth/.

python evaluate.py
This calls GPT-4o to provide a semantic assessment of extraction quality.

Prints evaluation reports per file.

Please run this evaluate.py file from your command line as it prints result there. 


Architecture and Design Decisions
PDF Parsing: Uses PyMuPDF (fitz) to extract text and images, capturing image captions from nearby text on the page.

Chunking: Text is chunked to avoid exceeding GPT model context limits before sending to the API.

LLM Extraction: GPT-4o model extracts issues following a strict JSON schema for consistency.

Image Matching: Captions from LLM output are matched to extracted images by substring matching to associate images with issues.

Evaluation: Uses an LLM-based evaluation prompt to assess completeness, content accuracy, and image association from a semantic perspective, beyond exact matches.

Modularity: Separate utility modules enable easy extension or replacement of components.

** Assumptions **
- PDF preprocessing (text + image extraction) is reliable and complete even tho the accuracy rate is not satisfactory fo all pdf files, but the ground truth wasn't prepared manually.

- Ground truth JSON files are generated with the help of Gemini as the PDF files were too lengthy for preparing groud truth manually and follow the same schema as extraction output.

- JSON filenames in output/ and ground_truth/ correspond exactly for evaluation.

- OpenAI API key is set correctly in .env.

** Next Steps and Improvements **

- Incorporate semantic similarity metrics for finer evaluation without relying fully on GPT 4o model.

- Build a simple web UI for easier user interaction.

- Manually preparing the ground truth.
