# encoding:utf-8
import json
import os
import datetime
import time
import urllib
import json
import urllib2
import sys
from elasticsearch import  Elasticsearch
import prometheus_client
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
import requests


app = Flask(__name__)

es=Elasticsearch(["172.18.230.84"],http_auth=('elastic','xxxxxxxxx'))






@app.route("/metrics")

def merchant():

    for merchant_number in open("/root/cole/conf.list"):
        #print line

        # addr = line
        #print addr

        body={"query":{"bool":{"must":{"match":{"message":merchant_number}},"filter":{"range":{"@timestamp":{"gte":"now-1m/m","lte":"now/m","format":"epoch_millis"}}}}}}

        data=es.search(index="qp-betinfo*",body=body)
        #print(type(data))


        merchant_data=str(data)
        #print sh
        #print (type(sh))

        merchant_data_count = merchant_data.split("value\':")[-1]
        #print(sh_a)

        total = merchant_data_count.split("}")[0]



        merchant_name.labels(merchant_number).set(3)

    return Response(prometheus_client.generate_latest(REGISTRY),
                    mimetype="text/plain")

if __name__ == "__main__":
    # 实例化 REGISTRY
    REGISTRY = CollectorRegistry(auto_describe=False)
    merchant_name = Gauge("merchant_name", "merchant count",['merchant_number'], registry=REGISTRY)
    #sh_total = Gauge("total", "toltal",['line'], registry=REGISTRY)
    app.run(host="0.0.0.0", port=2712, debug=True)
