import os
import pyttsx3
import speech_recognition as sr
import subprocess

# Initialize voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# Optional: Set voice
voices = engine.getProperty('voices')
for voice in voices:
    if "zira" in voice.name.lower():
        engine.setProperty('voice', voice.id)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't get that.")
        return ""
    except sr.RequestError:
        speak("Speech recognition failed.")
        return ""

def activate_environment():
    # Path to your virtual environment's activate.bat
    env_path = r"W:\cvd_risk_webapp\cvd\Scripts\activate.bat"
    speak("Activating your environment now.")
    subprocess.Popen(["start", "cmd", "/k", env_path], shell=True)

# === MAIN LOOP ===
while True:
    command = listen()
    if "jarvis" in command and "turn on" in command and "environment" in command:
        activate_environment()
        break
    elif "exit" in command or "quit" in command:
        speak("Goodbye.")
        break
