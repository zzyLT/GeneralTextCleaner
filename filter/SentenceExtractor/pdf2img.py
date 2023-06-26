##environment: pytorch_py3.7
import datetime
import os
import fitz  # fitz就是pip install PyMuPDF


def pyMuPDF_fitz(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间

    print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.page_count):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6
        # 的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 2  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 2
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        if imagePath[-1] == ' ': imagePath = imagePath[:-1]
        pix.save(imagePath + '/' + 'images_%s.png' % pg)  # 将图片写入指定的文件夹内

    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds)
    return 0


if __name__ == "__main__":
    # 1、PDF地址

    PDF_PATH = (r'E:\NOS\/documents/国家标准PDF')
    pdf_paths = os.listdir(PDF_PATH)

    for pdfPath in pdf_paths:
        if '.pdf' in pdfPath and not os.path.exists(f'./all/imgs/{pdfPath.replace(".pdf", "")}'):
            # 2、需要储存图片的目录
            imagePath = f'./all/imgs/{pdfPath.replace(".pdf", "")}'
            pyMuPDF_fitz(f"{PDF_PATH}/{pdfPath}", imagePath)


