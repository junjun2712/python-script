# -*- coding: utf-8 -*-
#pip3 install pyocr
#pip3 install install atlassian-python-api
#pip3 install pdfminer
#pip3 install python-telegram-bot

import telegram
import pyocr
import importlib
import sys
import time
import re
from datetime import datetime, date, timedelta
from atlassian import Confluence
importlib.reload(sys)
import os.path
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed

tg_bot = telegram.Bot(token="xxxxxxxx")
tg_chatID = "-xxxxxxxxx"

now_time = time.strftime("%H:%M:%S", time.localtime())     # 现在的时间
print("现在是北京时间：{}".format(now_time))

text_path = r'日报.pdf'

confluence = Confluence(
    url='https://www.confluence.com/',
    username='username',
    password='psssword')



def parse():
    '''解析PDF文本，并保存到TXT文件中'''
    fp = open(text_path, 'rb')
    # 用文件对象创建一个PDF文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument(parser)
    # 连接分析器，与文档对象
    parser.set_document(doc)

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page内容
        # doc.get_pages() 获取page列表
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象���text属性，

            for x in layout:
                if(isinstance(x,LTTextBoxHorizontal)):
                    with open(r'日报.txt','a') as f:
                      #qp_dy_name = ["cole","webb"]
                        results = x.get_text()
                    #print(results)

                        f.write(results)


def czname():
    if "09:00:00" < now_time < "18:00:00":
        qp_dy_name = ["xxx","bbb"]

    if "15:00:00" < now_time < "00:00:00":
        qp_dy_name = ["aa","vv","vvv","vvv","vv"]

    if "00:00:00" < now_time < "09:00:00":
        qp_dy_name = ["vv","vv","vv","vv","vv","vv","vv"]
    print(qp_dy_name)

    with open(r'日报.txt', 'r') as f:
        data = f.readlines()
        for item in qp_dy_name:
            daka=re.findall(item,str(data))
            #print(signal_data[0])
            if len(daka) > 0:
                print(item,'存在')
            else:
                print(item,'不存在')
                send_msg_to_mango.sendmsg2mango('notice','{},日报,别忘记哦！'.format(item))
                tg_ret = tg_bot.sendMessage(chat_id=tg_chatID, text='{}日报,别忘记哦'.format(item))
                
if __name__ == '__main__':
    creat_pdf()
    parse()
    czname()
