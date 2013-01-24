#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Filename:util.py

import sys,re
reload(sys)
sys.setdefaultencoding('utf-8')

def readSettingFile(settingFile,settingDict):
    import ConfigParser
    '''read setting.ini file'''
    confParser = ConfigParser.ConfigParser()
    confParser.read(settingFile)
    settingDict['hive_ip']=confParser.get("HIVE_SERVER","ip")
    settingDict['hive_port']=confParser.getint("HIVE_SERVER","port")
    settingDict['database']=confParser.get("HIVE_SERVER","database")
    
    settingDict['cycle']=confParser.getint("INPUT","cycle")
    settingDict['sql']=confParser.get("INPUT","sql")
    settingDict['time_begin']=confParser.get("INPUT","time_begin")
    settingDict['time_end']=confParser.get("INPUT","time_end")
    settingDict['limit_num']=confParser.getint("INPUT","limit_num")

    settingDict['result_file']=confParser.get("OUTPUT","result_file")
    
def initLog(logName,logFileName):
    from datetime import datetime
    import logging
                 
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='./%s' %(logFileName),
                        filemode='w')
    logger = logging.getLogger(logName)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)
                                              
    return logger


