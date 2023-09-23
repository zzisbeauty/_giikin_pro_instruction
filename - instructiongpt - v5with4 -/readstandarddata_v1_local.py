# 封装成接口; 相对于readocrdata_v1.py中的本地测试，通过查库封装参数更加完整，因此对于指令相对本地测试也有微调
import sys

sys.path.append('..')
sys.path.append(r'F:\FinalNotion\instructiongpt')

import requests
from flask import Flask, jsonify, request
from transwithgpt.v5with4.preparedataprocess import part1toparams, lang2line_name

import re

app = Flask(__name__)
import logging

# logger = logging.getLogger('transLoggerV5with4')
logging.basicConfig(filename='trans.v4.gpt4.log', encoding='utf-8', level=logging.INFO)


# def part1(goodsCls, goodsName):
def part1(product_name, sale_name, product_name_ali, ad_slogans, souLangText, souL, tarL):
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
    1.商品类别：{product_name}；
    2.商品{tarL}标题：{sale_name}；
    3.商品中文标题：{product_name_ali}；
    4.商品{tarL}广告文案：{ad_slogans}；
    5.商品{souL}商品详情描述文本：{souLangText}；
    请你根据上述信息仔细理解当前商品，并从"商品功能"、"商品的应用场景"、"商品的适用人群"、"商品的适用时间"、"商品卖点"
    五个方面分析这个商品的特点与标签信息，并以{json1}的格式输出。
    """
    return p1


# def part2(goodsCls, goodsName, res_part1):
def part2(product_name, sale_name, product_name_ali, ad_slogans, res_part1, tarL):
    p2 = f"""
    在你每次执行商品文案描述的撰写时，你第二步会做的工作是总结目前已知的信息如下：
    1.商品所属类别：{product_name}；
    2.商品{tarL}标题：{sale_name}；
    3.商品中文标题：{product_name_ali}；
    4.商品{tarL}广告文案：{ad_slogans}；
    5.商品的标签以及卖点信息：{res_part1}；
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


# todo 以history的形式使用的part4
# def part4(goodsCls, goodsName, res_part1, res_part2, souLangText, line_name, souL, tarL):
def _part4_(product_name, sale_name, res_part1, res_part2, souLangText, line_code='', souL='', tarL=''):
    changeText = {}
    for i in souLangText:
        changeText[i] = ''
    p4 = f"""
        你第四步会做的工作就是开始真正的广告文案翻译工作，你的具体工作步骤如下：
        一、首先你会检视已知的所有信息：
        1.商品所属类别：{product_name}；
        2.商品标题名词：{sale_name}；
        3.商品的标签以及卖点信息：{res_part1}；
        4.该商品投放时编写广告语需要贴合的主题：{res_part2}；
        5.原始文本的语言：{souL}；
        6.投放地区的语言：{tarL}；
        二、基于上述商品基础信息，你将会开始生成{tarL}广告文案工作，具体步骤如下：
        1.你需要处理的原始广告文案有如下几条：{souLangText}；
        2.对于其中的每一条原始文案，你都会结合上述已知信息，翻译为{tarL}广告文案。
        三、输出你的翻译结果：你最终处理的结果以{changeText}的格式输出。
        """
    return p4


