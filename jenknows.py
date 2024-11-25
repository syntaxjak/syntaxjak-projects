from openai import OpenAI
import json
import os
from colorama import Fore, Style, init
from sentence_transformers import SentenceTransformer, util
import time

# Initialize Colorama (for Windows compatibility)
init(autoreset=True)

# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Small and efficient model

# Function to get the OpenAI API key
def get_api_key():
    api_key_file = 'api_key.json'
    if os.path.exists(api_key_file):
        with open(api_key_file, 'r') as file:
            data = json.load(file)
        return data['api_key']
    else:
        api_key = input("Enter your OpenAI API key: ")
        with open(api_key_file, 'w') as file:
            json.dump({'api_key': api_key}, file)
        return api_key

# Get the API key
api_key = get_api_key()

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# ANSI escape codes for colored output
PURPLE = "\033[95m"
WHITE = "\033[97m"
BRIGHT_GREEN = "\033[92m"
RESET = "\033[0m"
BRIGHT_RED = "\033[91m"
BRIGHT_BLUE = "\033[94m"
GREEN = "\033[32m"

# Function to find relevant messages using semantic similarity
def find_relevant_messages_semantic(stored_messages, current_prompt, max_messages=10, min_score=0.5):
    # Encode the current prompt
    prompt_embedding = model.encode(current_prompt, convert_to_tensor=True)
    
    # Collect all message contents
    messages_content = [msg['content'] for msg in stored_messages]
    
    if not messages_content:
        return []
    
    # Encode all messages at once (batch processing for efficiency)
    message_embeddings = model.encode(messages_content, convert_to_tensor=True)
    
    # Compute cosine similarities between the prompt and all messages
    cosine_scores = util.pytorch_cos_sim(prompt_embedding, message_embeddings)[0]
    
    message_scores = []
    for idx, score in enumerate(cosine_scores):
        score_value = score.item()
        if score_value >= min_score:
            message_scores.append((score_value, idx, stored_messages[idx]))
    
    # If no messages meet the minimum score, return an empty list
    if not message_scores:
        return []
    
    # Sort messages by score in descending order
    message_scores.sort(reverse=True, key=lambda x: (x[0], -x[1]))
    
    # Extract messages, up to max_messages
    relevant_messages = [message for score, idx, message in message_scores[:max_messages]]
    
    # Sort relevant messages by their original order
    relevant_messages.sort(key=lambda msg: stored_messages.index(msg))
    
    return relevant_messages

# Main Program Loop
while True:
    print(f"{GREEN}Handle: {RESET}", end="")
    user_name = input().strip()
    if user_name.lower() == 'q':
        break
    user_file = f"user_profiles_{user_name}.json"
    # Attempt to load a user profile, if it exists; otherwise, start with an empty list
    try:
        with open(user_file, "r") as file:
            user_profile = json.load(file)
    except FileNotFoundError:
        user_profile = []
    
    while True:
        print(f"{BRIGHT_RED}Query... ('b'ack or 'q'uit): {RESET}", end="")
        prompt = input(f"{BRIGHT_BLUE}").strip()
        if prompt.lower() == 'b':
            break
        if prompt.lower() == 'q':
            exit(0)
        user_message = {"role": "user", "content": prompt}
        user_profile.append(user_message)
        
        # Start timing the relevance search
        #start_time = time.time()
        
        # Extracting only messages from the conversation history relevant to the current prompt
        # Exclude the last message (current user message) from the stored messages
        relevant_history = find_relevant_messages_semantic(
            user_profile[:-1],
            prompt,
            max_messages=10,
            min_score=0.5  # Adjust the minimum similarity score as needed
        )
        
        # End timing
        #end_time = time.time()
        #print(f"Relevance search time: {end_time - start_time:.2f} seconds")
        
        # Prepare the payload using only relevant parts of the conversation history
        payload_messages = relevant_history + [user_message]
        
        try:
            # Call the OpenAI API
            response = client.chat.completions.create(
                model="o1-preview",
                messages=payload_messages,
                # max_tokens=3000,  # Omit or adjust as needed
            )
            # Extract and display the assistant's response
            assistant_response = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"{BRIGHT_RED}An error occurred: {e}{RESET}")
            # Remove the last user message in case of error
            user_profile.pop()
            continue
        
        print(" ")
        print(f"{PURPLE}Jen{WHITE}:{BRIGHT_GREEN} {assistant_response}{RESET}")
        print(" ")
        bot_message = {"role": "assistant", "content": assistant_response}
        user_profile.append(bot_message)
        # Save to file after each response
        with open(user_file, "w") as file:
            json.dump(user_profile, file, indent=4)
