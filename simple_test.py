"""
简单的 Lucky Vicky 测试
使用您的 Token
"""

from huggingface_hub import InferenceClient
import os

# 您的 Token (请从环境变量或 .env 文件读取)
TOKEN = os.getenv('HF_TOKEN', 'your_huggingface_token_here')

print("🤗 开始测试 Hugging Face API\n")

try:
    # 创建客户端
    client = InferenceClient(token=TOKEN)
    print("✅ 客户端创建成功")
    
    # 测试简单对话
    print("\n正在测试 API...")
    messages = [{"role": "user", "content": "Hi"}]
    
    response = client.chat_completion(
        messages=messages,
        model="Qwen/Qwen2.5-1.5B-Instruct",
        max_tokens=50
    )
    
    print(f"✅ API 响应成功!")
    print(f"回复: {response.choices[0].message.content}")
    
    # 测试 Lucky Vicky
    print("\n" + "="*60)
    print("测试 Lucky Vicky 生成器")
    print("="*60)
    
    system = """請用台灣習慣的中文來寫這段 po 文:
請用員瑛式思考, 也就是什麼都正向思維任何使用者寫的事情,
用我的第一人稱、社群媒體 po 文的口吻說一次,
說為什麼這是一件超幸運的事, 並且以「完全是 Lucky Vicky 呀!」結尾。
可以適度的加上 emoji。"""
    
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": "今天咖啡灑了"}
    ]
    
    response = client.chat_completion(
        messages=messages,
        model="Qwen/Qwen2.5-7B-Instruct",
        max_tokens=300,
        temperature=0.8
    )
    
    result = response.choices[0].message.content
    print(f"\n📣 Lucky Vicky 貼文:\n{result}")
    
    print("\n" + "="*60)
    print("🎉 所有测试成功!")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    print("\n💡 可能的解决方案:")
    print("1. 检查网络连接")
    print("2. 在 Hugging Face 网站确认 Token 状态")
    print("3. 尝试重新生成 Token")
    print("4. 稍后再试 (可能是 API 暂时繁忙)")

input("\n按 Enter 键退出...")
