from flask import render_template
from flask import Flask
from flask import request
import os
import sys

import requests


import logging

# jy: level 默认是 logging.WARNING
logging.basicConfig(level=logging.DEBUG,
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s : %(name)s : %(levelname)s : %(message)s')



app = Flask(__name__)



def get_resp(prompt_text, url_, api_key, str_model):
    """
    传入参数如: 
    prompt_text: "What is the OpenAI mission?"

    返回结果如: 
    {'id': 'chatcmpl-6pTJMcRcArxrmLtUaGkjaxsCuVsZE',
     'object': 'chat.completion', 'created': 1677725420,
     'model': 'gpt-3.5-turbo-0301',
     'usage': {'prompt_tokens': 14, 'completion_tokens': 151, 'total_tokens': 165},
     'choices': [{'message': {'role': 'assistant', 'content': "\n\nAs an AI language model, I cannot provide my personal opinion, but I can certainly provide information. \n\nOpenAI's mission is to ensure that artificial intelligence (AI) technology serves humanity in a way that benefits all people. Its aim is to create safe and beneficial AI that can be used to solve important problems and improve the quality of life for everyone. \n\nSpecifically, OpenAI works on advancing AI capabilities with a team of leading researchers in machine learning and AI safety. They also aim to educate people about AI and its potential impact on society. Additionally, they provide API access and tools for developers to build AI applications. OpenAI is committed to fostering collaboration between researchers and developers in order to advance AI technology in a responsible and beneficial way."}, 'finish_reason': 'stop', 'index': 0}]}
    """
    headers = {
        'Authorization':'Bearer %s' % api_key
    }

    json_data = {
    'model': str_model,
    'messages': [
        {
            'role': 'user',
            'content': prompt_text,
        },
    ],
    }

    response = requests.post(url_, headers=headers, json=json_data)
    dict_res = response.json()
    return dict_res



url_ = "https://api.openai.com/v1/chat/completions"
api_key = "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"
str_model = "gpt-3.5-turbo"

"""
text = "What is the OpenAI mission?"
dict_res = get_resp(text, url_, api_key, str_model)
print(dict_res)
"""



logging.info('程序开始运行')

@app.route('/get_res', methods=['POST', 'GET'])
def get_result():
    if request.method == 'POST':
        # jy: html 页面表单(form)提交时的表单数据获取方式是通过 request 的 form 属性;
        #import pdb; pdb.set_trace()
        input_text = request.form["input_text"]

        dict_res = get_resp(input_text, url_, api_key, str_model)

        logging.info("gpt 模型返回结果为: %s" % dict_res)
        ls_choices = dict_res["choices"]
        str_res = ls_choices[0]["message"]["content"]        

        output = {"result": {"gpt_resp": str_res.strip()}}

        return render_template('paper_result.html', result=output, input_text=input_text)
    elif request.method == 'GET':
        # jy: 载入表单请求页面(HTML 模板中会依据是否传入返回结果值显示相应的页面部分);
        return render_template('paper_result.html', is_synonym=False, is_defType_edismax=True)
    else:
        return "ERROR! Only support for POST/GET request!"


