import json
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.secret_key = 'aYT>.L$kk2h>!'
app.config['BASIC_AUTH_USERNAME'] = 'root'
app.config['BASIC_AUTH_PASSWORD'] = 'root'
basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_FORCE'] = True


def seconds_to_hms(st):
    """秒转换成时分秒"""
    m, s = divmod(st, 60)
    h, m = divmod(m, 60)
    return '{:.0f}时{:.0f}分{:.0f}秒'.format(h,m,s)


@app.route('/alert', methods = ['POST'])
def postAlertmanager():
    msg = ""
    content = json.loads(request.get_data())
    num = len(content['alerts'])
    print('alert num: {}'.format(num))
    #print json.dumps(content, ensure_ascii=False)

    for i in range(0,num):
        alert_status = content['alerts'][i]['status']
        alert_name = content['alerts'][i]['labels']['alertname']
        alert_host = content['alerts'][i]['labels']['instance']
        alert_group = content['alerts'][i]['labels']['group']
        alert_ip = content['alerts'][i]['labels']['host_ip']
        alert_sumary = content['alerts'][i]['annotations']['summary']
        alert_desc = content['alerts'][i]['annotations']['description']
        alert_time = content['alerts'][i]['startsAt']
        instance_env = alert_host.split('-')[0]

        if content['alerts'][i]['status'] == "firing":
            msg = '🔴#{}#\n'.format(alert_status)
            msg += '告警类型: {}/{}/{}\n'.format(instance_env,alert_group,alert_name)
            msg += '监控主机: {}:{}\n'.format(alert_host,alert_ip)
            msg += '触发时间: {}\n'.format(alert_time)
            msg += '告警描述: {}\n'.format(alert_sumary)
            msg += '告警详情: {}\n'.format(alert_desc)
        elif content['alerts'][i]['status'] == "resolved":
            endsAt = content['alerts'][i]['endsAt']
            start_time_stramp = time.mktime(time.strptime(alert_time.split('.')[0].replace('T', ' '), '%Y-%m-%d %H:%M:%S'))
            end_time_stramp = time.mktime(time.strptime(endsAt.split('.')[0].replace('T', ' '), '%Y-%m-%d %H:%M:%S'))
            duration_time = end_time_stramp-start_time_stramp
            msg = '✅#{}#\n'.format(alert_status)
            msg += '告警类型: {}/{}/{}\n'.format(instance_env,alert_group,alert_name)
            msg += '监控主机: {}:{}\n'.format(alert_host,alert_ip)
            msg += '故障时长: {}\n'.format(seconds_to_hms(duration_time))
        logging.info(msg)

        if instance_env == 'prod':
            prod_bot.sendMessage(chat_id=prod_chatID, text=msg)
        elif instance_env == 'uat':
            uat_bot.sendMessage(chat_id=uat_chatID, text=msg)

    print('send done')
    return "Alert OK", 200


if __name__ == '__main__':
    logging.basicConfig(filename='logs/flaskAlert.log',
                        level=logging.INFO,
                        format='%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(message)s',
                        datafmt='%Y/%m/%d %H:%M:%S %p')
    prod_bot = telegram.Bot(token="ferrwr53434:fdsfsfsfsf")
    prod_chatID = "-2222"
    uat_bot = telegram.Bot(token="134535345:AfsdfsdfjY")
    uat_chatID = "-11111"
    app.run(debug=True,host='0.0.0.0', port=9119)
