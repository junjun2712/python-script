# encoding:utf-8
import json
import re
import os
from elasticsearch import  Elasticsearch
from bson.json_util import dumps



es=Elasticsearch(["172.18.230.84:9200"])



body={
  "query": {
    "bool": {
      "must": {
        "match": {
         "message": "172.18.230.222"
        }
      },
      "filter": {
        "range": {
          "@timestamp": {
            "gte": "now-1m/m",
            "lte": "now/m",
            "format": "epoch_millis"
          }
        }
      }
    }
 }
}

data=es.search(index="qp-betinfo*",body=body)
#print(type(data))


fh=str(data)
#print fh
#print (type(fh))

str_a = fh.split("value\':")[-1]
#print(str_a)

str_b = str_a.split("}")[0]
print(str_b)
