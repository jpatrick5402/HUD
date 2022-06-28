import os
import threading
from http.client import PROXY_AUTHENTICATION_REQUIRED
from typing import final
#pip install requests
import requests
#pip install geopy
from geopy.geocoders import Nominatim
#pip install geocoder
import geocoder

from datetime import datetime
#pip install tk
import tkinter as tk
#pip install opencv-python
import cv2

import json
#pip install vosk

#pip install sounddevice
import sounddevice as sd
#pip install scipy
from scipy.io.wavfile import write
#pip install SpeechRecognition
import speech_recognition as sr
#pip install pipwin          :        Only Necessary if on testing on windows platform
#pipwin install pyaudio
import pyaudio
#pipwin install pocketsphinx

#pip install beautifulsoup4
from bs4 import BeautifulSoup

import urllib.request

import time

def checkWifi():
    url = "https://google.com"
    timeout = 4
    try:
        requests.get(url, timeout=timeout)
        return True
    except:
        return False

def getLocation():
    if checkWifi():
        return geocoder.ip("me").city
    else:
        print("Note: No WiFi Connection. Using Last Known Location...")
        configs = json.load(open("./HUD/PriorConfigs.json", "r"))
        return configs["LastKnownLoc"]

def getLatLon(Location):
    if checkWifi():
        # calling the Nominatim tool
        loc = Nominatim(user_agent="GetLoc")
        # entering the location name
        getLoc = loc.geocode(Location)
        # printing address
        #print(getLoc.address)
        # printing latitude and longitude
        #print("Latitude = ", getLoc.latitude, "\n")
        #print("Longitude = ", getLoc.longitude)
        return getLoc.latitude, getLoc.longitude
    else:
        print("Note: No WiFi Connection. Using Last Known Latitude and Longitude...")
        configs = json.load(open("./HUD/PriorConfigs.json", "r"))
        return configs["LastKnownLatLon"]

def getWeather(City, Breif=False):
    #! I want to work on this because it could be neater
    if Breif:
        return requests.get(f"https://wttr.in/{City}").text
    else:  
        return requests.get(f"https://wttr.in/{City}").text

def getSpeed():
    pass

def toggleDayMode(Light):
    if Light == "Day":
        os.system("color 70")
    elif Light == "Night":
        os.system("color 07")

def STT(show=False):
    fs = 44100  # Sample rate
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        audio = rec.listen(source)
        #write(f'./HUD/Recordings/Saved_STT_{str(datetime.now()).replace(":", ".")}.wav', fs, audio)
        try:
            if checkWifi():
                words = rec.recognize_google(audio)
            else:
                words = rec.recognize_sphinx(audio)
        except:
            print("Can't recognize speech")
            return "0"
        if show:
            print("---" + words)
    return words

def saveAudio(seconds, write=False):
    fs = 44100  # Sample rate
    print(f"Listening for {seconds} seconds")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    if write:
        words = STT(show=True)
    else:
        words = STT(show=False)
    sd.wait()  # Wait until recording is finished
    write(f'./HUD/Recordings/Saved_Audio_{str(datetime.now()).replace(":", ".")}.wav', fs, myrecording)  # Save as WAV file
    return words

def callback(recognizer, audio):
    print(recognizer.recognize_sphinx(audio))

def listenForSpeech():
    r = sr.Recognizer()
    m = sr.Microphone()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)      
    stop_listening = r.listen_in_background(m, callback)
    stop_listening()



def Save():
    print("Saving Configs")
    Loc = getLocation()
    LatLon = getLatLon(Loc)
    data = {
        "LastKnownLoc" : Loc,
        "LastKnownLatLon" : LatLon,
        "PreviousTimeAtClose" : str(datetime.now())
    }
    
    with open("./HUD/PriorConfigs.json", "w") as f:
        json.dump(data, f)

def checkKeyword(Key):
    words = STT(show=True)
    if "show" in words:
        if "weather" in words:
            print(getWeather(getLocation()))
        if "latitude" in words or "longitude" in words:
            print(getLatLon(getLocation()))

def mainLoop(Name):
    while True:
        words = STT(show=True)
        if words[0:len(Name)].lower() == Name:
            checkKeyword(words)

def main():
    deviceName = input("Name Your Device: ")
    print("Good Morning Sir")
    print("It is currently: " + str(datetime.now()))

    mainLoop(deviceName)
    
    Save() #last line of main()





if __name__ == "__main__":
    main()