#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Marathon <jsdymarathon@itcom888.com>
# Date:
# Location: Pasay
# Desc:     通过gateway info接口获取所有游戏与大厅的当前状态，并提接口给prometheus采集，最终在garafa展示

import prometheus_client
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
import requests
import json

app = Flask(__name__)
# 实例化 REGISTRY
REGISTRY = CollectorRegistry(auto_describe=False)
# 这里加了 labels，定义的 labels 一定要被用到，否则会报错
game_status = Gauge("game_status", "hall and game status.", ["gameID", "gameHost"], registry=REGISTRY)


def get_gate_info():
    """"从gateway网关info接口获取所有游戏与大厅的状态"""
    gate_info_url = 'http://172.18.xxx.xx:40000/info'
    gate_user = 'xxxx'
    gate_pass = 'xxxx'
    r = requests.get(gate_info_url, auth=(gate_user, gate_pass))
    r_json = json.loads(r.text)
    return r_json['info'][1]['wss']


@app.route("/metrics")
def requests_count():
    game_data = get_gate_info()
    for game in game_data:
        #print(f'serverID: {game["lineID"]}, serverHost: {game["remote"]}, running: {game["running"]}, delay: {game["delay"]}')
        game_id = game.get('lineID')
        game_host = game.get('remote')
        game_delay = game.get('delay')
        game_status.labels(game_id, game_host).set(game_delay)
    return Response(prometheus_client.generate_latest(game_status),
                    mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=31672, debug=True)
