# -*- coding: utf-8 -*-
__author__ = "lovefox"

"""
运行文件。
1、登录网站
1.1、先用谷歌浏览器登录ETC和票根网
1.2、保存cookies到文本文件

2、从ETC按结算日期获取通行记录,并按xxxx-xx.json的格式文件名保存
3、从票根网获取通行记录。
4、申请发票
5、下载发票
6、合并PDF
"""
import os
import sys
import json
import shutil
import fnmatch
import etcOperateSeek
import txffpOperate

from com.myDatetimeUtil import myDatetimeUtil
from com.getCookie import Getcookies
from com import myUtils

#0.开始运行程序
"""
with open("welcome.txt","r", encoding="utf-8") as f:
    welcome = f.read()
    print(welcome)
"""
print("欢迎使用小锦的ETC自助程序。")
userinput = input("是否开始运行“车辆费用自动结算收集”程序？（Y/N）：")
if userinput.upper() == "N":
    print("程序退出。谢谢使用。")
    sys.exit()

#基础路径
BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
#月份
monthbeforeLast = myDatetimeUtil.getMonthbeforeLast() 
lastMonth  = myDatetimeUtil.getLastMonth()
currentMonth = myDatetimeUtil.getCurrentMonth()
#发票下载路径
download_dir = os.path.join(BASE_DIR,'download',lastMonth)

#后续可考虑用数组的方法，传递数组：上上月，上月，当前月。
# 上上月用于票根网查询开票信息，上月用于票根网查询开票信息和ETC结算记录，当前月用于票根网下载发票
#months = [monthbeforeLast,lastMonth,currentMonth]

print("开始运行程序......")
#1.获取ETC卡结算记录
#1.1.获取第一张ETC卡的结算记录
userinput = input("请使用谷歌浏览器登录www.fject.com网站。完成后，请输入“Y”。跳过请输入“N”：")
if userinput.upper() == "Y":
    etcfile = lastMonth + ".json"
    json_str = []
    with open(etcfile, 'w') as f:
        print(json_str, file = f)

    print("开始获取",lastMonth,"ETC结算记录......")
    etcOperateSeek.main()
    print("************第一次获取ETC结算记录完毕。***************")
elif userinput.upper() == "N":
    print("跳过")
else:
    print("输入指令异常，程序退出。谢谢使用。")
    sys.exit()

#1.2.获取第二张卡ETC卡的结算记录
userinput = input("请更换卡号再次登录www.fject.com网站。完成后，请输入“Y”。跳过请输入“N”：")
if userinput.upper() == "Y":
    etcfile = lastMonth + ".json"
    print("开始再次获取",lastMonth,"ETC结算记录......")
    etcOperateSeek.main()
    print("************第二次获取ETC结算记录完毕。***************")
elif userinput.upper() == "N":
    print("跳过")
else:
    print("输入指令异常，程序退出。谢谢使用。")
    sys.exit()

#3.登录票根网，获取开票信息
#3.1获取下txffp的cookie

userinput = input("请登录票根网（www.txffp.com）。完成后，请输入“Y”；跳过，请输入“N”：")
if userinput.upper() == "Y":
    Getcookies.getCookieTotxt('%pss.txffp.com','cookie.txt')
    event_handler = txffpOperate.APIHandler(txffpOperate.COOKIE, txffpOperate.HEADERS, req_sleep=5)
    userinput = input("是否申请开票？确认，请输入“Y”；跳过请输入“N”：")
    if userinput.upper() == "Y":
        #3.2开票申请。应查询上月，并开票"""
        print("开始申请%s开票，请耐心等待....." % (lastMonth))
        event_handler.submit_apply_all(lastMonth)
        #3.3开票申请。应查询上月，并开票"""
        print("开始申请%s开票，请耐心等待....." % (monthbeforeLast))
        event_handler.submit_apply_all(monthbeforeLast)
    elif userinput.upper() == "N":
        print("你已跳过开票阶段。")
    else:
        print("输入指令异常，程序退出。谢谢使用。")
        sys.exit()

    #4.当前月下载当前月申请开出的发票，这些发票是4月结算的记录
    userinput = input("你是否开始下载发票？确认，请输入“Y”；跳过，请输入“N”：")
    
    if userinput.upper() == "Y":
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        #print(download_dir)
        event_handler.inv_download_all(currentMonth,download_dir)
        #event_handler.inv_download_all(lastMonth,download_dir)
        print("恭喜你，下载完成。")
    elif userinput.upper() == "N":
        print("跳过下载程序部分。")
    else:
        print("输入指令异常，程序退出。谢谢使用。")
        sys.exit()
else:
    print("你已跳过票根网操作部分。")

#5.解压缩文件
print("开始解压缩下载文件，请耐心等待......")
#5.1.获取文件夹内的文件列表
zipFileList = fnmatch.filter(os.listdir(download_dir), '*.zip')
#5.2.获取压缩包文件名，读取压缩包内文件，如果还有压缩包则再解压缩，修改文件名
pdfLists = []#待移除的pdf列表
for zipFile in zipFileList:
    pdfList = []
    zipFileName = os.path.join(download_dir,zipFile)
    pdfList = myUtils.myUnzip(zipFileName,pdfList)
    print("解压缩%s完成。开始合并PDF文件" % (zipFile))
    #5.3.合并PDF文件
    newPDFFileName = os.path.join(download_dir,os.path.basename(zipFileName)+".pdf")
 
    myUtils.mergePdf(pdfList,newPDFFileName)
    print("解压缩/合并PDF完成。")
#5.4.移除多余PDF
print("开始移除临时文件夹。")
shutil.rmtree(os.path.join(download_dir,"temp"))

#5.5.移除已解压的压缩包
print("开始移除已解压的压缩包。")
zipFileList = fnmatch.filter(os.listdir(download_dir), '*.zip')
for zipFile in zipFileList:
    zipFileName = os.path.join(download_dir,zipFile)
    os.remove(zipFileName)

#6.完成
print("恭喜你，任务完成。可以开始愉快的打印了！")




