import sys, os, re, time, random, requests, logging, json, jsonlines
from random import choice

sys.path.append(os.path.dirname(sys.path[0]))

from apikeys import keys
from flask import Flask, jsonify, request

app = Flask(__name__)

# from main_rc.preparedataprocess import part1toparams, lang2line_name
# from main_rc.preparedataprocess import allTextDict
# from main_rc.preparedataprocess import allTextList as souLangText  # 一个测试数据


proxies_list = [{'http': 'socks5://117.160.199.40:46566', 'https': 'socks5h://117.160.199.40:46566'}, ]
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + keys, }
json_data = {'model': 'gpt-3.5-turbo-0613', 'temperature': 0.6, 'messages': []}


def requestApi(json_data, proxies_list):
    response = requests.post('https://api.openai.com/v1/chat/completions',
                             headers=headers, json=json_data, proxies=random.choice(proxies_list), verify=False, timeout=600)
    return response


with open('sdtconvdatahuman.json', 'r', encoding='utf-8') as f:
    std_data = json.load(f)

while True:
    try:
        p1 = """
        现有一个台湾电商平台，其主要客户均来自台湾，且其商品均售卖给台湾用户。
        你是该平台的一个客服业务系统专家。请你基于上述背景与身份，我们将要开始完成一些任务。
        """
        # step-1
        json_data['messages'].append({"role": "user", "content": p1})
        res = requestApi(json_data, proxies_list)
        res = res.content.decode('utf-8')
        res = eval(res)['choices'][0]['message']
        json_data['messages'].append(res)

        # step-2
        p2 = """
        首先需要明确的是，当用户找到你的时候，他有特定目的，即他的对话意图，同时他还会告诉你一些必要的信息，以从你这里得到相应的帮助。
        因此，你可以从用户那里得到以下的关键信息：
        1.用户意图，即他找到你是需要解决什么问题；
        2.对话槽位，即用户会告诉你哪些关键信息以便于你帮他解决问题，这些槽位有如下几种：
          slot-1：goods:用户购买的商品信息；
          slot-2：phone:用户的电话号码信息，这是一个关键槽位，帮助用户查询订单状态，查询物流状态，查询退换货进度，修改订单信息等关键业务均依赖电话号码查询订单；
          slot-3：name：用户的姓名信息；
          slot-4：count：用户购买的商品数量；
          slot-5：style：用户购买的商品款式；
          slot-6：code：用户的订单编号，有的用户是清楚自己的订单编号的，因此有的用户可能会直接给你提供订单编号；
          slot-7：account：用户的银行账户号，当用户需要退款时，他会告诉你他的银行账户编号；
          slot-8：bank：用户的银行账户的开户银行，一般都是台湾地区的银行；
          slot-9：payment：用户的付款方式，台湾地区的用户一般都是7-11/全家等商超取货；
          slot-10：height：用户的身高信息，有的用户因为商品的一些原因可能会告诉你他的身高信息；
          slot-11：weight：用户的体重信息，有的用户因为商品的一些原因可能会告诉你他的体重信息；
          对于每一个用户告诉你的信息，可能不会涉及到所有槽位信息，但是如果有上述任意一种槽位出现，你需要将其识别并标注出来，至于slot信息具体的标注方式，我将会在标准的对话示例中告诉你。
        """
        json_data['messages'].append({"role": "user", "content": p2})
        res = requestApi(json_data, proxies_list)
        res = res.content.decode('utf-8')
        res = eval(res)['choices'][0]['message']
        json_data['messages'].append(res)

        demo = choice(std_data)
        intent = demo['category']
        # step-3
        p3 = f"""
        现在我将为你提供一个标准的对话示例如下：{demo}
        上述示例有如下特征：
        1.此对话是一个多轮对话，其中用户发送的消息符合台湾人的用户的口语表达习惯与讲话风格。
        2.此对话有一个专属的对话id字段；
        3.此对话有一个用户意图字段：category，且当前示例的意图为：{intent}；
        假设在有另外一个用户，他因为相同的意图：{intent}来找你寻求帮助，你需要回答它的问题。你在解决他的问题的过程有以下几点要求：
        1.请你按照上述示例对话相同的json结构，复现一个处理相同意图的对话过程，且当前意图为：{intent}；
        2.由于你处理的用户意图：{intent}与示例的意图一致，因此你可以以类似的话术处理相同的意图，但是用户发送的消息应该和示例保持较大的差异；
        3.你虚构的人名不允许使用"张三"、"李四"等此类虚假的人名信息，你虚构的电话号码必须以09开头，符合台湾地区的电话号码规范，不允许使用123456等虚构的电话号码；
        4.对话过程的最后一句话必须有助手assistant发出；
        5.你需要以相同的json结构输出结果，且你只需要输出对话的json结果，不需要输出任何提示性内容。
        """
        json_data['messages'].append({"role": "user", "content": p3})
        res = requestApi(json_data, proxies_list)
        res = res.content.decode('utf-8')
        res = eval(res)['choices'][0]['message']
        # json_data['messages'].append(res)
        enhance_conv = res['content']
        try:
            if "```" in res['content']:
                enhance_conv = res['content'].replace('```', '')
            if '\n\n' in res['content']:
                enhance_conv = eval(enhance_conv.split('\n\n')[1])
            else:
                enhance_conv = eval(enhance_conv)

            with jsonlines.open('enhanceData.jsonl', mode='a') as f:
                f.write(enhance_conv)
        except:
            # 这里记录的是成功请求但是解析错误的对话
            with jsonlines.open('wrongparser.jsonl', mode='a') as f:
                f.write(enhance_conv)

        json_data['messages'] = []
    except:
        json_data['messages'] = []
        pass
