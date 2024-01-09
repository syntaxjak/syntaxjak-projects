import sys
from openai import OpenAI

def main(question):
    api_key = 'your-openai-keys-here'
    client = OpenAI(api_key=api_key)

    payload = {
        "messages": [
            {"role": "system", "content": "You are helpful young female that is a master coder, elite hacker, and professional cryptocurrency trader named Jen who goes by the handle Shadowbyte"},
            {"role": "user", "content": question}
        ]
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=payload["messages"],
            max_tokens=4000,
        )

        reply = response.choices[0].message.content.strip()
        print(f"Jen: {reply}")
    except errors.InvalidRequestError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fastjen.py \"Your question here\"")
        sys.exit(1)
    
    question = ' '.join(sys.argv[1:])
    main(question)
