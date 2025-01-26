import json

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

app = Flask(__name__)

with open("C:/Users/Anand/OneDrive/Desktop/WCE_WORKSHOP/day_2/eduChatbot/backend/qna.json", "r") as file:
    qna_data = json.load(file)

print("Loaded Q&A data:", qna_data)


AZURE_ENDPOINT = "https://educationchatbot07.cognitiveservices.azure.com/"
AZURE_KEY = "BTlMt2SJbrSoIdTd8JkoWHQFA0VGUFBgj7XAjdwdFvmStq9Fk1LXJQQJ99BAACYeBjFXJ3w3AAAaACOGjU3x"

def get_answer(user_input):
    for qa in qna_data["questions_and_answers"]:
        if user_input.lower() in qa["question"].lower():
            return qa["answer"]
    return "Sorry, I don't have an answer for that. Can you rephrase your question?"


def analyze_feedback(feedback):
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "documents": [{"id": "1", "language": "en", "text": feedback}]
    }
    url = f"{AZURE_ENDPOINT}text/analytics/v3.1/sentiment"
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        result = response.json()
        sentiment = result["documents"][0]["sentiment"]
        return f"Your feedback has been analyzed. Sentiment detected: {sentiment.capitalize()}."
    else:
        return "Failed to analyze feedback. Please try again later."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    if "feedback" in user_input.lower():
        return jsonify({"response": analyze_feedback(user_input)})

    answer = get_answer(user_input)
    if answer:
        return jsonify({"response": answer})
    return jsonify({"response": "Sorry, I don't have an answer for that. Can you rephrase your question?"})

if __name__ == "__main__":
    app.run(debug=True)
