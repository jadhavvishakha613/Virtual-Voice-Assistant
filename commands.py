
import re
import urllib.parse


class CommandRouter:
    """Maps natural-language commands to assistant actions."""

    def __init__(self, assistant):
        self.assistant = assistant

    def handle(self, command: str) -> bool:
        command = command.lower().strip()

        # Exit
        if any(x in command for x in [
            "exit", "quit", "stop assistant", "goodbye", "shut down assistant"
        ]):
            self.assistant.running = False
            return True

        # Help
        if command in {"help", "what can you do", "commands"}:
            self.help()
            return True

        # Greeting
        if any(x in command for x in [
            "hello", "hi assistant", "hey assistant"
        ]):
            self.assistant.speak("Hello. How can I help you?")
            return True

        # Time/date
        if "time" in command:
            self.assistant.tell_time()
            return True

        if "date" in command or "today" in command:
            self.assistant.tell_date()
            return True

        # Applications
        for app in ("notepad", "calculator", "paint"):
            if f"open {app}" in command or f"launch {app}" in command:
                self.assistant.open_application(app)
                return True

        # Websites
        sites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "gmail": "https://mail.google.com",
            "github": "https://github.com",
        }

        for name, url in sites.items():
            if f"open {name}" in command:
                self.assistant.open_url(url)
                self.assistant.speak(f"Opening {name}")
                return True

        # Search
        search_match = re.search(
            r"(?:search for|search|google)\s+(.+)", command
        )

        if search_match:
            query = search_match.group(1).strip()

            if query:
                self.assistant.search_web(query)
                return True

        # System information
        if (
            "system information" in command
            or "computer information" in command
        ):
            self.assistant.system_info()
            return True

        # Python
        if "what is python" in command or command == "python":
            self.assistant.speak(
                "Python is a popular programming language used for "
                "web development, automation, data science, and "
                "artificial intelligence."
            )
            return True

        # Unknown command
        self.assistant.speak(
            "I am still learning how to answer that."
        )
        return True

    def help(self):
        commands = [
            "say hello",
            "tell me the time",
            "tell me today's date",
            "open notepad",
            "open calculator",
            "open paint",
            "open YouTube",
            "open Google",
            "open Gmail",
            "search for Python tutorials",
            "tell me system information",
            "what is Python",
            "exit",
        ]

        print("\nAvailable commands:")

        for item in commands:
            print(f"  - {item}")

        self.assistant.speak(
            "I can open applications and websites, search the web, "
            "tell you the time and date, provide system information, "
            "and answer some basic questions."
        )

