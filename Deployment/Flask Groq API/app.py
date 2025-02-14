from flask import Flask, render_template, request, jsonify
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Get Groq API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Langchain conversation chain and memory
model_name = 'llama3-70b-8192'  # You can change the model if needed
conversational_memory_length = 5  # Set the length of conversational memory
memory = ConversationBufferWindowMemory(k=conversational_memory_length)
groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name=model_name)
conversation = ConversationChain(llm=groq_chat, memory=memory)

# Route for the chat page
@app.route('/')
def chat():
    return render_template('index.html')

# Route for handling user queries
@app.route('/query', methods=['POST'])
def query():
    user_input = request.form['user_input']
    
    # If the user has asked a question,
    if user_input:
        # The chatbot's answer is generated by sending the full prompt to the Groq API.
        response = conversation(user_input)  # Generating response from the conversation object
        # Save the conversation context to memory
        memory.save_context({'input': user_input}, {'output': response['response']})
        response_with_code_snippet = "AI: " + "```\n" + response['response'] + "\n```"
        return jsonify({'response': response_with_code_snippet})
    else:
        return jsonify({'response': ''})

if __name__ == '__main__':
    app.run(debug=True)
