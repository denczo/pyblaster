import spidev
import time


class MCP3008:
    def __init__(self, chip_select):
        self.spi = spidev.SpiDev()
        self.spi.open(0, chip_select)
        self.spi.max_speed_hz = 1000000

    def analogInput(self, channel):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data


mcp = MCP3008(0)
# analog inputs
amount = 8

while True:
    for i in range(amount):
        print("CH", str(i)+":", mcp.analogInput(i))
    print("===========")
    time.sleep(0.5)





