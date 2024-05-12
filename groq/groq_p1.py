import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# GROQ_API_KEY = os.getenv('GROQ_API_KEY')

client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
    # api_key=os.environ.get(),

)
user_in = input('enter query: ')

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": user_in,
        }
    ],
    model="llama3-70b-8192",
)
print(chat_completion.choices[0].message.content)