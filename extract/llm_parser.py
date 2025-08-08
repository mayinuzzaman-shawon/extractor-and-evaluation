import openai
import json
import re
import tiktoken
from config import OPENAI_API_KEY, MODEL

openai.api_key = OPENAI_API_KEY

def split_text_into_token_chunks(text, max_tokens=120000, model="gpt-4o"):
    """
    Splits text into chunks based on token count to avoid hitting model context limits.
    """
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)

    chunks = []
    while len(tokens) > max_tokens:
        chunk_tokens = tokens[:max_tokens]
        chunks.append(enc.decode(chunk_tokens))
        tokens = tokens[max_tokens:]
    chunks.append(enc.decode(tokens))
    return chunks

def extract_issues_with_llm(full_report_text, image_names):
    chunks = split_text_into_token_chunks(full_report_text)
    all_issues = []

    for idx, chunk in enumerate(chunks):
        print(f"Sending chunk {idx + 1}/{len(chunks)} to OpenAI...")

        prompt = f"""
You are an expert building inspection report parser.

Only extract *issues* that are clearly described in the following text chunk. Follow this schema:

- report_name
- issue_name
- issue_type
- issue_description
- issue_summary
- additional_information
- issue_images (imaage caption same as issue name)

### Report Text (chunk {idx+1}/{len(chunks)}):
{chunk}

### Images:
{", ".join(image_names[:5])}

Return ONLY a valid JSON array of issues. Do NOT include markdown formatting or extra explanations.
"""

        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You extract structured issues from reports and return only raw JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )

            output = response["choices"][0]["message"]["content"].strip()

            if not output:
                print(f"Empty response for chunk {idx+1}. Skipping.")
                continue

            output = re.sub(r"^```(?:json)?\n?", "", output)
            output = re.sub(r"\n?```$", "", output)

            try:
                parsed_chunk = json.loads(output)
                if isinstance(parsed_chunk, list):
                    all_issues.extend(parsed_chunk)
                else:
                    print(f"Chunk {idx+1} did not return a list.")
            except Exception as e:
                print(f"Failed to parse chunk {idx + 1}: {e}")
                print(f"Cleaned response: {output[:300]}...")
                continue

        except openai.error.OpenAIError as e:
            print(f"OpenAI API error for chunk {idx+1}: {e}")
            continue

    return json.dumps(all_issues, indent=2)
