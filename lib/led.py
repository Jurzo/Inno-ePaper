import RPi.GPIO as GPIO
import asyncio
led1 = 21
led2 = 20
led3 = 16
led4 = 12

class leds:
    def __init__(self):
        self.pwm = []
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led1, GPIO.OUT)
        self.pwm.append(GPIO.PWM(led1, 100))
        GPIO.setup(led2, GPIO.OUT)
        self.pwm.append(GPIO.PWM(led2, 100))
        GPIO.setup(led3, GPIO.OUT)
        self.pwm.append(GPIO.PWM(led3, 100))
        GPIO.setup(led4, GPIO.OUT)
        self.pwm.append(GPIO.PWM(led4, 100))

        for cycle in self.pwm:
            cycle.start(0)

        self.on = False

    async def brighter(self):
        for x in range(0, 100):
            for cycle in self.pwm:
                cycle.ChangeDutyCycle(x)
                await asyncio.sleep(0.1)
        self.on = True
        return

    async def dim(self):
        for x in range(100,-1,-1):
            for cycle in self.pwm:
                cycle.ChangeDutyCycle(x)
                await asyncio.sleep(0.01)
        self.on = False
        return

    def stop(self):
        for cycle in self.pwm:
            cycle.stop()
        GPIO.cleanup()
