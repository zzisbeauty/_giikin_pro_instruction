import json, jsonlines

# todo  check  enhance  data
# with open('enhanceData.jsonl', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#
#     tag = True
#
#     for idx, _ in enumerate(lines):
#         i = eval(_)
#         if len(i) != 4:
#             print(idx, '######################======================')
#
#         if len(i['conversation']) % 2 != 0:
#             print(idx, '**********************')
#         if i['conversation'][-1]['from'] == 'human':
#             print(idx, '######################')
#
#         for idx_, __ in enumerate(i['conversation']):
#             if idx_ % 2 == 0 and __['from'] != 'human':
#                 print(idx, '-----------')
#                 # continue
#             if idx_ % 2 != 0 and __['from'] != 'assistant':
#                 print(idx, '===========================')
#                 # continue
#
#             # if __['from'] != 'human' or __['from'] != 'assistant':
#             #     print(idx, '+++++++++++++++++++++++++++++++++')

# todo check human data
pass

# ====================================================================================================

# todo trans enhance data to std format for ly
enhancedata = r'G:\_giikin_pro_instruction\instructionfordataenhance\enhanceData.jsonl'
correct_enhance_data = 'correct_enhance_data.jsonl'

stdhumandata = r'G:\_giikin_pro_instruction\instructionfordataenhance\sdtconvdatahuman.json'
correct_human_data = 'correct_human_data.jsonl'

with open(enhancedata, 'r', encoding='utf-8') as f:
    data = json.load(f)
    parsers = []
    for idx, edata in enumerate(data):
        one_convs = {}
        one_convs['conversation_id'] = edata['id']
        one_convs['conversation'] = []
        convs = edata['conversations']
        if len(convs) % 2 == 0:
            oneroundConv = {}
            one_rounds = [convs[i:i + 2] for i in range(0, len(convs), 2)]
            for one in one_rounds:
                oneroundConv['human'] = one[0]['value']
                oneroundConv['assistant'] = one[1]['value']
                one_convs['conversation'].append(oneroundConv)
                oneroundConv = {}
            parsers.append(one_convs)

for i in parsers:
    i['dataset'] = 'giikin'
    with jsonlines.open(correct_enhance_data, mode='a') as writer:
        writer.write(i)
    # with open('giikin_train_data.jsonl', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, indent=4, ensure_ascii=False)
