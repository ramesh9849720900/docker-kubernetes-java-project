import os
import json

issues = {}

def analyze_code(folder):
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith(".java") or f.endswith(".py"):
                path = os.path.join(root, f)

                with open(path) as file:
                    code = file.read()

                problems = []

                if "System.out.println" in code:
                    problems.append("Debug print found")

                if "TODO" in code:
                    problems.append("TODO comment found")

                if len(code) > 5000:
                    problems.append("File too large")

                if problems:
                    issues[path] = problems

    with open("ai_report.json","w") as out:
        json.dump(issues,out,indent=2)

analyze_code("src")
