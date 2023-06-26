import json

import pandas as pd
from SentenceExtractor import text_filter,text_structure

data = pd.read_excel(r'E:\NOS\documents\物流：课程内容\物流数据内容（中诺思提供）.xlsx', sheet_name='Sheet2')
for text in list(data['文件内容']):
    # print(text_structure.addLable(text))
    sentence = json.loads(text_filter.extractSentences(text))
    print(sentence['sentences'])
