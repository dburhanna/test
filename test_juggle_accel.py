#test_juggle_accel.py
# added another comment
# cheeseburgers are yummy

# funny

import board
import time
import math

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_circuitplayground import cp

ble = BLERadio()
ble.name = "JuggleCounter"
uart = UARTService()

advertisement = ProvideServicesAdvertisement(uart)

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    # Now we're connected

    while ble.connected:
        if uart.in_waiting:
            recvd = uart.read(32)
            if recvd is not None:
                # convert bytearray to string
                data_string = ''.join([chr(b) for b in recvd])
                print(data_string, end="")
                uart.write(data_string)
            if "Juggle" in data_string:
                uart.write("enter target")
                recvd = None
                while not uart.in_waiting:
                    print("getting target value")
                    time.sleep(1)
                recvd = uart.read(32)
                juggle_target = ''.join([chr(b) for b in recvd])
                print(juggle_target, end="")
                uart.write(juggle_target)

                uart.write("Counting juggles...")
                count = 0
                while count<int(juggle_target):

                    xsquared = cp.acceleration[0]*cp.acceleration[0]
                    ysquared = cp.acceleration[1]*cp.acceleration[1]
                    zsquared = cp.acceleration[2]*cp.acceleration[2]

                    #force_vector = xsquared+ysquared+zsquared
                    force_vector = math.sqrt(abs(xsquared+ysquared+zsquared))*100
                    if force_vector < 15 :
                        count = count +1
                        uart.write(str(count)+" " +str(force_vector))
                    print(force_vector)
                    time.sleep(.05)


                uart.write("You did it!")
