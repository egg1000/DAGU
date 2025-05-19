import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# OpenRouter API 키 및 엔드포인트 설정
openai.api_key = os.environ.get('OPENROUTER_API_KEY')
openai.api_base = "https://openrouter.ai/api/v1"  # OpenAI SDK를 OpenRouter로 향하도록 설정

# 기본 루트 경로 - 서버 상태 확인용
@app.route('/', methods=['GET'])
def index():
    return "OpenRouter GPT-4 서버가 실행 중입니다.", 200

# /generate 경로 - POST로 프롬프트를 받아 GPT-4 응답 생성
@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': '요청에 prompt가 없습니다.'}), 400

        user_prompt = data['prompt']

        # GPT-4 모델(OpenAI ChatCompletion API)을 사용하여 응답 생성
        completion = openai.chat.completions.create(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": user_prompt}]
        )
        assistant_reply = completion.choices[0].message.content  # GPT-4의 응답 내용 추출

        return jsonify({'response': assistant_reply}), 200

    except openai.OpenAIError as e:
        # OpenAI API 호출 중 발생한 오류 처리 (잘못된 요청, 한도 초과 등)
        error_msg = str(e)
        status_code = getattr(e, 'status', 500)
        if not isinstance(status_code, int) or not (100 <= status_code < 600):
            status_code = 500
        return jsonify({'error': error_msg}), status_code

    except Exception as e:
        # 기타 예외 처리 (서버 내부 오류 등)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Render 플랫폼 환경에서는 PORT 환경 변수가 지정됩니다.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
