import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

filename = "messages_history\\messages.txt"

messages = [
    {"role": "system", "content": "You are a helpful assistant. Avoid all emojis entirely—respond using only standard text characters."}
]

with open(filename) as file:
    for index, line in enumerate(file):
        if index % 2 == 0:
            messages.append({"role": "user", "content": line[0:-1]})
        else:
            messages.append({"role": "assistant", "content": line[0:-1]})


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)



print("AI Chatbot started! Type 'quit' to stop.")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["quit", "exit"]:
        print("Chat ended.")
        with open(filename, "w") as file:
            messages.pop(0)
            for conversation in messages:
                file.write(conversation["content"] + "\n")
        break

    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=messages
        )

        reply = response.choices[0].message.content
        print("AI:", reply)

        messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        print("Error:", e)