# todo 以history的形式使用的part4
# def part4(goodsCls, goodsName, res_part1, res_part2, souLangText, line_name, souL, tarL):
def part4(product_name, sale_name, res_part1, res_part2, souLangText, line_code='', souL='', tarL=''):
    changeText = {}
    for i in souLangText:
        changeText[i] = ''
    p4 = f"""
        你要完成{souL}广告文案翻译到{tarL}的工作。好的广告文案可以突出展现商品的标签与卖点特征，增加商品的表现力，增强广告平台的投放效果。
        你的具体工作步骤如下：
        一、首先你会检视已知的所有信息：
        1.商品所属类别：{product_name}；
        2.商品标题名词：{sale_name}；
        3.商品的标签以及卖点信息：{res_part1}；
        4.该商品投放时编写广告语需要贴合的主题：{res_part2}；
        5.原始文本的语言：{souL}；
        6.投放地区的语言：{tarL}；
        7.你需要处理的原始广告文案：{souLangText}；
        二、基于上述商品基础信息，你将会开始生成{tarL}广告文案工作，具体执行过程中有如下基准原则：
        1.对于其中的每一条原始文案，你都会结合{res_part1}以及{res_part2}中描述的商品核心信息，分析当前广告文案体现了其中哪些标签；
        2.翻译过程{tarL}结果要保持该{souL}广告文案具备的标签内容；
        3.翻译的结果不应改变原始{souL}广告文案的含义；
        三、输出你的翻译结果。最终的处理结果以{changeText}标准json格式输出，不要输出任何其它无关内容。
        """
    """
    你撰写新的广告文案是基于给定的原始{souL}广告文案，重新表述为{tarL}的广告文案，你在重新表述的过程中将会基于如下规则：
    1.对于{souLangText}中的每一条原始广告文案，你首先会将其翻译成{tarL}的广告文案；
    2.你在翻译之后，{tarL}广告文案时，应该结合上述你所知的商品信息，保证撰写的结果贴合商品的标签、卖点与商品主题；
    4.你改写的结果符合电商广告文案的特征：高效、优美、突出商品商品卖点，同时符合{line_name}地区人群的语言表达习惯，足够吸引{line_name}地区的受众人群；
    """
    return p4


import time

import concurrent.futures
from apikeys import gptURLFast


def thread_todo(tp4, souLangText):
    try:
        # res_part4 = eval(requests.post(url=gptURLFast, json=hisTalks).text) # todo change 适配3
        res_part4 = eval(requests.post(
            url=gptURLFast, json={'message': [{'content': tp4, 'role': 'user'}], 'role': 'taskTransPicture'}).text)
        return (res_part4, souLangText)
    except:
        return (souLangText)


