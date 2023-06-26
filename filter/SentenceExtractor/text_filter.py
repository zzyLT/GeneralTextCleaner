# interpreter pytorch_py3.7

import json
import pandas as pd
import re
import numpy as np
import os
# from read_file import *
from .text_structure import addLable

KEYWORDS = [
    '目标 要求 名称 技能'.split(' '),
    '能力 知识 素质 技能'.split(' '),
    '教学[\s\u4e00-\u9fa5]*?要求|主要[\s\u4e00-\u9fa5]*?内容|课程[\s\u4e00-\u9fa5]*?名称'
]

def getSentences(text, type = 'text') -> list:
    """
    :param text: 待清洗的文本
    :param type: 文本格式
                'text':纯文本
                'table':表格
    :return: 清洗后得到的语句数组
    """
    sentences = []
    if type == 'text':
        text = text.replace('\n', '[ligne]')
        pattern0 = r'</title_(\d{3})_(\d{3})>(.*?(' + '|'.join(KEYWORDS[1]) + ')[\u4e00-\u9fa5]*?(' + '|'.join(KEYWORDS[0]) + '))[\s\t]*?[\：\:\n]?\[ligne\]'
        result = re.finditer(pattern0, text)
        candidates = []
        for lst in result:
            # print(lst.start(), lst.end(), text[lst.start(): lst.end()])
            conf = re.findall(r'</title_(.{3})_(.{3})>', text[lst.start(): lst.end()])
            if len(conf) > 0:
                conf = conf[0]
                next_part = re.search(f'</title_{conf[0]}_{conf[1]}>', text[lst.end():])
                if next_part != None:
                    candidates.append(text[lst.end(): lst.end() + next_part.start()])
                    text = text.replace('\n'.join(text[lst.end(): lst.end() + next_part.start()].split('\n')[:-1]), '')
                else :
                    candidates.append(text[lst.end()])
                    text = text.replace(text[lst.end():], '')
            else:
                candidates.append(text[lst.end():])
        candidates = [item for item in candidates if item]
        for candidat in candidates:
            try:
                (cls, z_index) = re.findall('^.*?<title_(\d+)_(\d+)>', candidat)[0]
                candidat = re.findall('</title_(\d+)_(\d+)>(.*?)(<title)+', candidat)
                for info in candidat:
                    if '。' in info[2]:
                        sentences.append(re.sub('\s|\t|\[ligne\]', '', info[2]))
                    else:
                        sentences.append(re.sub('\[ligne\]', '\n', info[2]))
            except:
                if '。' in candidat:
                    sentences.append(re.sub('\s|\t|\[ligne\]', '', candidat))
                else:
                    sentences.append(re.sub('\s|\t|\[ligne\]', '', candidat))

    elif type == 'table':
        def getNbOfRow(row):
            i = len(row)
            for i in range(len(row))[::-1]:
                if str(row[i]) != 'nan': return i + 1
            return i

        for key in text.keys():
            data = text[key]

            nb = 0
            row_idx = []
            for index, row in data.iterrows():
                # print(list(row))
                newL = False
                nbOfRow = getNbOfRow(list(row))
                if not (nb == nbOfRow or nb - nbOfRow == 1) and str(list(row)[0]) != 'nan':
                    print('new line', list(row)[:nbOfRow])
                    print(list(row)[nbOfRow:])
                    nb = nbOfRow
                    newL = True
                    row_idx = []
                for i in range(nb):
                    item = list(row)[i]
                    if str(item) == 'nan': continue
                    if len(re.findall('(' + '|'.join(KEYWORDS[0]) + ')$', item)) > 0 and len(
                            re.findall(KEYWORDS[2], item)) == 0:
                        print('find a row', list(row), item)
                        if newL == False:
                            newL = True
                            row_idx = []
                        row_idx.append(i)
                if newL == False and len(row_idx) > 0:
                    for id in row_idx:
                        if str(list(row)[id]) != 'nan':
                            if len(sentences) > 0:
                                if sentences[-1][-1] != '。':
                                    sentences[-1] += list(row)[id]
                                else: sentences.append(list(row)[id])
                            else:
                                sentences.append(list(row)[id])
                            print('>> append: ', list(row)[id])

    return [item for item in sentences if item]


def extractSentences(text:str) -> str:
    """
    :param text: 待清洗的文本内容
    :return: json结果
    """
    sentence = [item for item in getSentences(addLable(text)) if item]
    result = []
    for s in sentence:
        result.extend(re.split(r'。|\n', s))
    return json.dumps({'sentences': [item for item in result if len(item)>4]}, ensure_ascii=False)

if __name__ == '__main__':

    #1. 文件读取
    root = '../documents/'
    files = os.listdir(root)
    for file in files:
        if '.txt' in file:
            f = open(root + file, 'r', encoding='utf-8')
            text = f.read()
            f.close()
            print(f'>> 【{file}】 \n', addLable(text))
            break

        elif '.doc' in file:
            pass
        elif '.ppt' in file or '.pptx' in file:
            pass
        elif '.pdf' in file and file.replace('.pdf', '.txt') not in files:
            pass
            # text = pdf2text(root, file)

        elif '.xlsx' in file or '.xls' in file:
            pass
        else: # 想不到先
            pass
    exit()
    file = pd.read_excel('物流数据内容（中诺思提供）.xlsx', sheet_name=None)
    data = file['Sheet2']
