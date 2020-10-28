import serial
import serial.tools.list_ports
import threading
from time import sleep, time
import os
import signal

def getTimeStamp() -> int:
    return int(round(time() * 1000))


def listPortName() -> set:
    device_name = set()
    for com in serial.tools.list_ports.comports():
        device_name.add(com.device)
    return device_name


def dealData(com, data):
    for d in data[:]:
        com.container.append(d)
    i = 0
    container = com.container
    if len(container) < 7:
        return
    while i < len(container):
        if container[i] != 105:
            i = i + 1
            continue
        if (i + 2) >= len(container):
            break
        length = container[i+1] + container[i+2]*256
        if i + length > 300:
            i = i + 1
            continue
        if i + length > len(container):
            break
        frame_ = container[i:i + length]
        if frame_[-1] != 67:
            i = i + 1
            continue
        if frame_[3] == int('87', 16):
            com.mac = frame_[4:20]
        if frame_[3] == int('81', 16):
            com.deal_rx(frame_)
        i = i + length
    com.container = com.container[i:]


def readData(com):
    while True:
        if com.exit is True:
            return
        if com.isOpen() is False:
            sleep(0.1)
            continue
        data = com.com.read(1)

        if len(data) != 0:
            com.dealFunc(com, data)


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
                bytesize=data_bits)
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
        if self.com.isOpen() is False:
            return True
        try:
            self.com.close()
        except Exception as e:
            return False
        return True

    def isOpen(self):
        return self.com.isOpen()

    def __del__(self):
        self.exit = True