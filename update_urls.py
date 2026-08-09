import json
import re

def slugify(text):
    # special case for pow
    if text.lower() == "pow(x, n)":
        return "powx-n"
    # replace non-alphanumeric with dashes
    slug = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return slug

with open('questions.json', 'r') as f:
    questions = json.load(f)

for q in questions:
    q['url'] = f"https://leetcode.com/problems/{slugify(q['title'])}/"

with open('questions.json', 'w') as f:
    json.dump(questions, f, indent=4)
print("Updated questions.json with URLs.")
