#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Filename:get_data.py

from hive_service import ThriftHive
from hive_service.ttypes import HiveServerException
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from util import initLog,readSettingFile
import datetime,time
import string, os, sys

import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 
print  sys.getdefaultencoding()


#-----------global val----------
settings = {}

#--------------------------hive operator----------------------------
class HiveOperator:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    def hiveConnection(self):
        self.transport = TSocket.TSocket(self.host, self.port)
        self.transport = TTransport.TBufferedTransport(self.transport)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        client = ThriftHive.Client(protocol)
        return client
    def hiveOpen(self):
        self.transport.open()
    def hiveClose(self):
        self.transport.close()
        
def getSearchLog(host, port,database,sql,to_file_path,limit_record_num,logger):
    record_num=0
    to_file = open(to_file_path, "w")

    try:
        ho = HiveOperator(host,port)
        logger.info("begin connect to hive...")
        client = ho.hiveConnection()
        ho.hiveOpen()

        if database and database!='default':
            client.execute('use %s'%database)
            logger.info("use database:%s"%database)
        else:
            client.execute('use default')
            logger.info("use default database.")
            
        logger.info("begin execute sql[%s] in hive..."%sql)
        client.execute(sql)
        logger.info("begin process return data...")
        while 1:
            try:
                print "0"
                list_row = client.fetchN(100)
                print "1"
                if 0 == len(list_row):
                    break
                list_row = [line.rstrip('\n')+'\n' for line in list_row]
                to_file.writelines(list_row)
                record_num+=len(list_row)
            except:
                logger.warning("An exception occurred in getSearchLog()")
                continue

        to_file.close() 
        ho.hiveClose()

        if record_num<limit_record_num:
            logger.error("record num <%d! record_num:%d"%(limit_record_num,record_num))
            return False
        if os.path.getsize(to_file_path)==0:
            logger.error("%s size is 0!"%to_file_path)
            return False

        logger.info("get search_log_data success! Total records Num:%d"%record_num)
        return True
    except Exception, tx:
        to_file.close()
        logger.error("An exception occurred in getSearchLog():%s" %(tx))
        return False
        
def main():
    logger = initLog('get_data','./get_data.log') 
    logger.info('---------- begin get_log_data ----------')
    readSettingFile('./setting.ini',settings) 
    logger.info('read setting.ini file success.')
    logger.info("[hive_server] ip:'%s',port:'%d' cycle:'%d'days" %(settings['hive_ip'],settings['hive_port'],settings['cycle']))

    date_today = datetime.datetime.date(datetime.datetime.now())
    date_end = date_today - datetime.timedelta(days=1)    #截止到1天前
    date_begin = date_today - datetime.timedelta(days=settings['cycle'])    #从cycle天前开始

    date_today = date_today.strftime("%Y%m%d")      #程序执行日期，比统计结束日期多一天
    date_end   = date_end.strftime("%Y%m%d")        #统计结束日期
    date_begin = date_begin.strftime("%Y%m%d")      #统计开始日期

    if settings['time_begin'].strip():
        date_begin = settings['time_begin']
    if settings['time_end'].strip():
        date_end = settings['time_end']

    logger.info("date_begin = %s date_end = %s date_today = %s" %(date_begin, date_end,date_today))

    if "%s" in settings['sql']:
        sql_str = settings['sql'].rstrip(';') %(date_begin,date_end)
        result_file=settings['result_file']+'.'+date_begin+'-'+date_end
    else:
        sql_str = settings['sql'].rstrip(';')
        result_file=settings['result_file']+'.'+date_today
    

    if os.path.exists(result_file):
        os.remove(result_file)
        logger.info("remove %s from hive last cycle."%result_file)
   
    logger.info("begin get data form hive and write to %s file..." %result_file)
    if getSearchLog(settings['hive_ip'],settings['hive_port'],settings['database'],sql_str,result_file,settings['limit_num'],logger):
        logger.info('---------- end get_log_data ----------')
        return True
    else:
        logger.info("get data failed!")
        if os.path.exists(result_file):
            os.remove(result_file)
        logger.info('---------- end get_log_data ----------')
        return False


if __name__ == '__main__':
    main()
