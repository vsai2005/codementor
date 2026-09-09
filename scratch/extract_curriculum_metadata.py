import re
import json

with open('frontend/lib/curriculum/curriculumData.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for days
# day_number: 1, title: "...", topic_name: "...", section_id: "...", estimated_minutes: 30, description: "...", concepts: [...]
day_blocks = re.findall(r'\{\s*day_number:\s*(\d+),\s*title:\s*"([^"]+)",\s*topic_name:\s*"([^"]+)",\s*section_id:\s*"([^"]+)",\s*estimated_minutes:\s*(\d+),\s*description:\s*"([^"]+)",\s*concepts:\s*\[(.*?)\]\s*\}', content, re.DOTALL)

print(f"Extracted {len(day_blocks)} days.")
days_data = []
for d in day_blocks:
    raw_concepts = d[6]
    concepts = [c.strip().strip('"').strip("'") for c in raw_concepts.split(',') if c.strip()]
    days_data.append({
        "day_number": int(d[0]),
        "title": d[1],
        "topic_name": d[2],
        "section_id": d[3],
        "estimated_minutes": int(d[4]),
        "description": d[5],
        "concepts": concepts
    })

with open('scratch/curriculum_160.json', 'w', encoding='utf-8') as f:
    json.dump(days_data, f, indent=2)

print("Saved scratch/curriculum_160.json successfully!")
