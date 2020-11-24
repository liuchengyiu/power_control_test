from test.lib import Com
from time import sleep
import threading

commands = ['AT', 'ATE0', 'ATI;+CSUB;+CSQ;+CPIN?;+COPS?;+CGREG?;&D2']
result = [{
    "flag": False,
    "message": 'open port failed!'
}]
def test_at(com, read_str):
    com.container = com.container + read_str.decode()
    flag = 'None'
    if com.container.find('OK') > -1:
        flag = 'OK'
    elif com.container.find('ERROR') > -1:
        flag = 'ERROR'
    if flag == 'None' or com.mod == '':
        return
    com.container = ''
    if flag == 'OK':
        com[com.mod] = True
    else:
        com[com.mod] = False
    com.mod = ''

def testCommand(com, command):
    global result
    mod = command.split(':')[0]
    print(command)
    com.setMod(mod)
    com.sendData(command+'\r\n')
    sleep(1)
    print(mod)
    if com[mod] is True:
        return True 
    result[0]['flag'] = False
    result[0]['message'] = '{} test failed'.format(mod)
    return False

def card_4g_at_test(d):
    global commands
    global result
    port = d["serial_4g"]
    baudrate = d["baudrate"]
    try:
        com = Com(test_at)
        flag = com.openCom(port_name=port, baud_rate=baudrate)
        if flag is False:
            com.closeCom()
            return result
        for command in commands:
            r = testCommand(com, command)
            if r is False:
                com.closeCom()
                return result
        sleep(1)
    except Exception as e:
        print(e)
        com.closeCom()
        result[0]['flag'] = False
        result[0]['message'] = '4G AT test error'
        return result
    result[0]['flag'] = True
    result[0]['message'] = '4G AT test pass'
    com.closeCom()
    sleep(1)
    return result
