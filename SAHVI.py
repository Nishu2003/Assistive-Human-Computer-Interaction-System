import speech_recognition as sr
import pyttsx3
import random
import datetime
import os

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[0].id')


def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print("....")
        query = r.recognize_google(audio, language='en-in')
    except Exception as e:
        print(e)
        speak("Try to say again")
        return "None"
    return query


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        a = "Good morning Guys", "Good morning", "Hello Guys Good Morning", "Oh, Good morning Friends", "Oh, good morning Budies", "Wow! Welcome back"
        speak(random.choice(a))
    elif hour >= 12 and hour < 17:
        b = "Good Afternoon Guys", "Good Afternoon", "Hello Guys Good Afternoon", "Oh, Good Afternoon Friends ", "Oh, good Afternoon Budies  ", "Wow! Welcome back"
        speak(random.choice(b))
    else:
        c = "Good Evening Guys", "Good Evening", "Hello Guys Good Evening", "Oh, Good Evening Friends", "Oh, Good Evening Budies", "Wow! Welcome back"
        speak(random.choice(c))


def main():

    speak("Make your choice")

    while True:
        query = takeCommand().lower()
        print(query)

        if 'play the volume controller' in query or 'the volume controller' in query or 'volume controller' in query or 'volume' in query:
         os.system('python aivolumecontroller.py')
         break

        elif 'play the mouse controller' in query or 'the mouse controller' in query or 'mouse controller' in query or 'mouse' in query:
           os.system('python aiVirtualMouse.py')
           break

        elif 'play the car game' in query or 'the car game' in query or 'car game' in query or 'game' in query:
           os.system('python steering.py')
           break

        elif 'play the calculator' in query or 'the calculator' in query or 'calculator' in query:
           os.system('python HandTracking_Calc.py')
           break

        elif 'play the painter' in query or 'the painter' in query or 'painter' in query:
           os.system('python aivirtual_painter.py')
           break

        elif 'close' in query or 'exit'in query:
            f = "Bye user", "Bye bye user","As your wish user","Waiting for activation user", "As your wish, but I don't want to go user!"
            speak(random.choice(f))
            break

        elif 'play the eye control' in query or 'eye control' in query or 'i control' in query:
           os.system('python eye_gaze.py')
           break

    

if __name__ == '__main__':
    wishMe()
    wel = "You can say either close or exit to close the application"
    wel1 = "Welcome to Artificial intelligence Virtual System. This is the hand tracking VR interface in which you can do some real tasks by interacting virtually with the system. Like you can controls the volume of the system by AI virtual volume controller or you can control pc's mouse with AI virtual mouse controller or AI car racing game and many more. So, from which one you want to start with. Before we start i'll provide you some instructions on how to fully use these features. Let's get started...Virtual volume controller To increase or decrease system's volume, increase or decrease distance between index fingertip and thumb fingertip respectively. Virtual mouse controller Our index fingertip acts as a replacement for mouse cursor. You can move around your index fingertip to move the cursor. To select any particular icon just click your index fingertip and middle fingertip over that icon. Virtual game controller Imagine you've a steering wheel in front of you and hold it, the direction you turn your hands in will be the direction your car moves in. To use brakes show your left palm. To move your car in reverse show your hand closed.  And to accelerate show both palms open like hurray. Virtual calculatorYou can see the calculator on right side of your screen. To select any number or sign just click your index fingertip or middle fingertip over it.  Virtual paint Sometimes you feel like drawing in air right? Let us help you with that. To use this feature, all you need to do is move you index finger in air as you wish to draw. To choose any other colour or feature click your index and middle fingertip. And to erase an error you made in drawing just slide the image on top of the error after selecting the eraser. "
    #speak((wel1))
    speak((wel))
    main()