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

es=Elasticsearch(["10.3.18.48"],http_auth=('elastic','xxxxxxxx'))






@app.route("/metrics")

def merchant():

    for merchant_number_dy in open("/data/merchant_check_dy/conf.list"):
        shbiao = merchant_number_dy.replace('\n', '').replace('\r', '')
        body={"query":{"bool":{"must":[{"term":{"message":shbiao}},{"term":{"message":"filter"}}],"filter":{"range":{"@timestamp":{"gte":"now-1m/m","lte":"now/m","format":"epoch_millis"}}}}}}

        data=es.search(index="proddy-backend-dy_betinfo*",body=body)
        total = data['hits']['total']['value']




        merchant_name_dy.labels(merchant_number_dy).set(total)

    return Response(prometheus_client.generate_latest(REGISTRY),
                    mimetype="text/plain")

if __name__ == "__main__":
    # 实例化 REGISTRY
    REGISTRY = CollectorRegistry(auto_describe=False)
    merchant_name_dy = Gauge("merchant_name_dy", "merchant count",['merchant_number_dy'], registry=REGISTRY)
    app.run(host="0.0.0.0", port=2713, debug=True)
~
