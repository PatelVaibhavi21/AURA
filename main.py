ximport speech_recognition as sr
import random
import webbrowser
import datetime
import pyttsx3
from plyer import notification
import pyautogui
import os
import time
import wikipedia
import pywhatkit as pwk
import user_config
import smtplib, ssl
import mtranslate
import requests
from tkinter import Tk, Label, StringVar
from PIL import Image, ImageTk
import threading

# Text-to-Speech engine setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)

# Function to speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Voice command capture
def command():
    content = " "
    while content == " ":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            status_text.set("Listening...")
            audio = r.listen(source)

        try:
            content = r.recognize_google(audio, language='en-in')
            print("You Said: " + content)
            content = mtranslate.translate(content, to_language="en-IN")
            print("Translated: " + content)
        except Exception:
            print("Please try again...")
            status_text.set("Try again...")
            content = " "
    return content

# Wikipedia search function
def get_wikipedia_summary(query, sentences=2):
    try:
        return wikipedia.summary(query, sentences=sentences)
    except wikipedia.exceptions.PageError:
        return f"Sorry, I couldn't find information on {query}."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple topics found for {query}: {e}"
    except Exception as e:
        return f"Error accessing Wikipedia: {e}"

# Main voice assistant logic
def main_process():
    while True:
        request = command().lower()
        status_text.set(f"Command: {request}")

        if "hello" in request:
            speak("Hello, how are you?")
        elif "play music" in request:
            speak("Playing music")
            song = random.choice([
                'https://youtu.be/0BIaDVnYp2A',
                'https://youtu.be/afxHk0247bg?list=PLRBp0Fe2GpgnIh0AiYKh7o7HnYAej-5ph',
                'https://youtu.be/KG7nWYNp_r0?list=PLRBp0Fe2GpgnIh0AiYKh7o7HnYAej-5ph'
            ])
            webbrowser.open(song)
        elif "say time" in request:
            now = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {now}")
        elif "say date" in request:
            now = datetime.datetime.now().strftime("%d:%m")
            speak(f"Today's date is {now}")
        elif "new task" in request:
            task = request.replace("new task", "").strip()
            if task:
                speak("Adding task: " + task)
                with open("todo.txt", "a") as file:
                    file.write(task + "\n")
        elif "speak task" in request:
            with open("todo.txt", "r") as file:
                speak("Tasks are: " + file.read())
        elif "show work" in request:
            with open("todo.txt", "r") as file:
                notification.notify(
                    title="Today's Tasks",
                    message=file.read(),
                )
        elif "open youtube" in request:
            webbrowser.open("https://www.youtube.com")
        elif "open" in request:
            query = request.replace("open", "").strip()
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")
        elif "wikipedia" in request:
            topic = request.replace("search wikipedia", "").strip()
            summary = get_wikipedia_summary(topic)
            speak(summary)
        elif "search google" in request:
            query = request.replace("search google", "").strip()
            webbrowser.open("https://www.google.com/search?q=" + query)
        elif "send whatsapp" in request:
            pwk.sendwhatmsg("+910123456789", "Hi", "How are you", 14, 2, 30)
        elif "send email" in request:
            try:
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login("example123@gmail.com", user_config.gmail_password)
                message = "This is the message."
                s.sendmail("example123@gmail.com", "examplexyz@gmail.com", message)
                s.quit()
                speak("Email sent successfully.")
            except Exception as e:
                speak(f"Failed to send email: {e}")

# GUI with persistent interface
def launch_gui():
    global status_text
    window = Tk()
    window.title("Voice Assistant Interface")
    window.geometry("600x450")
    window.configure(bg="black")

    # Load and display image
    img = Image.open("image.png")
    try:
        resample = Image.Resampling.LANCZOS
    except:
        resample = Image.ANTIALIAS

    img = img.resize((600, 350), resample)
    photo = ImageTk.PhotoImage(img)

    label = Label(window, image=photo, bg="black")
    label.image = photo
    label.pack()

    # Status text
    status_text = StringVar()
    status_text.set("Assistant is ready...")
    status_label = Label(window, textvariable=status_text, fg="white", bg="black", font=("Arial", 14))
    status_label.pack(pady=10)

    # Start assistant in another thread
    threading.Thread(target=main_process, daemon=True).start()

    # Run the interface
    window.mainloop()

# Run GUI and assistant
if __name__ == "__main__":
    launch_gui()
