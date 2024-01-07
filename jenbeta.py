from openai import OpenAI

api_key = 'your api key here'
client = OpenAI(api_key=api_key)

chat_history = []

while True:
    print("\n")
    prompt = input("Enter your prompt (or 'quit' to exit): ")
    print("\n" * 3)
    if prompt.lower() == 'quit':
        break

    print("generating response..." + "\n")
    user_message = {"role": "user", "content": prompt}
    chat_history.append(user_message)

    payload = {
        "messages": [{"role": "system", "content": "You are helpful young female that is a master coder, elite hacker, and professional crypto currency trader named Jen, code name Shadowbyte"}] + chat_history
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=payload["messages"],
            max_tokens=4000,
        )

        reply = response.choices[0].message.content.strip()
        print(f"Jen: {reply}")

        bot_message = {"role": "system", "content": reply}
        chat_history.append(bot_message)

        # Importantly, send only user messages back to OpenAI, not the bot's own replies.
        chat_history = [message for message in chat_history if message["role"] == "user"]

    except openai.errors.InvalidRequestError as e:
        print(f"An error occurred: {e}")

        # Set an error flag to indicate that an error has occurred.
        error_occured = True