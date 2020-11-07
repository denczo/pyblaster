import spidev
import time

class MCP3008:
    def __init__(self, chip_select):
        self.spi = spidev.SpiDev()
        self.spi.open(1, chip_select)
        self.spi.max_speed_hz = 1000000

    def analogInput(self, channel):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data


def read_pots(amount):
    for i in range(amount):
        print(mcp.analogInput(i))
        time.sleep(500)
    print("________________")


mcp = MCP3008(0)
while True:
    read_pots(5)
