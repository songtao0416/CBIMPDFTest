#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2020 gongzihui. All rights reserved.

"""
  Author:  gongzihui
  Email:   gongzihui@cadg.cn
  Created: 2020/7/10
"""

import os
import sys
import pandas as pd
import pdfplumber
import pdfplumber.utils
import functools
from tqdm import tqdm

from pdf2image import convert_from_path
import cv2 as cv2
import numpy as np
import copy

from draw_tab import DramTable
from decimal import Decimal
import math

max_tol = 1e-03  # 相对于输入值的大小，被认为是“接近”的最大差异;

# 下面的参数用来定义表格读取中的参数
DEFAULT_SNAP_TOLERANCE = 3
DEFAULT_JOIN_TOLERANCE = 3
DEFAULT_MIN_WORDS_VERTICAL = 3
DEFAULT_MIN_WORDS_HORIZONTAL = 1

DEFAULT_X_TOLERANCE = 3
DEFAULT_Y_TOLERANCE = 3


"""
Setting	Description:

	"vertical_strategy" : Either "lines", "lines_strict", "text", or "explicit". See explanation below.
	
	"horizontal_strategy" : Either "lines", "lines_strict", "text", or "explicit". See explanation below.
	
	"explicit_vertical_lines" : A list of vertical lines that explicitly demarcate cells in the table. 
								Can be used in combination with any of the strategies above. 
								Items in the list should be either numbers — indicating the x coordinate of 
								a line the full height of the page — or line/rect/curve objects.
	
	"explicit_horizontal_lines" : A list of horizontal lines that explicitly demarcate cells in the table. 
								Can be used in combination with any of the strategies above. 
								Items in the list should be either numbers — 
								indicating the y coordinate of a line the full height of the page — or line/rect/curve objects.
	
	"snap_tolerance" : Parallel lines within snap_tolerance pixels will be "snapped" to the same horizontal or vertical position.
	
	"join_tolerance" : Line segments on the same infinite line, and whose ends are within join_tolerance of one another, 
								will be "joined" into a single line segment.
	
	"edge_min_length" : Edges shorter than edge_min_length will be discarded before attempting to reconstruct the table.
	
	"min_words_vertical" : When using "vertical_strategy": "text", at least min_words_vertical words must share the same alignment.
	
	"min_words_horizontal" : When using "horizontal_strategy": "text", at least min_words_horizontal words must share the same alignment.
	
	"keep_blank_chars" : When using the text strategy, consider " " chars to be parts of words and not word-separators.
	
	"text_tolerance", "text_x_tolerance", "text_y_tolerance" : When the text strategy searches for words, 
								it will expect the individual letters in each word to be no more than text_tolerance pixels apart.
	
	"intersection_tolerance", "intersection_x_tolerance", "intersection_y_tolerance" : When combining edges into cells, 
								orthogonal edges must be within intersection_tolerance pixels to be considered intersecting.
"""
TABLE_SETTINGS = {
	"vertical_strategy": "lines",
	"horizontal_strategy": "lines",
	"explicit_vertical_lines": [],
	"explicit_horizontal_lines": [],
	"snap_tolerance": DEFAULT_SNAP_TOLERANCE,
	"join_tolerance": DEFAULT_JOIN_TOLERANCE,
	"edge_min_length": 3,
	"min_words_vertical": DEFAULT_MIN_WORDS_VERTICAL,
	"min_words_horizontal": DEFAULT_MIN_WORDS_HORIZONTAL,
	"keep_blank_chars": False,
	"text_tolerance": 3,
	"text_x_tolerance": 3,
	"text_y_tolerance": 3,
	"intersection_tolerance": 3,
	"intersection_x_tolerance": None,
	"intersection_y_tolerance": None,
}


def my_extract(table, x_tolerance=DEFAULT_X_TOLERANCE, y_tolerance=DEFAULT_Y_TOLERANCE):
	"""自定义抽取表格，改写抽取的数据结构，新添加了表格的坐标"""

	chars = table.page.chars
	table_arr = []

	def char_in_bbox(char, bbox):
		v_mid = (char["top"] + char["bottom"]) / 2
		h_mid = (char["x0"] + char["x1"]) / 2
		x0, top, x1, bottom = bbox
		return (
				(h_mid >= x0) and
				(h_mid < x1) and
				(v_mid >= top) and
				(v_mid < bottom)
		)

	for row in table.rows:
		arr = []
		row_chars = [char for char in chars
					 if char_in_bbox(char, row.bbox)]

		for cell in row.cells:
			if cell is None:
				cell_text = None
			else:
				cell_chars = [char for char in row_chars
							  if char_in_bbox(char, cell)]

				if len(cell_chars):
					cell_text = pdfplumber.utils.extract_text(cell_chars,
															  x_tolerance=x_tolerance,
															  y_tolerance=y_tolerance).strip()
					cell_text = cell_text.replace("\n", "").replace(" ", "")
				else:
					cell_text = ""
			arr.append(cell_text)
		table_arr.append(arr)

	return table_arr


