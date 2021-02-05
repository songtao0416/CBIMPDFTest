from flask import request, Flask, jsonify

from matplotlib import pyplot as plt
import sys
sys.path.append("..")
from flask import Flask, request, jsonify
import json
from apiPDF.apiJson import apiJson

app = Flask(__name__)


# 只接受get方法访问
@app.route("/test_01", methods=["POST"])
def check():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.form is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    print("1")
    pdfFile = request.files.get('pdfPath')
    print("传入的文件为：", pdfFile)
    # 对参数进行操作
    return_dict['result'] = tt(pdfFile, pdfName="测试")
    return json.dumps(return_dict, ensure_ascii=False)



# 功能函数
def tt(pdfPath, pdfName):
    # result_str = apiJson(pdfPath, pdfName).apiJson
    try:
        result_str = apiJson(pdfPath, pdfName).apiJson
    except:
        result_str = "未知错误"
    return result_str


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10200, debug=True)
