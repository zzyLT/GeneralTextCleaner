import re, os, sys
import pandas as pd

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

#所有标题识别正则表达式及其对应id
PATTERN_TITLE_LIST = {
    '\??[一二三四五六七八九十]+\s*、': 0,
    '（\s*[一二三四五六七八九十]+\s*）|\(\s*[一二三四五六七八九十]+\s*\)': 1,
    '\??\d+\s*[\.\．]': 2,
    '\??\d{1,2}\s?[\.．]\s?\d{1,2}': 3,
    '\(?\d+\)|（?\d+）': 4,
    '\??\d+\s*、': 5,
    '附\s*[录表][一二三四五六七八九十0-9]?[：\:\d+]?': 10,
    '[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]':11,
    '模\s*块?\s*[一二三四五六七八九十0-9]\s*[、：]?': 997,
    '项\s*目\s*[一二三四五六七八九十0-9]\s*、?': 998,
    '表\d+\s': 999,  # [\u4e00-\u9fa5_a-zA-Z0-9]{2,6}\s*[\:：]
}
PATTERN_LABEL_NUMBER = r'[^一二三四五六七八九十0-9①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]+'

def initWithLabels(text:str) -> str:
    """
    :param text:待清洗的文本
    :return: 带有文章结构标签的文本
    """

    text = re.sub(r'[\s\t\u3000\n\?]{2,}', '\n', text)
    for title_pattern in PATTERN_TITLE_LIST:
        #         print('>> ', title_pattern)
        # 先全标
        pattern = r"([\n\s\t]+)(" + title_pattern + r")(\s*[\u4e00-\u9fa5_a-zA-Z])"
        text = re.sub(pattern,
                      r'\1<title_' + str(PATTERN_TITLE_LIST[title_pattern]).zfill(3) + r'_999>\2</title_' + str(
                          PATTERN_TITLE_LIST[title_pattern]).zfill(3) + r'_999>\3', text)
    return text


def lastNumber(current:str)->str:
    """
    :param current:当前文章标题编码
    :return: 当前所处标题的前一个同级标题编码
    """
    print('in lastNumber:', current)
    try:
        current = re.findall(f'<title_\d+_\d+>(.*?)</title_\d+_\d+>', current)[0]
    except:
        pass
    current = re.sub('</?title_\d+_(\d+)>', '', current)  # re.findall(f'<title_\d+_\d+>(.*?)</title_\d+_\d+>', current)
    label = re.sub(PATTERN_LABEL_NUMBER, '', current)
    if label in '一 二 三 四 五 六 七 八 九 十 十一 十二 十三 十四 十五'.split(' '):
        tmp = '一 二 三 四 五 六 七 八 九 十 十一 十二 十三 十四 十五'.split(' ')
        try:
            return tmp[tmp.index(label) - 1]
        except:
            pass
    elif label in '① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬ ⑭ ⑮ ⑯ ⑰ ⑱ ⑲ ⑳'.split(' '):
        tmp = '① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬ ⑭ ⑮ ⑯ ⑰ ⑱ ⑲ ⑳'.split(' ')
        try:
            return tmp[tmp.index(label) - 1]
        except:
            pass
    else:
        try:
            return str(int(label) - 1)
        except:
            pass  # TODO: 没想到还有什么情况
    return str(-1)


def lastTitle(number, current):
    if len(re.findall('[0-9一二三四五六七八九十]+', current)) == 1:
        return re.sub('[0-9一二三四五六七八九十]+', number, current)


