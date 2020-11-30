#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5
import weather as W
import Sensor as S
from Screen import Screen
from Img import ImageCreator
import time as t
from datetime import *
import traceback
import asyncio
from functools import wraps, partial
from aioudp import *
import led

logging.basicConfig(level=logging.DEBUG)
logging.info("e-Paper testausta")

w = W.weatherData()
sensors = S.sensors()
screen = Screen()
img = ImageCreator()
leds = led.leds()
alarmOn = False

UDP_IP = "0.0.0.0" # listen to everything
UDP_PORT = 1235 # port

def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run

async def getDist():
    while 1:
        x = sensors.getDist()
        logging.info(x)
        if x < 200:
            break
        await asyncio.sleep(1)
    return

async def UDPReceiver():
    local = await open_local_endpoint(UDP_IP, UDP_PORT)
    data, address = await local.receive()

    print(f"Got {data!r} from {address[0]} port {address[1]}")
    return data.decode("utf-8")

def update():
    w.update()
    img.initiate()
    img.write(w.getLoc() + " " + w.getTime(), 42, (10, 0))
    img.setImage("pilviä.png", (330,100))
    img.write(w.getWindSpd() + "m/s", 30, (410, 160))
    img.write(w.getTemp() + "°C", 100, (10, 150))
    screen.draw(img.getImg())

async_update = async_wrap(update)

async def refresh():
    print("updateloop")
    while 1:
        await async_update()

async def main_loop():
    global alarmOn
    alarmTime = time(0,0)
    command = ""
    while 1:
        if len(command) == 0:
            command = await UDPReceiver()
            print(command)
            params = command.split("-")

            if command == "alarm":
                try:
                    if (len(params) == 0):
                        raise TypeError("No time given")
                    alarmTime = time(params[:2], params[3:])
                    alarmOn = True
                except TypeError as e:
                    print("Incorrect time parameters: " + params)
                    print(e)

            if alarmOn and alarmTime < datetime.now().time():
                await alarm()

            command = ""

async def alarm():
    # todo: play alarm sound and turn on lights
    global alarmOn
    print("Alarm on")
    await getDist()
    alarmOn = False
    print("Alarm off")
    return

async def ledControl():
    while 1:
        if alarmOn and not leds.on:
            await leds.brighter()
        elif not alarmOn and leds.on:
            await leds.dim()
        else:
            await asyncio.sleep(1)

def main():
    loop = asyncio.get_event_loop()
    loop.create_task(ledControl())
    loop.create_task(main_loop())
    loop.create_task(refresh())
    loop.run_forever()

try:
    main()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    
finally:
    t.sleep(4)
    screen.clear()
    epd7in5.epdconfig.module_exit()
    exit()

