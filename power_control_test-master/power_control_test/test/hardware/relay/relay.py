import binascii
from time import sleep
import serial

serial_read_data = ''

def serial_com(serial, com):  # 连接
    serial = serial.Serial(com, 115200)
    return serial;


def serial_send(serial, byte):  # 发送
    serial.write(byte);

def serial_read(serial):  # 接收
    n = serial.inWaiting()
    if n:
        count = str(binascii.b2a_hex(serial.read(n)))[2:-1]
        return count

def serial_run(serial, sleep_stop, data, judag):
    byte = bytes.fromhex(data)
    serial.flushInput()
    serial_send(serial, byte)
    sleep(sleep_stop)
    serial_data = serial_read(serial)
    if serial_data[6:8] == judag:
        return 1
    else:
        return 0


def relay_test(d):
    print("a")
    result = [{
        "flag": True,
        "message": "relay_test pass!"
    }]
    try:
        judag= [];
        serial_01 = serial.Serial(d['serial_relay'], 115200);
        serial_02 = serial.Serial(d['serial_relay2'], 115200);
        judag.append(serial_run(serial_01, d['time'], '68 05 00 42 00 11 02 12 00 00 1d 85 16', 'c2'));
        judag.append(serial_run(serial_02, d['time'], '68 07 00 42 00 11 03 12 03 71 11 00 82 25 16', 'c2'));
        judag.append(serial_run(serial_02, d['time'], '68 07 00 42 00 11 03 12 03 71 11 01 0b 34 16', 'c2'));
    except Exception as e:
        result[0]['flag'] = False
        result[0]['message'] = "ttyACM serial error!"
        return result
    for judag_ in judag:
        print(judag_)
        if judag_ == 0:
            result[0]['flag'] = False
            result[0]['message'] = "relay_test file!"
    return result
