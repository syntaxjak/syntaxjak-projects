import os
from openai import OpenAI

# Replace with your actual API key
api_key = 'YOUR KEY HERE'
client = OpenAI(api_key=api_key)

while True:  # Start of the loop
    try:
        # Ask the user for input text
        prompt = input("Please type what you want me to speak (or 'quit' to exit): ")

        # Check if the user wants to exit the loop
        if prompt.lower() == 'quit':
            break

        # Generate speech from the text
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=prompt
        )

        # Define the path for the output audio file
        audio_file_path = "output.mp3"

        # Save the audio stream to the specified file
        response.stream_to_file(audio_file_path)

        # Print a message indicating that the file has been saved
        print(f"Speech has been generated and saved to {audio_file_path}")

        # Play the audio file using the default media player on Windows
        os.system(f"mpg123 -q {audio_file_path}")

    except KeyboardInterrupt:
        # Handle any interrupt such as CTRL+C gracefully
        break

# Print a message indicating that the script is exiting
print("Exiting the program.")