from openai import OpenAI
import json

api_key = 'YOUR API KEY HERE BOYEEEEEEEEEE'
client = OpenAI(api_key=api_key)

while True:
    user_name = input("Enter your Handle (or 'quit' to exit): ")

    if user_name.lower() == 'quit':
        break  # Exit the loop if the user enters 'quit'

    user_file = f"user_profiles_{user_name}.json"

    try:
        with open(user_file, "r") as file:
            user_profile = json.load(file)
    except FileNotFoundError:
        user_profile = []

    while True:
        prompt = input("Enter your prompt (or 'quit' to save and exit or 'back' to choose a different user): ")

        if prompt.lower() == 'back':
            break  # Go back to choosing a different user

        if prompt.lower() == 'quit':
            # Save user profile and exit the program if the user enters 'quit'
            with open(user_file, "w") as file:
                json.dump(user_profile, file)
            exit(0)

        user_message = {"role": "user", "content": prompt}
        user_profile.append(user_message)

        payload = {
            "messages": [{"role": "system", "content": "You are young, beautiful, and helpful. Talented Cryptocurrency investor. You are also an expert programmer and ethical hacker named Jen whose super-secret hacker handle name is shadowbyte. You specialize in Python and Rust but are skilled in all programming languages."}] + user_profile
        }

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=payload["messages"],
            max_tokens=3000,
        )

        reply = response.choices[0].message.content.strip()
        print("Jen:", reply)

        bot_message = {"role": "system", "content": reply}
        user_profile.append(bot_message)
