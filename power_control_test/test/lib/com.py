import serial
import serial.tools.list_ports
import threading
from time import sleep

def listPortName() -> set:
    device_name = set()
    for com in serial.tools.list_ports.comports():
        device_name.add(com.device)
    return device_name


def readData(com):
    while True:
        if com.exit is True:
            break
        if com.isOpen() is False:
            sleep(0.1)
            continue
        if not com.com.readable():
            continue
        data = com.com.read(1)
        if len(data) != 0:
            com.dealFunc(com, data)
    return

class Com:
    def __init__(self, dealFunc):
        self.com = serial.Serial()
        self.container = ""
        self.dealFunc = dealFunc
        self.exit = False
        self.mod = ''
        self.AT = False
        self.ATE0 = False
        self.ATI = False
        try:
            self.deal_thread = threading.Thread(target=readData, args=(self,))
            self.deal_thread.start()
        except Exception as e:
            print(e)

    def openCom(
            self,
            port_name='',
            baud_rate=9600,
            parity=serial.PARITY_NONE,
            stop_bits=serial.STOPBITS_ONE,
            data_bits=serial.EIGHTBITS) -> bool:
        if port_name not in listPortName():
            return False
        try:
            if self.com.isOpen() is True:
                self.com.close()
            self.com = serial.Serial(
                port=port_name,
                baudrate=baud_rate,
                parity=parity,
                stopbits=stop_bits,
                bytesize=data_bits,
                timeout=1)
        except Exception as e:
            print(e)
            return False
        return True

    def __setitem__(self, k, v):
        self.k = v

    def __getitem__(self, k):
        return self.k

    def sendData(self, data) -> bool:
        if self.com.isOpen() is False:
            return False
        try:
            self.com.write(data.encode())
        except Exception as e:
            return False
        return True

    def setMod(self, mod):
        self.mod = mod

    def closeCom(self) -> bool:
        self.Exit()
        self.com.flush()
        sleep(1)
        if self.com.isOpen() is False:
            return True
        try:
            self.com.close()
        except Exception as e:
            return False
        return True

    def isOpen(self):
        return self.com.isOpen()

    def Exit(self):
        self.exit = True