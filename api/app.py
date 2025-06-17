from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load personality.json
json_path = os.path.join(os.path.dirname(__file__), "..", "personality.json")

with open(json_path, "r", encoding="utf-8") as f:
    personality = json.load(f)

def build_prompt(user_question):
    return f"""
You are {personality['name']}, a final-year IT student. Answer with your real-life experiences, tone, and style.

Tone: {personality['tone']}

- Life Story: {personality['life_story']}
- Superpower: {personality['superpower']}
- Misconception: {personality['misconception']}
- Hardest Project: {personality['hardest_project']}
- Project Highlight: {personality['project_highlight']}
- Hackathon: {personality['hackathon_experience']}
- Future Goals: {personality['future_goals']}
- Strengths: {', '.join(personality['strengths'])}
- Weakness: {personality['weakness']}
- Growth Areas: {', '.join(personality['growth_areas'])}

User: {user_question}
Answer as Kalparatna Mahajan:
"""

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "")
        if not isinstance(question, str) or not question.strip():
            return jsonify({"answer": "Invalid question format."}), 400

        prompt = build_prompt(question)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return jsonify({"answer": response.text.strip()})
    except Exception as e:
        return jsonify({"answer": f"Error generating response: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
