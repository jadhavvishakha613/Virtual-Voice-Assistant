import speech_recognition as sr


class VoiceInput:
    """Speech-to-text using SpeechRecognition."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    def listen(self) -> str:
        try:
            with sr.Microphone() as source:
                print("Listening...")

                audio = self.recognizer.listen(
                    source,
                    timeout=6,
                    phrase_time_limit=10,
                )

            print("Recognizing...")
            text = self.recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text.lower().strip()

        except sr.WaitTimeoutError:
            print("No speech detected.")
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as exc:
            print(f"Speech recognition service error: {exc}")
        except OSError as exc:
            print(f"Microphone/audio error: {exc}")

        return ""