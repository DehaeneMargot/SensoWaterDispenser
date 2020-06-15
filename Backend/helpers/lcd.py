from RPi import GPIO
import time

class LCD:

    def __init__(self, E=19, RS= 13, SDA=23, SCL=18, address=32):
        
        GPIO.setmode(GPIO.BCM)
        self.E = E
        self.RS = RS
        self.bus = I2C(SDA, SCL, address)

        GPIO.setup(self.RS, GPIO.OUT)
        GPIO.setup(self.E, GPIO.OUT)

        self.send_instruction(0x38) #function set
        self.send_instruction(0xF) #display on
        self.send_instruction(0x1) #clear display

    def send_instruction(self, value):
        GPIO.output(self.RS, GPIO.LOW)
        GPIO.output(self.E, GPIO.HIGH)
        self.set_data_bits(value)
        GPIO.output(self.E, GPIO.LOW)
        time.sleep(0.01)

    def send_character(self, value):
        GPIO.output(self.RS, GPIO.HIGH)
        GPIO.output(self.E, GPIO.HIGH)
        self.set_data_bits(value)
        GPIO.output(self.E, GPIO.LOW)
        time.sleep(0.01)
    
    def clear_screen(self):
        self.send_instruction(0x1) #clear display

    def write_message(self, message):
        i = 0
        if len(message) < 17:
            for i in range(0, len(message)):
                self.send_character(ord(message[i]))
        else:
            for i in range(0, 16):
                self.send_character(ord((message[i])))
            self.send_instruction(0xC0)
            for i in range(16,len(message)):
                self.send_character(ord(message[i]))


    def set_data_bits(self, value):
        self.bus.write_outputs(value)

    def cursor_line(self, positie):
        if (positie == 0):
            self.send_instruction(0x2)
        if (positie == 1):
            self.send_instruction(0xC0)

class I2C:

    cijfers = { 0:63, 1:6, 2:91, 3:79, 4:102, 5:109, 6:125, 7:7, 8:127, 9:111}

    def __init__(self, SDA, SCL, Address):
        self._SDA = SDA
        self._SCL = SCL
        GPIO.setup(self._SDA, GPIO.OUT)
        GPIO.setup(self._SCL, GPIO.OUT)
        self._address = Address

    def __start_conditie(self):
        GPIO.output(self._SDA, GPIO.HIGH)
        GPIO.output(self._SCL, GPIO.HIGH)
        time.sleep(0.002)
        GPIO.output(self._SDA, GPIO.LOW)
        time.sleep(0.002)
        GPIO.output(self._SCL, GPIO.LOW)
        time.sleep(0.002)

    def __stop_conditie(self):
        GPIO.output(self._SCL,GPIO.LOW)
        GPIO.output(self._SDA,GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(self._SCL,GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self._SDA,GPIO.HIGH)

    def __write_bit(self, bit):
        GPIO.output(self._SDA, bit)
        time.sleep(0.002)
        GPIO.output(self._SCL,GPIO.HIGH)
        time.sleep(0.002)
        GPIO.output(self._SCL,GPIO.LOW)
        time.sleep(0.002)

    def __write_byte(self, byte):
        mask = 0x80
        for i in range(0,8):
            self.__write_bit(byte & (mask >> i))

    def __ack(self):
        GPIO.setup(self._SDA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(self._SCL, 1)
        value = GPIO.input(self._SDA)
        GPIO.setup(self._SDA,GPIO.OUT)
        GPIO.output(self._SCL,0)
        return value

    def write_outputs(self, data:int):
        self.__start_conditie()
        self.__write_byte(self._address << 1)
        self.__ack()
        self.__write_byte(data)
        self.__ack()
        self.__stop_conditie()