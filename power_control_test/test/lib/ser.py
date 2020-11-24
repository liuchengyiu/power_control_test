import serial, threading, time

def serial_send(serial, byte):
    if len(byte) > 0:
        serial.write(byte);

def serial_read(self, serial, lenth):
    times = int(time.time())
    while True:
        self.read = self.read + serial.read(1)
        if int(time.time()) == times + 2:
            return self.read
        # print('len=', len(self.read), ' ', self.read)
        if len(self.read) == lenth:
            return self.read
    return count

class Ser:
    def __init__(self):
        self.com = serial.Serial()
        self.read = b''

    def closrCom(self):
        if self.com.isOpen():
            self.com.close()

    def openCom(
            self,
            port_name='',
            baud_rate=115200,
            parity=serial.PARITY_NONE,
            stop_bits=serial.STOPBITS_ONE,
            data_bits=serial.EIGHTBITS) -> bool:
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

    def run(self, send ,correct) -> bytes or bool:
        if self.com.isOpen():
            self.com.flushInput()
            self.read = b''
            f = threading.Thread(target=serial_read, args=(self, self.com, correct))
            f.start()
            serial_send(self.com, send)
            f.join()
            print('len', len(self.read), self.read)
            return self.read
        else:
            return False



