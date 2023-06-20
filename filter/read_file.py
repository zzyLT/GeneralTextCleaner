import pandas as pd
import re
import numpy as np
import PyPDF2
import os
import shutil
from ....OCR.pdf2img import *
from ....OCR.img2text import *

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
