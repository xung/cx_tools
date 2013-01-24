#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Filename:rank_relate_querys.py

import sys,operator,math,redis,os

redis_ip='127.0.0.1'
redis_port=6379
redis_db=6

def initLog(logName,logFileName):
    from datetime import datetime
    import logging
                 
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='./%s' %(logFileName),
                        filemode='a')
    logger = logging.getLogger(logName)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)
    return logger

def read_from_redis(logger,all_data):
    r = redis.StrictRedis(host=redis_ip,port=redis_port, db=redis_db,socket_timeout=6000)
    try:
        if r.ping():
            logger.info('connect to redis[ip:%s port:%d,db:%d] success.' %(redis_ip,redis_port,redis_db))
    except redis.exceptions.ConnectionError:
        logger.info('connect to redis[ip:%s port:%d,db:%d] failed.' %(redis_ip,redis_port,redis_db))
        logger.info('read from redis[ip:%s] failed!'%redis_ip)
        return
    logger.info('redis size:%d' %r.dbsize())
    redis_keys = set(r.keys())
    logger.info('begin write read data from redis[ip:%s]...' %redis_ip)
    for key in redis_keys:
        value = r.get(key)
        all_data.setdefault(key,value)
    logger.info('get %d records from redis.' %len(all_data))
    


def main(result_file):
    all_data = {}
    logger = initLog('to_file_from_redis','./to_file_from_redis.log')
    logger.info('begin read redis...')
    #read data from redis
    read_from_redis(logger,all_data)
    #write to file
    result_f = file(result_file,'w') 
    for key,value in all_data.items():
        result_f.write(key+':'+value+'\n')
    result_f.close()
        
    logger.info('write file finished.')
    logger.info('end.')
        

if __name__ == '__main__':
    main(sys.argv[1])
