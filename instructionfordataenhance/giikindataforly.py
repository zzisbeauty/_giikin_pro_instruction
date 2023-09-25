import json, jsonlines

# todo  check  enhance  data
with open('check.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

parsers = []
lines = filter(lambda x: len(eval(x)['conversation']) % 2 == 0, lines)  # 过滤器可以过滤【得到】lambda 表示的内容
for idx, i in enumerate(lines):
    parsers.append(eval(i))

for idx, i in enumerate(parsers):
    if (i['conversation'][0]['from'] != 'human') and (i['conversation'][0]['from'] == 'user'):
        print(idx, 'not start with human and start with user')

for idx in range(len(parsers) - 1, -1, -1):
    eachidxConv = parsers[idx]['conversation']
    for idx_, __ in enumerate(eachidxConv):
        if idx_ % 2 == 0 and __['from'] != 'human':
            parsers.remove(parsers[idx])
            print(f'parsers {idx} conversation is removed by human')
            break

for idx in range(len(parsers) - 1, -1, -1):
    eachidxConv = parsers[idx]['conversation']
    for idx_, __ in enumerate(eachidxConv):
        if idx_ % 2 != 0 and __['from'] != 'assistant':
            parsers.remove(parsers[idx])
            print(f'parsers {idx} conversation is removed by assistant')
            break

# todo check human data
pass
A = 1

# ====================================================================================================

# # todo trans enhance data to std format for ly
# enhancedata = r'G:\_giikin_pro_instruction\instructionfordataenhance\enhanceData.jsonl'
# stdhumandata = r'G:\_giikin_pro_instruction\instructionfordataenhance\sdtconvdatahuman.json'
correct_enhance_data = 'correct_enhance_data.jsonl'
correct_human_data = 'correct_human_data.jsonl'

final_parsers = []
for idx, edata in enumerate(parsers):
    one_convs = {}
    one_convs['conversation_id'] = edata['id']
    one_convs['conversation'] = []
    convs = edata['conversation']
    if len(convs) % 2 == 0:
        oneroundConv = {}
        one_rounds = [convs[i:i + 2] for i in range(0, len(convs), 2)]
        for one in one_rounds:
            oneroundConv['human'] = one[0]['value']
            oneroundConv['assistant'] = one[1]['value']
            one_convs['conversation'].append(oneroundConv)
            oneroundConv = {}
        final_parsers.append(one_convs)

for i in final_parsers:
    i['dataset'] = 'giikin'
    with jsonlines.open(correct_enhance_data, mode='a') as writer:
        writer.write(i)

a = 10
# ====================================================================================================
