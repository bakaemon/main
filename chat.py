import requests, openai
import json
from dotenv import load_dotenv
from datetime import date
import os





class ChatGPT:
    content = []

    def __init__(self, model="gpt-3.5-turbo", default_prompt=""):
        load_dotenv()
        openAIKey = os.getenv('OPENAPI')
        openai.api_key = openAIKey
        self.model = model
    
    def add_content(self, content, role):
        self.content.append({"role": role, "content": content})

    def chat(self, message):
        messages = self.content
        messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.content
        )
        content = response.choices[0]['message']["content"]
        self.add_content(content, "assistant")
        return content
    
    def save_history(self, history_file):
        with open(history_file, "w") as f:
            json.dump(self.content, f)
    
    def load_history(self, history_file):
        with open(history_file, "r") as f:
            self.content = json.load(f)

    
    



