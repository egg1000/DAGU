import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# OpenRouter API settings
openai.api_key = os.environ.get('OPENROUTER_API_KEY')
openai.api_base = "https://openrouter.ai/api/v1"

@app.route('/', methods=['GET'])
def index():
    return "OpenRouter GPT-3.5 server is running.", 200

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        print("📥 Received JSON:", data)

        if not data or 'prompt' not in data:
            print("🚫 'prompt' key is missing.")
            return jsonify({'error': "Missing 'prompt' in request."}), 400

        prompt = data['prompt']
        print("🧠 Prompt:", prompt)

        print("🔑 API Key present:", openai.api_key is not None)
        print("🌐 API Base:", openai.api_base)

        # ✅ Using a stable and free model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ✅ safest free model
            messages=[{"role": "user", "content": prompt}]
        )

        print("✅ Completion result:", response)

        reply = response['choices'][0]['message']['content']
        return jsonify({'response': reply}), 200

    except openai.OpenAIError as e:
        print("❌ OpenAI API Error:", str(e))
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        import traceback
        print("❗ Unexpected error:")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
