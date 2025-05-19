import openai
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# OpenRouter 설정
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = os.environ.get("OPENROUTER_API_KEY")

@app.route("/generate", methods=["POST"])
def generate_script():
    try:
        data = request.get_json()
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"error": "No prompt provided."}), 400

        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",  # 또는 openai/gpt-4
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        result = response.choices[0].message.content
        return jsonify({"result": result})

    except Exception as e:
        print(f"\u2757 GPT 호출 중 오류 발생: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "\u2705 OpenRouter 기반 GPT 서버 작동 중!"

# Render에서 포트를 인식하게 설정
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
