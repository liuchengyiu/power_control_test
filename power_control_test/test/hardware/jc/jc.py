import paho.mqtt.client as mqtt
import json
from time import sleep
import threading
from test.lib import Ser

jc_result = {
    'flag': False,
    'message':'jc module dont response'
}

mqttc = {}

def jc_test(d):
    ip = d['ip']
    port = d['port']
    interval = d['interval']
    times = d['times']
    try:
        mqtt_init(ip, port, interval, times)
    except Exception as e:
        return [{
            "flag": False,
            "message": 'create mqtt client error!'
        }]
    for i in range(times * interval + 3):
        if jc_result['flag'] == True:
            break;
        sleep(1)
    mqttc.disconnect()
    mqttc.loop_stop(force=True)

    try:
        ser = Ser()
        ser.openCom(port_name=d['serial_jc'])
        read = ser.run(bytes.fromhex('69 07 00 10 ad b5 43'), 108)
        ser.closrCom()
        if read == False or len(read) > 0:
            jc_result['flag'] = False
            jc_result['message'] = "ttyS6 connection fail!"
            return [jc_result]
    except Exception as e:
        print('error=', e)
        jc_result['flag'] = False
        jc_result['message'] = "ttyS6 serial error!"
        return [jc_result]
    return [jc_result]


def on_message(mqttc, obj, msg):
    topic = msg.topic
    payload = bytes.decode(msg.payload)
    print('topic=='+topic)
    if topic == 'test/jc/response':
        data = json.loads(payload)
        print('payload==', payload)
        global jc_result
        if data['body']['RD_REAL2'] == 1 and data['body']['RD_EVENT'] == 1 and data['body']['RD_REAL'] == 1:
            jc_result['flag'] = True
            jc_result['message'] = json.dumps(data['body'])
        else:
            jc_result['flag'] = False
            jc_result['message'] = data['body']['errorDesc']


def send_message(mqttc, interval, time):
    i = 0
    d = {
            "token":"123456",
            "timestamp":"",
            "body": {
                "type":"get",
            }
    }
    try:
        while i < time:
            mqttc.publish('test/jc/request', json.dumps(d))
            sleep(interval)
            i += 1;
    except Exception as e:
        print(e)


def mqtt_init(ip, port, interval, times):
    global mqttc
    mqttc = mqtt.Client(clean_session=True, userdata=None, protocol=mqtt.MQTTv31, transport="tcp")
    mqttc.on_message = on_message
    mqttc.connect(ip, port, 30)
    threading.Thread(target=send_message, args=(mqttc, interval, times)).start()
    mqttc.subscribe('test/jc/response', 2)
    mqttc.loop_start()