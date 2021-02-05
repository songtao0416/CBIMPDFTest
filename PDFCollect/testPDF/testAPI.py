import requests, json
from requests_toolbelt import MultipartEncoder


github_url = "http://127.0.0.1:9100/test_01"
pdfName = "崇礼度假区（建筑单专业） K建施-001 - 设计说明及图纸目录.pdf"
pdfPath = "F:\\项目代码\\Python代码\\CBIM设计说明文档识别\\PDFCollect\\resources\\pdf文本\\崇礼度假区\\%s" % pdfName
# files = {"pdfPath": open(pdfPath, "rb"), "pdfName": pdfName, "pdfType": "1", "pdfMajor": "建筑"}
files = MultipartEncoder(
    fields={'pdfPath': (pdfName, open(pdfPath, "rb"), 'text/plain'),
          "pdfName": pdfName,
          "pdfType": "1",
          "pdfMajor": "建筑"})
print(files)
# print(files["fields"])
# data = {"pdfPath": pdfPath, "pdfName": pdfName, "pdfType": "1", "pdfMajor": "建筑"}
# print(data["pdfName"])
# headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}
# r = requests.get(github_url, data, headers=headers)
r = requests.post(github_url, files=files, headers={'Content-Type': files.content_type})
print(r.json)
print(r.text)