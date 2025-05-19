import os
import openai
from flask import Flask, request, jsonify

# ✅ app 정의 먼저!
app = Flask(__name__)

# ✅ OpenRouter API 설정
openai.api_key = os.environ.get('OPENROUTER_API_KEY')
openai.api_base = "https://openrouter.ai/api/v1"

# ✅ 라우팅은 그 다음에
@app.route('/', methods=['GET'])
def index():
    return "OpenRouter GPT-3.5 server is running.", 200

@app.route('/generate', methods=['POST'])
def generate():
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = None
        print("📥 Received JSON:", data)

        if not data or 'prompt' not in data:
            print("🚫 'prompt' key is missing or no JSON received.")
            return jsonify({'error': "Missing 'prompt' in request."}), 400

        prompt = data['prompt']
        print("🧠 Prompt:", prompt)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        print("✅ Completion result:", response)

        reply = response['choices'][0]['message']['content']
        return jsonify({'response': reply}), 200

    except Exception as e:
        import traceback
        print("❗ Unexpected error:")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# ✅ 마지막에 run()
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
