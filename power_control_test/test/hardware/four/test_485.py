from time import sleep
import serial
from test.lib import Ser

def comm(send, read):
    byte = '485 rx-tx test data'
    ser_send = serial.Serial(send, 115200)
    ser_read = serial.Serial(read, 115200)
    ser_read.flushInput()
    ser_send.write(byte.encode('utf-8'));
    sleep(0.1)
    count = ser_read.inWaiting()
    count = ser_read.read(count)
    if str(count).find('485 rx-tx test data') > -1:
        return True
    return False



def test_485(d):
    result = [{
        "flag": True,
        "message": "485 send_receive pass!"
    }]
    comm_result = []
    try:
        ser = Ser()
        ser.openCom(port_name = d['serial_485_sub'])
        read = ser.run(bytes.fromhex('68 05 00 42 00 11 02 12 00 00 1d 85 16'), 87)
        ser.closrCom()
        if read == False or str(read).find('RS485') == -1:
            result[0]['flag'] = False
            result[0]['message'] = "Serial Protocol error!"
            return result
        comm_result.append(comm(d['serial_send'], d['serial_read']))
        comm_result.append(comm(d['serial_read'], d['serial_send']))
        print(comm_result)

    except Exception as e:
        print(e)
        result[0]['flag'] = False
        result[0]['message'] = "ttyACM serial error!"
        return result
    return result
