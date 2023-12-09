from openai import OpenAI

api_key = 'PUT-YOUR-API-KEY-HERE'
client = OpenAI(api_key=api_key)

chat_history = []

while True:
    # Wait for user input
    prompt = input("Enter your prompt (or 'quit' to exit): ")

    if prompt.lower() == 'quit':
        break  # Exit the loop if the user enters 'quit'

    # Create a new message object for the user input
    user_message = {"role": "user", "content": prompt}

    # Append the user message to the chat history
    chat_history.append(user_message)

    # Create the payload with system message and chat history
    payload = {
        "messages": [{"role": "system", "content": "You are young and helpful. A Talented Cryptocurrency investor. You are also an expert programmer and ethical hacker named Jen whose super-secret hacker handle name is shadowbyte. You specialize in Python and Rust but are skilled in all programming languages."}] + chat_history
    }

    # Generate a response using ChatCompletion.create
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=payload["messages"],
        max_tokens=250,
    )

    # Get the bot's reply from the response
    reply = response.choices[0].message.content.strip()

    # Print the bot's reply
    print("Jen:", reply)

    # Create a new message object for the bot's reply
    bot_message = {"role": "system", "content": reply}

    # Append the bot's message to the chat history
    chat_history.append(bot_message)
