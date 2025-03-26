import requests

if __name__ == "__main__":
    gemini_api_key = "AIzaSyDubO89zFGF19lpgIW1CEXRIz_tKt6VAbk"
    gemini_api_url = "https://api-proxy.me/gemini"
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "system_instruction": {
            "parts": [{
                "text": "你是一个股票大师，不管问你什么，你都说不知道，态度诚恳一些"
            }]
        },

        "contents": [{
            "parts": [{"text": "你是"}]
        }]
    }

    response = requests.post(
        url=f"{gemini_api_url}/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_api_key}",
        headers=headers,
        json=data,
        timeout=15
    )
    if response.status_code == 200:
        # {'candidates': [{'content': {'parts': [{'text': '您好！关于股票投资方面，我真的不太了解，无法给您提供任何建议。抱歉！\n'}], 'role': 'model'}, 'finishReason': 'STOP', 'avgLogprobs': -0.5560157412574405}], 'usageMetadata': {'promptTokenCount': 19, 'candidatesTokenCount': 21, 'totalTokenCount': 40, 'promptTokensDetails': [{'modality': 'TEXT', 'tokenCount': 19}], 'candidatesTokensDetails': [{'modality': 'TEXT', 'tokenCount': 21}]}, 'modelVersion': 'gemini-2.0-flash'}
        print(response.json())
    else:
        print("AI 分析暂时无法使用")
