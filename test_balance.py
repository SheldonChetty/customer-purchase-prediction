import csv

target_col = 'purchase'
counts = {}
with open("d:/Hackathon/Dataset/customer_activity_dataset.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        val = row.get(target_col)
        if val in counts:
            counts[val] += 1
        else:
            counts[val] = 1

total = sum(counts.values())
for k, v in counts.items():
    print(f"Class {k}: {v/total*100:.2f}% ({v})")
