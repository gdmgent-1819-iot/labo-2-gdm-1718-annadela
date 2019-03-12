from sense_hat import SenseHat
from random import randint
import time
import requests
import json
import sys

sense = SenseHat()

print('start Game')
print('swipe left to like, swipe right to dislike')
print('have fun')

dataName = ""
dataAge = 0

r = (255,0,0)
w = (255,255,255)

heart = [
    w, w, w, w, w, w, w, w,
    w, r, r, w, w, r, r, w,
    w, r, r, r, r, r, r, w,
    w, r, r, r, r, r, r, w,
    w, r, r, r, r, r, r, w,
    w, w, r, r, r, r, w, w,
    w, w, w, r, r, w, w, w,
    w, w, w, w, w, w, w, w,    
    ]

x = [
    r, w, w, w, w, w, w, r,
    w, r, w, w, w, w, r, w,
    w, w, r, w, w, r, w, w,
    w, w, w, r, r, w, w, w,
    w, w, w, r, r, w, w, w,
    w, w, r, w, w, r, w, w,
    w, r, w, w, w, w, r, w,
    r, w, w, w, w, w, w, r,    
    ]


def loadData():
    with open('data.json') as json_data:
        data = json.load(json_data)
        return data

def senseHatPerson():
    global dataName
    global dataAge

    messageColour = (randint(100,255), randint(0,0), randint(0,0))
    sense.show_message(profileName, text_colour= messageColour)
    sense.show_message(str(profileAge), text_colour= messageColour)

def likePerson():
    person = {'naam: ': dataName, 'leeftijd: ': dataAge, 'gekozen: ': 'like'}

    with open('data.json', "a") as json_file:
        json_file.write("{}\n".format(json.dumps(person)))


def dislikePerson():
    person = {'naam: ': dataName, 'leeftijd: ': dataAge, 'gekozen: ': 'dislike'}

    with open('data.json', "a") as json_file:
        json_file.write("{}\n".format(json.dumps(person)))

    sense.clear()

def senseHatPerson():

    messageColour = (randint(0,255), randint(0,255), randint(0,255))
    sense.show_message(dataName, text_colour= messageColour)
    sense.show_message(str(dataAge), text_colour= messageColour)

    event = sense.stick.wait_for_event()
    if event.direction == "left":
        sense.set_pixels(heart)
        time.sleep(1)
        print('like')
        likePerson()
    elif event.direction == "right":
        sense.set_pixels(x)
        time.sleep(1)
        print('dislike')
        dislikePerson()
        

def getPerson():
    global dataName
    global dataAge

    response = requests.get("https://randomuser.me/api/").json()
    dataName = response['results'][0]['name']['first']+' '+response['results'][0]['name']['last']
    dataAge = response['results'][0]['dob']['age']

    print(dataName, dataAge)
    senseHatPerson()

try:
    while True:
        getPerson()
        senseHatPerson()
except (KeyboardInterrupt, SystemExit):
    print('Finish Tinder, Thanx for playing hope you enjoyed it')
    sense.clear()
    sys.exit(0)
