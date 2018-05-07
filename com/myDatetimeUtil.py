#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
import calendar


class myDatetimeUtil:
    """
    类功能：计算上一个月第一天和最后一天
    作者：lovefox
    时间：2018-04-23 23:05
    """
    @staticmethod
    def getLastDayOfLastMonth():
        d = datetime.now()
        
        year = d.year
        month = d.month

        if month == 1 :
            month = 12
            year -= 1
        else :
            month -= 1
        days = calendar.monthrange(year, month)[1]
        #print(year,month,days)   
        return (datetime(year,month,days)).strftime('%Y-%m-%d')
    
    @staticmethod
    def getFirstDayofLastMonth():
        d = datetime.now()
        
        year = d.year
        month = d.month

        if month == 1 :
            month = 12
            year -= 1
        else :
            month -= 1
          
        return (datetime(year,month,1)).strftime('%Y-%m-%d')
    
    @staticmethod
    def getLastMonth():
        """
        函数功能：返回上一个月，格式如：201803
        """
        d = datetime.now()
        
        year = d.year
        month = d.month

        if month == 1 :
            month = 12
            year -= 1
        else :
            month -= 1
          
        return (datetime(year,month,1)).strftime('%Y%m')
    
    @staticmethod
    def getLastMonth2():
        """
        函数功能：返回上一个月，格式如：2018.03
        """
        d = datetime.now()
        
        year = d.year
        month = d.month

        if month == 1 :
            month = 12
            year -= 1
        else :
            month -= 1
          
        return (datetime(year,month,1)).strftime('%Y.%m')
    
    @staticmethod
    def getMonthbeforeLast():
        """
        函数功能：返回上上月，格式如：201803
        """
        d = datetime.now()
        
        year = d.year
        month = d.month

        if month == 1 :
            month = 11
            year -= 1
        elif month == 2:
            month = 12
            year -= 1
        else :
            month -= 2
          
        return (datetime(year,month,1)).strftime('%Y%m')

    @staticmethod
    def getCurrentMonth():
        """
        函数功能：返回当前月，格式如：201803
        """
        d = datetime.now()
        
        year = d.year
        month = d.month
          
        return (datetime(year,month,1)).strftime('%Y%m')