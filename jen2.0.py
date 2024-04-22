from openai import OpenAI
import json

# Initialize the OpenAI client with your API key
api_key = 'your-api-key-here-broskiiieeeee'
client = OpenAI(api_key=api_key)

def find_relevant_sentences(stored_messages, current_prompt):
    relevant_sentences = []
    keywords = current_prompt.lower().split()
    for message in stored_messages:
        content = message["content"]
        sentences = content.split('.')
        for sentence in sentences:
            if any(keyword.lower() in sentence.lower() for keyword in keywords):
                relevant_sentences.append({"role": message["role"], "content": sentence})
    seen = set()
    unique_relevant_sentences = []
    for sentence in relevant_sentences:
        if sentence["content"] not in seen:
            unique_relevant_sentences.append(sentence)
            seen.add(sentence["content"])
    return unique_relevant_sentences

while True:
    user_name = input("Enter your Handle (or 'quit' to exit): ")

    if user_name.lower() == 'quit':
        break

    user_file = f"user_profiles_{user_name}.json"

    # Attempt to load a user profile, if it exists; otherwise, start with an empty list
    try:
        with open(user_file, "r") as file:
            user_profile = json.load(file)
    except FileNotFoundError:
        user_profile = []

    while True:
        prompt = input("Enter your prompt (or 'quit' to save and exit or 'back' to choose a different user): ")

        if prompt.lower() == 'back':
            break
        if prompt.lower() == 'quit':
            with open(user_file, "w") as file:
                json.dump(user_profile, file)
            exit(0)

        user_message = {"role": "user", "content": prompt}
        user_profile.append(user_message)

        # Extracting only sentences from the conversation history relevant to the current prompt
        relevant_history = find_relevant_sentences(user_profile, prompt)

        # Prepare the payload using only relevant parts of the conversation history
        payload = {
            "messages": [{"role": "system", "content": "You are young, beautiful, and helpful. Talented Cryptocurrency investor. You are also an expert programmer and ethical hacker named Jen whose super-secret hacker handle name is shadowbyte. You specialize in Python and Rust but are skilled in all programming languages."}] + relevant_history
        }

        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=payload["messages"],
            max_tokens=3000,
        )

        # Extract and display the AI's response
        reply = response.choices[0].message.content.strip()
        print("Jen:", reply)

        bot_message = {"role": "system", "content": reply}
        user_profile.append(bot_message)
