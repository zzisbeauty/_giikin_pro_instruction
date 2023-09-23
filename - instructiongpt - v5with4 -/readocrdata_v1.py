# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:UmeAI
@File:readocrdata.py
@Time:2023/7/12 16:21
@Read: 构建多轮对话的形式完成翻译；  本地测试与编写指令，参数不是特别完整
"""
import os
import gc
from apikeys import gptURLFast
import concurrent.futures


# todo 基于本地文件构建一批测试数据

def readOCRData(myPath):
    files = os.listdir(myPath)
    return files


noName = ['厂家批发', 'TR90', '外贸', '跨境', '2021']
originalFiles = readOCRData('../标准OCR文本数据已修正/ocr_standardtext')
files = list(set([e[:-14] for e in originalFiles]))
toDataParts = []
for file in files:
    goodsName = file.split('___')[0]
    goodsCls = file.split('___')[1]
    for i in noName:
        if i in goodsName:
            goodsName = goodsName.replace(i, '')
    toDataParts.append({'商品类别': goodsCls, '原语言商品标题': goodsName, 'souLangText': []})

del files

for eachT in toDataParts:
    goodsCls = list(eachT.values())[0]
    goodsName = list(eachT.values())[1]
    for ef in originalFiles:  # save text file name
        ef_ = os.path.join('../标准OCR文本数据已修正/ocr_standardtext', ef)  # save text file path
        with open(ef_, 'r', encoding='utf-8') as fr:  # read text from save text file
            allText = fr.readlines()
            goodsClsYZ = allText[0].split(':')[1].strip()
            onlyText = [et.strip() for et in allText[2:]]
            if goodsClsYZ == goodsCls:
                eachT['souLangText'] += onlyText

gc.collect()

# todo gpt4 的接口请求，以构造历史对话的形式


import requests


# todo 构造指令开始请求


def part1(goodsCls, goodsName):
    json1 = """{
        "商品功能":
        "商品的应用场景":
        "商品的适用人群":
        "商品的适用时间":
        "商品卖点":
    }
    """
    # 现在你一个翻译专家，你精通多国语言，你每一次执行翻译任务时，你每次任务需要处理的文本是关于电商平台某一个商品的介绍信息。
    # 你每一次执行翻译任务时，你每次任务需要处理的文本是关于电商平台某一个商品的介绍信息。
    # 现在我有一个商品的广告文案需要你协助翻译。商品的具体信息如下：
    p1 = f"""
    你是一个商品投放专家，你擅长撰写精美的商品描述帮助提升商品的投放效果。
    在你每次执行商品文案描述的撰写时，你第一步会做的工作是仔细理解商品的内在信息。
    现在有如下商品基础信息：
    1.商品类别：{goodsCls}；
    2.商品标题：{goodsName}；
    3. 
    请你根据上述信息仔细理解当前商品，并从"商品功能"、"商品的应用场景"、"商品的适用人群"、"商品的适用时间"、"商品卖点"
    五个方面分析这个商品的特点与标签信息，并以{json1}的格式输出。
    """
    return p1


def part2(goodsCls, goodsName, res_part1):
    p2 = f"""
    在你每次执行商品文案描述的撰写时，你第二步会做的工作是总结目前已知的信息如下：
    1 商品所属类别：{goodsCls}；
    2 商品标题名词：{goodsName}；
    3 商品的标签以及卖点信息：{res_part1}；
    你会通过综合上述所有已知信息，撰写一段商品主题文案，该主题文案将会包含该商品所有的标签、卖点等关键信息，该文案将会辅助你未来新的广告文案撰写工作。
    现在，请你输出这个商品主题文案内容。 
    """
    return p2


def part3(souLangText):
    json3 = {}
    for i in souLangText:
        json3[i] = ''
    json3 = f"""{json3}"""
    # 在你每次执行商品文案描述的撰写时，你第三步会做的工作是仔细参考已有的广告描述文案，对已有的广告描述文案进行分类。
    # 关于当前商品，现在已有一批广告文案如下：{souLangText}。对于这批商品介绍文本可以分为3大类共6种，具体说明如下：
    p3 = f"""
    在你每次执行商品文案描述的撰写时，你第三步会做的工作是仔细参考已有的广告描述文案，对已有的广告描述文案进行分类。
    关于当前商品，现在已有一批广告文案。对于这批商品介绍文本可以分为3大类共6种，具体说明如下：
    第一大类：短广告文本，每句话的字符长度小于10个中文字符，如果文本长度大于10个中文字符，那它必不可能属于如下几类：
        class-1:人们日常生活中具体事物的概念。此类文本是日常生活中的客观事实或事物。
        class-2:商品的SKU信息。此类文本是商品的颜色、尺寸、设计款式等具体规格信息。例如类似黄色、军绿、紧身、宽松、微弹、圆领之类的表述；
        class-3:人们日常生活中存在的技术概念。此类文本可以清晰地说明一种专业技术。具有的主要特征是简洁明了，且是专业名词，专业性高：
                例如类似焦距、放大率、干洗、漂白、压铸之类的表述；        
    第二大类：一般情况下，每句话的字符长度大于10个中文字符，但不绝对，当文本很短但是在描述商品的标签、卖点等信息以突出商品优质特性，那么它也应该属于如下class-4类别：
        class-4:商品卖点与特点描述。此类文本长度通常大于10个中文字符且十分具体，内容包含了大量的商品标签信息，包括商品的功能、适用人群、适用场景等。
                这些标签信息突出了商品的良好性质与卖点信息，是商品的详细描述，是吸引用户关注商品并完成购买的关键文案信息。
    第三大类：其它广告文本，每句话的字符长度不确定：
        class-5:售后与备注信息。此类文本长度通常大于10个中文字符。通常包含了一些售后备注信息：例如赠品说明，退换货政策、使用说明之类的表述。
        class-6:促销术语。此类文本长度通常不确定，该部分内容是商品的促销与折扣信息，意在表明商品的合理定价，吸引用户及时购买。
    现在你首先需要做的工作是：判断每一条广告文案所属类型。并以{json3}的格式输出你的判断结果。
    """
    return p3


def part4(goodsCls, goodsName, res_part1, res_part2, souLangText, line_name, souL, tarL):
    changeText = {}
    for i in souLangText:
        changeText[i] = ''
    p4 = f"""
    你第四步会做的工作就是开始真正的广告文案撰写工作，你的具体工作步骤如下：
    一、首先你会检视已知的所有信息：
    1.商品所属类别：{goodsCls}；
    2.商品标题名词：{goodsName}；
    3.商品的标签以及卖点信息：{res_part1}；
    4.该商品投放时编写广告语需要贴合的主题：{res_part2}；
    5.原始文本的语言：{souL}；
    6.投放地区的语言：{tarL}；
    二、基于上述商品基础信息，你将会开始生成{tarL}广告文案工作，具体步骤如下：
    1.你需要处理的原始广告文案有如下几条：{souLangText}；
    2.对于其中的每一条原始文案，你都会结合上述已知信息，撰写出一条新的{tarL}广告文案。
    三、输出你的改写结果：你最终处理的结果以{changeText}的格式输出。
    """
    return p4
    """
    你撰写新的广告文案是基于给定的原始{souL}广告文案，重新表述为{tarL}的广告文案，你在重新表述的过程中将会基于如下规则：
    1.对于{souLangText}中的每一条原始广告文案，你首先会将其翻译成{tarL}的广告文案；
    2.你在翻译之后，{tarL}广告文案时，应该结合上述你所知的商品信息，保证撰写的结果贴合商品的标签、卖点与商品主题；
    4.你改写的结果符合电商广告文案的特征：高效、优美、突出商品商品卖点，同时符合{line_name}地区人群的语言表达习惯，足够吸引{line_name}地区的受众人群；
    """


def transProcess():  # user -- > gpt -- > user -- > gpt ...
    for eachToDataPart in toDataParts:
        gCls = list(eachToDataPart.values())[0]
        gName = list(eachToDataPart.values())[1]
        souLangText = list(eachToDataPart.values())[2]

        hisTalks = {'message': [], 'role': 'taskTransPicture'}

        tp1 = part1(gCls, gName)  # 开始对话：用户发送的第一句话
        hisTalks['message'].append({'content': tp1, 'role': 'user'})
        # res = requests.post(url=gptURLFast, json=hisTalks).text
        res_part1 = eval(requests.post(url=gptURLFast, json=hisTalks).text)
        res_part1 = res_part1['data']['data']  # 这里是真正解析出来了对话执行下去需要的信息
        hisTalks['message'].append({'content': res_part1, 'role': 'assistant'})
        pass  # gpt ----------> 答复用户的第一句话结束  这轮对话对于同一个品可以复用

        tp2 = part2(gCls, gName, res_part1)  # 第二轮对话
        hisTalks['message'].append({'content': tp2, 'role': 'user'})
        res_part2 = eval(requests.post(url=gptURLFast, json=hisTalks).text)
        res_part2 = res_part2['data']['data']
        hisTalks['message'].append({'content': res_part2, 'role': 'assistant'})
        pass  # 第二轮对话结束 ----------------->

        tp3 = part3(souLangText)  # 第三轮对话
        hisTalks['message'].append({'content': tp3, 'role': 'user'})
        res_part3 = eval(requests.post(url=gptURLFast, json=hisTalks).text)
        res_part3 = res_part3['data']['data']  # 这里是真正解析出来了对话执行下去需要的信息
        hisTalks['message'].append({'content': res_part3, 'role': 'assistant'})
        pass  # 第三轮对话结束 -------- >

        mtList, gpttList = [], []
        eachText_cls = {'class-1': 0, 'class-2': 0, 'class-3': 0, 'class-4': 1, 'class-5': 1, 'class-6': 1}
        res_part3_dict = eval(res_part3)
        for k, v in res_part3_dict.items():
            if v == 'class-1' or v == 'class-2' or v == 'class-3':
                mtList.append(k)
            else:
                gpttList.append(k)

        splitSeqList = []
        if len(gpttList) == 1:
            splitSeqList = [gpttList]
        if 1 < len(gpttList) <= 6:
            splitSeqList = [gpttList[i:i + int(len(gpttList) / 2)] for i in
                            range(0, len(gpttList), int(len(gpttList) / 2))]
        if 6 < len(gpttList) <= 10:
            splitSeqList = [gpttList[i:i + int(len(gpttList) / 3)] for i in
                            range(0, len(gpttList), int(len(gpttList) / 3))]
        if len(gpttList) > 10:
            splitSeqList = [gpttList[i:i + int(len(gpttList) / 5)] for i in
                            range(0, len(gpttList), int(len(gpttList) / 5))]

        for souLangText in splitSeqList:
            tp4 = part4(gCls, gName, res_part1, res_part2, souLangText, line_name='Japan', souL='Chinese',
                        tarL='Japanese')
            hisTalks['message'].append({'content': tp4, 'role': 'user'})
            res_part4 = eval(requests.post(url=gptURLFast, json=hisTalks).text)
            res_part4 = res_part4['data']['data']
            hisTalks['message'].append({'content': res_part4, 'role': 'assistant'})
            pass  # 第四轮对话结束 -------- >
            A = 1

# todo 基于测试数据的本地测试方法
# transProcess()


# def mulitProcess():
#     with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#         to_do = []
#         for souLangText in splitSeqList:  # splitSeqList 2 souLangText
#             future = executor.submit(AllTransPicApiLocal, souL, tarL, line_name, toDataPart, souLangText)

# =============================================

# 如下情况是请求失败的 try catch
# try:
#     {'code': 40001, 'comment': 'OK',
#      'data': '程序异常HTTPSConnectionPool(host=\'chatgpt.giikin.com\', port=443): Max retries exceeded with url: /v1/chat/conversationV4?t=1689678221.6745355&sign=386dcd56424709ce071739e2be17581688e6c1c7 (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7f7699623be0>: Failed to resolve \'chatgpt.giikin.com\' ([Errno -3] Temporary failure in name resolution)"))'}
# except
#     pass
