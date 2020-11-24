import binascii, time
from test.lib import *

def verify_data(bate: str) -> str:#计算校验
    data_list = bate.split(" ")
    verify_int = 0
    for data_int in data_list:
        data_int= sixteen_to_10(data_int)
        if int(data_int) > 256:
            continue
        verify_int= verify_int+ data_int
    bate= bate+ " "+ ten_to_16(verify_int)[-2:]+ " 16"
    return bate

def df_len(list_date: list) -> str:
    lenth= len(list_date)- 2
    lenth= ten_to_16(lenth)
    return lenth

def two_list_16(list_datea: list) -> str:
    bate= ""
    i= 0
    list_date= []
    list_date.extend(list_datea)
    list_date.insert(2, df_len(list_date))#计算长度
    for list_ in list_date:
        if i < 3:
            i += 1
            if len(str(list_)) == 1:
                list_ = "0"+ str(list_)
            bate = bate + str(list_) + " "
            continue
        bate= bate+ twoBcd_to_16(list_)+ " "
    bate= bate[0:-1]
    bate= verify_data(bate)#计算校验
    return bate

def serial_send(serial, byte):
    serial.write(byte)

def serial_read(serial):
    count = serial.inWaiting()
    a=0
    if count:
        data= list(str(binascii.b2a_hex(serial.read(count)))[2:-1])
        for i in range(len(data)):
            if i==0:
                continue
            if i%2 == 0:
                data.insert(i+a, " ")
                a+=1
        data= "".join(data)
        return data
    return False

def triphase_run(ser, send_list: list):
    try:
        send_str= two_list_16(send_list)
        print('power_send==', send_str)
        ser.flushInput()
        serial_send(ser, bytes.fromhex(send_str))
        time.sleep(1)
        serial_read_data= serial_read(ser)
    except  Exception as e:
        return False
    print('power_read==', serial_read_data)
    if not serial_read_data:
        print("No promise")
        return False
    return serial_read_data

