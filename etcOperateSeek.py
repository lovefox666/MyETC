
# -*- coding: utf-8 -*-
__author__ = 'lovefox'

import requests
import codecs
import time
import random
import os
import json

from lxml import etree
from com.myDatetimeUtil import myDatetimeUtil
from com.getCookie import Getcookies


#第一步：自动识别验证码，登录成功后，进入详单页
#第二步，用xpath解析html代码，找到卡号和车牌号
#第三步，逐个提交并获取ETC卡的月度结算信息

#cookies = {'ASP.NET_SessionId': 'xxx'}

class ETCoperate(object):
    def __init__(self,cookies):
        self.cookies = cookies
    """
    函数功能：根据cookie，获取查询初始页面的ECT卡号
    作者：lovefox
    @return 返回卡号列表
    """
    def __get_etc_cards(self):
        #f=codecs.open("etc_cookies.txt","r","utf-8")
        #将字符串转换为字典类型
        #cookies=eval(f.read().strip())
        #f.close()
        #print(type(self.cookies))

        url = 'http://www.fjetc.com/OperateSeek.aspx'
        r = requests.get(url, cookies = self.cookies)
        html = r.text
        
        tree=etree.HTML(html)
        cardid_list = []
        cards=tree.xpath("//select[@id='ContentPlaceHolder1_DDLCardNum']/option")
        if not cards:
            return cardid_list

        for card in cards:
            cardid = card.get('value')
            carid = card.text
            if not (('停用' in carid) or ('挂失' in carid) or (cardid == '-1')):
                cardid_list.append((cardid, carid))
                #print(cardid,'=',carid)
        
        return cardid_list

    """
    函数功能：根据起始时间，ETC卡号，获得查询结果页面
    作者：lovefox
    @stime:按结算日期查询的开始时间，格式：2018-03-01
    @etime:按结算日期查询的结束时间，格式：2018-03-31
    @cardid:ETC卡号
    """
    def __get_etc_cardDetial(self,stime,etime,cardid):
        #f=codecs.open("etc_cookies.txt","r","utf-8")
        #cookies=f.read()
        #f.close()

        #1.获取HTML
        detail_list = []
        url = 'http://www.fjetc.com/Ajax/LSSeekHandler.ashx'
        data = {
            'Stime':stime,
            'Etime':etime,
            'keyword':cardid,
            'type':'72'
        }
        r = requests.get(url, data=data, cookies = self.cookies)
        html = r.text
        if html == '操作不能完成，原因是:用户没有成功登录。':
            print('请用谷歌浏览器登录www.fjetc.com后，再运行程序。')
            return detail_list
        
        #2.用xpath处理html，获取结算列表
        tree=etree.HTML(html)
        details=tree.xpath("//table[@width='90%']/tr[@bgcolor='#FFCC00']")
        if not details:
            return detail_list

        for detail in details:
            outtime = detail.xpath("./td[2]/text()")[0]
            billtime = detail.xpath("./td[3]/text()")[0]
            money = detail.xpath("./td[5]/text()")[0]
            detail_data = {
                "outtime" : outtime,
                "billtime" : billtime,
                "money" : money
            }
            #detail_list.append((outtime, billtime,money))
            detail_list.append(detail_data)
            #print('出口通行时间:',outtime,'结算日期:',billtime,'金额:',money)
        
        return detail_list

    """
    函数功能：获取所有ETC卡的结算记录
    作者：lovefox
    时间：2018-04-23 21:35
    """
    def getAllCardDetail(self,firstday,lastday):
        cardid_list = self.__get_etc_cards()
        if not cardid_list:
            return {}
        #读取信息，文件信息
        searchMonth = firstday[0:7].replace("-","")
        with open(searchMonth+'.json', 'r',encoding='utf-8') as f:
            data = json.load(f)

        AllDetails = data
        for car_info in cardid_list:
            #print(cardid[0])
            cardid = car_info[0]
            carid  = car_info[1]
            time.sleep(random.randint(1, 5))
            
            #__get_etc_cardDetial('2018-03-01','2018-03-31',cardid)
            details = self.__get_etc_cardDetial(firstday,lastday,cardid)
            json_details = {
                "cardid" : cardid,
                "carid"  : carid,
                "details": details            
            }
            if details:
                print('======正在添加“',carid,'”的结算数据，请耐心等待。======') 
                AllDetails.append(json_details)
            #
        json_str = json.dumps(AllDetails)
        
        with open(searchMonth+'.json', 'w',encoding='utf-8') as f:
                print(json_str, file = f)

def main():
    cookies = Getcookies.getcookiefromchrome('www.fjetc.com','etc_cookies.txt')
    if cookies:
        #firstday = myDatetimeUtil.getFirstDayofLastMonth()
        #lastday = myDatetimeUtil.getLastDayOfLastMonth()
        firstday = '2018-04-01'
        lastday = '2018-04-30'
        etc = ETCoperate(cookies)
        etc.getAllCardDetail(firstday,lastday)
    else:
        print("网络连接异常或未登录网站，请先登录后，再运行程序。")

if __name__ == "__main__":
    main()