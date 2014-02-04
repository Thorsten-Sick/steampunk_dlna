__author__ = 'thorsten'

# At the moment just everything together

import gaugette.rotary_encoder
import gaugette.switch
import gaugette.rgbled
import time
R_PIN = 8
G_PIN = 9
B_PIN = 7

A_PIN = 0
B_PIN = 2
SW_PIN = 3

last_state = None

gaugette.platform ="raspberrypi"
encoder = gaugette.rotary_encoder.RotaryEncoder(A_PIN, B_PIN)
switch = gaugette.switch.Switch(SW_PIN, False)
led = gaugette.rgbled.RgbLed(R_PIN, G_PIN, B_PIN)


while True:
    delta = encoder.get_delta()
    switch_state = switch.get_state()
    if switch_state != last_state:
        print("SW state: %s" % str(switch_state))
        last_state = switch_state
    #state = encoder.rotation_state()
    #print ("%s" % str(state))
    if delta != 0:
        print "rotate %d %s" % (delta,str(encoder.rotation_sequence()))
    led.fade(0,255,255)
    time.sleep(1)
    led.fade(255,0,255)
    time.sleep(1)
    led.fade(255,255,0)
    time.sleep(1)








