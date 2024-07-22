import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')

if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
# else:
#     engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()
    time.sleep(6)

def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'vedu' in command:
                command = command.replace('vedu', '')
                return command
    except sr.UnknownValueError:
        talk("Sorry, I did not understand that.")
        time.sleep(6)
    except sr.RequestError:
        talk("Sorry, my speech service is down.")
    except Exception as e:
        print(f"Error: {e}")
    return ""

def run_vedu():
    command = take_command()
    if command:
        print(command)
        if 'play' in command:
            song = command.replace('play', '')
            talk('playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            talk('Current time is ' + current_time)
        elif 'tell me about' in command:
            person = command.replace('tell me about', '')
            info = wikipedia.summary(person, sentences=5)
            print(info)
            talk(info)
        elif 'will you come on a date with me' in command:
            talk('sorry, I am not interested in dating any human')
        elif 'are you single' in command:
            talk('yes')
        elif 'tell me a joke' in command:
            talk(pyjokes.get_joke())
        elif 'stop' in command or 'exit' in command:
            talk('Goodbye')
            return False
        else:
            talk('Please say the command again.')
    else:
        print("No command detected.")
    return True

while True:
    if not run_vedu():
        break
