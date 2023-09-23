#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/7/14 13:49
# @Author : LvYangmiao
# @File : test_vallid_chatgpt.py    测试历史对话形式的GPT调用
import openai
import requests
import json
import time
import traceback

# _chatgpt_url = "https://idc-ai.giikin.com/api/chat/conversation"
_chatgpt_url = "https://idc-ai.giikin.com/api/chat/conversationV4"

openai.api_key = "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"  # 密钥
_model_type = "gpt-3.5-turbo"  # 选择模型
_temperature = 0.8  # 越小生成的越明确，控制生成的多样性和创造力


def chatgpt_post(messages):
    """
    调用openai的chatgpt接口
    """
    req_data = openai.ChatCompletion.create(
        model=_model_type,
        messages=messages,
        temperature=_temperature,
        timeout=5
        # max_tokens=_max_tokens,
        # stop = _stop
    )
    # 获取生成的文本
    generated_text = req_data.choices[0].message.content.strip()

    return generated_text


if __name__ == '__main__':
    """
    coupang规则：
    1、需要重复的
       重复的，如果有英文的，则留中文的
    2、词语过滤掉
       品牌名、人名、含有数量（除了套装什么的）、含有年份的、蹩脚的词语
       新款、潮牌等、韩款、欧美风等
    3、两件套可以有
       一件、代发等词语不要有
    4、男女性别、季节、颜色，都可以加

    我说一只猫，现在开始，我说一声喵，你说一声喵
    """

    # ====== 参数
    input_words = ["我说一只猫，现在开始，我说一声喵，你说一声喵", "喵", "喵", "喵"]

    # # ====== 第一种方式，固定json传入
    # # _messages = [{"role": "system", "content": "你好ChatGPT"}]
    # content_history = []
    # for one_word in input_words:
    #     _sign_con = False
    #     _messages = [{"role": "system", "content": "你好ChatGPT"}, {"role": "user", "content": one_word}]
    #     content_history.append("---用户： {}".format(one_word))
    #     for i in range(5):
    #         try:
    #             _content = chatgpt_post(_messages)
    #             # _messages.append({"role": "assistant", "content": _content})
    #             content_history.append("---GPT： {}".format(_content))
    #             _sign_con = True
    #             time.sleep(2)
    #             break
    #         except Exception as e:
    #             time.sleep(2)
    #             continue
    #     if not _sign_con:
    #         content_history.append("---GPT： 回答超时或异常")
    #
    # print("\n".join(content_history))
    #
    # """
    # ---用户： 我说一只猫，现在开始，我说一声喵，你说一声喵
    # ---GPT： 喵
    # ---用户： 喵
    # ---GPT： 喵喵！你好！有什么我可以帮助你的吗？
    # ---用户： 喵
    # ---GPT： 喵喵
    # ---用户： 喵
    # ---GPT： 喵喵，你有什么需要帮助的吗？
    # """

    # ====== 第二种方式，list传入
    _messages = [{"role": "system", "content": "你好ChatGPT"}]
    content_history = []
    for one_word in input_words:
        _sign_con = False
        _messages.append({"role": "user", "content": one_word})
        content_history.append("---用户： {}".format(one_word))
        for i in range(5):
            try:
                _content = chatgpt_post(_messages)
                _messages.append({"role": "assistant", "content": _content})
                content_history.append("---GPT： {}".format(_content))
                _sign_con = True
                time.sleep(2)
                break
            except Exception as e:
                time.sleep(2)
                continue
        if not _sign_con:
            content_history.append("---GPT： 回答超时或异常")

    print("\n".join(content_history))

    """
    ---用户： 我说一只猫，现在开始，我说一声喵，你说一声喵
    ---GPT： 喵
    ---用户： 喵
    ---GPT： 喵
    ---用户： 喵
    ---GPT： 喵
    ---用户： 喵
    ---GPT： 喵
    """