def getIndex(above, id, current, below):
    if len(above) > 0:
        print('en(above) > 0')
        if isFirst(current):
            print('>> 当前语句为标题1')
            result = re.findall(f'<title_(\d+)_(\d+)>(.*?)</title_\d+_\d+>', above)
            if len(result) > 0:
                print(result[-1])
                if int(result[-1][0]) == id:
                    return int(result[-1][1])
                else:
                    return int(result[-1][1]) + 1
        else:
            last_number = lastNumber(current)
            print('last number: ', last_number)
            if last_number != '-1':
                print('last number:::', last_number, current)
                label = re.findall(
                    f'<title_{str(id).zfill(3)}_(\d+)>(.*?)</title_{str(id).zfill(3)}_(\d+)>[\s\t]*?(.*?)[\s\t\n]',
                    above)
                if len(label) > 0:
                    print('>> 对应标签记录： ', label)
                    zidx = [int(lab[0]) for lab in label]
                    content = [lab[1] for lab in label]
                    df = pd.DataFrame(columns=['z_index', 'content', 'title'])
                    df['z_index'] = zidx
                    df['content'] = content
                    df['title'] = [lab[-1] for lab in label]
                    print('>> all last label: ', df)
                    df = df.drop_duplicates(['z_index'], keep='last')
                    possible_index, possible_title = [], []
                    for index, row in df.iterrows():
                        if last_number == re.sub(PATTERN_LABEL_NUMBER, '', row['content']):
                            print(row['content'])
                            possible_index.append(row['z_index'])
                            possible_title.append(row['title'])
                    print('possible_index: ', possible_index)
                    if len(possible_index) == 1:
                        return possible_index[0]
                    elif len(possible_index) > 1:
                        coincidence, most_plossible_index = 0, -1
                        current_title = re.sub(f'<title_\d+_(\d+)>.*?</title_\d+_\d+>|[\s\t\n]', '', current)
                        print('当前标题内容：', current_title, possible_index)
                        for i in range(len(possible_index)):  # [::-1], possible_title[::-1])
                            idx, text = possible_index[::-1][i], possible_title[::-1][i]
                            print("过往标题内容：", idx, text)
                            if i < len(possible_index) - 1:
                                context = \
                                re.split(f'</title_{str(id).zfill(3)}_{str(possible_index[::-1][i + 1]).zfill(3)}>',
                                         above)[-1]
                                context = f'<title_{str(id).zfill(3)}_{str(idx).zfill(3)}>'.join(
                                    re.split(f'<title_{str(id).zfill(3)}_{str(idx).zfill(3)}>', context)[:-1])
                                all_label = re.findall(r'</title_\d{3}_\d{3}>', context)
                                tmp_index = 999
                                for lab in all_label[::-1]:
                                    past_idx = re.findall(r'</title_\d{3}_(\d{3})>', lab)[0]
                                    if tmp_index <= int(past_idx): continue
                                    past_class = re.findall(r'</title_(\d{3})_\d{3}>', lab)[0]
                                    print(past_idx, past_class,
                                          f'</title_{past_class}_{past_idx}>(.*?)</title_{past_class}_{past_idx}>')
                                    past_label = \
                                    re.findall(f'<title_{past_class}_{past_idx}>(.*?)</title_{past_class}_{past_idx}>',
                                               context)[-1]
                                    next_label = re.findall(f'<title_{past_class}_\d+>(.*?)</title_{past_class}_\d+>',
                                                            below)
                                    if len(next_label) > 0:
                                        if re.sub(PATTERN_LABEL_NUMBER, '', past_label) == lastNumber(
                                            re.sub(PATTERN_LABEL_NUMBER, '', next_label[0])): return idx
                                    tmp_index = int(past_idx)
                            coinci = len(set(current_title).intersection(set(re.sub('[\s\n\t]', '', text))))
                            print('重合率: ', coinci)
                            if coinci > coincidence:
                                coincidence, most_plossible_index = coinci, idx
                        if most_plossible_index == -1:
                            return possible_index[-1]
                        else:
                            return most_plossible_index
                    else:
                        print('无相关过往纪录', id)
    return 0


def isFirst(current):
    current = re.sub('</title_\d+_(\d+)>.*?$', '', current)
    current = re.sub('<title_\d+_(\d+)>', '', current)
    current_tag = re.sub(PATTERN_LABEL_NUMBER, '', current)
    print('标题数： ', current_tag)
    try:
        (str(current_tag) in ['1', '一', '①'] and not ('.' in current or '．' in current)) or \
        (list(str(current_tag))[-1] in ['1', '一'] and ('.' in current or '．' in current))
    except:
        print()
    return (str(current_tag) in ['1', '一', '①'] and not ('.' in current or '．' in current)) or \
           (list(str(current_tag))[-1] in ['1', '一'] and ('.' in current or '．' in current))


def stuctureIdentifier(text:str)->str:
    """
    :param text:待清洗的文本
    :return: 识别并重新定义个标题层级关系的文本
    """
    above = ''
    below = initWithLabels(text)

    while len(below) > 0:
        #         print('已完成： ',above)

        print('\n************************** loop **********************************')
        #         print(below)
        pos = re.search(r"\<title_\d+_\d+\>(.*?)\</title_\d+_\d+\>[\s\t]*?(.*?)[\s\t\n]", below)
        if pos == None: return above + below
        print('>> 当前语句： ', below[pos.start():pos.end()])
        id = (re.findall(r"\<title_(\d{3})_\d+\>.*?\</title_\d+_\d+\>", below[pos.start():pos.end()])[0])
        print('>> 当前标题id： ', id)
        z_index = getIndex(above + below[:pos.start()], id, below[pos.start():pos.end()], below[pos.end():])
        print('图层：   ', str(z_index).zfill(3))
        if int(id) >= 0:
            above += below[:pos.start()]
            above += re.sub(r'_\d+(>)', '_' + str(z_index).zfill(3) + '>', below[pos.start():pos.end()])
            print('add above')
            below = below[pos.end():]
            continue
        above += below[:pos.end()]
        below = below[pos.end():]
    return above

def addLable(text:str)->str:
    """
    :param text: 待清洗的文本
    :return: 最终还有文章结构的文本
    console不输出任何log
    """
    with HiddenPrints():
        text = stuctureIdentifier(re.sub('\n+', '\n', text))
    return text

if __name__ == '__main__':
    pass