from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def ask_openrouter(user_input):
    api_key = os.getenv("OPENROUTER_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost:5000",  # or your deployed domain
        "X-Title": "CarAdvisorMCP",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",  # You can change to mistralai/mistral-7b-instruct etc.
        "messages": [
            {"role": "system", "content": "You are a car expert helping users choose cars based on their needs."},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        user_input = request.form["question"]
        answer = ask_openrouter(user_input)
    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
