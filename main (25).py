"""
Dev Voice Assistant — "Nova"
-----------------------------
Voice-controlled assistant for the AI Bootcamp. Opens dev tools, answers
common ML / NLP / CV / Generative AI questions, searches YouTube and
Google by voice, and chats a little.

Say things like:
  "open colab" / "open github" / "open code dot org" / "open vs code"
  "open chatgpt" / "open kaggle" / "open stack overflow"
  "search youtube for neural networks"
  "search google for transformers"
  "what is machine learning"
  "what is nlp"
  "what is computer vision"
  "what is generative ai"
  "tell me a joke"
  "stop" / "exit" (to quit)
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import random
import time
from colorama import init, Fore, Style

init(autoreset=True)

ASSISTANT_NAME = "Nova"
recognizer = sr.Recognizer()


# ---------- SPEAK (rebuilds the engine every call — fixes the "stops after one command" bug) ----------
def speak(text):
    print(Fore.CYAN + f"{ASSISTANT_NAME}: " + Style.RESET_ALL + text)
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(Fore.RED + f"(voice output failed: {e})" + Style.RESET_ALL)


def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print(Fore.YELLOW + "🎤 Listening..." + Style.RESET_ALL)
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio).lower()
        print(Fore.GREEN + f"You said: {text}" + Style.RESET_ALL)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("I can't reach the speech service right now. Check your internet connection.")
        return ""


def print_banner():
    banner = f"""
{Fore.MAGENTA}╔══════════════════════════════════════════╗
║        🚀  {ASSISTANT_NAME} — AI BOOTCAMP ASSISTANT  🚀        ║
╚══════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def type_effect(text, delay=0.02):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def time_based_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"


# ---------- CONTENT ----------
JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
    "Why do Java developers wear glasses? Because they don't see sharp.",
    "There are 10 types of people in the world: those who understand binary and those who don't.",
    "Why did the developer go broke? Because he used up all his cache.",
]

QUOTES = [
    "The best way to predict the future is to build it.",
    "Code is like humor. When you have to explain it, it's bad.",
    "First, solve the problem. Then, write the code.",
    "Talk is cheap. Show me the code.",
]

HOW_ARE_YOU_REPLIES = [
    "I'm running smoothly, thanks for asking! How about you?",
    "Feeling great, all systems online. What are we building today?",
    "Doing well! Ready to help whenever you are.",
]

COMPLIMENT_REPLIES = [
    "Aw, thank you! I try my best.",
    "That means a lot, coming from a human!",
    "You're pretty great yourself.",
]

CAPABILITIES_TEXT = (
    "I can open Colab, GitHub, code dot org, VS Code, ChatGPT, Kaggle, "
    "Stack Overflow, YouTube, and Google. I can search YouTube or Google "
    "for anything you ask. And I can answer questions about machine "
    "learning, NLP, computer vision, and generative AI from the bootcamp."
)

# AI Bootcamp knowledge base — keyword: spoken answer
# Order matters: more specific phrases are checked before general ones.
KNOWLEDGE_BASE = [
    ("generative ai", "Generative AI creates new content, like text, images, or code, "
                       "by learning patterns from huge amounts of existing data. "
                       "Tools like ChatGPT and Midjourney are examples."),
    ("prompt engineering", "Prompt engineering is the skill of writing clear, well "
                            "structured instructions so an AI model gives you the best "
                            "possible response."),
    ("computer vision", "Computer vision is the field of AI that lets computers understand "
                         "and interpret images and video, like detecting faces or objects."),
    ("natural language processing", "Natural Language Processing, or NLP, is how computers "
                                     "understand, interpret, and generate human language, like text and speech."),
    ("nlp", "NLP stands for Natural Language Processing. It's how computers understand "
            "and work with human language, like text and speech."),
    ("neural network", "A neural network is a model inspired by the human brain, made of "
                        "layers of connected nodes that learn patterns from data."),
    ("deep learning", "Deep learning is a type of machine learning that uses neural "
                       "networks with many layers to learn complex patterns from large amounts of data."),
    ("overfitting", "Overfitting is when a model learns the training data too well, "
                     "including its noise, so it performs poorly on new, unseen data."),
    ("difference between ai and ml", "AI is the broad idea of machines being smart. "
                                      "Machine learning is one way to achieve that, by letting "
                                      "computers learn patterns from data instead of being explicitly programmed."),
    ("what is ai", "AI, or artificial intelligence, is the field of building machines that "
                   "can perform tasks that normally require human intelligence."),
    ("machine learning", "Machine learning is a part of AI where computers learn patterns "
                          "from data and improve their performance without being explicitly programmed."),
    ("chatbot", "A chatbot is a program that can hold a conversation with a person, "
                "usually using NLP to understand and respond to text or voice input."),
    ("agentic ai", "Agentic AI refers to AI systems that can take actions and make "
                    "decisions on their own to complete multi-step tasks, not just answer questions."),
]


