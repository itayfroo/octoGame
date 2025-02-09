import json
import socket
import time
import pyttsx3
from gtts import gTTS
import io
import pygame
import threading
import tkinter as tk
from PIL import Image, ImageTk
import pythoncom
import sys
root = tk.Tk()
root.title("TTS Animation")

# Load and keep images in memory.
img1 = ImageTk.PhotoImage(Image.open("octo.png"))  # Replace with your actual image path.
img2 = ImageTk.PhotoImage(Image.open("open_mouth.png"))
label = tk.Label(root, image=img1)
label.pack()

# Create an entry widget for user input.
user_input_var = tk.StringVar()
text_box = tk.Entry(root, textvariable=user_input_var, width=40)
text_box.pack()

# We’ll use a threading.Event to signal that input is ready.
input_event = threading.Event()
# Global variable to hold the input string.
input_value = ""

def pyttsx3_tts(text, voice_index, speaking):
    """Function for TTS using pyttsx3"""
    pythoncom.CoInitialize()  # Initialize COM in the new thread
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
    engine.setProperty('rate', 250)
    engine.say(text)
    engine.runAndWait()
    speaking[0] = False  # Stop the animation

def gtts_tts(text, lang, speaking):
    """Function for TTS using gTTS"""
    tts = gTTS(text=text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp, 'mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    speaking[0] = False  # Stop the animation
def speak(label, img1, img2, text,lang):
    """Convenience wrapper to start the TTS and image animation."""
    goofy_tts(text, label, img1, img2,lang, voice_index=0)

def start_gui(text,lang='en'):
    speak(label, img1, img2, text,lang)
def goofy_tts(text, label, img1, img2, lang="en", voice_index=0, use_gtts=False):
    """Start animation and TTS in separate threads."""
    speaking = [True]
    threading.Thread(target=animate_images, args=(label, img1, img2, speaking), daemon=True).start()
    if use_gtts:
        threading.Thread(target=gtts_tts, args=(text, lang, speaking), daemon=True).start()
    else:
        threading.Thread(target=pyttsx3_tts, args=(text, voice_index, speaking), daemon=True).start()