def my_extract_tables_by_type(page, table_settings={}, type="record"):
	"""自定义表格抽取，主要是想得到每个表格的坐标\n
		type:
		      - list  返回坐标和嵌套list;
		      - df   返回坐标和dataframe格式数据;
		      - record  返回坐标和dataframe的records格式数据.
	"""

	tables = page.find_tables(table_settings)

	# ------------------------------------------------------------------------------------------------------------------
	# '''可视化提取到的表格结构边框，
	# pdf页面大小与图片页面大小不一致，需要调整'''
	# # 将pdf转换成图片
	# global pdf_path
	# pilimage = convert_from_path(pdf_path, dpi=96)[0]
	# cv2image = cv2.cvtColor(np.asarray(pilimage), cv2.COLOR_BGR2RGB)
	# ## 设置卷积核5*5
	# #kernel = np.ones((11, 11), np.uint8)
	# ## 图像的腐蚀，默认迭代次数
	# #cv2image = cv2.erode(cv2image, kernel)
	# # 在图片上框选出所有表格
	# for rect in tables:
	# 	cv2.rectangle(cv2image, (rect.bbox[0], rect.bbox[2]), (rect.bbox[1], rect.bbox[3]), (0, 255, 0), 4)
	# # 显示框选结果
	# cv2.namedWindow("Image", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_AUTOSIZE)
	# cv2.imshow("image", cv2image)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	# # 保存结果
	# imagename = os.path.splitext(os.path.split(pdf_path)[1])[0] + '.jpg'
	# cv2.imwrite("./result/" + imagename, cv2image)
	# ------------------------------------------------------------------------------------------------------------------

	extract_kwargs = dict((k, table_settings["text_" + k]) for k in [
		"x_tolerance",
		"y_tolerance",
	] if "text_" + k in table_settings)

	result_list = [{"bbox": table.bbox, "text": my_extract(table, **extract_kwargs)} for table in tables]
	if type == 'list':
		return result_list

	result_df = []
	for index, tab in enumerate(result_list):
		if index != 0:
			df = pd.DataFrame(tab['text'][1:], columns=tab['text'][0])  # 得到的table是嵌套list类型，转化成DataFrame更加方便查看和分析
			result_df.append({"bbox": tab["bbox"], "df": df})
	if type == 'df':
		return result_df

	table_records = []
	for item in result_df:
		new_col = [chr(ord('A') + i) + str(col) for i, col in enumerate(item['df'].columns)]
		item['df'].columns = new_col
		temp = item['df'].to_json(lines=True, orient="records", force_ascii=False) + "\n"
		table_records.append({'bbox': item['bbox'], "records": temp.replace("}", "}。")})

	return table_records


def box_sort(box_a, box_b, threshold_x=100, threshold_y=8):
	"""pdf页中，文本块的排序规则\n
		1、总体上，先按照x轴排，然后按照y轴排；\n
		2、如果x轴上的差距`threshold_x`很小，认为是相同的x值，顺序不分先后，开始用y轴排；\n
		3、如果y轴上的差距`threshold_y`很小，认为是相同的y值，顺序不变。
	:param box_a:  文本块a
	:param box_b:  文本块b
	:param threshold_x: 两个文本块在x轴的差距
	:param threshold_y: 两个文本块在y轴的差距
	:return:
	"""
	x_distence = box_a["x0"] - box_b["x0"]
	y_distence = box_a["bottom"] - box_b["bottom"]

	if abs(x_distence) >= threshold_x and x_distence < 0:        # x小的排前
		return -1
	elif abs(x_distence) >= threshold_x and x_distence > 0:      # x大的排后
		return 1
	elif abs(x_distence) < threshold_x:                          # x相等，用y排

		if abs(y_distence) > threshold_y and y_distence > 0:     # y大的排前
			return 1
		elif abs(y_distence) > threshold_y and y_distence <= 0:  # y小的排后
			return -1
		else:
			return 0


