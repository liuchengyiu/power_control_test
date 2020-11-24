import paho.mqtt.client as mqtt
import json

def mqtt_up(t, percent, count, message):
    host= '127.0.0.1'
    port= 1883
    d = {
        "token": "",
        "timestamp": "",
        "body": {
            "type": 255,
            "len": 33,
            "data": {
                "percent": percent,
                "topic": "topic",
                "message": message,
                "index": count,
                "entire": 9
            }

        }
    }
    try:
        mqttc = mqtt.Client(clean_session=True, userdata=None, protocol=mqtt.MQTTv31, transport="tcp")
        mqttc.connect(host, port, 30);
        mqttc.publish(t, json.dumps(d));
        mqttc.disconnect();
        return 1
    except Exception as e:
        mqttc.publish(t, json.dumps(d));
        return 0