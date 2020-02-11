# -*- coding: utf-8 -*-
import telegram
import logging
import json
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.secret_key = 'aYT>.L$kk2h>!'
app.config['BASIC_AUTH_USERNAME'] = 'root'
app.config['BASIC_AUTH_PASSWORD'] = 'root'

basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_FORCE'] = True

bot = telegram.Bot(token="45435345:fsdfsdfsf")
chatID = "-fsdfsdfsf"

@app.route('/alert', methods = ['POST'])
def postAlertmanager():
    msg = ""
    msg1 = ""
    msg2 = ""
    content = json.loads(request.get_data())
    num = len(content['alerts'])
    print json.dumps(content)
    for i in range(0,num):
        #print content['alerts'][i]
        alert_status = content['alerts'][i]['status']
        alert_name = content['alerts'][i]['labels']['alertname']
        alert_pod = content['alerts'][i]['labels']['instance']
        #alert_pod = content['alerts'][i]['annotations']['description']
        alert_value = content['alerts'][i]['annotations']['summary']
        alert_summary = content['alerts'][i]['startsAt']

        instance_env = alert_pod.split('-')[0]
        print('env:' + instance_env)



        if content['alerts'][i]['status'] == "firing":
            msg1 = msg1 + "【告警触发】\n" + "告警级别: " + alert_status + "\n告警类型: " + alert_name + "\n监控项目: " + alert_pod + "\n触发时间: " + alert_summary  + "\n问题描述: " + alert_value + "\n\n"
            #msg1 = msg1 + "【告警触发】\n" + "告警级别: " + alert_status + "\n告警类型: " + alert_name + "\n监控项目: " + alert_pod + "\n触发时间: " + alert_summary  + "\n\n"
            #print (msg1)
        elif content['alerts'][i]['status'] == "resolved":
            msg2 = msg2 + "【告警恢复】\n" + "告警级别: " + alert_status + "\n告警类型: " + alert_name + "\n监控项目: " + alert_pod + "\n触发时间: " + alert_summary  +  "\n\n"

    if msg1 == "":
        msg = msg2
    elif msg2 == "":
        msg = msg1
    else:
        msg = msg1 + "\n" + msg2
    print('msg: ' + msg)

    bot.sendMessage(chat_id=chatID, text=msg)
    return "Alert OK", 200




if __name__ == '__main__':
    logging.basicConfig(filename='flaskAlert.log', level=logging.INFO)
    app.run(debug=True,host='0.0.0.0', port=9119)
