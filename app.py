@app.route('/generate', methods=['POST'])
def generate():
    try:
        # 🔍 1. JSON 요청 데이터 확인용 출력
        data = request.get_json()
        print("📥 받은 데이터:", data)

        if not data or 'prompt' not in data:
            return jsonify({'error': '요청에 prompt가 없습니다.'}), 400

        user_prompt = data['prompt']
        print("🧠 프롬프트:", user_prompt)

        # 🔍 2. GPT 호출 시도
        completion = openai.ChatCompletion.create(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": user_prompt}]
        )

        # 🔍 3. GPT 응답 전체 구조 확인
        print("✅ 응답 원본:", completion)

        assistant_reply = completion['choices'][0]['message']['content']
        return jsonify({'response': assistant_reply}), 200

    # 👇 이건 OpenAI 오류 처리
    except openai.OpenAIError as e:
        print("❌ OpenAI 오류 발생:", str(e))
        return jsonify({'error': str(e)}), 500

    # 👇 이건 그 외 모든 오류 처리
    except Exception as e:
        import traceback
        print("❗ 예외 발생:")
        traceback.print_exc()  # ✅ 에러 상세 로그가 콘솔에 찍힘
        return jsonify({'error': str(e)}), 500
