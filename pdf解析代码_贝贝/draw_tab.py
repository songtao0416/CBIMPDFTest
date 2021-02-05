#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 linxinluo. All rights reserved.

"""
  Author:  linxinluo  -- <luolx@cadg.cn>
  Purpose: Python3 File
  Created: 2019-08-02
"""
import os

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from pdftabextract.common import read_xml, parse_pages


#######################################################################################
class DramTable(object):
    """这是DramTable"""

    def __init__(self, max_x=1200, max_y=900):
        """Constructor"""

        self.plt, self.ax = plt.subplots()
        # 设置x，y值域
        self.ax.set_xlim(left=0, right=float(max_x))
        self.ax.set_ylim(bottom=0, top=float(max_y))

        self.ax.xaxis.set_ticks_position('top')  # 将X坐标轴移到上面
        self.ax.invert_yaxis()  # 反转Y坐标轴

    # ------------------------------------------------
    def draw_line_by_pos(self, top, left, width, height):
        """
        画一条线段
        :param top:
        :param left:
        :param width:
        :param height:
        :return:
        """
        p1 = (left, top)
        p2 = (left + width, top)
        p3 = (left + width, top + height)
        p4 = (left, top + height)

        sp = (top, left)
        ep = (top + width, left + height)

        self.draw_2d_line([p1, p2])
        self.draw_2d_line([p2, p3])
        self.draw_2d_line([p3, p4])
        self.draw_2d_line([p4, p1])

    # ------------------------------------------------
    def draw_2d_line(self, line_pos, text=''):
        """
        画一条线段
        :param line_pos:    list(tuple)     [(1, 1), (3, 2)]
        :return:
        """
        # print(line_pos)
        line1_xs, line1_ys = zip(*line_pos)

        self.ax.add_line(Line2D(line1_xs, line1_ys, linewidth=1, color='blue'))
        mid_posx, mid_posy = (line_pos[0][0] + line_pos[1][0]) / 2, (line_pos[0][1] + line_pos[1][1]) / 2
        if text is not None and text != '':
            self.ax.text(mid_posx, mid_posy, text)

    # ------------------------------------------------
    def draw_rect(self, rect):
        """
        画矩形
        :param rect:        dict        {
                'crop_box': (n1, n2, n3, n4),
                'left_top': (may_map_frame[0]['x0'], may_map_frame[0]['y1']),  # 矩形的 左上角 坐标点
                'width': may_map_frame[0]['width'],  # 矩形宽度
                'height': may_map_frame[0]['height'],  # 矩形高度
                'x_range': (may_map_frame[0]['x0'], may_map_frame[0]['x1']),
                'y_range': (may_map_frame[0]['y0'], may_map_frame[0]['y1']),
            }
        :return:
        """
        p1 = rect['crop_box'][:2]
        p3 = rect['crop_box'][2:]
        p2 = (p3[0], p1[1])
        p4 = (p1[0], p3[1])

        self.draw_2d_line([p1, p2])
        self.draw_2d_line([p2, p3])
        self.draw_2d_line([p3, p4])
        self.draw_2d_line([p4, p1])

    # ------------------------------------------------
    def draw_bbox(self, rect):
        """
        画矩形
        :param rect:        tuple        (n1, n2, n3, n4)四元组
        :return:
        """
        p1 = rect[:2]
        p3 = rect[2:]
        p2 = (p3[0], p1[1])
        p4 = (p1[0], p3[1])

        self.draw_2d_line([p1, p2])
        self.draw_2d_line([p2, p3])
        self.draw_2d_line([p3, p4])
        self.draw_2d_line([p4, p1])

    # ------------------------------------------------
    def show_table(self):
        """"""
        # 展示
        # self.plt.plot()
        # plt.rcParams['savefig.dpi'] = 600  # 图片像素
        # plt.rcParams['figure.dpi'] = 600  # 分辨率
        self.plt.show()


# ------------------------------------------------
def draw_design_tab():
    """"""
    DATAPATH = '/Users/linxinluo/open-app/pdf2xml-viewer/design_spec/'
    OUTPUTPATH = '/Users/linxinluo/open-app/pdf2xml-viewer/design_spec/generated_output/'
    INPUT_XML = '/Users/linxinluo/open-app/pdf2xml-viewer/design_spec/cbim_word_spec_template.pdf.xml'

    # Load the XML that was generated with pdftohtml
    xmltree, xmlroot = read_xml(os.path.join(DATAPATH, INPUT_XML))

    # parse it and generate a dict of pages
    pages = parse_pages(xmlroot)

    p_num = 0
    p = pages[1]

    print('number', p['number'])
    print('width', p['width'])
    print('height', p['height'])
    print('image', p['image'])
    print('the first three text boxes:')

    tab = DramTable()
    tab.draw_line_by_pos(p.get('top', 0), p.get('left', 0), p['width'], p['height'])

    for txt in p['texts']:
        tab.draw_line_by_pos(txt['top'], txt['left'], txt['width'], txt['height'])

    tab.show_table()


if __name__ == '__main__':
    draw_design_tab()
