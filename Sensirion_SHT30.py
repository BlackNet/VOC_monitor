import time
import smbus

sht30_bus = smbus.SMBus(1)


class Sensirion_SHT30():
    def __init__(self):
        self.sht30_bus = smbus.SMBus(1)
        self.temperature = None
        self.humidity = None


    def sht30_read(self):
        sht30_bus.write_i2c_block_data(0x44, 0x2C, [0x06])
        time.sleep(0.5)
        data = sht30_bus.read_i2c_block_data(0x44, 0x00, 6)
        self.temperature = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
        self.humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
