from microbit import *

# The robot motor control is based on work I did for @ScienceOxford
# Line-following code adapted from MultiWingSpan: http://www.multiwingspan.co.uk/micro.php?page=botline
# HCSR04 class created by fizban99: https://github.com/fizban99/microbit_hcsr04

display.off()

LF = pin12
LB = pin8
RF = pin14
RB = pin15


# 1023 turns the motors off; 0 turns them on at full speed
def stop():
    LF.write_analog(1023)
    LB.write_analog(1023)
    RF.write_analog(1023)
    RB.write_analog(1023)
    display.show(Image.DUCK)


# Inputs between 0-1023 to control both motors
def drive(L, R):
    # Below controls the left wheel: forward, backward, stop at given speed
    if L > 0 and L <= 1023:
        LF.write_analog(abs(L-1023))  # go forwards at speed given
        LB.write_analog(1023)         # don't go backwards
    elif L < 0 and L >= -1023:
        LF.write_analog(1023)         # don't go forwards
        LB.write_analog(abs(L+1023))  # go backwards at speed given
    else:
        LF.write_analog(1023)         # stop the left wheel
        LB.write_analog(1023)
    # Below controls the right wheel: forward, backward, stop at given speed
    if R > 0 and R <= 1023:
        RF.write_analog(abs(R-1023))  # go forwards at speed given
        RB.write_analog(1023)         # don't go backwards
    elif R < 0 and R >= -1023:
        RF.write_analog(1023)         # don't go forwards
        RB.write_analog(abs(R+1023))  # go backwards at speed given
    else:
        RF.write_analog(1023)         # stop the right wheel
        RB.write_analog(1023)

class HCSR04:
    def __init__(self, tpin=pin0, epin=pin1, spin=pin13):
        self.trigger_pin = tpin
        self.echo_pin = epin
        self.sclk_pin = spin

    def distance_mm(self):
        spi.init(baudrate=125000, sclk=self.sclk_pin,
                 mosi=self.trigger_pin, miso=self.echo_pin)
        pre = 0
        post = 0
        k = -1
        length = 500
        resp = bytearray(length)
        resp[0] = 0xFF
        spi.write_readinto(resp, resp)
        # find first non zero value
        try:
            i, value = next((ind, v) for ind, v in enumerate(resp) if v)
        except StopIteration:
            i = -1
        if i > 0:
            pre = bin(value).count("1")
            # find first non full high value afterwards
            try:
                k, value = next((ind, v)
                                for ind, v in enumerate(resp[i:length - 2]) if resp[i + ind + 1] == 0)
                post = bin(value).count("1") if k else 0
                k = k + i
            except StopIteration:
                i = -1
        dist= -1 if i < 0 else round((pre + (k - i) * 8. + post) * 8 * 0.172)
        return dist

sensor = HCSR04(tpin=pin0, epin=pin1)

while True:
    distance = round(sensor.distance_mm()/10)
    left_sensor = pin2.read_analog()
    right_sensor = pin3.read_analog()
    while distance <= 3:
        stop()
        sleep(5000)
        distance = round(sensor.distance_mm()/10)
    if left_sensor <= 10 and right_sensor <= 10:
        #display.show(Image.ARROW_N)
        drive(400, 400)
        sleep(100)
    elif left_sensor >= 10 and right_sensor < 10:
        #display.show(Image.ARROW_W)
        drive(0, 300)
        sleep(100)
    elif left_sensor < 10 and right_sensor >= 10:
        #display.show(Image.ARROW_E)
        drive(300, 0)
        sleep(100)
    else:
        stop()
        sleep(100)
  
  # NOTES - currently working when micro:bit powered from computer, not working when powered from AAA battery pack.
  # need to adjust numbers to make this work
  
  # NOTES - does HCSR04 need to use pin0 for the trigger? Would a digital pin work? Then I can use the display again.
