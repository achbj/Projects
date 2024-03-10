# import requests

# def query(payload, model_id, api_token):
# 	headers = {"Authorization": f"Bearer {api_token}"}
# 	API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()

# model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
# api_token = "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" # get yours at hf.co/settings/tokens
# data = query("Hello", model_id, api_token)
# print(data)

import requests
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
data = query({"inputs": "[INST] hello [/INST]"})
print(data)