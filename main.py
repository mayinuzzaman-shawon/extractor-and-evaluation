import os
import json
from difflib import SequenceMatcher

from extract.pdf_parser import extract_pdf_content
from extract.llm_parser import extract_issues_with_llm
from utils.file_utils import get_pdf_files
from config import DATA_DIR, OUTPUT_DIR

def find_best_matching_image(caption, image_data):
    """
    Try to match an image by checking if the caption and image description overlap.
    """
    if not caption:
        return None

    clean_caption = caption.lower().strip()

    for filename, meta in image_data.items():
        image_caption = meta.get("caption", "").lower().strip()

        # Check for substring match in image caption
        if clean_caption in image_caption or image_caption in clean_caption:
            print(f"Matched caption: '{caption}' - '{image_caption}'")
            return filename

    print(f"No match found for caption: '{caption}'")
    return None


def process_pdf(pdf_path):
    print(f"\nProcessing: {pdf_path}")

    report_text, image_data = extract_pdf_content(pdf_path)

    image_descriptions = [
        f"{filename}: {meta['caption'] or 'No caption'}"
        for filename, meta in image_data.items()
    ]

    json_str = extract_issues_with_llm(report_text, image_descriptions)

    try:
        issue_data = json.loads(json_str)
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        print(f"Raw output: {json_str[:300]}...")
        return

    # Save structured JSON to file
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_path = os.path.join(OUTPUT_DIR, f"{pdf_name}.json")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(issue_data, f, indent=2)

    print(f"JSON saved: {json_path}")

    # Extract and save images associated with each issue
    matched_images = set()

    for issue in issue_data:
        issue_images = issue.get("issue_images", [])
        if isinstance(issue_images, str):
            issue_images = [issue_images]

        for img_caption in issue_images:
            best_match = find_best_matching_image(img_caption, image_data)
            if best_match and best_match not in matched_images:
                image_bytes = image_data[best_match]["bytes"]

                pdf_name_base = os.path.splitext(os.path.basename(pdf_path))[0]

                issue_name = issue['issue_name'].strip().lower().replace(" ", "_").replace("/", "_")

                img_ext = os.path.splitext(best_match)[1]

                safe_filename = f"{pdf_name_base}_{issue_name}{img_ext}"

                image_path = os.path.join(OUTPUT_DIR, safe_filename)

                with open(image_path, "wb") as f:
                    f.write(image_bytes)

                matched_images.add(best_match)
                print(f"Saved image '{safe_filename}' for issue: {issue['issue_name']}")
            else:
                print(f"No matching image found for caption: '{img_caption}'")
    


def main():
    pdf_files = get_pdf_files(DATA_DIR)
    for pdf in pdf_files:
        process_pdf(pdf)

if __name__ == "__main__":
    main()
