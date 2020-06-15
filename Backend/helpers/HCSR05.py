from RPi import GPIO
import time

class HCSR05:
    def __init__(self, echo, trigger):
        self._echo = echo
        self._trigger = trigger
        self.__init_gpio()
    
    @property
    def echo(self):
        """The echo property."""
        return self._echo
    
    @property
    def trigger(self):
        """The trigger property."""
        return self._trigger

    def __init_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.setup(self.trigger, GPIO.OUT)
        time.sleep(0.5)

    def get_distance(self):
        GPIO.output(self.trigger, GPIO.LOW)
        time.sleep(1)

        GPIO.output(self.trigger, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trigger, GPIO.LOW)

        while GPIO.input(self.echo) == 0:
            start_time = time.time()

        while GPIO.input(self.echo) == 1:
            end_time = time.time()
        
        time_range = end_time - start_time
        return round(time_range * 17150,2)
