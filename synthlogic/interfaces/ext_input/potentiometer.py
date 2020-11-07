import spidev


class Potentiometer:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(1, 0)
        self.spi.max_speed_hz = 1000000

    def analogInput(self, channel):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data


class PotGroup:
    def __init__(self, amount):
        self.pots = self.create_pots(amount)
        self.pot_amount = amount

    def create_pots(self, amount):
        pots = []
        for i in range(amount):
            pot = Potentiometer()
            pots.append(pot)

        return pots

    def print_pots(self):
        for i in range(self.pot_amount):
            print(self.pots[i].analogInput(i))


pots = PotGroup(8)
while True:
    pots.print_pots()