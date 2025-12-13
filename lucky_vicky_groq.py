"""
Lucky Vicky 生成器 - 使用 Groq (无需 Hugging Face Token)
这个版本使用您已经配置好的 Groq API
"""

import os

print("="*60)
print("🌈 Lucky Vicky 生成器")
print("="*60)
print("\n💡 提示: 这个版本使用 Groq API (不需要 Hugging Face Token)")
print("如果您想使用 Hugging Face,请确保 Token 有效\n")

# 检查是否安装了 aisuite
try:
    import aisuite as ai
    print("✅ AISuite 已安装")
except ImportError:
    print("❌ 未找到 AISuite")
    print("请运行: pip install aisuite[all]")
    input("\n按 Enter 退出...")
    exit()

# 系统提示
system = """請用台灣習慣的中文來寫這段 po 文:
請用員瑛式思考, 也就是什麼都正向思維任何使用者寫的事情,
用我的第一人稱、社群媒體 po 文的口吻說一次,
說為什麼這是一件超幸運的事, 並且以「完全是 Lucky Vicky 呀!」結尾。
可以適度的加上 emoji。"""

def lucky_vicky_groq(event):
    """使用 Groq 的 Lucky Vicky 生成器"""
    try:
        client = ai.Client()
        
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": event}
        ]
        
        response = client.chat.completions.create(
            model="groq:llama-3.3-70b-versatile",
            messages=messages
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"❌ 错误: {e}"

# 测试示例
print("\n" + "="*60)
print("测试示例")
print("="*60)

test_events = [
    "今天咖啡灑到電腦上了!",
    "出門忘記帶傘,結果下大雨",
    "考試考得不太好"
]

for i, event in enumerate(test_events, 1):
    print(f"\n【示例 {i}】")
    print(f"事件: {event}")
    print(f"\n📣 員瑛式貼文:")
    result = lucky_vicky_groq(event)
    print(result)
    print("\n" + "-"*60)

# 交互模式
print("\n" + "="*60)
print("交互模式")
print("="*60)
print("\n输入您的事件,我会用 Lucky Vicky 的方式重新诠释!")
print("输入 'quit' 或 'exit' 退出\n")

while True:
    event = input("📝 发生了什么事? > ")
    
    if event.lower() in ['quit', 'exit', 'q', '']:
        print("\n再见! 🌈\n")
        break
    
    print(f"\n📣 員瑛式貼文:")
    result = lucky_vicky_groq(event)
    print(result)
    print("\n" + "-"*60 + "\n")
