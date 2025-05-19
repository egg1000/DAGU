import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# OpenRouter API key and endpoint
openai.api_key = os.environ.get('OPENROUTER_API_KEY')
openai.api_base = "https://openrouter.ai/api/v1"

@app.route('/', methods=['GET'])
def index():
    return "OpenRouter GPT-4 Server is running.", 200

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        print("📥 Received data:", data)

        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt in request.'}), 400

        user_prompt = data['prompt']
        print("🧠 User prompt:", user_prompt)

        completion = openai.ChatCompletion.create(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": user_prompt}]
        )

        print("✅ Raw completion result:", completion)

        assistant_reply = completion['choices'][0]['message']['content']
        return jsonify({'response': assistant_reply}), 200

    except openai.OpenAIError as e:
        print("❌ OpenAI API error:", str(e))
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        import traceback
        print("❗ Unknown error occurred:")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
