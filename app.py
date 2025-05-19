from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# API 키 체크
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ 환경변수 'OPENAI_API_KEY'가 설정되지 않았습니다.")
openai.api_key = api_key

@app.route("/generate", methods=["POST"])
def generate_script():
    try:
        data = request.get_json()
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"error": "No prompt provided."}), 400

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        result = response.choices[0].message.content
        return jsonify({"result": result})

    except Exception as e:
        print(f"❗ 내부 오류 발생: {str(e)}")  # 🔥 Render 로그에 출력됨
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "✅ GPT-4 Vegetable Script Server is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render가 지정한 포트 사용
    app.run(host="0.0.0.0", port=port)

@app.route("/generate", methods=["POST"])
def generate_script():
    try:
        data = request.get_json()
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"error": "No prompt provided."}), 400

        response = openai.ChatCompletion.create(
            model="gpt-4",  # ← 혹시 유료 계정 아니면 gpt-3.5-turbo로 바꿔줘
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        result = response.choices[0].message.content
        return jsonify({"result": result})

    except Exception as e:
        print(f"❗ GPT 호출 중 오류 발생: {str(e)}")  # 이 로그를 Render에서 볼 수 있음
        return jsonify({"error": str(e)}), 500
