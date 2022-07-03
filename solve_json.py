from utils import data
import json

dic = open('../ArknightsGameData/zh_CN/gamedata/excel/activity_table.json', encoding='utf-8')
jdic = json.load(dic)
dic.close()

write2 = open('tmp.txt', mode='w', encoding='utf-8')

data.solve_dict('', jdic, write2, extract_ch=True)

write2.close()
