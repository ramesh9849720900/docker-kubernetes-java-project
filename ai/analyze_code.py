import os
import json
from transformers import pipeline

def analyze_code(folder):
    analyzer = pipeline("text-generation", model="gpt2")
    results = {}

    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith(".java") or f.endswith(".py"):
                path = os.path.join(root, f)
                with open(path, "r") as file:
                    code = file.read()

                ai_output = analyzer(f"Analyze this code: {code}", max_length=200)[0]['generated_text']
                results[path] = ai_output

    with open("ai_output.json", "w") as out:
        json.dump(results, out, indent=2)

if __name__ == "__main__":
    analyze_code("src")
