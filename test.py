import nxt
import nxt.locator
from nxt.sensor import *
import sys
import time
import urllib
import pickle
import random
import numpy as np
from policy import Policy
from msvcrt import *
from PIL import Image

#some boilerplate code adapted from https://github.com/iqbalmohomed/selfdrivingrobot

def initBrick():
    global b
    global right
    global left
    b = nxt.find_one_brick()
    right = nxt.Motor(b, nxt.PORT_C)
    left = nxt.Motor(b, nxt.PORT_B)

def download_image(theurl):
    urllib.urlretrieve(theurl)

def take_pic():
    res = urllib.urlretrieve('http://192.168.0.24:8080/photo.jpg')
    im = Image.open(res[0])
    gray = im.resize((300,150))
    gray = gray.convert('L')
    gray = gray.rotate(180)
    f = np.array(gray, dtype=np.uint8)
    gray.show()
    return f

def getColor():
    Light(b, PORT_2).set_illuminated(True)
    s = Light(b, PORT_2).get_sample()
    Light(b, PORT_2).set_illuminated(False)
    if s > 50:
        return 1
    else:
        return 0

def forward():
    return 0
    right.run(power=65)
    left.run(power=65)

def stop():
    right.run(power=0)
    left.run(power=0)

def turn(amount):
    #return 0
    amount /= 300.0
    if amount < 0:
        right.turn(power=int(65-40*amount), tacho_units=180)
        #left.turn(power=0, tacho_units=180)
    if amount > 0:
        #right.turn(power=0, tacho_units=180)
        left.turn(power=int(65+40*amount), tacho_units=180)

def randomAction():
    return (np.random.randn() - 0.5)

def step(action):
    turn(action)
    time.sleep(0.05)
    ss = take_pic()
    color = getColor()
    r = 0
    if color == 1:
        r = 1000
    else:
        r = -100
    return ss, r

initBrick()
num_reps = 1000
timesteps = 3
e = 0.5
PG = Policy()
rewards = []
totalSteps = 0
if True:
    PG.model.load_weights('modelweights_700.h5')
    e = 0.01

s = take_pic()
print PG.getAction(s)
turn(PG.getAction(s))