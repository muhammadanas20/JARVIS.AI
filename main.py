from win32com.client import Dispatch
import speech_recognition as sr
import webbrowser

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            try:
                query = r.recognize_google(audio, language='en-in')
                print(f"User said: {query}")
                return query
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand what you said")
                return "None"
            except sr.RequestError:
                print("Sorry, there was an error with the speech recognition service")
                return "None"
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again")
            return "None"

def say(text):
    try:
        speaker = Dispatch("SAPI.SpVoice")
        speaker.Speak(text)
    except Exception as e:
        print(f"Error in text-to-speech: {str(e)}")

def open_website(query):
    # Dictionary of websites with their URLs
    websites = {
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "twitter": "https://twitter.com",
        "x": "https://twitter.com",
        "discord": "https://discord.com",
        "github": "https://github.com",
        "linkedin": "https://www.linkedin.com",
        "reddit": "https://www.reddit.com",
        "amazon": "https://www.amazon.com",
        "netflix": "https://www.netflix.com",
        "spotify": "https://www.spotify.com",
        "twitch": "https://www.twitch.tv",
        "pinterest": "https://www.pinterest.com",
        "whatsapp": "https://web.whatsapp.com",
        "gmail": "https://mail.google.com",
        "google": "https://www.google.com",
        "maps": "https://www.google.com/maps",
        "drive": "https://drive.google.com",
        "meet": "https://meet.google.com",
        "classroom": "https://classroom.google.com",
        "wikipedia": "https://www.wikipedia.org"
    }
    
    # Convert query to lowercase for better matching
    query = query.lower()
    
    # Check if any website name is mentioned in the query
    for site_name, url in websites.items():
        if site_name in query:
            say(f"Opening {site_name}")
            webbrowser.open(url)
            return True
            
    # If no specific website is found but user wants to search something
    if "search for" in query or "google" in query:
        search_query = query.replace("search for", "").replace("google", "").strip()
        if search_query:
            say(f"Searching for {search_query}")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            return True
            
    return False

if __name__ == '__main__':
    print("PyCharm")
    say("Hello, I am JARVIS AI")
    while True:
        query = takeCommand()
        if query == "None":
            continue
            
        # Try to open website if mentioned in query
        if not open_website(query):
            # Handle other commands if no website was opened
            if "hello" in query.lower():
                say("Hello Sir")
            elif "bye" in query.lower():
                say("Bye Sir, have a good day")
                break
            else:
                say(query)