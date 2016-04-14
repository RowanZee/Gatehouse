try:
    import RPi.GPIO as GPIO
except:
    print 'Notice: Not Connect To A Pi.'
import time


class Garage:
    pinList = [4]

    def __init__(self):
        try:
            GPIO.setmode(GPIO.BCM)
            self.cleanupRelay()
        except:
            print 'Warning: Could Not Init Garage.'

    # TOGGLE FUNCTION
    def toggleDoor(self):
        try:
            for pin in self.pinList:
                GPIO.output(pin, GPIO.HIGH)

            time.sleep(.2)
            GPIO.cleanup()
            GPIO.setmode(GPIO.BCM)
            self.cleanupRelay()
        except:
            print 'Warning: Failed To Toggle Door.'

    # Cleanup PI
    def cleanupRelay(self):
        try:
            for pin in self.pinList:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)
        except:
            print 'Warning: Failed To Clean Up.'
