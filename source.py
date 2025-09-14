import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random
import speech_recognition as sr

# Initialize the speech recognition and text-to-speech engines
engine = pyttsx3.init()
listener = sr.Recognizer()

# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to set the voice (optional, but good for personalization)
def set_voice():
    voices = engine.getProperty('voices')
    # You can change the index to use a different voice
    # Index 0 is often a male voice, 1 is a female voice
    engine.setProperty('voice', voices[0].id)

# Function to greet the user
def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    
    speak("I am your voice assistant. How may I help you?")

# Function to take voice commands
def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            # Adjust for ambient noise
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            command = listener.recognize_google(voice, language='en-US')
            print(f"User said: {command}")
            return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

# Main function to process commands
def run_jarvis():
    set_voice()
    wish_me()
    while True:
        command = take_command()
        if not command:
            continue

        if "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")

        elif "wikipedia" in command:
            speak("Searching Wikipedia...")
            query = command.replace("wikipedia", "").strip()
            try:
                # Set number of sentences for summary
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia, " + result)
            except wikipedia.exceptions.PageError:
                speak("Sorry, I could not find that on Wikipedia.")
            except wikipedia.exceptions.DisambiguationError as e:
                speak("Please be more specific. Your search may refer to one of the following:")
                speak(", ".join(e.options[:5]))
        
        elif "open youtube" in command:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")
        
        elif "open google" in command:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")

        elif "play music" in command:
            music_dir = 'C:\\Users\\YourUser\\Music' # Change this to your music directory
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, random.choice(songs)))
                speak("Playing a random song.")
            else:
                speak("Sorry, I couldn't find any music files.")
        
        elif "hello" in command:
            speak("Hello there!")
        
        elif "how are you" in command:
            speak("I'm fine, thank you for asking!")

        elif "exit" in command or "bye" in command or "stop" in command:
            speak("Goodbye!")
            break

# Run the assistant
if __name__ == "__main__":
    run_jarvis()
