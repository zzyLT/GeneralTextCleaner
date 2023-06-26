import os
from paddleocr import PaddleOCR
import datetime
# import ocr_util
import re

IMG_PATH = (r'./all/imgs')
ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=True)

def traversal_file(img_path,out_path):
    list = os.listdir(img_path)
    for i in range(0,len(list)):
        path = os.path.join(img_path,list[i])
        file_name = list[i][:-4]
        ocr_img(path, file_name, out_path)


def ocr_img(IMG_PATH, path,name):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间
    result = ocr.ocr(IMG_PATH+'/'+name+'/'+path, cls=True)


    datas = []
    for a in result:
        for b in a:
            datas.append(b[1][0])
    #
    # xy_info.sort(key=lambda x:-x[1])
    # # data = xy_info.sort(key=takeSecond)
    # datas = []
    # for xy in xy_info:
    #     if (len(xy[0])>4) and re.match(r'[\u4e00-\u9fa5]+',xy[0],re.S):
    #         datas.append(xy[0])
    #     # print(xy[0],xy[1],xy[2])
    # # print(xy_info[0])
    # if datas:
    #     file_path = os.path.join(out_path,name+'.txt')
    #     with open(file_path,'w',encoding='utf-8') as f:
    #         for line in datas:
    #             f.write(line+'\n')
    # endTime_pdf2img = datetime.datetime.now()  # 结束时间
    # print(name,'时间消耗', (endTime_pdf2img - startTime_pdf2img).seconds,'S')
    return datas

if __name__ == "__main__":
    # img_path = r'imgs/qyj/images_76.png'
    # ocr_img(img_path, 'images_76', r'./txt')

    for file_name in os.listdir(IMG_PATH):
        with open(f"./text/{file_name}.txt", 'w', encoding='utf-8') as f:
            print('>> ',file_name)
            img_length = len(os.listdir(IMG_PATH + '/' + file_name))
            for i in range(img_length):
                print('>> ',f'images_{i}.png')
                f.write('\n'.join(ocr_img(f'images_{i}.png', file_name)))
                f.write('[PAGE]')
        print('>> done  ', file_name)

    img_path = r'imgs/qyj'
    out_path = r'./txt'
