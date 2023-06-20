import re

PATTERN_TITLE_LIST = {
    '[一二三四五六七八九十]+\s*、|附\s*[录表][：\:\d]?': 0,
    '（\s*[一二三四五六七八九十]+\s*）|\(\s*[一二三四五六七八九十]+\s*\)': 1,
    '\d\s*[\.\．、]': 2,
    '\d{1,2}\s?[\.．]\s?\d{1,2}': 3,
    '\(?\d\)|（?\d）': 4,

    '表\d+\s|项\s*目\s*[一二三四五六七八九十0-9]\s*、?|模\s*块?\s*[一二三四五六七八九十0-9]\s*、?|[\u4e00-\u9fa5_a-zA-Z0-9]{2,6}\s*[\:：]': 999,
}

PATTERN_LABEL_NUMBER = r'[^一二三四五六七八九十0-9]+'

def stuctureIdentifier(text):
    def next_label(label):
        pass

    def next_number(label):
        if label in '一 二 三 四 五 六 七 八 九 十 十一 十二 十三 十四 十五'.split(' '):
            tmp = '一 二 三 四 五 六 七 八 九 十 十一 十二 十三 十四 十五'.split(' ')
            try: return tmp[tmp.index(label) + 1]
            except: return '十六'
        else:
            try: return str(int(label) + 1)
            except: pass  # TODO: 没想到还有什么情况
        return 'unnamed'

    # 先全标
    for title_pattern in PATTERN_TITLE_LIST:
        pattern = r"([\n\s\t]+)(" + title_pattern + r")(\s*[\u4e00-\u9fa5_a-zA-Z])"
        text = re.sub(pattern, r'\1<title' + str(PATTERN_TITLE_LIST[title_pattern]) + r'>\2</title' + str(
            PATTERN_TITLE_LIST[title_pattern]) + r'>\3', text)

    # 再过滤掉层级不对的label <- 并不需要提前分句
    for title_pattern in PATTERN_TITLE_LIST:
        finded = re.finditer(f'<title{PATTERN_TITLE_LIST[title_pattern]}>(.+?)</title{PATTERN_TITLE_LIST[title_pattern]}>(.+?)\n', text)

        for it in finded:
            above_text = text[: it.start()]
            current_class = re.findall('<title(\d+)>', text[it.start():it.end()])[0]
            current = re.findall('<title\d+>(.*?)</title\d+>', text[it.start():it.end()])[0]
            current_tag = re.sub(PATTERN_LABEL_NUMBER, '', current)
            if len(current_tag) == 0: continue
            if (str(current_tag) in ['1', '一'] and not ('.' in current or '．' in current)) or \
                    (list(str(current_tag))[-1] in ['1', '一'] and ('.' in current or '．' in current)):
                try:
                    if int(re.findall('<title(\d+)>', above_text)[-1]) < int(current_class): continue
                #                     elif int(re.findall('<title(\d+)>',above_text)[-1]) < int(current_class) and \
                #                             list(str(re.sub(PATTERN_LABEL_NUMBER, '', re.findall('<title\d+>(.*?)</title',above_text)[-1])))[-1] in ['1', '一']:
                #                         print('cas1')
                #                         continue
                except:
                    pass

            above_finded = re.findall(f'<title{str(current_class)}>(.*?)</title{str(current_class)}>', above_text)
            if len(above_finded) > 0:
                last_tag = re.sub(PATTERN_LABEL_NUMBER, '', above_finded[-1])
                if current_tag == next_number(last_tag):
                    last_delete = re.findall(f'<delet{str(current_class)}>(.*?)</delet{str(current_class)}>',
                                             above_text)
                    if len(last_delete) > 0:
                        if current_tag == next_number(re.sub(PATTERN_LABEL_NUMBER, '', last_delete[-1])):
                            pass
                        else:
                            continue
                    else:
                        continue

                # 判断next同级标签
                below_finded = re.findall(f'<title{str(current_class)}>(.*?)</title{str(current_class)}>', text[it.end():])
                if len(below_finded) > 0:
                    if below_finded[0] == next_number(current_tag): continue

                # 判断next标签是否为一个新的子标签
                below_finded = re.findall(f'<title(\d+)>(.*?)</title\d+>', text[it.end():])
                if len(below_finded) > 0:
                    next_class = re.sub(PATTERN_LABEL_NUMBER, '', below_finded[0][1])
                    try:
                        if below_finded[0][0] != current_class and (str(next_class) in ['1', '一'] or
                                (list(str(next_class))[-1] in ['1', '一'] and ('.' in below_finded[0][1] or '．' in below_finded[0][1]))):
                            continue
                    except:
                        pass
                tmp = list(text)
                tmp[it.start():it.end()] = re.sub('title', 'delet', text[it.start():it.end()])
                text = ''.join(tmp)

    return re.sub('[\n\t]+', '\n', re.sub('</?delet\d+>', '', text))

if __name__ == '__main__':
    pass