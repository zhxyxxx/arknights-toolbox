import json
import csv

anni = 6.5
pre_anni = anni - 0.5

def anni_to_file(anni):
    if anni * 10 % 10 == 0:
        return anni
    else:
        return anni * 10

char_file = '../ArknightsGameData/zh_CN/gamedata/excel/character_table.json'
char_list = [['char', 'star', 'item1', 'num1', 'item2', 'num2', 'item3', 'num3', 'item4', 'num4', 'time']]

item_file = '../ArknightsGameData/zh_CN/gamedata/excel/item_table.json'
with open(item_file, encoding='utf-8') as f:
    item_dic = json.load(f)['items']
item_id2name = {}
for k, v in item_dic.items():
    item_id2name[k] = v['name']

prev_char = []
with open(f"./data/elite_data/elite_data_{anni_to_file(pre_anni)}.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'char':
            continue
        prev_char.append(row[0])

with open(char_file, encoding='utf-8') as f:
    char_dic = json.load(f)

for k,v in char_dic.items():
    if k[:4] == 'char':
        charid = k
        char_name = v['name']
        obtainable = not v['isNotObtainable']
        star = v['rarity'][-1]
        if obtainable and int(star) >= 4:
            if v['spTargetType'] != 'NONE': # 电弧
                # print(k, char_name, v['spTargetType'])
                continue
            phases1 = v['phases'][1]
            material1 = phases1['evolveCost'][1]
            mat1_name = item_id2name[material1['id']]
            mat1_num = material1['count']
            material2 = phases1['evolveCost'][2]
            mat2_name = item_id2name[material2['id']]
            mat2_num = material2['count']
            phases2 = v['phases'][2]
            material3 = phases2['evolveCost'][1]
            mat3_name = item_id2name[material3['id']]
            mat3_num = material3['count']
            material4 = phases2['evolveCost'][2]
            mat4_name = item_id2name[material4['id']]
            mat4_num = material4['count']
            if char_name not in prev_char:
                time = 'new'
            else:
                time = '-'
            char_list.append([char_name, star, mat1_name, mat1_num, mat2_name, mat2_num, mat3_name, mat3_num, mat4_name, mat4_num, time])

# print(char_list)

with open(f"./data/elite_data/elite_data_{anni_to_file(anni)}.csv", mode="w", encoding="utf-8", newline="") as out:
    writer = csv.writer(out)
    writer.writerows(char_list)
