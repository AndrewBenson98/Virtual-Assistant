"""
IDEAS
-Say something motivating
-What should i eat for (breakfast/lunch/dinner)
-Set a timer
-Tell me a joke
-Google something----
-Language translation
-Check the weather
-Greeting --------
-Open youtube video
-Time-----
-Play music------

"""

import random
import requests
import sys
import os
import datetime
import speech_recognition as sr
import pyttsx3
import pyaudio
import webbrowser
import urllib
from pygame import mixer
from googlesearch import search


# Set up the text to speech
engine = pyttsx3.init()
voices = engine.getProperty("voices")
# Set the voice you want
engine.setProperty("voice", voices[len(voices) - 1].id)

# Set the speed at wich the engine speaks
rate = engine.getProperty("rate")
# Slows down the speaking speed of the engine voice.
engine.setProperty("rate", rate - 62)

cmd = sr.Recognizer()

name = "Navi"

"""
@param audio - the string of text you want the engine to say
"""


def speak(audio):
    # Print the text to the console
    print(name + ": " + audio)
    engine.say(audio)
    engine.runAndWait()


"""
Converts speech to texts to recieve a command
"""


def command():
    # Initialize the speech recognition object

    with sr.Microphone() as source:
        # Adjusts the level to recieve voice even in case of noise in surroundings
        # cmd.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = cmd.listen(source)
        query = ""

        try:
            # Turns speech into text
            query = cmd.recognize_google(audio, language="en-us")
            query = query.lower()
        except sr.UnknownValueError:
            pass

    return query


def test():
    speak("This is a test")


def greeting():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak("Good Morning")
    if currentH >= 12 and currentH < 17:
        speak("Good Afternoon")
    if currentH >= 17 and currentH != 0:
        speak("Good Evening")


def googleSearch(query, resultsList):

    for result in search(query, tld="co.in", num=10, stop=5, pause=2):
        print(result)
        resultsList.append(result)
    speak("Here are the top five results")
    return resultsList


def openLink(result):
    webbrowser.open(result)


"""
Plays a random song from a folder
"""


def playMusic(type):
    folder = "D:\\Users\\Andrew\\Documents\\Projects\\Desktop Assistant\Music\\"
    musicList = os.listdir(folder)
    mixer.init()
    mixer.music.set_volume(0.30)
    if type == "random":
        randomSong = folder + random.choice(musicList)
        mixer.music.load(randomSong)
        mixer.music.play()
    elif type == "baka":
        song = folder + "baka_mitai.mp3"
        mixer.music.load(song)
        mixer.music.play()
    return


def sheesh():
    speak("sheeeeeesh")


def getTime():
    currentTime = datetime.datetime.now()
    currentTime = currentTime.strftime("%H:%M:%S")
    timeArray = currentTime.split(":")

    hour = timeArray[0]
    minute = timeArray[1]
    meridiem = "AM"

    # Check if it is AM or PM
    if int(hour) > 12:
        hour = int(hour) - 12
        meridiem = "PM"
    speak("It is " + str(hour) + " : " + minute + " " + meridiem)
    return

def openFile(file):
    try:
        os.startfile(file)
        speak("Here is your file")
    except:
        speak("File cannot be found")




speak(name + " here.")
greeting()


if __name__ == "__main__":
    while True:
        query = command()
        query = query.lower()

        if name.lower() in query:

            if mixer.get_init() != None:
                print("Mixer is active")
                if mixer.get_num_channels() == 0:
                    print("qutting mixer")
                    mixer.quit()
                else:
                    print("setting mixer volume")
                    mixer.music.set_volume(0.05)

            speak("What can I help you with?")
            query = command()
            query = query.lower()
            print("User: " + query)

            if "test" in query:
                test()

            if "search" in query or "google" in query:

                speak("What would you like to search for?")
                query = command()
                resultsList = []
                googleSearch(query, resultsList)
                speak("Would you like me to open the first link?")
                query = command()
                if "yes" in query or "sure" in query or "open" in query:
                    speak("Opening the first link")
                    openLink(resultsList[0])
                else:
                    speak("Alright")

            if ("stop" in query and "music" in query) or (
                "stop" in query and "song" in query
            ):
                mixer.music.stop()
                mixer.quit()
                speak("The music has stopped")

            if ("song" in query or "music" in query) and "play" in query:
                speak("Here is your song")
                playMusic("random")

            if "baka" in query:
                sheesh()
                speak("Here we go again")
                speak("Playing Baka Mitai")
                playMusic("baka")

            if "sheesh" in query or "can i get a" in query:
                sheesh()

            if "time" in query:
                getTime()

            if 'to-do list' in query or 'todo list' in query:
                openFile("C:\\Users\\andre\\Desktop\\Fall 2020 Todo List.xlsx")

            # Tell Navi to stop listening and exit
            if (
                "stop listening" in query
                or "nevermind" in query
                or "that is all" in query
                or "do the thing" in query
            ):
                speak("Goodbye")
                sys.exit()

            if mixer.get_init() != None:
                mixer.music.set_volume(0.30)
        """
        #Quit mixer if no song is playing        
        if mixer.get_init() != None:
                #print('Mixer is active')
                #print('Active Channels: '+str(mixer.get_num_channels()))
                if mixer.get_num_channels() == 0:
                    print('Qutting mixer')
                    mixer.quit()
        """
