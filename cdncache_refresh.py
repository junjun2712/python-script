#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:  xxxxx
# Date:     2020/2/25 0:52
# Location: xxx
# Desc:     云盾CDN缓存刷新


import logging
from ydsdk import YdSdk
import sys

# 添加日志
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

# 日志输出到文件
fileHandle = logging.FileHandler('ydsdk.log', encoding='utf-8')
fileHandle.setFormatter(formatter)
logger.addHandler(fileHandle)

# 日志输出到stdout
streamHandle = logging.StreamHandler()
streamHandle.setFormatter(formatter)
logger.addHandler(streamHandle)

sdk = YdSdk({
    "app_id": 'xxxxx',
    "app_secert": 'xxxxxxx',
    "api_pre": "http://apiv4.yundun.com/V4/",
    "user_id": xxxxx,
    "timeout": 30,
    "logger": logger,               ##如果不需要，此参数可不传
})


def do_refresh(refresh_type, refresh_url):
    """
    执行缓存清理
    :param refresh_type: 刷新类别, 全站: wholesite, 指定url: specialurl, 指定目录: specialdir
    :param refresh_url: 要刷的url,注意目录刷新后缀一定是/
    :return: raw,body,err
    """
    query = {refresh_type: refresh_url.split(',')}
    raw, body, err = sdk.put('Web.Domain.DashBoard.saveCache', query=query)
    return [raw, body, err]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f'Usage: python3 {sys.argv[0]} 刷新类别[site,dir,url] 刷新的url')
    else:
        refresh_type_map = {
            'site': 'wholesite',
            'dir': 'specialdir',
            'url': 'specialurl'
        }
        ret_list=do_refresh(refresh_type_map.get(sys.argv[1]), sys.argv[2])
        # 格式化输出执行结果
        for k,v in ret_list[1].items():
            print(f'### {k}:')
            for nk,nv in v.items():
                print(f'\t{nk}: {nv}')
        # 给jenkins返回执行状态码
        sys.exit(0 if ret_list[1].get('status').get('code') == 1 else 1)
