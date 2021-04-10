from machine import Pin, lightsleep, I2C
from ssd1306 import SSD1306_I2C
from fdrawer import FontDrawer
import utime

''' This example only requires a button between gpio15 and ground.
'''

class FlowMonitor:

    def __init__(self, bounce=150, fontname='/lib/veram_m23', debug=False):

        self.debug = debug
        self.bounce = bounce

        self.button = Pin(15, Pin.IN, pull=Pin.PULL_UP)
        self.button.irq(self.pressed, trigger=Pin.IRQ_FALLING)
        # we want to capture the full press/release sequence so wake on press trigger.
        event = Pin.IRQ_FALLING
        print('Wake Event:',event)
        self.button.dormant_wake_irq(event=event)
        self.ptime = 0
        self.bpressed = 0

    def pressed(self, pin):

        if self.debug: print('Pressed Button-{}'.format(pin))
        self.ptime = utime.ticks_ms()
        self.button.irq(self.released, trigger=Pin.IRQ_RISING)

    def released(self, pin):

        if self.ptime > 0:
            ntime = utime.ticks_ms()
            dtime = utime.ticks_diff(ntime, self.ptime)
            if dtime < self.bounce:
                self.ptime = 0
                return
            if self.debug: print('Released Button-{} time {}'.format(pin, dtime))
            self.ptime = ntime
            self.bpressed += 1

        self.button.irq(self.pressed, trigger=Pin.IRQ_FALLING)

    def run(self):

        count = 0
        while(True):
            utime.sleep(1)
            count += 1
            print('Running ...')
            if count > 5:
                print('Sleep (Dormant) Activated')
                # utime.sleep(3)
                lightsleep()
                print('Woken')
                count = 1
                print('reset loop counter\nbpressed=',self.bpressed)

            pass

if __name__ == '__main__':

    prog = FlowMonitor(debug=True)
    prog.run()
