from repositories.DataRepository import DataRepository
import time

class DS18B20():

    def __init__(self, address):
        self.address = address 

    @property
    def address(self):
        """The address property."""
        return self._address

    @address.setter
    def address(self, value):
        if isinstance(value, str):
            self._address = value
        else:
            raise ValueError('Address datatype is not valid')

    @property
    def __slave_file(self):
        """The slave_file property."""
        return f'/sys/bus/w1/devices/w1_bus_master1/{self.address}/w1_slave'

    def get_temperature(self):
        data = open(self.__slave_file)
        temperature = data.readlines()[1].rstrip('\n').split('t=')[1]
        data.close()
        return float(f'{temperature[:-3]}.{temperature[-3:]}')
