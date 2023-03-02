import os
# flask.__version__ 为 1.1.2
from flask import render_template
from flask import Flask
from flask import request
import logging


app = Flask(__name__)


logger = logging.getLogger("jyhuang_log_data")
# Log 等级总开关
logger.setLevel(logging.DEBUG)

# 创建一个 handler, 用于写入日志文件, 用的是 logging.FileHandler 函数, 注意它的参数信息
logfile = './log_data.txt'
fh = logging.FileHandler(logfile, encoding="utf-8", mode="a")    # mode="a"则是追加
# 输出到 file 的 log 等级的开关
fh.setLevel(logging.INFO)

# 再创建一个 handler, 用于输出到控制台
ch = logging.StreamHandler()
# 输出到 console 的 log 等级的开关
ch.setLevel(logging.DEBUG)

# 定义 handler 的输出格式; 控制台和输出到文件的 handler 可以共用
formatter = logging.Formatter("%(asctime)s : %(name)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 将 logger 添加到 handler 里面, 这一步是最重要的, 本质上就是为 logger 添加多个 handler
logger.addHandler(fh)
logger.addHandler(ch)



@app.route('/logging_data', methods=['POST'])
def log_data():
    abst = request.form["abst"]
    paper_text = request.form["paper_text"]
    paper_id = request.form["paper_id"]
    ttl = request.form["ttl"]
    index = request.form["index"]
    relation = request.form["relation"]
    str_out = "%s <==> %s <==> %s <==> %s <==> %s <==> %s" % (relation, index, paper_text, paper_id, ttl, abst)
    logger.info(str_out)
    return str_out   


def fun_test(input_dict):
    return {"lang": "En", 
            "str_keywords": "keyword1 keyword2",
            "ls_paper_info": [
                {"paper_title": "paper_title-1", "abstract": "abstract-1", "year": 2023, "paper_id": "001"},
                {"paper_title": "paper_title-2", "abstract": "abstract-2", "year": 2022, "paper_id": "002"},
            ]}

@app.route('/paper_search', methods=['POST', 'GET'])
def get_result():
    if request.method == 'POST':
        # jy: html 页面表单(form)提交时的表单数据获取方式是通过 request 的 form 属性;
        form_json = request.form.get("paper_text", None)
        actual_json = None
        if request.json:
            actual_json = request.json.get("text", None)
            top_index = request.json.get("top_index", 1000)
            is_expand_synonyms = request.json.get("is_expand_synonyms", False)
        paper_text = form_json or actual_json
        if form_json:
            input_dict = {"text": paper_text}
        elif actual_json:
            input_dict = {"text": paper_text, "limit": top_index}
        output = fun_test(input_dict)
        dict_paper_info = output
        # jy: 执行模型请求结果, 载入结果页面; paper_text 为获取得到的用户表单数据, 返回时
        #     将其传入模板页面, 使得可以保持原有输入框中的输入内容不变; result 对应的结果
        #     此处为设置的固定值, 实际应用中应为堆 paper_text 进行处理后得到的返回结果; 后
        #     台 HTML 模板中使用字典的方式与 python 中使用字典的方式基本相同;
        if form_json:
            return render_template('paper_result.html', paper_text=paper_text,
                                   result=dict_paper_info)
        elif actual_json:
            return dict_paper_info
    elif request.method == 'GET':
        # jy: 载入表单请求页面(HTML 模板中会依据是否传入返回结果值显示相应的页面部分);
        return render_template('paper_result.html', is_synonym=False)
    else:
        return "ERROR! Only support for POST/GET request!"





