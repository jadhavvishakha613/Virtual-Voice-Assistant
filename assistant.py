import datetime
import os
import platform
import subprocess
import webbrowser
from pathlib import Path

import pyttsx3

from voice import VoiceInput
from commands import CommandRouter


class VoiceAssistant:
    """Voice-controlled desktop assistant."""

    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)
        self.engine.setProperty("volume", 1.0)

        self.voice = VoiceInput()
        self.router = CommandRouter(self)

        self.running = True

    def speak(self, text: str):
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self) -> str:
        return self.voice.listen()

    def open_url(self, url: str):
        webbrowser.open(url)

    def search_web(self, query: str):
        url = "https://www.google.com/search?q=" + query.replace(" ", "+")
        self.open_url(url)
        self.speak(f"Searching the web for {query}")

    def open_application(self, app_name: str):
        system = platform.system()

        commands = {
            "notepad": ["notepad.exe"],
            "calculator": ["calc.exe"],
            "paint": ["mspaint.exe"],
        }

        if app_name not in commands:
            self.speak(f"I do not have a launcher configured for {app_name}")
            return

        try:
            if system == "Windows":
                subprocess.Popen(commands[app_name])
            else:
                self.speak("This application launcher is currently configured for Windows.")
                return
            self.speak(f"Opening {app_name}")
        except Exception as exc:
            self.speak(f"I could not open {app_name}.")
            print(f"Error: {exc}")

    def tell_time(self):
        current = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The time is {current}")

    def tell_date(self):
        current = datetime.datetime.now().strftime("%A, %d %B %Y")
        self.speak(f"Today is {current}")

    def system_info(self):
        self.speak(
            f"You are using {platform.system()} {platform.release()} "
            f"on a {platform.machine()} machine."
        )

    def run(self):
        self.speak("Virtual voice assistant started. How can I help you?")
        print("\nSay 'help' for available commands or 'exit' to quit.\n")

        while self.running:
            command = self.listen()

            if not command:
                continue

            try:
                handled = self.router.handle(command)
                if not handled:
                    self.speak(
                        "I did not recognize that command. "
                        "Say help to see what I can do."
                    )
            except KeyboardInterrupt:
                self.running = False
            except Exception as exc:
                print(f"Unexpected error: {exc}")
                self.speak("Something went wrong while processing that command.")

        self.speak("Goodbye.")
