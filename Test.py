import speech_recognition as sr
import pyttsx3
from datetime import datetime

def initialize_text_to_speech():
    try:
        engine = pyttsx3.init()
        return engine
    except Exception as e:
        print(f"Error initializing text-to-speech engine: {e}")
        return None

def speak_text(engine, text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening... Speak something.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def handle_unrecognized_command(engine):
    response = "I'm sorry, I didn't understand that. Can you please repeat?"
    speak_text(engine, response)
    print(f"AI: {response}")

def get_current_time():
    current_time = datetime.now().strftime("%H:%M")
    return f"The current time is {current_time}."

def get_current_date():
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"Today is {current_date}."

def respond_to_conversation():
    responses = [
        "I'm doing well, thank you!",
        "How can I assist you today?",
        "Tell me more about what's on your mind.",
    ]
    return responses

def process_request(engine, request):
    if "hello" in request:
        response = "Hi there! How can I help you?"
    elif "time" in request:
        response = get_current_time()
    elif "date" in request:
        response = get_current_date()
    elif "conversation" in request:
        response = respond_to_conversation()
    elif "your specific command" in request:
        # Add your specific command logic here
        response = "You triggered a specific command!"
    else:
        handle_unrecognized_command(engine)
        return

    speak_text(engine, response)
    print(f"AI: {response}")

def main():
    text_to_speech_engine = initialize_text_to_speech()

    if text_to_speech_engine:
        while True:
            user_request = recognize_speech()

            if user_request:
                if "exit" in user_request:
                    speak_text(text_to_speech_engine, "Exiting. Goodbye!")
                    print("Exiting...")
                    break
                else:
                    process_request(text_to_speech_engine, user_request)

if __name__ == "__main__":
    main()
