from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)


import requests
API_TOKEN = "you-huggingface-api-access-token"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

@app.route('/')
def index():
    # Render the chat interface template
    return render_template('chat.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    headers = {
        "Authorization": f"Bearer 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"
    }
    payload = {
        "inputs": '[INST]' + user_message + '[/INST]',
        # "inputs": user_message
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        full_response = response.json()[0]['generated_text']
        chat_response = full_response.split("[/INST]")[-1].strip()

        return jsonify({"reply": chat_response})
    else:
        return jsonify({"error": "Could not fetch response from the model"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
