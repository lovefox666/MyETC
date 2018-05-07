# -*- coding: utf-8 -*-
"""
python3从chrome浏览器读取cookie
get cookie from chrome
2016年5月26日 19:50:38 codegay

参考资料：

python模拟发送动弹
http://www.oschina.net/code/snippet_209614_21944

用Python进行SQLite数据库操作
http://www.cnblogs.com/yuxc/archive/2011/08/18/2143606.html

encrypted_value解密脚本
http://www.ftium4.com/chrome-cookies-encrypted-value-python.html

利用cookie劫持微博私信
https://segmentfault.com/a/1190000002569850

你所不知道的HostOnly Cookie
https://imququ.com/post/host-only-cookie.html
"""
import os
import sqlite3
import requests
import win32crypt

class Getcookies(object):
    @staticmethod
    def getcookiefromchrome(host='pss.txffp.com',filename='cookie.txt'):
        cookiepath=os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
        sql="select host_key,name,encrypted_value from cookies where host_key like '%s'" % host
        with sqlite3.connect(cookiepath) as conn:
            cu=conn.cursor()        
            cookies={name:win32crypt.CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}
            #cookies=[name:CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()]
            #print(cookies)
            with open(filename, 'w') as f:
                print(cookies, file = f)
        return cookies
    """
    函数功能：从数据库读取cookies，保存到指定的文本
    """
    @staticmethod
    def saveCookieTotxt(host,filename):
        #1.第一步，从本地浏览器COOKIES数据库读取cookies
        cookies = Getcookies.getcookiefromchrome(host,filename)
        #2.第二步，将cookies字典转换为以“;”分割的字符串
        split_str = "; "
        list_cookies = []
        for cookies_key,cookies_value in cookies.items():
            list_cookies.append(cookies_key + "=" + str(cookies_value))
        str_cookies = split_str.join(list_cookies)
        #3.第三步，保存到文件
        with open(filename, 'w') as f:
            print(str_cookies, file = f)

    @staticmethod
    def getCookieTotxt(host,filename):
        #1.第一步从本地浏览器COOKIES数据库读取数据
        cookiepath=os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
        sql="select name,encrypted_value from cookies where host_key like '%s'" % host
        cookie_list = []
        split_str = "; "
        with sqlite3.connect(cookiepath) as conn:
            cu=conn.cursor()
            for name,encrypted_value in cu.execute(sql).fetchall():
                cookie_list.append(name + "=" + win32crypt.CryptUnprotectData(encrypted_value)[1].decode())
            str_cookies = split_str.join(cookie_list)
        with open(filename, 'w') as f:
            print(str_cookies, file = f)
            

#运行环境windows 2012 server python3.4 x64 chrome 50
#以下是测试代码
#Getcookies.getcookiefromchrome('www.fjetc.com','etc_cookie.txt')
#Getcookies.saveCookieTotxt('%pss.txffp.com','cookies.txt')
#Getcookies.getCookieTotxt('%pss.txffp.com','cookies.txt')

#设置allow_redirects为真
#r=requests.get(url,headers=httphead,cookies=getcookiefromchrome('pss.txffp.com'),allow_redirects=1)
#print(r.text)