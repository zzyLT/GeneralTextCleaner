import pandas as pd
import re
import numpy as np
import PyPDF2
import os
import shutil
from pdf2img import *
from img2text import *

import pdfplumber
import xlwt

def pdf2excel(pdf_path):
    '''
    :param：
    pdf_path:   pdf 文档的路径
    '''
    workbook = xlwt.Workbook()            # 定义一个空的工作表，名为workbook
    sheet = workbook.add_sheet('Sheet1')  # 为工作表添加一个 sheet，sheet名称为 'Sheet1'，变量名为 sheet

    # 使用 pdfplumber.open 方法读取pdf 中所有信息
    pdf = pdfplumber.open(pdf_path)

    i = 0   # Excel 行序号起始位置，Python 中往往从 0 开始是计算
    getThings = False
    # 以 PDF 的一页为单位，循环读取所有 PDF 页
    for page in pdf.pages:
        for table in page.extract_tables():
            # table 表示这一页的所有表格，格式为多维列表
            # lrow = 1
            for row in table:
                # row 表示表 table 中的一行，格式为列表
                # if lrow != len(row):
                #     print(sheetNB)
                #     sheet = workbook.add_sheet('Sheet'+str(sheetNB))
                #     lrow = len(row)
                #     sheetNB += 1
                #     i = 0
                for j in range(len(row)):
                    sheet.write(i, j, row[j].replace('\n',''))
                    getThings = True
                i += 1
    pdf.close()
    rt = '/'.join(pdf_path.split('/')[:-1]) if len(pdf_path.split('/')) > 1 else './'
    if not os.path.exists(rt + '/tmpEXCEL/'):
        os.mkdir(rt + '/tmpEXCEL/')
    workbook.save(rt + '/tmpEXCEL/' + pdf_path.split('/')[-1].replace('.pdf', '.xlsx'))
    print('写入excel成功!')
    return getThings, rt + '/tmpEXCEL/', pdf_path.split('/')[-1].replace('.pdf', '.xlsx')

def pdf2text(folder_path, file_name):
    folder_path += '/' if folder_path[-1] != '/' or folder_path[-1] != '\\' else ''
    if file_name[-len('.pdf'):] == '.pdf': file_name = file_name[:-len('.pdf')]
    if file_name[0]== '/' or folder_path[:1] == '\\': file_name = file_name[:-len('.pdf')]

    pdfFileObj = open(folder_path + file_name + '.pdf', 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    text = ''
    for page_number in range(len(pdfReader.pages)):
        tmp = (pdfReader.pages[page_number]).extract_text()
        if len(tmp) == 0: break
        text += tmp
    pdfFileObj.close()

    if text == '': #没有提取出文字，有可能pdf为图片形式
        print('transforming the images...')
        folder_path = folder_path
        if not os.path.exists(folder_path+'tmpOCR/'):
            os.mkdir(folder_path+'tmpOCR/')
        pyMuPDF_fitz(folder_path + file_name + '.pdf', folder_path+'tmpOCR/'+file_name)

        img_length = len(os.listdir(folder_path+'tmpOCR/'+file_name))
        for i in range(img_length):
            print('>> ', f'images_{i}.png')
            text += '\n'.join(ocr_img(folder_path+'tmpOCR/', f'images_{i}.png', file_name))
        print('>> done  ', file_name)

        try:
            shutil.rmtree(folder_path + 'tmpOCR/' + file_name)
        except:
            pass

    return text

def pdf2puretext(path:str):
    """:param path: pdf文件路径
    """
    def not_within_bboxes(obj):
        """Check if the object is in any of the table's bbox."""

        def obj_in_bbox(_bbox):
            """See https://github.com/jsvine/pdfplumber/blob/stable/pdfplumber/table.py#L404"""
            v_mid = (obj["top"] + obj["bottom"]) / 2
            h_mid = (obj["x0"] + obj["x1"]) / 2
            x0, top, x1, bottom = _bbox
            return (h_mid >= x0) and (h_mid < x1) and (v_mid >= top) and (v_mid < bottom)

        return not any(obj_in_bbox(__bbox) for __bbox in bboxes)

    puretext = ''
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            # print("\n\n\n\n\nAll text:")
            # print(page.extract_text())
            # Get the bounding boxes of the tables on the page.
            bboxes = [
                table.bbox
                for table in page.find_tables(
                    # table_settings={
                    #     "vertical_strategy": "explicit",
                    #     "horizontal_strategy": "explicit",
                    #     "explicit_vertical_lines": page.curves + page.edges,
                    #     "explicit_horizontal_lines": page.curves + page.edges,
                    # }
                )
            ]
            # print("\n\n\n\n\nText outside the tables:")
            puretext += page.filter(not_within_bboxes).extract_text()

    return re.sub('-\s*\d+\s*-', '', puretext)

if __name__ == '__main__':

    #1. 文件读取
    root = '../documents/'
    files = os.listdir(root)
    for file in files:
        if '.txt' in file:
            pass
        elif '.doc' in file:
            pass
        elif '.ppt' in file or '.pptx' in file:
            pass
        elif '.pdf' in file and file.replace('.pdf', '.txt') not in files:
            if '贵州交通职业技术学院——2020级人才培养方案-物流管理专业-11-10' in file:
                hasTable, folder, excel = pdf2excel(root+file)
                print(hasTable, folder, excel)
                puretext = pdf2puretext(root+file)
                print(text)
            continue
            text = pdf2text(root, file)
            # print(text)
            with open(root+file.replace('.pdf','.txt'), 'w', encoding='utf-8') as f:
                f.write(text)
            f.close()
            print('>> done  ', file)

        elif '.xlsx' in file or '.xls' in file:
            pass
        else: # 想不到先
            pass
