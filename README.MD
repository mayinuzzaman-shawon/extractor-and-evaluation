# Home Inspection PDF Extraction and Evaluation Pipeline

## Overview
This project processes **home inspection PDF reports** to extract **structured issue data** using **OpenAI’s GPT-4o** model.  
It then **evaluates the extraction quality** against **ground truth JSON annotations**, which were generated with the help of another LLM, **Google Gemini**.

---

## Project Structure


```
├── data/               # Input folder containing PDF files to process
├── output/             # Output folder where extracted JSON and images are saved
├── ground_truth/       # Folder with ground truth JSON files for evaluation
├── extract/            # Extraction pipeline code (PDF parsing and LLM parsing)
│   ├── llm_parser.py
│   └── pdf_parser.py
├── utils/              # Utility scripts (chunking text, file utils, JSON saving)
│   ├── chunk_text.py
│   ├── file_utils.py
│   └── save_json.py
├── config.py           # Configuration for API keys, model name, and folders
├── evaluate.py         # Evaluation pipeline using GPT-based quality assessment
├── main.py             # Main script that executes PDF processing and extraction
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```


## Installation

1. **Install dependencies**  
   ```bash
   pip install -r requirements.txt

Create a .env file in the root folder and add your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here


## Configuration

`config.py` handles loading environment variables and sets constants for:

 **MODEL** — OpenAI model to use (**gpt-4o** by default)  
- **DATA_DIR** — Input PDF folder (`data/`)  
- **OUTPUT_DIR** — Folder to save extracted JSON and images (`output/`)  

Make sure the `.env` file contains a valid OpenAI API key.

---

## Usage

1️. Run the Extraction Pipeline  
Reads PDFs from `data/`, extracts text and images, sends text to **GPT-4o** for issue extraction, and saves results to `output/`:

```bash
python main.py
```
- Extracted JSON files will be saved as <pdf_filename>.json in output/.
- Extracted images linked to issues will also be saved in output/.

 2. Evaluate Extraction Quality
Compare the extracted JSON outputs against ground truth JSON files (randomly 3 pdf files were selected for evaluation) in ground_truth/.


```bash
python evaluate.py
```
- This calls GPT-4o to provide a semantic assessment of extraction quality.
- Prints evaluation reports per file.

Please run this evaluate.py file from your command line as it prints result there. 


## Architecture and Design Decisions

- **PDF Parsing** — Uses **PyMuPDF (fitz)** to extract text and images, capturing image captions from nearby text on the page.  
- **Chunking** — Splits text into manageable chunks to avoid exceeding GPT model context limits before sending to the API.  
- **LLM Extraction** — Uses the **GPT-4o** model to extract issues following a strict JSON schema for consistency.  
- **Image Matching** — Matches captions from LLM output to extracted images by substring matching to associate images with issues.  
- **Evaluation** — Uses an LLM-based evaluation prompt to assess:
  - Extraction completeness  
  - Content accuracy  
  - Image association accuracy  
  beyond exact string matches.  
- **Modularity** — Separate utility modules enable easy extension or replacement of components.

---

## Assumptions

- PDF preprocessing (**text + image extraction**) is reliable and complete, though accuracy is not perfect for all PDF files.  
- Ground truth JSON files are generated with the help of **Gemini**, since PDFs were too lengthy to manually annotate.  
- Ground truth files follow the **same schema** as extraction output.  
- JSON filenames in `output/` and `ground_truth/` correspond exactly for evaluation.  
- The **OpenAI API key** is set correctly in `.env`.

---

## Next Steps & Improvements

- Incorporate **semantic similarity metrics** for finer evaluation without fully relying on GPT-4o.  
- Build a simple **web UI** for easier interaction.  
- Manually prepare the **ground truth** for higher-quality evaluation.
