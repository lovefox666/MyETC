# -*- coding: utf-8 -*-
__author__ = 'lovefox'

import os
import zipfile
import filetype
import random
from PyPDF2 import PdfFileReader, PdfFileWriter

def myUnzip(zipFileName,pdfList):
    """
    函数说明：递归调用解压。
    参数说明：zipFileName——压缩包文件名
        pdfList——PDF文件列表，用于其他操作使用。例如：PDF文件提取、合并
    """
    zf = zipfile.ZipFile(zipFileName, 'r')
    dirpath = os.path.dirname(zipFileName)
    zipName = os.path.splitext(os.path.basename(zipFileName))[0]
    
    fileList = zf.namelist()
    for file in fileList:
        try:
            with zipfile.ZipFile(zipFileName) as zfile:
                #5.2.1.1解压缩
                #oldFile = zfile.extract(file)
                oldFile = zfile.extract(file,path=os.path.join(dirpath,"temp"))
                #5.2.1.2修改文件名
                fileext = os.path.splitext(oldFile)[1]
                newFile = os.path.join(dirpath,"temp",zipName+"_"+str(random.randint(1,1000000))+fileext)
                os.rename(oldFile,newFile)
                kind =  filetype.guess(newFile)
                if kind.extension == "zip":
                    return myUnzip(newFile,pdfList)
                else:
                    pdfList.append(newFile)
            #print("PDF文件列表",pdfList)
            
        except zipfile.BadZipFile:
            print (zipFileName + " 压缩包损坏。请重新下载。")
    return pdfList

def mergePdf(inFileList, outFile, blankpage=1):
    '''
    合并文档
    param: inFileList: 要合并的文档的 list
    param: outFile:    合并后的输出文件
    parma: blankpage: 是否在通行记录末尾追加一页空白页，便于打印。
    :return:
    '''
    pdfFileWriter = PdfFileWriter()
    for i,inFile in enumerate(inFileList):
        # 依次循环打开要合并文件
        pdfFile = open(inFile, 'rb')
        pdfReader = PdfFileReader(pdfFile)
        numPages = pdfReader.getNumPages()
        for index in range(0, numPages):
            pageObj = pdfReader.getPage(index)
            pdfFileWriter.addPage(pageObj)
            
        if (i==0) and (numPages % 2 == 1):
            #print("发现通行记录为奇数页，增加一个空白页，便于一页两版的打印")
            pdfFileWriter.addBlankPage()
        
        # 最后,统一写入到输出文件中，写入后，记得关闭文件。否则后续无法删除。
        pdfFileWriter.write(open(outFile, 'wb'))
        pdfFile.close()