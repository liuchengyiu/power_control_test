from .triphase import triphase_run
from test.lib import *
from .jc import jc_run
import time, serial

def int_to_bcd(data: str)-> list:
    data_list = []
    a = 0
    b = 0
    for i in data:
        if i == ".":
            continue
        if len(data_list) % 2 == 0 and a == 0:
            data_list.append(ten_to_2(int(i)))
            a += 1
            continue
        if b % 2 == 0:
            data_list.append(ten_to_2(int(i)))
        else:
            data_list[a] = data_list[a] + ten_to_2(int(i))
            a += 1
        b += 1
    return data_list

def batebcd_to_int(data: str) -> dict:
    if data == False:
        return False
    send_jc_dict = {}
    data_list= data.split(" ")
    data_value = ""
    data_type = ""
    for i in range(sixteen_to_10(data_list[2])):
        if data_list[i + 3] == "33":
            continue
        if i == 0:
            data_type = ten_to_16(sixteen_to_10(data_list[i+3]) - sixteen_to_10("33"))
            continue
        if i % 9 == 0:
            send_jc_dict[data_type] = data_value
            data_value = ''
            data_type = ten_to_16(sixteen_to_10(data_list[i+3]) - sixteen_to_10("33"))
        else:
            data_int = sixteen_to_10(data_list[i+3]) - sixteen_to_10("63")
            if data_int < 0:
                data_int = '.'
            data_value = data_value + str(data_int)
    return send_jc_dict

def jcread_to_int(data: str) -> list:
    data= data.split(" ")
    voltage_current = []
    for index, values in enumerate(data):
        data[index]= sixteen_to_10(values)
    if data[3] == 144:
        for i in range(29):
            voltage_current.append(round(int4_to_float([data[i * 4 + 7], data[i * 4 + 6], data[i * 4 + 5], data[i * 4 + 4]]), 5))
    return voltage_current

def int_relative(jc, power, gap) -> bool:
    jc= float(jc)
    power= float(power)
    if jc >= power:
        resuln= jc- power
    else:
        resuln= power- jc
    if jc * gap > resuln:
        return True
    else:
        return False


def jc_relative_power(jc_dict: dict, power_list: list) -> bool:
    result= []
    if len(jc_dict) == 0 and len(power_list) == 0:
        return False
    result.append(int_relative(jc_dict['40'], power_list[0], 0.002))
    result.append(int_relative(jc_dict['43'], power_list[1]* 0.001, 0.002))
    result.append(int_relative(jc_dict['41'], power_list[6], 0.002))
    result.append(int_relative(jc_dict['44'], power_list[7]*0.001, 0.002))
    result.append(int_relative(jc_dict['42'], power_list[12], 0.002))
    result.append(int_relative(jc_dict['45'], power_list[13]*0.001, 0.002))
    result.append(int_relative(jc_dict['50'], power_list[2], 0.005))
    result.append(int_relative(jc_dict['51'], power_list[8], 0.005))
    result.append(int_relative(jc_dict['52'], power_list[14], 0.005))
    for res in result:
        if res == False:
            print("error too big")
            return False
        else:
            print("calibration pass")
            return True

send_tr_list=[
    ["68", "01"],#三相四线
    ["68", "07", "01110000", "00100010", "00100000", "00000000", "00000000", "00000000"],#电压220
    ["68", "07", "01110001", "00100000", "00000001", "01010000", "00000000", "00000000"],#电流1.5
    ["68", "03"],#打开功能
    ["68", "07", "01110011", "00100000", "01100000", "00000000"],#功率因数0.5
    ["68", "0a"],#读电压结果
    ["68", "07", "01110001", "00100000", "00000000", "00000111", "01010000", "00000000"],#电流0.075
    ["68", "07", "01110001", "00100000", "00000000", "00000000", "00000000", "00000000"],#电流0
    ["68", "07", "01110011", "00100000", "00000000", "00000000"],#功率因数1
    ["68", "0b"],#读功率结果
    ["68", "05"],#关闭功能
]

result = [{
    "flag": False,
    "message": 'auto calibrate failed!'
}]

def runCaLib(ser_triphase, ser_jc):
    if triphase_run(ser_triphase, send_tr_list[0]) == False:
        return False
    triphase_run(ser_triphase, send_tr_list[1])
    triphase_run(ser_triphase, send_tr_list[2])
    triphase_run(ser_triphase, send_tr_list[3])
    triphase_run(ser_triphase, send_tr_list[8])
    time.sleep(10)
    read_data= batebcd_to_int(triphase_run(ser_triphase, send_tr_list[5]))
    if read_data==False or round(float(read_data["40"])) != 220 or round(float(read_data["43"]), 1) != 1.5:
        return False
    jc_run(ser_jc, {}, 1, 1)
    time.sleep(1)
    jc_run(ser_jc, {}, 5, 1)
    jc_run(ser_jc, read_data, 6, 1)
    triphase_run(ser_triphase, send_tr_list[4])
    time.sleep(5)
    read_data = batebcd_to_int(triphase_run(ser_triphase, send_tr_list[5]))
    jc_run(ser_jc, read_data, 7, 0.5)
    triphase_run(ser_triphase, send_tr_list[6])
    time.sleep(5)
    read_data = batebcd_to_int(triphase_run(ser_triphase, send_tr_list[5]))
    if read_data==False or round(float(read_data["43"]), 3) != 0.075:
        return False
    jc_run(ser_jc, read_data, 8, 0.5)
    triphase_run(ser_triphase, send_tr_list[7])
    time.sleep(5)
    jc_run(ser_jc, {}, 9, 0.5)
    triphase_run(ser_triphase, send_tr_list[1])
    triphase_run(ser_triphase, send_tr_list[2])
    triphase_run(ser_triphase, send_tr_list[8])
    time.sleep(5)
    read_data = batebcd_to_int(triphase_run(ser_triphase, send_tr_list[5]))
    if read_data==False or round(float(read_data["40"])) != 220 or round(float(read_data["43"]), 1) != 1.5:
        return False
    jc_run(ser_jc, read_data, 10, 1)
    jc_run(ser_jc, {}, 11, 1)

    triphase_dict = dict(batebcd_to_int(triphase_run(ser_triphase, send_tr_list[5])), **batebcd_to_int(triphase_run(ser_triphase, send_tr_list[9])))
    jc_read_data= jcread_to_int(jc_run(ser_jc, {}, 16, 1))
    print(triphase_dict, jc_read_data)
    return jc_relative_power(triphase_dict, jc_read_data)
def auto_jc(d):
    try:
        ser_jc = serial.Serial(d['serial_jc'], 115200)
        ser_triphase = serial.Serial(d['serial_power'], 9600)
    except Exception as e:
        result[0]['flag'] = False
        result[0]['message'] = 'open serial error!'
        return result
    if runCaLib(ser_triphase, ser_jc):
        result[0]['flag'] = True
        result[0]['message'] = 'auto calibrate pass!'
        return result
    return result