@app.route('/tbTrans', methods=['POST'])
def getparmas():  # true   4 API
    # postValues = request.json
    # souL = postValues.get('souL', "CN")  # 填入图像中的原始语言代码，默认CN。一般OCR识别的都是中文素材，因此是CN；
    # line_code = postValues.get('line_code', "")  # 必填，要投放地区；参考lang2line_name说明
    # tarL = lang2line_name[line_code][0]
    # souLangText = postValues.get('souLangText', "")  # 要输入的文本，必填
    # product_name_ali = postValues.get('中文商品标题', "")  # 要输入的文本，必填
    # product_name = postValues.get('商品类别', "")  # 要输入的文本，必填

    sale_name, ad_slogans = '', ''

    # local test
    from transwithgpt.标准OCR文本数据已修正.difficultpicturedemo2.a_picture_handler import finalDict
    souL = 'CN'
    line_codes = ['JP', 'KR', 'MY', 'TH', 'EN', 'PH', 'AR', 'PL']
    for line_code in line_codes:
        tarL = lang2line_name[line_code][0]
        for k, v in finalDict.items():
            souLangText = [i.strip() for i in v]
            product_name = k.split('-')[0]
            product_name_ali = k.split('-')[1]

            hisTalks = {'message': [], 'role': 'taskTransPicture'}
            tp1 = part1(product_name, sale_name, product_name_ali, ad_slogans, souLangText, souL, tarL)
            hisTalks['message'].append({'content': tp1, 'role': 'user'})  # todo change 适配1
            res_part1 = ''
            try:
                # res_part1 = eval(requests.post(url=gptURLFast, json=hisTalks).text) # todo change  适配1
                res_part1 = eval(requests.post(
                    url=gptURLFast,
                    json={'message': [{'content': tp1, 'role': 'user'}], 'role': 'taskTransPicture'}).text)
                res_part1 = res_part1['data']['data']  # 这里是真正解析出来了对话执行下去需要的信息
                logging.info(f'该商品的标签与卖点详情信息如下：{res_part1}\n'
                             f'-----------------------')
                hisTalks['message'].append({'content': res_part1, 'role': 'assistant'})
            except:
                logging.info(f'【过程】Step-1分析商品详情信息过程中出错，检查数据响应数据：\n'
                             f'{res_part1}\n'
                             f'程序退出；\n')
                # return '0'
                continue

            pass

            tp2 = part2(product_name, sale_name, product_name_ali, ad_slogans, res_part1, tarL)
            hisTalks['message'].append({'content': tp2, 'role': 'user'})  # todo change 适配2
            res_part2 = ''
            try:
                # res_part2 = eval(requests.post(url=gptURLFast, json=hisTalks).text) # todo change 适配2
                res_part2 = eval(requests.post(
                    url=gptURLFast,
                    json={'message': [{'content': tp2, 'role': 'user'}], 'role': 'taskTransPicture'}).text)
                res_part2 = res_part2['data']['data']
                logging.info(f'该商品主题信息如下：{res_part2}\n'
                             f'-----------------------')
                hisTalks['message'].append({'content': res_part2, 'role': 'assistant'})
            except:
                logging.info(f'【过程】Step-2商品主题抽取过程中出错，检查响应数据：\n'
                             f'{res_part2}\n'
                             f'程序退出：\n')
                continue
                # return '0'
            pass  # 第二轮对话结束 ----------------->

            splitSeqList, res_part3, allseqClsDict = '', '', {}

            # todo change 第三步判断类别取消时，直接使用这个这接替原始的 gpttList
            gpttList = souLangText

            finalResDict, wrongFinalRes = {}, []
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

            # todo 多线程计算模块
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                to_do = []
                for idx, souLangText in enumerate(splitSeqList):
                    tp4 = part4(product_name, sale_name, res_part1, res_part2,
                                souLangText, line_code=line_code, souL=souL, tarL=tarL)
                    # todo 多线程计算模块
                    future = executor.submit(thread_todo, tp4, souLangText)
                    to_do.append(future)
                    # break

                start = time.time()
                try:
                    for future in concurrent.futures.as_completed(to_do):  # 并发执行
                        _res_part4_ = future.result()
                        if len(_res_part4_) == 2:
                            _res_part4_ = _res_part4_[0]['data']['data']
                            sindex, eindex = 0, 0
                            for each in list(enumerate(_res_part4_)):
                                if each[1] == '{':
                                    sindex = each[0]
                                if each[1] == '}':
                                    eindex = each[0]
                            finalResDict.update(eval(_res_part4_[sindex:eindex + 1]))
                        else:
                            wrongFinalRes.append(_res_part4_[0])
                            logging. \
                                info(
                                f'【过程】在解析 step-4 Threads Finale result 时出错，这是模型Prompt的问题。出错信息已记录 \n')
                except:
                    logging.info(f'【过程】判定step-4 Threads Finale result 过程出错，检查响应数据：\n'
                                 f'{_res_part4_}\n'
                                 f'该部分错误处理sequence已记录，程序退出！\n')

                chaTime = time.time() - start
                logging.info(f'所有数据处理完毕总耗时：{chaTime}')

            if finalResDict:
                logging.info(f"【结束任务】step-4翻译过程结束，得到如下结果：\n"
                             f"翻译结果：{finalResDict}\n"
                             f"以下数据未能完成翻译：{wrongFinalRes}，可以重新请求，或者指定人工翻译！\n"
                             f"----------------当前任务结束！----------------\n\n")
                print(f"{product_name}-{product_name_ali}-{tarL}------------")
                with open(f'{product_name}-{product_name_ali}-{line_code}.txt', 'a+', encoding='utf-8') as f:
                    f.write(f"【结束任务】step-4翻译过程结束，得到如下结果：\n"
                            f"翻译结果：{finalResDict}\n"
                            f"以下数据未能完成翻译：{wrongFinalRes}，可以重新请求，或者指定人工翻译！\n")

                # return f"""
                # 翻译结果：{finalResDict}\n
                # 未能完成翻译的数据：{wrongFinalRes}\n
                # """
            else:
                logging.info(f'【过程】Step-4翻译过程中出错，程序退出；\n'
                             f'以下数据未能完成翻译：{wrongFinalRes}，可以重新请求，或者指定人工翻译！')
                continue
                # return '0'

            # res_part4 = str(finalResDict)
            # hisTalks['message'].append({'content': res_part4, 'role': 'assistant'})
            pass  # 第四轮对话结束 -------- >
            A = 1


if __name__ == '__main__':
    # app.config['JSON_AS_ASCII'] = False
    # app.run(host='0.0.0.0', debug=True, port=5025)

    # local test
    res = getparmas()
