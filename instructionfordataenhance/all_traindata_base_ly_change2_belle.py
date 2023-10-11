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

parsers2belle = []
for eachLine in lines:
    # eachLine = eval(eachLine)  # for  *.jsonl format data file
    allconvs = eachLine['conversation']

    # 每一个对话一个 {}，包含如下字段
    allConvInfo = {}
    allConvInfo['id'] = eachLine['conversation_id']
    allConvInfo['conversations'] = []

    for i in allconvs:
        tmp_human, tmp_assis = {}, {}
        tmp_human['from'] = 'human'
        tmp_human['value'] = i['human']
        allConvInfo['conversations'].append(tmp_human)
        tmp_assis['from'] = 'assistant'
        tmp_assis['value'] = i['assistant']
        allConvInfo['conversations'].append(tmp_assis)

    parsers2belle.append(allConvInfo)

# todo 读取 BELLE 的 format instruction  data
with open('train_instdata.belle.batch.1.json', 'r', encoding='utf-8') as f:
    belle_inst_data = json.load(f)

parsers2belle = parsers2belle + belle_inst_data
random.shuffle(parsers2belle)

# bl format data
dev = random.sample(parsers2belle, 30)
train = [i for i in parsers2belle if i not in dev]
with open('all_train_human_enhancedata_all_belle.version.2.train.json', 'w', encoding='utf-8') as f:
    json.dump(train, f, indent=4, ensure_ascii=False)
with open('all_train_human_enhancedata_all_belle.version.2.dev.json', 'w', encoding='utf-8') as f:
    json.dump(dev, f, indent=4, ensure_ascii=False)
