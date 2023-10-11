# todo 将 LY 格式数据（这个格式也是标注的格式）转化为BL需要的格式数据
import json, random

# # LY format data
# # todo change LY data 2 BL data and save data with NELLE format   -  jsonl
# with open('all_train_human_enhancedata_all.jsonl', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     random.shuffle(lines)

# todo change LY data 2 BL data and save data with BELLE format   -  json
with open('all_train_human_enhancedata_all_conv.batch.1.json', 'r', encoding='utf-8') as f:
    lines = json.load(f)
    random.shuffle(lines)

# todo version-2 人工标注数据  （ly format data，读取后，准备转化为BL数据）
with open('sdtconvdatahuman_1007.json', 'r', encoding='utf-8') as f:
    lines_human = json.load(f)
    random.shuffle(lines_human)

lines = lines_human + lines

# # todo save data for LY
# random.shuffle(lines)
# with open('all_train_human_enhancedata_all_ly.json', 'w', encoding='utf-8') as f:
#     json.dump(lines, f, indent=4, ensure_ascii=False)