def sort_for_merge(word_list, threshold_x=0, threshold_y=10):
	"""
	文本块合并模块，解决一个句子中中英文被分隔开且无序的问题
	先预排序，之后合并文本块
	:param box_a:  文本块a
	:param box_b:  文本块b
	:param threshold_x: 两个文本块在x轴的差距
	:param threshold_y: 两个文本块在y轴的差距
	:return:
	"""
	def box_sort_x(box_a, box_b, threshold_x=0):
		"""
		按x轴由小到大排序
		"""
		x_distence = box_a["x0"] - box_b["x0"]
		if abs(x_distence) >= threshold_x and x_distence < 0:  # x小的排前
			return -1
		elif abs(x_distence) >= threshold_x and x_distence > 0:  # x大的排后
			return 1
		else:
			return 0

	def box_sort_y(box_a, box_b, threshold_y=15):
		"""
		按y轴由大到小排序
		"""
		y_distence = box_a["bottom"] - box_b["bottom"]  # 中英文字体高低不同，采用bottom进行距离计算比较可靠
		if abs(y_distence) >= threshold_y and y_distence > 0:  # y大的排前
			return 1
		elif abs(y_distence) >= threshold_y and y_distence < 0:  # y小的排后
			return -1
		else:
			return 0

	word_list = sorted(word_list, key=functools.cmp_to_key(box_sort_y))
	merged_list = []
	if word_list:
		head = 0  # 首
		for end in range(len(word_list) - 1):  # end --> 尾
			if abs(word_list[end]['bottom'] - word_list[end+1]['bottom']) >= threshold_y:  # y的距离超过阈值进行分行
				word_row = word_list[head:end + 1]  # 得到一行
				word_row = sorted(word_row, key=functools.cmp_to_key(box_sort_x))  # 对一行进行排序
				word_row = merge_blocks(word_row, threshold_sents=100, threshold_y=threshold_y)  # 合并文本块
				merged_list += word_row
				head = end + 1
			else:  # 不分行
				continue

	return merged_list

def merge_blocks(word_list, threshold_sents=100, threshold_y=15):
	"""
	合并属于同一句的文本块
	:param word_list:       位于同一水平线的文本块
	:param threshold_sents: 属于同一句的两个文本块x差距的阈值
	:return merged_list:    合并同句文本块的列表
	"""
	merged_list = []
	if word_list:
		box_a = word_list[0]  # 取出第一个比较的块
		merged_list.append(box_a)
		for box_b in word_list[1:]:
			if box_b:  # word_list中有超过两个
				x_distence = min(abs(box_b["x0"] - box_a["x0"]), abs(box_b["x1"] - box_a["x1"]))  # 计算x距离
				y_distence = abs(box_b["bottom"] - box_a["bottom"])
				if (x_distence <= threshold_sents) and (y_distence <=threshold_y):  # 属于同一句，进行合并
					box_ab = copy.deepcopy(box_a)  # 合并文本块
					box_ab['x0'] = box_a["x0"]
					box_ab['x1'] = box_b["x1"]
					box_ab['top'] = (box_a["top"] + box_b["top"])/2
					box_ab['bottom'] = (box_a["bottom"] + box_b["bottom"])/2
					box_ab['text'] = box_a["text"] + ' ' + box_b["text"]
					merged_list[-1] = box_ab
					box_a = box_ab
				else:  # 不从属于同一句
					merged_list.append(box_b)
					box_a = box_b
		return merged_list
	else:
		return merged_list


def replace_text_by_record(word_list,
						   result_records,
						   threshold_x=300):
	"""表格的json字符串，替换文字列表的相应内容
		1、根据表格的坐标，找到表格的范围；
		2、找到范围内的文本块；
	"""
	result_list = []
	for item_a in word_list:
		x0_a, x1_a, top_a, bottom_a = item_a['x0'], item_a['x1'], item_a['top'], item_a['bottom']
		result_list.append(item_a['text'])
		x_flag, y_flag = False, False
		for item_b in result_records:
			x_flag, y_flag = False, False
			bbox_b = item_b['bbox']
			x_flag = (x0_a > bbox_b[0]) and (x0_a < bbox_b[0]+threshold_x)
			y_flag = (top_a > bbox_b[1]) and (bottom_a < bbox_b[3])
			if x_flag and y_flag:
				result_list.remove(item_a['text'])
				temp_table_str = item_b['records'].replace("\"", "").replace("\/", "").replace("\\n", "")
				break
		if x_flag and y_flag and (temp_table_str not in result_list):
			result_list.append(temp_table_str)

	return result_list

def show_map_rect(rects, max_x=1200, max_y=900, with_text=False):
    """
    展示页面框架
    :param rects:
    :param max_x:
    :param max_y:
    :param with_text:
    :return:
    """
    tab = DramTable(max_x=max_x, max_y=max_y)

    idx = 0
    for obj in rects:
        tab.draw_2d_line([(obj["x0"], obj["top"]), (obj["x1"], obj["bottom"])])
        idx += 1

    tab.show_table()

