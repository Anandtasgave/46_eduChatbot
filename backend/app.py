from flask import Flask, request, jsonify # type: ignore
import json
import requests

app = Flask(__name__)

# Load Q&A data
with open("qna.json", "r") as file:
    qna_data = json.load(file)

# Azure Text Analytics Configuration
AZURE_ENDPOINT = "https://<your-text-analytics-resource>.cognitiveservices.azure.com/"
AZURE_KEY = "<your-azure-key>"

def get_answer(user_input):
    # Check for matching question in Q&A
    for qa in qna_data["questions_and_answers"]:
        if user_input.lower() in qa["question"].lower():
            return qa["answer"]
    return None

def analyze_feedback(feedback):
    # Analyze feedback using Azure Text Analytics
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

    # Check for feedback keyword
    if "feedback" in user_input.lower():
        return jsonify({"response": analyze_feedback(user_input)})

    # Get answer from Q&A
    answer = get_answer(user_input)
    if answer:
        return jsonify({"response": answer})
    return jsonify({"response": "Sorry, I don't have an answer for that. Can you rephrase your question?"})

if __name__ == "__main__":
    app.run(debug=True)
