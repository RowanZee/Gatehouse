try:
    #import RPi.GPIO as GPIO
    import wiringpi
except:
    print("Notice: Not Connected To A Pi.")
import time


class Garage:
    pinList = [4]

    def __init__(self):
        try:
            io = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_SYS)
            #GPIO.setmode(GPIO.BCM)
            io.pinMode(4,io.OUTPUT) # Setup pin 22 (GPIO25)
            self.cleanupRelay()
        except:
            print("Warning: Could Not Init Gate.")

    # TOGGLE FUNCTION
    def toggleDoor(self):
        try:
            for pin in self.pinList:
                io.pinMode(4,io.OUTPUT) # Setup pin 22 (GPIO25)
                #GPIO.output(pin, GPIO.HIGH)

            time.sleep(.2)
            #GPIO.cleanup()
            #GPIO.setmode(GPIO.BCM)
            self.cleanupRelay()
        except:
            print("Warning: Failed To Toggle Door.")

    # Cleanup PI
    def cleanupRelay(self):
        try:
            for pin in self.pinList:
                #GPIO.setup(pin, GPIO.OUT)
                io.digitalWrite(pin,io.LOW) 
                #GPIO.output(pin, GPIO.LOW)
        except:
            print("Warning: Failed To Clean Up.")
