import sys
import time
import webbrowser
import smtplib
import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import psutil
from pyjokes import pyjokes
from requests import get
import wikipedia
import pywhatkit
import pyautogui
import instaloader
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from frontend import Ui_AthenaUI
from pywikihow import search_wikihow

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        speak("Good Morning")
    elif hour>=12 and hour<16:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("Iam Athena sir. Please tell me how may i help you")

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('mrbeasthindishorts0@gmail.com', 'wtgbldvnpzfllvit')
    server.sendmail('mrbeasthindishorts0@gmail.com', to, content)
    server.close()


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def takeCommand(self):
        r=sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=5, phrase_time_limit=5)

            try:
                print("Recognizing...")
                self.query = r.recognize_google(audio, language='en-in')
                print(f"User said: {self.query}\n")

            except Exception as e:
                print("Say that again please...")
                return "None"
            return self.query

    def TaskExecution(self):
        wish()
        # takeCommand()
        # speak("This is Athena")
        while True:
            self.query = self.takeCommand().lower()
            # For Task
            if "notepad" in self.query:
                npath = "C:\\Windows\\notepad.exe"
                os.startfile(npath)

            elif "command prompt" in self.query:
                os.system("start cmd")

            elif "camera" in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, frame = cap.read()
                    cv2.imshow('webcam', frame)
                    key = cv2.waitKey(50)
                    if key == 27:
                        break;
                cap.release()
                cv2.destroyAllWindows()

            elif "youtube" in self.query:
                speak("What would you like to do?, Senore")
                cmd = self.takeCommand().lower()
                pywhatkit.playonyt(cmd)

            elif "open google" in self.query:
                speak("What to search?, Senore")
                cm = self.takeCommand().lower()
                webbrowser.open(f"https://www.google.com/search?q={cm}")

            elif "ip address" in self.query:
                ip = get('https://api.ipify.org').text
                speak("Ip address is {}".format(ip))

            elif "wikipedia" in self.query:
                speak("Searching in Wikipedia...")
                self.query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(self.query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
                print(results)

            elif "send message" in self.query:
                speak("what to send?, Senore")
                cmd = self.takeCommand().lower()
                pywhatkit.sendwhatmsg("+918431660608", cmd,14,27 )

            elif "send email" in self.query:
                try:
                    speak("What would you like to send?, Sir")
                    content = self.takeCommand().lower()
                    to = "reetubichali@gmail.com"
                    sendEmail(to, content)
                    speak("Email has been sent")

                except Exception as e:
                    print(e)
                    speak("Sorry, I am not able to send this email")

            elif "no thanks" in self.query:
                speak("Thanks for using Athena, Let me know if you have any work")
                break

            elif "close all" in self.query:
                speak("As you order, Senore")
                os.system("taskkill /f /im notepad.exe")
                os.system("taskkill /f /im webcam.exe")
                os.system("taskkill /f /im youtube.com")
                os.system("taskkill /f /im wiki.com")
                os.system("taskkill /f /im cmd.exe")
                os.system("taskkill /f /im google.com")

            elif "tell me a joke" in self.query:
                joke = pyjokes.get_joke(language="en")
                speak(joke)

            elif "shutdown" in self.query:
                os.system("shutdown /s /t 5")

            elif "restart" in self.query:
                os.system("shutdown /r /t 5")

            elif "switch window" in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            # # elif "where am i" in query:
            #     speak("wait senore, let me check")
            #     try:
            #         ipAdd = requests.get("https://api.ipify.org").text
            #         print(ipAdd)
            #         url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
            #         geo_request = requests.get(url)
            #         geo_data = geo_request.json()
            #         city = geo_data['city']
            #         country = geo_data['country']
            #         speak(f"You are in {city} city, of {country} country")
            #     except Exception as e:
            #         speak("Sorry, Iam unable to fetch location")
            #         pass

            elif "instagram" in self.query:
                speak("Please enter correct username")
                name = input("Enter username: ")
                webbrowser.open("https://www.instagram.com/"+name)
                speak("here is an instagram username")
                time.sleep(5)
                speak("sir would like to download the profile picture")
                condition = self.takeCommand().lower()
                if "yes" in condition:
                    mod = instaloader.Instaloader()
                    mod.download_profile(name, profile_pic_only=True)
                    speak("I am done sir, Profile picture is saved successfully")
                else:
                    pass

            elif "take screenshot" in self.query:
                speak("Please provide name for screenshot")
                name = self.takeCommand().lower()
                speak("Hold the screen for few seconds senore, im taking screenshot")
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("screenshot has been saved successfully")

            # elif "temperature" in self.query:

            #     search = self.query
            #     url = f"https://www.google.com/search?q={search}"
            #     r = requests.get(url)
            #     data = BeautifulSoup(r.text, "html.parser")
            #     temp = data.find("div", class_ = "BNeawe iBp4i AP7Wnd").text
            #     speak(f"current {search} is {temp}")

            # elif "temperature" in self.query:
            #     try:
            #         # Mimic a browser request
            #         headers = {
            #             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            #         }
            #         search = self.query
            #         url = f"https://www.google.com/search?q={search}"
            #         r = requests.get(url, headers=headers)
                    
            #         # Parse the response
            #         data = BeautifulSoup(r.text, "html.parser")
            #         temp_element = data.find("div", class_="BNeawe iBp4i AP7Wnd").text  # Updated class
                    
            #         if temp_element:
            #             temp = temp_element.text
            #             speak(f"The current {search} is {temp}")
            #         else:
            #             speak("Sorry, I couldn't fetch the temperature.")
            #     except Exception as e:
            #         speak(f"An error occurred: {e}")



            elif "activate chatbot" in self.query:
                speak("Chatbot is activated, please let me know what to do now")
                how = self.takeCommand()
                max_results = 1
                how_to = search_wikihow(how, max_results)
                assert len(how_to) == 1
                how_to[0].print() and how_to[0].speak()
                speak(how_to[0].summary)

            elif "battery" in self.query:
                battery = psutil.sensors_battery()
                percentage = battery.percent
                speak(f"Sir, our system has {percentage}percent of battery")
                
            elif "normal message" in self.query:
                speak("what should i send sir")
                msz = self.takeCommand()
                from twilio.rest import Client

                account_sid = 'AC9701fbbf176971f2b3a3389a0f837b8b'
                auth_token = '5f5173e0e0febc7d54536ec316b29371'

                client = Client(account_sid, auth_token)
                message = client.messages \
                    .create(
                        body=msz,
                        from_='+17405204862',
                        to='+919035531011'
                    )
                print(message.sid)
                speak("Sir, message has been sent successfully")

            elif "make a call" in self.query:
                from twilio.rest import Client
                speak("making a call")
                account_sid = 'AC9701fbbf176971f2b3a3389a0f837b8b'
                auth_token = '5f5173e0e0febc7d54536ec316b29371'

                client = Client(account_sid, auth_token)
                message = client.calls \
                    .create(
                        twiml='<Response><Say>Good afternoon sir, This is testing call from Poject Athena.. Hope you have a good day.Thank you</Say></Response>',
                        from_='+17405204862',
                        to='+919035531011'
                    )
                print(message.sid)

            speak("Sir, Do you have any other work")
        
        if __name__ == "__main__":
            while True:
                permission = self.takeCommand()
                if "wake up" in permission:
                        wish()
                elif "goodbye" in permission:
                    speak("Signing Off Sir")
                    sys.exit()    
    

startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AthenaUI()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)


    def startTask(self):
        self.ui.movie = QtGui.QMovie("../Optimus/siri.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        # timer = QTimer(self)
        # timer.timeout.connect(self.showTime)
        # time.start(5000)
        startExecution.start()

    # def showTime(self):
    #     ct = QTime.currentTime()
    #     label_time = ct.toString('hh:mm:ss')
    #     self.ui.textBrowser.setText(label_time)

app = QApplication(sys.argv)
athena = Main()
athena.show()
exit(app.exec_())