def filter_split_line(box, split_lines, threshold_dist=500):
	"""
	 过滤掉切分太细的分割线，是为了解决文本块最后一列全是表格时被划分得太细的问题
	:param box: 要切分的文本块
	:param split_lines: 切割线
	:param threshold_dist: 分割线的距离筛选阈值
	:return filtered_split_lines: 筛选后的切割线
	"""
	box_v_lines = [box[0]] + split_lines + [box[2]]
	if len(box_v_lines) > 3:  # 检索出多条分割线时，复查是否有把表格分割太细的情况
		del_list = []
		del_list_tmp = []
		for start in range(len(box_v_lines)-1):
			if (box_v_lines[start+1] - box_v_lines[start]) < threshold_dist:
				del_list_tmp.append(box_v_lines[start])
			else:
				del_list += del_list_tmp[1:]
				del_list_tmp = []
		del_list += del_list_tmp[1:]
		filtered_split_lines = [line for line in box_v_lines if (line not in del_list)]
		return filtered_split_lines
	else:
		return box_v_lines


def extract_frame(page, show_frame=False):
	"""
	提取页面中列文本和图框区域的框线
	:param page: 页面
	:return: 分割出的文本区域和图框区域的框线坐标
	"""
	# 1.找出所有线条
	max_width, max_height = page.width, page.height
	# 调试画出所有线
	if show_frame:
		show_map_rect(page.edges, max_x=max_width, max_y=max_height, with_text=True)

	# 2.保留长度超过0.7倍页面宽的水平线，以及高度超过0.8被页面高的竖直线
	vert_lines = sorted(
		[x for x in page.vertical_edges if x['height'] > page.height * Decimal(0.65)],
		key=lambda x: x['x0'])
	# 筛掉页面以外的线
	vert_lines = [x for x in vert_lines
				  if x['x0']>=0 and x['x1']>=0 and x['y0']>=0 and x['y1']>0]
	hori_lines = sorted(
		[x for x in page.horizontal_edges if x['width'] > page.width * Decimal(0.7)],
		key=lambda x: x['top'])
	hori_lines = [x for x in hori_lines
				  if x['x0'] >= 0 and x['x1'] >= 0 and x['y0'] >= 0 and x['y1'] > 0]
	# 调试画出长的框线
	long_lines = vert_lines + hori_lines
	if show_frame:
		show_map_rect(long_lines, max_x=max_width, max_y=max_height, with_text=True)

	# 3.切分出矩形块
	total_area = max_width * max_height
	text_bboxs = []
	side_bboxs = []
	for v_idx in range(len(vert_lines)-1):
		for h_idx in range(len(hori_lines)-1):
			left = vert_lines[v_idx]['x0']
			left = left if left == 0 else left-1
			right = vert_lines[v_idx+1]['x1']
			right = right if right == max_width else right+1
			top = hori_lines[h_idx+1]['y0']
			top = top if top == max_height else top+1
			bottom = hori_lines[h_idx]['y1']
			bottom = bottom if bottom == 0 else bottom-1
			bbox = (left, top, right, bottom)
			bbox_area = (right-left)*(bottom-top)
			if bbox_area > Decimal(0.1) * total_area: # 判断为文本区域
				text_bboxs.append(bbox)
			elif bbox_area > Decimal(0.05) * total_area:  # 判断为图框区域
				side_bboxs.append(bbox)
			else:  # 判断为边界区域
				pass
	# 调试画出文本区域和图框区域的框架
	if not text_bboxs:
		print('没有提取到文本区域框架！！！')
	if not side_bboxs:
		print('没有提取到图框区域框架!!!')
	all_bboxs = text_bboxs + side_bboxs
	if not all_bboxs:
		return  {
		'split_text_bboxs': text_bboxs,  # 左侧文本内容切分后列的 binding box
		'side_bboxs': side_bboxs  # 右侧图框 binding box
	}
	if show_frame:
		pt = DramTable(max_x=max_width, max_y=max_height)
		for little_box in all_bboxs:
			pt.draw_bbox(little_box)
		pt.show_table()
		
	# 5.对文本区域分列
	split_text_bboxs = []
	for text_box in text_bboxs:
		words = page.crop(text_box).extract_words(keep_blank_chars=True)
		min_x = math.ceil(text_box[0])
		max_x = math.floor(text_box[2])
		non_insert_xs = []
		for x in range(min_x, max_x):
			is_insert = False
			for word in words:
				if word['x0'] <= x <= word['x1']:
					is_insert = True
					break
			if not is_insert:
				x = Decimal(x)
				if len(non_insert_xs) == 0:
					non_insert_xs.append(x)
				else:  # 去掉连续间距为1的线
					dist = x - non_insert_xs[-1]
					if math.isclose(dist, 1, rel_tol=max_tol):
						non_insert_xs[-1] = x
					else:
						non_insert_xs.append(x)
		# 筛选切割线
		box_v_lines = filter_split_line(text_box, non_insert_xs, threshold_dist=Decimal(0.15) * max_width)

		# 根据切割线分割文本块，筛掉面积过小的块（认为不包含文本）
		for box_v_idx in range(len(box_v_lines)-1):
			split_text_box = (box_v_lines[box_v_idx],
							  text_box[1],
							  box_v_lines[box_v_idx+1],
							  text_box[3])
			split_bbox_area = (split_text_box[2] - split_text_box[0]) * (split_text_box[3] - split_text_box[1])
			if split_bbox_area > Decimal(0.05) * total_area:  # 包含文本的区域
				split_text_bboxs.append(split_text_box)
			else:
				pass
	return {
		'split_text_bboxs': split_text_bboxs,  # 左侧文本内容切分后列的 binding box
		'side_bboxs': side_bboxs  # 右侧图框 binding box
	}

