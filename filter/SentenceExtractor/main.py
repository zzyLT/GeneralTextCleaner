import os

import pandas as pd

from .read_file import *
from .text_structure import *
from .text_filter import *

if __name__ == '__main__':

    data = pd.read_excel(r'E:\NOS\documents\物流：课程内容\物流数据内容（中诺思提供）.xlsx', sheet_name='Sheet2')
    for text in list(data['文件内容']):
        sentence = extractSentences(text)
        print(sentence)

    exit()
    #1. 文件读取
    root = '../../documents/'
    files = os.listdir(root)
    for file in files:
        if '.txt' in file:
            pass
        elif '.doc' in file:
            pass
        elif '.ppt' in file or '.pptx' in file:
            pass
        elif '.pdf' in file and file.replace('.pdf', '.txt') not in files:
            continue
            if '贵州交通职业技术学院——2020级人才培养方案-物流管理专业-11-10' in file:
                hasTable, folder, excel = pdf2excel(root+file)
                puretext = pdf2puretext(root+file)
                puretext = addLable(puretext)
                sentence = getSentences(puretext)
                if hasTable:
                    sentence = getSentences(pd.read_excel(folder+excel, sheet_name=None, header=None), type='table')
                print('\n'.join(sentence))
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
