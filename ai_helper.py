def ai_helper_webxpath(user_input='',always=False):
    '''
    网页解析函数，参数：
    user_input:输入要解析的网站url，并直接说出需要提取的内容
    '''
    import requests
    import json
    
    user_input = str( user_input ) 
    # 替换为你的实际 API Key
    api_key = "***"
    
    # API 端点
    url = "https://ark.cn-.com/api/v3/bots/chat/completions"
    
    # 请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    model = "bot-**-6hcxm" #该模型使用doubao-pro-4k创建的智能体
    
    def chat_with_ai(message):
        """与 AI 进行聊天"""
    
        data = {
            "model": model,  # 或者其他你选择的模型
            "messages": [
                {"role": "user", "content": message}
            ]
        }
    
        response = requests.post(url, headers=headers, data=json.dumps(data))
    
        if response.status_code == 200:
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]
            return ai_response
        else:
            return f"请求失败，状态码：{response.status_code}"
    
    ai_output = chat_with_ai(user_input)
    print(f"AI: {ai_output}")
def ai_helper_websearcher(user_input = '当前你不需要做任何事情，只需要输出一段文字"可以开始冲浪了"',always = False):
    import requests
    import json
    
    user_input = str( user_input ) 
    # 替换为你的实际 API Key
    api_key = ***"
    
    # API 端点
    url = "https://ark.cn-beijing.volces.com/api/v3/bots/chat/completions"
    
    # 请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    model = "bot--t5sxz" #该模型使用doubao-pro-4k创建的智能体
    
    def chat_with_ai(message):
        """与 AI 进行聊天"""
    
        data = {
            "model": model,  # 或者其他你选择的模型
            "messages": [
                {"role": "user", "content": message}
            ]
        }
    
        response = requests.post(url, headers=headers, data=json.dumps(data))
    
        if response.status_code == 200:
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]
            return ai_response
        else:
            return f"请求失败，状态码：{response.status_code}"
    
    ai_output = chat_with_ai(user_input)
    print(f"AI: {ai_output}")
    
    
def ai_helper_requests(user_input = '方涛', always = False):
    import requests
    import json
    
    user_input = str( user_input )
    always = bool(always)    
    # 替换为你的实际 API Key
    api_key = "***"
    
    # API 端点
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    
    # 请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    model = "ep-hfmjg" # 该模型使用doubao-pro-4k
    
    def chat_with_ai(message):
        """与 AI 进行聊天"""
    
        data = {
            "model": model,  # 或者其他你选择的模型
            "messages": [
                {"role": "user", "content": message}
            ]
        }
    
        response = requests.post(url, headers=headers, data=json.dumps(data))
    
        if response.status_code == 200:
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]
            return ai_response
        else:
            return f"请求失败，状态码：{response.status_code}"
    
    ai_output = chat_with_ai(user_input)
    print(f"AI: {ai_output}")
    
    # 开始聊天循环
    while always:
        user_input = input("你: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            break
        ai_output = chat_with_ai(user_input)
        print(f"AI: {ai_output}")

def ai_helper_stream(user_input = '方涛', always = False):
    from volcenginesdkarkruntime import Ark

    user_input = str( user_input )
    always = bool(always)     
    
    client = Ark(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key = "***",
    )

    messages = [
            {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
            {"role": "user", "content": user_input} 
    ]
    
    # Streaming:
    print("-----------------------------------")
    
    stream = client.chat.completions.create(
        model="ep-3-wzrg6",
        messages = messages,
        stream=True
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        print(chunk.choices[0].delta.content, end="")
    

    # 开始聊天循环
    while always:
        print('\n')
        print("------")
        user_input = input("*你：")
        messages.append({'role':'user','content':user_input})
        if user_input.lower() in ["exit", "quit", "bye"]:
            break
        stream = client.chat.completions.create(
            model="ep--wzrg6",
            messages = messages,
            stream=True
        )
        print('*AI： ',end='')
        for chunk in stream:
            if not chunk.choices:
                continue
            print(chunk.choices[0].delta.content, end="")
        
    print("\n-----------------------------------")
