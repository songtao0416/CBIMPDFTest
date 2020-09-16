import sys
sys.path.append("/PDFCollect")

class configPDF:

    def __init__(self):
        self.pdfPath = "resources\\pdf文本\\崇礼度假区"
        self.aecdictPath = "resources\\aecuserdict.txt"

        # 保存路径相关
        self.txtPath = "resources\\pdf_txt_file"
        self.excelPath = "resources\\pdf_xls_file"

        # 参数库规则相关
        self.rulePath = "resources\\参数规则库\\rule.xls"
        self.rulesheetIndex = 0

        # 表格相关
        self.rightCSNames = ["项目经理", "设计部门负责人", "总图", "建筑", "结构", "给排水", "暖通", "动力", "电气", "电讯",
                             "工程名称", "子项", "设计号", "图号", "比例", "日期", "图名", "设计主持人", "工种负责人", "设计制图人",
                             "审定", "审核", "校对", "设计部门", "设计证书号"]
        self.formKeywords = ["电梯相关参数", "传热系数", "性能指标"]
        self.formFixHeading = ["序号", "编号", "类别"]

        # 标题结果相关
        self.pdfName = ["设计说明"]
        self.titleNames = ["设计依据", "工程概况", "工程材料及做法", "设计范围", "标高及单位", "墙体工程", "门窗工程", "幕墙工程",
                           "室外工程", "装修工程", "防水工程", "无障碍设计", "建筑采光设计", "建筑隔声设计", "建筑设备", "设施工程",
                           "安全防护", "人防工程", "其它", "附录", "图纸目录", "消防设计", "工程做法"]

        # 输出信息配置{ID,fcsID,fcsName,csName,csValue,csType,titleID,lastText,nextText,rowID,rowData}
        self.parameterHeadings = ['参数ID', '父参数ID', '父参数名称', '参数名称', '参数值', '参数类型', '父级标题ID', '上文', '上文', '所在行数',
                                  '所在行内容']
        self.titleHeadings = ['标题ID', '标题名称', '所在行数', '标题层级', '标题包含内容']

        self.evaluationIndex = [["变量", "量化指标", "计算公式"],
                                ["csrowNumRate", "参数行比率", " = 参数行数量/PDF总行数"],
                                ["uncsrowNumRate", "非参数行比率", " = 非参数行检出率/PDF总行数"],
                                ["ruleCSJCRate", "参数检准率", " = 检出的参数库参数数量 / PDF中全部参数库参数数量"],
                                ["ruleCSJQRate", "参数检全率", " = 检出的参数库参数数量 / 全部检出的参数数量"],
                                ["ruleCSF1", "参数检出F1值", " = 2*参数检准率*参数检全率 /（参数检出率+参数检准率）"],
                                ["ruleCSJZRate", "参数值精准率", " = 检出精准参数值数量 / 全部检出参数库参数数量"],
                                ["newCSNumRate", "新参数占比率", " = 新参数的数量 / 全部检出的参数数量"],
                                ["formCSJZRate", "表格参数检准率", " = 检出的表格参数中参数库参数数量/表格中全部参数库参数数量"],
                                ["formCSJQRate", "表格参数检全率", " = 检出的表格参数中参数库参数数量/表格中全部参数数量"]]
