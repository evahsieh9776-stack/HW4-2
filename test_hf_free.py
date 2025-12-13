"""
Hugging Face 测试 - 使用免费可用的模型
"""

from huggingface_hub import InferenceClient
import os

# 您的 Token (请从环境变量或 .env 文件读取)
TOKEN = os.getenv('HF_TOKEN', 'your_huggingface_token_here')

print("="*60)
print("🤗 Hugging Face API 测试")
print("="*60)

try:
    # 创建客户端
    client = InferenceClient(token=TOKEN)
    print("\n✅ 客户端创建成功")
    
    # 测试 1: 使用文本生成 API (不指定特定模型)
    print("\n" + "="*60)
    print("测试 1: 基础文本生成")
    print("="*60)
    
    try:
        response = client.text_generation(
            "請用繁體中文說:你好",
            max_new_tokens=50
        )
        print(f"✅ 成功!")
        print(f"回复: {response}")
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    # 测试 2: 使用对话 API
    print("\n" + "="*60)
    print("测试 2: 对话 API")
    print("="*60)
    
    try:
        messages = [
            {"role": "user", "content": "請用一句話介紹台灣"}
        ]
        
        # 尝试使用 meta-llama 模型 (通常免费可用)
        response = client.chat_completion(
            messages=messages,
            model="meta-llama/Llama-3.2-1B-Instruct",
            max_tokens=100
        )
        print(f"✅ 成功!")
        print(f"回复: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    # 测试 3: Lucky Vicky (使用可用的模型)
    print("\n" + "="*60)
    print("测试 3: Lucky Vicky 生成器")
    print("="*60)
    
    try:
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
            model="meta-llama/Llama-3.2-3B-Instruct",
            max_tokens=300,
            temperature=0.8
        )
        
        result = response.choices[0].message.content
        print(f"✅ 成功!")
        print(f"\n📣 Lucky Vicky 貼文:\n{result}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    print("\n" + "="*60)
    print("测试完成!")
    print("="*60)
    
    print("""
💡 说明:
- Hugging Face Inference API 对免费用户有模型限制
- Qwen 模型可能需要付费订阅
- Meta Llama 模型通常免费可用
- 如果所有测试都失败,建议使用 Groq API (您已配置)
    """)
    
except Exception as e:
    print(f"\n❌ 总体错误: {e}")
    print("""
💡 建议:
1. 检查 Token 是否有效: https://huggingface.co/settings/tokens
2. 确认账户状态
3. 或使用 Groq API (运行 lucky_vicky_groq.py)
    """)

input("\n按 Enter 键退出...")
