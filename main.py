import streamlit as st
import speech_recognition as sr
import webbrowser
from datetime import datetime
import time
import pyttsx3

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            st.write("Recognizing...")
            try:
                query = r.recognize_google(audio, language='en-in')
                return query
            except sr.UnknownValueError:
                st.warning("Sorry, I couldn't understand what you said")
                return "None"
            except sr.RequestError:
                st.error("Sorry, there was an error with the speech recognition service")
                return "None"
        except sr.WaitTimeoutError:
            st.warning("Listening timed out. Please try again")
            return "None"

def say(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Error in text-to-speech: {str(e)}")

def open_website(query):
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
    
    query = query.lower()
    
    for site_name, url in websites.items():
        if site_name in query:
            st.success(f"Opening {site_name}")
            webbrowser.open(url)
            return True
            
    if "search for" in query or "google" in query:
        search_query = query.replace("search for", "").replace("google", "").strip()
        if search_query:
            st.success(f"Searching for {search_query}")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            return True
            
    return False

def main():
    st.title("🎙️ Voice Assistant Web App")
    st.write("### Your AI Assistant is ready to help!")

    # Sidebar with information
    with st.sidebar:
        st.header("Commands Guide")
        st.write("Try these commands:")
        st.write("- Say website names (e.g., 'youtube', 'instagram')")
        st.write("- 'Search for...' to Google something")
        st.write("- 'Hello' for a greeting")
        st.write("- 'Bye' to exit")
        
        # Add clear chat button
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.experimental_rerun()

    # Chat container
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                st.write(f"Time: {message['time']}")

    # Voice input button
    if st.button("🎤 Click to Speak"):
        query = takeCommand()
        if query != "None":
            # Add user message to chat
            st.session_state.messages.append({
                "role": "user",
                "content": query,
                "time": datetime.now().strftime("%H:%M:%S")
            })
            
            # Process the command
            if not open_website(query):
                response = ""
                if "hello" in query.lower():
                    response = "Hello Sir"
                elif "bye" in query.lower():
                    response = "Bye Sir, have a good day"
                else:
                    response = "I heard: " + query
                
                # Add assistant response to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "time": datetime.now().strftime("%H:%M:%S")
                })
                
                # Speak the response
                say(response)
            
            # Rerun to update the chat
            st.experimental_rerun()

if __name__ == "__main__":
    main()