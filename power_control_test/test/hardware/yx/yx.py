from time import sleep
from test.lib import Ser

def yx_test(d):
    print("a")
    result = [{
        "flag": True,
        "message": "relay test pass!"
    }]
    try:
        ser = Ser()
        ser.openCom(port_name=d['serial_yx_business'])
        read = ser.run(bytes.fromhex('68 05 00 42 00 11 02 12 00 00 1d 85 16'), 108)
        ser.closrCom()
        if read == False or str(read).find('YX') == -1:
            result[0]['flag'] = False
            result[0]['message'] = "Serial Protocol error!"
            return result
    except Exception as e:
        print('error=', e)
        result[0]['flag'] = False
        result[0]['message'] = "ttyACM serial error!"
        return result
    return result
