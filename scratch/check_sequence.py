import json

with open("scratch/curriculum_160.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Days 26 to 50:")
for d in data[25:50]:
    print(f"Day {d['day_number']}: {d['title']}")

print("\nDays 101 to 120:")
for d in data[100:120]:
    print(f"Day {d['day_number']}: {d['title']}")

print("\nDays 121 to 140:")
for d in data[120:140]:
    print(f"Day {d['day_number']}: {d['title']}")

print("\nDays 141 to 160:")
for d in data[140:160]:
    print(f"Day {d['day_number']}: {d['title']}")
