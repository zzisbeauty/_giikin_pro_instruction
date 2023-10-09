# 将标注的all_train_human_enhancedata_all_intentslot.batch.1.json data 转化为 BELLE 的 instruction data
import json

with open('all_train_human_enhancedata_all_intentslot.batch.1.json', 'r', encoding='utf-8') as f:
    inst_data = json.load(f)

allinstdata = []
for idx, i in enumerate(inst_data):
    tmp = {}
    k = list(i.keys())[0]
    v = list(i.values())[0]

    inst_res, intent_slots_name = '', list(v.keys())
    # intent_slots_value = list(v.values())
    if intent_slots_name:  # 用户的信息中有可能的intent or slot 信息
        if '意图' in intent_slots_name and len(intent_slots_name) == 1:  # 用户的话只有意图信息
            intent = v['意图']
            inst_res = f"根据给定文本，用户当前输入的信息想要表达的意图为：{intent}。没有包含任何额外的实体信息。"
        if '意图' in intent_slots_name and len(intent_slots_name) != 1:  # 不仅仅包含意图，还包含其它实体信息
            intent = v.pop('意图')
            inst_res = f"根据给定文本，用户当前输入的信息想要表达的意图为：{intent}。另外还包含了如下实体信息：{v}"
        if '意图' not in intent_slots_name:  # 用户的话意图为空且用户的实体信息不为空，说明用户的话中没有意图，而且还包含了其它的实体信息
            inst_res = f"根据给定文本，用户当前输入的信息并不包含任何明确的意图信息。但是包含如下实体信息：{v}。"
    else:
        inst_res = '根据给定文本，用户当前输入的信息不包含任何明确的意图信息，且不包含任何其它实体信息。'

    tmp['id'] = str(idx)
    tmp['conversations'] = []
    tmp['conversations'].append(
        {
            'from': 'human',
            'value': k
        }
    )
    tmp['conversations'].append(
        {
            'from': "assistant",
            'value': inst_res
        }
    )
    allinstdata.append(tmp)

with open('train_instdata.belle.batch.1.json', 'w', encoding='utf-8') as f:
    json.dump(allinstdata, f, indent=4, ensure_ascii=False)