def extract_orderly_words(page, noside=False):
	"""
	提取按列排好序的所有文本块，第二版排序方案
	:param page: 输入页面
	:param noside: Boolean 是否提取侧边图框区域 False表示留下side图框区域并提取相关内容
	:return words:
	"""
	map_frame = extract_frame(page, show_frame=True)  # 提取页面中的框线
	split_text_bboxs = map_frame['split_text_bboxs']
	side_bboxs = map_frame['side_bboxs']

	words = []
	for text_box in split_text_bboxs:
		paragraph_words = page.crop(text_box).extract_words(keep_blank_chars=True)
		paragraph_words = sorted(paragraph_words, key=lambda x: x['top'])
		threshold_sents = Decimal(0.6)*(text_box[2] - text_box[0])
		paragraph_words = merge_blocks(paragraph_words, threshold_sents=threshold_sents, threshold_y=8)
		words += paragraph_words

	if not noside:  # 提取侧边图框的信息
		for side_box in side_bboxs:
			paragraph_words = page.crop(side_box).extract_words(keep_blank_chars=True)
			threshold_sents = Decimal(0.6) * (side_box[2] - side_box[0])
			paragraph_words = merge_blocks(paragraph_words, threshold_sents=threshold_sents, threshold_y=8)
			words += paragraph_words
	return words

def pdfplumber_extract_txt(pdf_path):
	"""
	抽取pdf内容：
		1、文本内容抽取；
		2、表格内容抽取；
		3、返回表格内容和文本内容
	"""
	all_sentence_list = []
	with pdfplumber.open(pdf_path) as pdf:
		for index in range(len(pdf.pages)):
			page = pdf.pages[index]
			word_list = extract_orderly_words(page)
			if not word_list:
				word_list = page.extract_words(keep_blank_chars=True)
				word_list = sort_for_merge(word_list)  # 预排序以及文本块合并
				word_list = sorted(word_list, key=functools.cmp_to_key(box_sort))
			result_records = my_extract_tables_by_type(page)
			all_sentence_list += replace_text_by_record(word_list, result_records)
		return "\n".join(all_sentence_list)


def pdfplumber_extract_all_txt(pdf_dir=r"..\resource\pdf\txt_pdf",
							   txt_dir=r"..\resource\txt"):
	"""
	解析文件夹下的pdf，并把结果写到文件夹
	:param pdf_dir: pdf所在目录
	:param txt_dir: pdf解析结果所在目录
	:return:
	"""
	global pdf_path
	for pdf_file in tqdm(os.listdir(pdf_dir)):
		if pdf_file.endswith("pdf"):
			pdf_path = os.path.join(pdf_dir, pdf_file)
			content = pdfplumber_extract_txt(pdf_path)
			print(content)
			with open(os.path.join(txt_dir, pdf_file) + ".txt", "w", encoding="utf-8") as f:
				f.write(content)


if __name__ == '__main__':
	# 单个pdf解析测试
	'''global pdf_path
	pdf_path = r"txt_pdf/test_url.pdf"
	txt = pdfplumber_extract_txt(pdf_path)
	print(txt)'''


	# 批量解析测试
	dir = r"txt_pdf"
	pdfplumber_extract_all_txt(pdf_dir=dir)