def check_knowledge_base(command):
    for keyword, answer in KNOWLEDGE_BASE:
        if keyword in command:
            return answer
    return None


# ---------- COMMAND HANDLING ----------
def handle_command(command):
    if not command:
        return True  # nothing heard, keep looping

    # --- Search commands (checked first so they don't get caught by generic "google"/"youtube") ---
    if "search youtube for" in command or "youtube search for" in command:
        query = command.split("for", 1)[1].strip()
        speak(f"Searching YouTube for {query}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
        return True

    if "search google for" in command or "google search for" in command or ("google" in command and "search" in command):
        query = command
        for phrase in ["search google for", "google search for", "search google", "google search"]:
            query = query.replace(phrase, "")
        query = query.strip()
        if query:
            speak(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        else:
            speak("What would you like me to search for?")
        return True

    # --- Dev tools ---
    if "colab" in command:
        speak("Opening Google Colab. Let's write some code!")
        webbrowser.open("https://colab.research.google.com")
        return True

    if "github" in command:
        speak("Opening GitHub.")
        webbrowser.open("https://github.com")
        return True

    if "code.org" in command or "code dot org" in command or "codeorg" in command:
        speak("Opening code dot org.")
        webbrowser.open("https://code.org")
        return True

    if "vs code" in command or "visual studio code" in command:
        speak("Opening VS Code.")
        try:
            os.system("code .")
        except Exception:
            speak("I couldn't launch VS Code directly. Make sure the 'code' command is in your PATH.")
        return True

    if "chatgpt" in command or "chat gpt" in command:
        speak("Opening ChatGPT.")
        webbrowser.open("https://chat.openai.com")
        return True

    if "kaggle" in command:
        speak("Opening Kaggle.")
        webbrowser.open("https://www.kaggle.com")
        return True

    if "stack overflow" in command or "stackoverflow" in command:
        speak("Opening Stack Overflow.")
        webbrowser.open("https://stackoverflow.com")
        return True

    if "youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")
        return True

    if "google" in command:
        speak("Opening Google.")
        webbrowser.open("https://google.com")
        return True

    # --- Bootcamp knowledge base ---
    kb_answer = check_knowledge_base(command)
    if kb_answer:
        speak(kb_answer)
        return True

    # --- Conversation / chit-chat ---
    if "how are you" in command:
        speak(random.choice(HOW_ARE_YOU_REPLIES))
        return True

    if "good job" in command or "well done" in command or "you're smart" in command:
        speak(random.choice(COMPLIMENT_REPLIES))
        return True

    if "what can you do" in command or command.strip() == "help":
        speak(CAPABILITIES_TEXT)
        return True

    if "hello" in command or command.strip() in ("hi", "hey"):
        speak(f"Hello! {time_based_greeting()}. What would you like to do?")
        return True

    # --- Fun / utility ---
    if "joke" in command:
        speak(random.choice(JOKES))
        return True

    if "quote" in command or "motivate" in command:
        speak(random.choice(QUOTES))
        return True

    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"It's {now}")
        return True

    if "date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {today}")
        return True

    if "your name" in command:
        speak(f"I'm {ASSISTANT_NAME}, your AI Bootcamp assistant.")
        return True

    if "thank you" in command or "thanks" in command:
        speak("Anytime! That's what I'm here for.")
        return True

    if "stop" in command or "exit" in command or "quit" in command:
        speak("Shutting down. Happy coding!")
        return False

    speak("I didn't catch a command I know. Say 'what can you do' to hear my full list.")
    return True


# ---------- MAIN LOOP ----------
def main():
    print_banner()
    greeting = time_based_greeting()
    type_effect(f"{greeting}! I'm {ASSISTANT_NAME}, your AI Bootcamp assistant.", delay=0.015)
    speak(f"{greeting}! I'm {ASSISTANT_NAME}. Say a command whenever you're ready.")

    running = True
    while running:
        try:
            command = listen()
            running = handle_command(command)
        except KeyboardInterrupt:
            speak("Goodbye!")
            break
        except Exception as e:
            # Catch-all so one bad response never kills the whole assistant
            print(Fore.RED + f"(error: {e}) — still listening, try again." + Style.RESET_ALL)
            continue


if __name__ == "__main__":
    main()
