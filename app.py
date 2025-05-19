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

        print("🔑 API Key present:", openai.api_key is not None)
        print("🌐 API Base:", openai.api_base)

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
