#importing libraries
import speech_recognition as sr
import pyttsx3
import pyjokes
import json
import wikipedia
import urllib.parse, urllib.request, urllib.error
from datetime import date
from datetime import datetime
from datetime import timedelta
import geocoder
import pywhatkit as py

#initializing the listener
listener = sr.Recognizer()
#initializing the endige for text to speech
engine = pyttsx3.init()
#Changing voices - voices[1] is female voice
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

#Function to speak text passed as argument
def speakFunc(text):
    engine.say(text)
    engine.runAndWait()

#Function to listen and return it into text
def listenFunc():
    #Surrounding in try catch if it is unable to listen
    try:
        #creating source from microphone
        with sr.Microphone() as source:
            #printing that it is listening
            print("listening")
            #listening the voice which is given as input
            voice = listener.listen(source)
            #converting it into text
            command = listener.recognize_google(voice)
            #converting it into lower case for filtering the command
            command = command.lower()
            #returning the command
            return command            
    except:
        pass


#Function to return true if user is exiting or saying bye
def exitFunc(text):
    #if any of these are in command said by user then return true
    if 'bye' in text or 'will talk later' in text or 'exit' in text:
        return True
    else:
        #else returning false
        return False

#Function to play songs on youtube
def playFunc(text):
    comm = text.split(' ')
    pos = comm.index('play')
    length = len(comm)
    if pos == (length-1):
        speakFunc("Which song would you like to Listen")
        song = str(listenFunc())
        py.playonyt(song)
    else:
        song = comm[pos+1:]
        py.playonyt(song)
            


#Function to filter the command and act accordingly
def determine(command):
    if 'play' in command:
        playFunc(command)
    elif 'weather' in command or 'whether' in command or 'temperature' in command:
        weatherFunc(command)
    elif 'news' in command:
        newsFunc(command)
    elif 'date' in command or 'time' in command or 'month' in command or 'year' in command:
        dateTime(command)


#Function to return data in json format
def returnJson(url):
    data = ""
    print(url)
    try:
        handle = urllib.request.urlopen(url)
        print("Retriving Data...")
        data = handle.read().decode()
    except:
        data = '{"cod":"404"}'
    jsonData = json.loads(data)
    return jsonData

#Function to return name of the month
def month(mon):
    if mon==1:
        mon='January'
    elif mon==2:
        mon='Feburary'
    elif mon==3:
        mon='March'
    elif mon==4:
        mon='April'
    elif mon==5:
        mon='May'
    elif mon==6:
        mon='June'
    elif mon==7:
        mon='July'
    elif mon==8:
        mon='August'
    elif mon==9:
        mon='September'
    elif mon==10:
        mon='October'
    elif mon==11:
        mon='November'
    elif mon==12:
        mon='December'
    return mon

#Function to tell date and time to the user
def dateTime(text):
    if 'yesterday' in text and 'date' in text:
        speakFunc("Yesterday5's date is "+str(date.today()- timedelta(days = 1)))
    elif 'date' in text and 'time' in text:
        speakFunc("Today's date is "+ str(date.today()))
        speakFunc("And current time is "+datetime.now().strftime("%H:%M %p"))
    elif 'date' in text:
        speakFunc("Today's date is "+str(date.today()))
    elif 'time' in text:
        speakFunc("Current time is "+datetime.now().strftime("%H:%M %p"))
    elif 'previous' in text and 'month' in text:
        mon = datetime.now().strftime("%m")
        mon = int(mon)-1
        speakFunc("Previous month was "+month(mon))
    elif 'month' in text:
        mon = int(datetime.now().strftime("%m"))
        speakFunc("Current month is "+month(mon))    
    elif 'year' in text:
        speakFunc("Current year is "+str(date.today().year))
        
#Function to tell weather or the temprature
def weatherFunc(text):
    apiKey = "67eeab22372620e2bc53dc7d22b36195"
    serviceurl = "https://api.openweathermap.org/data/2.5/weather?"
    split = text.split(' ')
    cityFound = 0
    cityname=""
    try:
        pos = split.index('weather')
    except:
        pos = split.index('temperature')
    if pos != (len(split)-1):
        if split[pos+1]=='in' or split[pos+1]=='of' :
            if len(split)!=(pos+1):
                cityname = split[pos+2]
                cityFound = 1
    if cityFound == 0:
       speakFunc("What is the name of the city?")
       cityname = listenFunc()
    while True:
        url = serviceurl + urllib.parse.urlencode({'q':cityname,'appid':apiKey})
        data = returnJson(url)
        if data['cod']!="404":
            temp = [data['main']['temp']-273.15,data['main']['humidity']]
            speak = "Current Temperature in "+cityname+" is nearly "
            if 'temperature' in split:
                speakFunc(speak+str(int(temp[0]))+" degree celcius.")
            else:
                speak2 = "and humidity is "+str(temp[1])+" percentage"
                speakFunc(speak+str(int(temp[0]))+" degree celcius "+speak2)
            break;
        else:
            speakFunc("City Not found...")
            speakFunc("What is the name of the city?")
            cityname = listenFunc()
            

#Function to tell news of specific category
def newsFunc(text):
    apiKey = "pub_8681e2997363e88e532a5ef2e9b4ac5b875c"
    serviceurl = "https://newsdata.io/api/1/news?"
    speakFunc("In which Language would you like to listen news?")
    lang = listenFunc()
    #lang=None
    if lang==None:
        lang='en'
    if 'english' in lang:
        lang = 'en'
    elif 'hindi' in lang:
        lang = 'hi'
    else:
        lang = 'en'
    speakFunc("What type of news would you like to hear?")
    speakFunc("Business News, Science News, Technology News, Sports News, World News?")
    cat = listenFunc()
    while True:
        catg = cat.split(' ')
        catg = catg[0]
        url = serviceurl + urllib.parse.urlencode({'apikey': apiKey,'country':'in','category': catg,'language':lang})  
        print(url)
        try:
            handle = urllib.request.urlopen(url)
            print("Retriving Data...")
            data = handle.read().decode()
        except:
            data = '{"status":"fail"}'
        jsonData = json.loads(data)
        if jsonData['status']=='success':
            allNews = jsonData['results']
            i = 0
            for news in allNews:
                title = news['title']
                print(title)
                if i <= 5:
                    speakFunc(title)
                    i = i + 1
                #description = news['description']
            break;
        else:
            speakFunc("Category Doesn't Exist")
            speakFunc("What type of news would you like to hear?")
            speakFunc("Science News, International News, Social News, Sports News?")
            cat = listenFunc()
                  
def mainFunc():
    speakFunc('Hello, Akshay here')
    dateTime('date and time')
    g = geocoder.ip('me')
    weatherFunc('temperature in '+g.city)
    speakFunc('How can I assist you?')    
    while True:
        comm = listenFunc()
        if comm==None:
            speakFunc("I didn't get it! Can you please repeat?")
            continue
        determine(comm)
        if exitFunc(comm):
            speakFunc('Okay Byee!, See you soon')
            break


mainFunc()












    
        














