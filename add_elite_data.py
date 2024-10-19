import csv

char_l = []
with open("./data/elite_data/elite_data.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'char':
            continue
        char_l.append(row[0])

out = open("./data/elite_data/elite_data.csv", mode="a", encoding="utf-8", newline="")
writer = csv.writer(out)
with open('./data/elite_data/elite_data.txt', encoding='utf-8') as f:
    lines = f.readlines()
for l in lines:
    l = l.strip().split(' ')
    if len(l) == 1:
        star = l[0][-4]
    if len(l) == 10:
        if l[0] not in char_l:
            l.insert(1, star)
            print(l)
            writer.writerow(l)
