import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# OpenRouter API 키 및 엔드포인트 설정
openai.api_key = os.environ.get('OPENROUTER_API_KEY')
openai.api_base = "https://openrouter.ai/api/v1"

@app.route('/', methods=['GET'])
def index():
    return "OpenRouter GPT-4 서버가 실행 중입니다.", 200

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': '요청에 prompt가 없습니다.'}), 400

        user_prompt = data['prompt']

        # ✅ 수정된 GPT 호출 방식
        completion = openai.ChatCompletion.create(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": user_prompt}]
        )

        # ✅ 수정된 응답 파싱 방식
        assistant_reply = completion['choices'][0]['message']['content']

        return jsonify({'response': assistant_reply}), 200

    except openai.OpenAIError as e:
        error_msg = str(e)
        status_code = getattr(e, 'status', 500)
        if not isinstance(status_code, int) or not (100 <= status_code < 600):
            status_code = 500
        return jsonify({'error': error_msg}), status_code

    except Exception as e:
        import traceback
        traceback.print_exc()  # 콘솔에 에러 출력
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
