import binascii, time
import struct
def trans_floats_to_bytes(array) -> list:
    d = []
    for i in array:
        d.extend(trans_float_to_bytes(i))
    return d
def trans_float_to_bytes(data) -> bytes:
    return struct.pack('f', data)

def crc16_a001(data) -> int:
    crc16 = 0xFFFF
    for d in data:
        crc16 = crc16 ^ d
        for j in range(0, 8):
            if (crc16 & 0x01) > 0:
                crc16 = (crc16 >> 1) ^ 0xa001
                continue
            crc16 = crc16 >> 1
    return crc16

def createFrame(head, command, data, end) -> list:
    length = 7 + len(data)
    frame = [head, length & 0xFF, (length & 0xFF00) >> 8, command]
    for d in data:
        frame.append(d)
    crc = crc16_a001(frame)
    frame.append(crc & 0xFF)
    frame.append((crc & 0xFF00) >> 8)
    frame.append(end)
    return frame

def serial_send(serial, byte):
    print('jc_send=', binascii.b2a_hex(byte))
    serial.write(byte)

def serial_read(serial):
    count = serial.inWaiting();
    a = 0;
    if count:
        data = list(str(binascii.b2a_hex(serial.read(count)))[2:-1]);
        for i in range(len(data)):
            if i == 0:
                continue;
            if i % 2 == 0:
                data.insert(i + a, " ");
                a += 1;
        data = "".join(data);
        return data
def dict_to_sixten(dict_data: dict, type, factor)-> str:
    # print("dict==", dict_data)
    data= []
    if type == 6 or type ==7 or type == 8 or type == 10:

        if type != 10:
            data= [float(dict_data['40']), round(float(dict_data['43']), 4), float(factor), float(dict_data['41']), round(float(dict_data['44']), 4), float(factor), float(dict_data['42']), round(float(dict_data['45']), 4), float(factor)]
        else:
            data= [float(dict_data['40']), round(float(dict_data['43']), 4), float(dict_data['41']), round(float(dict_data['44']), 4), float(dict_data['42']), round(float(dict_data['45']), 4)]

        data= trans_floats_to_bytes(data)
        data.insert(0, 7)

    send_data= createFrame(105, type, data, 67)
    return send_data



def jc_run(ser, send_list: dict, type, factor):

    send_list= dict_to_sixten(send_list, type, factor)
    ser.flushInput()
    serial_send(ser, bytes(send_list))
    time.sleep(0.5)
    data = serial_read(ser)
    print('jc_read==', data)
    if not data:
        print("No promise")
        return False
    return data