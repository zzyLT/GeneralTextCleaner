# interpreter pytorch_py3.7

import pandas as pd
import re
import numpy as np
import os
# from read_file import *
from text_structure import stuctureIdentifier

def newDic(index, name, first, second, third, fourth, sentence):
    return {
        'file_index': index,
        'class':name,
        'first':first,
        'second':second,
        'third':third,
        'fourth': fourth,
        'sentence':sentence,
    }

def clean():
    principe = []

    def addDic(fileID, name, first, second, third, fourth, sentence):

        sentence = re.sub(r'\d+、|（\d+）|\(\d+\)|\d+\.|\d．|\t|\u3000\u3000|\?|项目\d：|：\u3000|\d\n', '[sentence]', sentence)
        sentence = re.sub('。', '。[sentence]', sentence)
        sentence = re.sub('；', '；[sentence]', sentence)

        s = re.split(r'\[sentence\]', sentence)
        s = [x.strip() for x in s if x.strip() != '']
        for content in s:
            if len(content) < 4:
                continue

            elif content[-2:] == '能力' and (len(content) == 4 or len(content) == 6):
                print('........', content)
                fourth = content
            else:
                print('................', content)
                principe.append(newDic(fileID, name, first, second, third, fourth, re.sub('\u3000', '', content)))

    #part: 课程目标
    for index, row in data.iterrows():

        name, first, second, third, fourth, sentence = row['课程名称'], '课程目标', '', '', '', ''
        print('\n===================', row['课程名称'], '===================\n')
        result0 = '\n'.join(re.findall('[一二三四五六七八九十]+[、\.]课程目标(.*?)[一二三四五六七八九十][、|\.|、]', row['文件内容'].replace('\n', '')))
        result0 = re.sub('\u3000\d[\.、]', '', result0)
        result0 = re.sub('[① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬ ⑭ ⑮ ⑯ ⑰ ⑱ ⑲ ⑳]', '\u3000', result0)
        result0 = re.sub('（.{1}）', '\u3000', result0)
        result = re.findall('(总体目标*)(.*?)(具体目标*)(.*?)$', result0)

        if len(result) > 0:

            addDic(index, name, first, result[0][0], third, fourth, result[0][1])

            # 具体目标
            print(result[0][2], "  -->  ")
            second = result[0][2]
            third, fourth = '', ''
            sentence = result[0][3]

        else: sentence = result0

        sentence = re.split('(\u3000|\t|\（.{1}\）|\d．|\d\.|\d\u3000)+(.{2}目标|.{4}目标|.{8}目标)[\u3000\t\?：]+(.*?)', sentence)
        sentence = [x.strip() for x in sentence if x.strip() != '']
        print(sentence)
        idx = 0
        while idx < len(sentence):
            if len(sentence[idx]) < 4:
                pass
            elif sentence[idx][-2:] == '目标' and (
                    len(sentence[idx]) == 4 or len(sentence[idx]) == 6 or len(sentence[idx]) == 10):
                print('....', sentence[idx])
                third = sentence[idx]
                fourth = ''
            else:
                addDic(index, name, first, second, third, fourth, sentence[idx])
            idx += 1

    #part: 课程内容
    for index, row in data.iterrows():
        first, second, third, fourth, sentence = '课程内容', '', '', '', ''
        print('\n\n\n\n===================', row['课程名称'], '===================')
        result = re.findall(
            '[一二三四五六七八九十]+[、\.．](课程内容.*?)[\u3000\n\t\s\d、]+(.*?)([一二三四五六七八九十][、\.、](教学|课程)?实施(建议)?.*?)\u3000',
            row['文件内容'].replace('\n', ''))

        if len(result) == 0:
            result = re.findall('[一二三四五六七八九十]+[、\.．](课程设计.*?)[\u3000\n\t\s\d、]+(.*?)$', row['文件内容'].replace('\n', ''))
        content = result[0][1]
        if '目标' not in content:
            print('当前文段中无【目标】字段')
            continue

        result = re.findall('(教学目标)：(.*?)(教学.{2})：', content)
        if len(result) == 0:
            result = re.findall('(教学目标)：(.*?)$', content)
            if len(result) == 0:
                result = re.findall('^(.*?)(教学.{2})：', content)
                if len(result) == 0:
                    result = [content]
                else:
                    print('solu1')
                    result = [l[0] for l in result]
            else:
                print('solu2')
                result = [l[1] for l in result]
        else:
            print('solu3')
            result = [l[1] for l in result]

        if len(result) > 0:
            for r in result:

                sentence = r[:-5] if '目标：' == r[-3:] else r

                sentence = re.sub('[\s]', '', sentence)  # (（\d）)(\d\.)(\d．)
                sentence = re.sub(r'\d+、|（\d+）|\d+\.|\d．|[\t\u3000]|：|\u3000\u3000', '[sentence]', sentence)
                sentence = re.sub(r'\d+、|（\d+）|\(\d+\)|\d+\.|\d．|\t|\u3000\u3000|表\？|项目\d：|：\u3000|\d\n|项目[一二三四五六七八九十]',
                                  '[sentence]', sentence)
                sentence = re.sub('。', '。[sentence]', sentence)
                sentence = re.sub('；', '；[sentence]', sentence)
                sentence = re.sub('学时\d', '[sentence]', sentence)

                second, third = '', ''
                for st in sentence.split('[sentence]'):
                    print('>> ', st)
                    if len(st) < 4: continue
                    if '目标' in st[-3:] and len(st) < 10:
                        for g in re.findall("(.{2}目标)", st):
                            if g == '学习目标':
                                second = g
                            else:
                                third = g
                            st = st.replace(g, '')
                    if third != '' and len(st) > 4:
                        if len(re.findall('表\d|\（.{1}\）', st)) > 0: break
                        addDic(index, row['课程名称'], first, second, third, fourth, st)
                        print(f'【{second}，{third}】-->', st)

    principe = pd.DataFrame(principe)
    principe['count'] = [len(sen) for sen in list(principe['sentence'])]
    principe.sort_values(by=['count'], ascending=False)
    return principe.drop_duplicates([ 'class', 'first', 'second', 'third', 'fourth', 'sentence'], ignore_index=True)

if __name__ == '__main__':

    #1. 文件读取
    root = '../documents/'
    files = os.listdir(root)
    for file in files:
        if '.txt' in file:
            f = open(root + file, 'r', encoding='utf-8')
            text = f.read()
            f.close()
            print(f'>> 【{file}】 \n', stuctureIdentifier(text))
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
