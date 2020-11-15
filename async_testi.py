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
import time
import traceback
import asyncio
from functools import wraps, partial
from aioudp import *

logging.basicConfig(level=logging.DEBUG)
logging.info("e-Paper testausta")

w = W.weatherData()
sensors = S.sensors()
#screen = Screen()
#img = ImageCreator()

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

#async def count():
#    x = 0
#    while x < 1000:
#        logging.info(x)
#        await asyncio.sleep(0.1)
#        x += 1
#    return

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

#def update():
#    w.update()
#    img.initiate()
#    img.write(w.getLoc() + " " + w.getTime(), 42, (10, 0))
#    img.setImage("pilviä.png", (330,100))
#    img.write(w.getWindSpd() + "m/s", 30, (410, 160))
#    img.write(w.getTemp() + "°C", 100, (10, 150))
#    screen.draw(img.getImg())

#async_update = async_wrap(update)
loop = asyncio.get_event_loop()

async def updateLoop():
    command = ""
    while 1:
        ##await async_update()
        print("--")
        if len(command) == 0:
            print(".")
            command = await UDPReceiver()
            ###todo
            print(command)
            command = ""


def main():
    d = loop.create_task(getDist())
    loop.create_task(updateLoop())
    loop.run_until_complete(d)

try:
    main()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    
finally:
    time.sleep(4)
    #screen.clear()
    epd7in5.epdconfig.module_exit()
    exit()

