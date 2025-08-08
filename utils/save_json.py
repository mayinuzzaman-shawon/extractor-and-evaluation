import json
import os

# Function to get output in JSON format
def save_output_as_json(json_data, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json_data)
