import paho.mqtt.client as mqtt
import json
from time import sleep
from test.lib import run_shell

key_list = ['button_ok', 'button_right', 'button_left', 'button_down', 'button_UP']
mqttc = {}
gpio = 0

def buzzer():
    run_shell('echo {} > /sys/class/gpio/export'.format(str(gpio)))
    run_shell('echo "out" > /sys/class/gpio/gpio{}/direction'.format(str(gpio)))
    run_shell('echo 1 > /sys/class/gpio/gpio{}/value'.format(str(gpio)))
    sleep(0.3)
    run_shell('echo 0 > /sys/class/gpio/gpio{}/value'.format(str(gpio)))

def on_message(msg):
    topic = msg.topic
    payload = bytes.decode(msg.payload)
    if topic == 'test/key/request':
        data = json.loads(payload)
        for a in key_list:
            if data['result'] == a:
                buzzer()
                key_list.remove(a)

def mqtt_init(ip, port):
    global mqttc
    mqttc = mqtt.Client(clean_session=True, userdata=None, protocol=mqtt.MQTTv31, transport="tcp")
    mqttc.on_message = on_message
    mqttc.connect(ip, port, 30)
    mqttc.subscribe('test/key/request')
    buzzer()
    mqttc.loop_start()

def key_test(d):
    global gpio
    global key_list
    gpio = d['gpio']
    ip = d['ip']
    port = d['port']
    times = d['times']
    key = {
        'flag': False,
        'message': 'Key test fails'
    }
    key_list = ['button_ok', 'button_right', 'button_left', 'button_down', 'button_UP']
    try:
        mqtt_init(ip, port)
    except Exception as e:
        return [{
            "flag": False,
            "message": 'create mqtt client error!'
        }]
    for i in range(times):
        if len(key_list) == 0:
            break;
        sleep(1)
    mqttc.disconnect()
    if len(key_list) == 0:
        key['flag'] = True
        key['message'] = 'key pass!'
    else:
        print(*key_list, sep='\n')
    return [key]