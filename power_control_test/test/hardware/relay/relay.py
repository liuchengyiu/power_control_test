from time import sleep
from test.lib import Ser

def relay_test(d):
    print("a")
    result = [{
        "flag": True,
        "message": "relay test pass!"
    }]
    try:
        ser = Ser()
        ser.openCom(port_name=d['serial_relay_business'])
        ser_yx = Ser()
        ser_yx.openCom(port_name=d['serial_yx_switch'])
        read = ser.run(bytes.fromhex('68 05 00 42 00 11 02 12 00 00 1d 85 16'), 108)
        ser.closrCom()
        if read == False or str(read).find('JDQ') == -1:
            result[0]['flag'] = False
            result[0]['message'] = "Serial Protocol error!"
            return result
        ser_switch = Ser()
        ser_switch.openCom(port_name=d['serial_relay_switch'])
        ser_switch.run(bytes.fromhex('68 07 00 42 00 11 03 12 03 71 11 00 82 25 16'), 15)
        yx_read = ser_yx.run(bytes.fromhex('68 05 00 42 00 11 02 12 00 40 19 C7 16'), 110)
        if yx_read[15] != 0:
            result[0]['flag'] = False
            result[0]['message'] = "yx serial error"
        sleep(1)
        ser_switch.run(bytes.fromhex('68 07 00 42 00 11 03 12 03 71 11 01 0b 34 16'), 15)
        yx_read = ser_yx.run(bytes.fromhex('68 05 00 42 00 11 02 12 00 40 19 C7 16'), 110)
        if yx_read[15] != 8:
            result[0]['flag'] = False
            result[0]['message'] = "yx serial error"
        ser_switch.closrCom()
        ser_yx.closrCom()
    except Exception as e:
        print('error=', e)
        result[0]['flag'] = False
        result[0]['message'] = "ttyACM serial error!"
        return result
    return result
