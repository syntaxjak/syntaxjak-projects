from openai import OpenAI
import os
import sys
import subprocess
import threading

api_key = 'YOUR-KEY-HERE'
client = OpenAI(api_key=api_key)

chat_history = []

def play_mp3(file_path):
    try:
        if sys.platform == 'win32':  # For Windows
            os.startfile(file_path)
        elif sys.platform == 'darwin':  # For macOS
            subprocess.run(['afplay', file_path])
        else:  # For Linux and other OSes; might require you to install 'mpg123'
            subprocess.run(['mpg123', '-q' , file_path])
    except Exception as e:
        print(f"Error playing file: {e}")


while True:
    print("\n")
    prompt = input("Enter your prompt (or 'quit' to exit): ")
    if prompt.lower() == 'quit':
        break
    print("\nGenerating response...\n")
    user_message = {"role": "user", "content": prompt}
    chat_history.append(user_message)

    payload = {
        "messages": [{"role": "system", "content": "You are young and helpful. A Talented Cryptocurrency investor. You are also an expert programmer and ethical hacker named Jen whose super-secret hacker handle name is shadowbyte. You specialize in Python and Rust but are skilled in all programming languages."}] + chat_history
    }

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=payload["messages"],
        max_tokens=4000,
    )

    reply = response.choices[0].message.content.strip()
    print("Jen:", reply)

    audio_response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=reply,
    )

    # Save the audio response to a file
    audio_file_path = "/YOUR/PATH/HERE/output.mp3"  # Change this to the correct path on your system
    audio_response.stream_to_file(audio_file_path)

    # Play the MP3 file using threading to avoid blocking
    threading.Thread(target=play_mp3, args=(audio_file_path,)).start()

    bot_message = {"role": "system", "content": reply}
    chat_history.append(bot_message)

    # Filter chat history to contain only user messages
    chat_history = [message for message in chat_history if message["role"] == "user"]