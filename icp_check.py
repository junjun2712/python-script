# -*- coding: utf-8 -*-
from prometheus_client import Gauge,Counter, generate_latest
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
import re
import os
import requests
import time
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

#s = requests.session()


# 定义一个带sesion的对象
icp_check_api = "http://icp.chinaz.com/"


@app.route("/metrics")
def testa():
    str1 = os.popen("grep -Ev '^#|^$' /data/scripts/game_status/domain.list").readlines() 
    for domain in str1:
       str_domain = domain.split(':')[0]
       str_env = domain.split(':')[1].replace("\n", "")
       str2 = requests.get(icp_check_api+str_domain)
       check_result = re.findall("未备案或备案取消",str2.text.encode())
       time.sleep(random.random())                              #形成一个0-1之间的随机数
       if str2.status_code == 200:
           if len(check_result) == 1:
               print check_result[0].decode()
               print str_domain
               record_domain_check.labels(str_domain,str_env).set(1)
           elif len(check_result) == 0:
               print check_result
               print str_domain
               record_domain_check.labels(str_domain,str_env).set(0)
       else:
           print check_result
           print str_domain
           print str2.status_code
           prod_domain_check.labels(str_domain, 'prod', '001').set(0)

    return Response(generate_latest(registry),mimetype="text/plain")



if __name__ == '__main__':
    registry = CollectorRegistry(auto_describe=False)
    record_domain_check = Gauge("record_domain_check", "record_domain_check", ['domain', 'env'], registry=registry)
    app.run(debug=True,host='0.0.0.0', port=5000)
