from time import sleep
import serial

serial_read_data = ''


def serial_com(serial, com):  # 连接
    serial = serial.Serial(com, 115200)
    return serial;


def serial_send(serial, byte):  # 发送
    serial.write(byte.encode('utf-8'));


def serial_read(serial):  # 接收
    count = serial.inWaiting()  # 返回接受缓存中的字节
    count = serial.read(count)
    return count


def test_485(d):
    result = [{
        "flag": True,
        "message": "485 send_receive pass!"
    }]
    try:
        serial_01 = serial_com(serial, d['serial_read']);
        serial_02 = serial_com(serial, d['serial_send']);
        byte = '485 rx-tx test data'
        sleep_stop = d['time']
        serial_02.flushInput()
        serial_send(serial_01, byte)
        sleep(sleep_stop)
        serial_data = serial_read(serial_02)

        serial_data = str(serial_data)[2:-1]
        print('len_date==' + serial_data)
    except Exception as e:
        result[0]['flag'] = False
        result[0]['message'] = "ttyUSB serial error!"
        return result

    if byte != serial_data:
        result[0]['flag'] = False
        result[0]['message'] = "485 send_receive file!"
    return result
