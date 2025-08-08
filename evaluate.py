import os
from dotenv import load_dotenv
import openai
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def make_prompt(gt_issues, ext_issues):
    return f"""
You are an expert evaluator assessing the quality of extracted data from a PDF home inspection report.

Ground truth issues:
{json.dumps(gt_issues, indent=2)}

Extracted issues:
{json.dumps(ext_issues, indent=2)}

Please evaluate the extraction accuracy with respect to:

1. Extraction completeness: What percentage of the ground truth issues were extracted? Rate from 0 to 100.
2. Content accuracy: How well do the extracted issue fields match the ground truth? Rate from 0 to 100.
3. Image association: How accurately are images matched to their issues? Rate from 0 to 100.

Return your evaluation ONLY as a JSON object with these keys exactly:

{{
  "extraction_completeness": float,
  "content_accuracy": float,
  "image_association_accuracy": float,
  "comments": string 
}}
"""

def evaluate_with_gpt(gt_issues, ext_issues):
    prompt = make_prompt(gt_issues, ext_issues)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a strict JSON generator. Return only valid JSON with no extra text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        text = response['choices'][0]['message']['content'].strip()

        # Try parsing as JSON directly
        try:
            result = json.loads(text)
        except json.JSONDecodeError:
            # extract JSON substring from messy text
            import re
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                result = json.loads(match.group(0))
            else:
                raise ValueError("No JSON object found in GPT output")

        return result

    except Exception as e:
        print("Error during GPT evaluation:", e)
        return None


def main():
    gt_folder = "ground_truth"
    out_folder = "output"
    reports = {}

    gt_files = [f for f in os.listdir(gt_folder) if f.endswith('.json')]
    print(f"Found {len(gt_files)} ground truth files")

    for gt_file in gt_files:
        print(f"Processing file: {gt_file}")
        gt_path = os.path.join(gt_folder, gt_file)
        out_path = os.path.join(out_folder, gt_file)

        if not os.path.exists(out_path):
            print(f"Output file missing for {gt_file}, skipping...")
            continue

        gt_data = load_json(gt_path)
        out_data = load_json(out_path)

        report = evaluate_with_gpt(gt_data, out_data)
        reports[gt_file] = report

        print(f"LLM Evaluation Report for {gt_file}:")
        print(json.dumps(report, indent=2))
        print("\n" + "-"*40 + "\n")

    # Save all results to a single JSON file
    eval_output_path = "evaluation_results.json"
    with open(eval_output_path, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2)

    print(f"LLM-based evaluation complete! Results saved to {eval_output_path}")


if __name__ == "__main__":
    main()
