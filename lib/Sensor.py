import RPi.GPIO as GPIO
import time

class Sensors:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
 
        self.GPIO_TRIGGER = 14
        self.GPIO_ECHO = 15
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

    def getDist(self):
        GPIO.output(self.GPIO_TRIGGER, True)
 
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (343000 mm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 343000) / 2
    
        return distance

    def cleanup(self):
        GPIO.cleanup()