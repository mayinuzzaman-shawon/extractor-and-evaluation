import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o"

# Folder paths for input pdf files and output json files and images
DATA_DIR = "data"
OUTPUT_DIR = "output"
