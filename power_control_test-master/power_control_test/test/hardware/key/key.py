import paho.mqtt.client as mqtt
import json
from time import sleep
from test.lib import run_shell


key = {
    'flag': False,
    'message':'Key test fails'
}
key_list = ['button_ok', 'button_right', 'button_left', 'button_down', 'button_UP']

mqttc = {}
gpio = 0

def buzzer():
    gpio
    run_shell('echo {} > /sys/class/gpio/export'.format(str(gpio)))
    run_shell('echo "out" > /sys/class/gpio/gpio{}/direction'.format(str(gpio)))
    run_shell('echo 1 > /sys/class/gpio/gpio{}/value'.format(str(gpio)))
    sleep(0.5)
    run_shell('echo 0 > /sys/class/gpio/gpio{}/value'.format(str(gpio)))

def key_test(d):
    ip = d['ip']
    port = d['port']
    interval = d['interval']
    times = d['times']
    global gpio
    gpio = d['gpio']
    try:
        mqtt_init(ip, port, interval, times)
    except Exception as e:
        return [{
            "flag": False,
            "message": 'create mqtt client error!'
        }]
    sleep(interval * times + 3)
    mqttc.disconnect()
    if len(key_list) == 0:

        key['flag'] = True
        key['message'] = 'key pass!'
    else:
        print(*key_list, sep='\n')
    return [key]


def on_message(mqttc, obj, msg):
    topic = msg.topic
    payload = bytes.decode(msg.payload)
    if topic == 'test/key/request':
        data = json.loads(payload)
        global key
        global key_list
        for a in key_list:
            if data['result'] == a:
                buzzer()
                key_list.remove(a)
        if len(key_list) == 0:
            mqttc.disconnect()


def mqtt_init(ip, port, interval, times):
    global mqttc
    mqttc = mqtt.Client(clean_session=True, userdata=None, protocol=mqtt.MQTTv31, transport="tcp")
    mqttc.on_message = on_message
    mqttc.connect(ip, port, 30)
    mqttc.subscribe('test/key/request')
    buzzer()
    mqttc.loop_start()
