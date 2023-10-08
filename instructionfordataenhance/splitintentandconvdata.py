# todo 拆分最原始的intent slot conv 标注数据
import json, jsonlines, re, gc

with open('all_train_human_enhancedata_all.jsonl', 'r', encoding='utf-8') as f:
    merdata = f.readlines()

    new_parsers = []
    prompts = []  # 用来存储intent slot抽取指令数据信息
    for idx, i in enumerate(merdata):  # all conversations
        mergei = eval(i)  # 每一轮多轮对话

        # 用来存储最新的训练对话数据信息
        newconvsdata = {}  # 移除了intent + slot 信息的对话数据
        newconvsdata['conversation_id'] = str(idx)
        newconvsdata['conversation'] = []
        for idx_, eachconv in enumerate(mergei['conversation']):  # 处理每一个完整的多轮对话中的每一个轮次信息
            newconvdataonerount = {}  # 【单轮】：用来存储更新过的 pure conv round data
            each_round_in_user_slot_intent_data = {}  # 用来存储每一轮对话中用户发送的信息中携带的 slot 和 intent 信息

            # 原始的单轮对话信息
            human = eachconv['human']
            assistant = eachconv['assistant']

            # 清洗出来slot 和 intent 信息
            rereg = re.findall(".*{(.*)}.*", assistant)
            todisplay = []
            for eachre in rereg:
                if '，' in eachre:
                    eachre = eachre.replace('，', ',')
                if '：' in eachre:
                    eachre = eachre.replace('：', ':')
                todisplay.append('{' + eachre + '}')
            for eachre in todisplay:
                assistant = assistant.replace(eachre, '')
            todisplaydict = {}
            for each in todisplay:
                tmp = eval(each)
                k = list(tmp.keys())[0]
                v = list(tmp.values())[0]
                if k == 'intent':
                    todisplaydict['意图'] = v
                if k == 'goods':
                    todisplaydict['商品'] = v
                if k == 'phone':
                    todisplaydict['电话号'] = v
                if k == 'name':
                    todisplaydict['姓名'] = v
                if k == 'count':
                    todisplaydict['数量'] = v
                if k == 'style':
                    todisplaydict['款式'] = v
                if k == 'code':
                    todisplaydict['订单号'] = v
                if k == 'bank':
                    todisplaydict['银行'] = v
                if k == 'account':
                    todisplaydict['银行户号'] = v
                if k == 'height':
                    todisplaydict['身高'] = v
                if k == 'weight':
                    todisplaydict['体重'] = v
                if k == 'city':
                    todisplaydict['城市'] = v
                if k == 'area':
                    todisplaydict['地区'] = v
                if k == 'street':
                    todisplaydict['街道'] = v
                if k == 'color':
                    todisplaydict['颜色'] = v

            if todisplaydict:
                prompt = f"给定文本：{human}。" \
                         f"首先是对该文本表示的意图进行分类，判断该文本属于以下意图中何种意图：[查询商品，询问运费，询问折扣，催促叮嘱，询问鉴赏期，" \
                         f"询问使用方式，查询订单，咨询收货方式，询问发货周期，查询发货物流，查询退货物流，咨询线下服务，询问商品品质，闲聊，修改订单，取消订单]。" \
                         f"其次是命名实体识别，从以下实体类型中识别文本中包含哪些实体：[电话号，姓名，商品，数量，款式，订单号，银行，银行户号，身高，体重，城市，地区，街道]。"
                # target = json.dumps(todisplaydict, ensure_ascii=False)
                # each_round_in_user_slot_intent_data[prompt] = target
                each_round_in_user_slot_intent_data[prompt] = todisplaydict
                prompts.append(each_round_in_user_slot_intent_data)
            else:
                print('当前轮次下，用户发送的信息中没有包含任何 intent 和 slot 信息')
                each_round_in_user_slot_intent_data[prompt] = '当前文本未包含任何意图和实体信息_' + str(idx) + '__' + str(idx_)
                prompts.append(each_round_in_user_slot_intent_data)
            del todisplay
            gc.collect()

            # 处理清洗后的对话信息
            if assistant.startswith(':'):
                assistant = assistant.replace(':', '')
            if assistant.startswith('：'):
                assistant = assistant.replace('：', '')
            newconvdataonerount['human'] = human
            newconvdataonerount['assistant'] = assistant
            newconvsdata['conversation'].append(newconvdataonerount)
            new_parsers.append(newconvsdata)

# 去重 convs
c = [json.dumps(i, ensure_ascii=False) for i in new_parsers]
d = list(set(c))

# 去重prompts
e = [json.dumps(i, ensure_ascii=False) for i in prompts]
f = list(set(e))

del c, e  # only   d f

g_conv = [json.loads(i) for i in d]
h_prompts = [json.loads(i) for i in f]

del d, f

gc.collect()

with open('all_train_human_enhancedata_all_conv.jsonl', 'w', encoding='utf-8') as f:
    json.dump(g_conv, f, indent=4, ensure_ascii=False)

with open('all_train_human_enhancedata_all_intentslot.jsonl', 'w', encoding='utf-8') as f:
    json.dump(h_prompts, f, indent=4, ensure_ascii=False)

with open('all_train_human_enhancedata_all_conv.json', 'w', encoding='utf-8') as f:
    json.dump(g_conv, f, indent=4, ensure_ascii=False)

with open('all_train_human_enhancedata_all_intentslot.json', 'w', encoding='utf-8') as f:
    json.dump(h_prompts, f, indent=4, ensure_ascii=False)
