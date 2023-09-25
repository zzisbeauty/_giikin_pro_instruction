import json, random

# todo sava data to NELLE
with open('all_train_human_enhancedata_all.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    random.shuffle(lines)

parsers2belle = []
for line in lines:
    eachLine = eval(line)
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

dev = random.sample(parsers2belle, 300)
train = [i for i in parsers2belle if i not in dev]

with open('all_train_human_enhancedata_all_belle.json', 'w', encoding='utf-8') as f:
    json.dump(train, f, indent=4, ensure_ascii=False)

with open('all_train_human_enhancedata_all_belle.dev.json', 'w', encoding='utf-8') as f:
    json.dump(dev, f, indent=4, ensure_ascii=False)
