"""
Lucky Vicky 生成器 - 简化版
这个版本展示了如何在 Jupyter Notebook 中使用 Hugging Face
"""

print("="*60)
print("🤗 Hugging Face 使用指南 - Lucky Vicky 示例")
print("="*60)

print("""
📚 在 Jupyter Notebook 中使用 Hugging Face 的完整示例

这个文件展示了您需要在 Notebook 中运行的代码。
请将以下代码复制到您的 Jupyter Notebook 中。

""")

print("="*60)
print("Cell 1: 安装库")
print("="*60)
print("""
!pip install huggingface_hub
""")

print("\n" + "="*60)
print("Cell 2: 导入库并设置 Token")
print("="*60)
print("""
from huggingface_hub import InferenceClient

# 在 Google Colab 中
from google.colab import userdata
hf_token = userdata.get('HuggingFace')

# 创建客户端
client = InferenceClient(token=hf_token)
print("✅ 客户端创建成功!")
""")

print("\n" + "="*60)
print("Cell 3: Lucky Vicky 函数 (使用免费模型)")
print("="*60)
print("""
def lucky_vicky_hf(event):
    '''使用 Hugging Face 的 Lucky Vicky 生成器'''
    
    system = '''請用台灣習慣的中文來寫這段 po 文:
請用員瑛式思考, 也就是什麼都正向思維任何使用者寫的事情,
用我的第一人稱、社群媒體 po 文的口吻說一次,
說為什麼這是一件超幸運的事, 並且以「完全是 Lucky Vicky 呀!」結尾。
可以適度的加上 emoji。'''
    
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": event}
    ]
    
    try:
        # 使用 Meta Llama 免费模型
        response = client.chat_completion(
            messages=messages,
            model="meta-llama/Llama-3.2-3B-Instruct",
            max_tokens=300,
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 错误: {e}\\n\\n💡 提示: 免费账户可能有限制,建议使用 Groq API"

# 测试
result = lucky_vicky_hf("今天咖啡灑了")
print(result)
""")

print("\n" + "="*60)
print("Cell 4: 使用 Groq (推荐 - 您已配置)")
print("="*60)
print("""
# 使用您原有的 reply 函数
system = '''請用台灣習慣的中文來寫這段 po 文:
請用員瑛式思考, 也就是什麼都正向思維任何使用者寫的事情,
用我的第一人稱、社群媒體 po 文的口吻說一次,
說為什麼這是一件超幸運的事, 並且以「完全是 Lucky Vicky 呀!」結尾。
可以適度的加上 emoji。'''

# 使用 Groq (快速且免费)
result = reply(
    system=system,
    prompt="今天咖啡灑了",
    provider="groq",
    model="llama-3.3-70b-versatile"
)

print(result)
""")

print("\n" + "="*60)
print("Cell 5: 多提供商版本")
print("="*60)
print("""
def lucky_vicky_multi(event, use_hf=False):
    '''支持 Hugging Face 和 Groq 的版本'''
    
    system = '''請用台灣習慣的中文來寫這段 po 文:
請用員瑛式思考, 也就是什麼都正向思維任何使用者寫的事情,
用我的第一人稱、社群媒體 po 文的口吻說一次,
說為什麼這是一件超幸運的事, 並且以「完全是 Lucky Vicky 呀!」結尾。
可以適度的加上 emoji。'''
    
    if use_hf:
        # 使用 Hugging Face
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": event}
        ]
        try:
            response = client.chat_completion(
                messages=messages,
                model="meta-llama/Llama-3.2-3B-Instruct",
                max_tokens=300,
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"HF 错误: {e}, 切换到 Groq...")
            use_hf = False
    
    if not use_hf:
        # 使用 Groq (默认)
        return reply(
            system=system,
            prompt=event,
            provider="groq",
            model="llama-3.3-70b-versatile"
        )

# 测试
print("使用 Groq:")
print(lucky_vicky_multi("今天遲到了10分鐘", use_hf=False))

print("\\n尝试使用 Hugging Face:")
print(lucky_vicky_multi("今天遲到了10分鐘", use_hf=True))
""")

print("\n" + "="*60)
print("Cell 6: Gradio App (整合版)")
print("="*60)
print("""
import gradio as gr

# 系统提示
system = '''請用台灣習慣的中文來寫這段 po 文:
請用員瑛式思考, 也就是什麼都正向思維任何使用者寫的事情,
用我的第一人稱、社群媒體 po 文的口吻說一次,
說為什麼這是一件超幸運的事, 並且以「完全是 Lucky Vicky 呀!」結尾。
可以適度的加上 emoji。'''

def lucky_vicky_app(prompt, provider_choice):
    if provider_choice == "🤗 Hugging Face":
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
        try:
            response = client.chat_completion(
                messages=messages,
                model="meta-llama/Llama-3.2-3B-Instruct",
                max_tokens=300,
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ HF 错误: {e}\\n\\n正在使用 Groq..."
    
    # 使用 Groq
    return reply(system=system, prompt=prompt, 
                provider="groq", model="llama-3.3-70b-versatile")

# 创建界面
with gr.Blocks(title="Lucky Vicky 生成器", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🌈 Lucky Vicky 生成器")
    gr.Markdown("支持 Hugging Face 和 Groq!")
    
    with gr.Row():
        user_input = gr.Textbox(
            label="📝 發生了什麼事?",
            placeholder="例如:今天咖啡灑了...",
            lines=3
        )
    
    provider = gr.Dropdown(
        choices=["⚡ Groq (推荐)", "🤗 Hugging Face"],
        value="⚡ Groq (推荐)",
        label="選擇 AI 提供商"
    )
    
    btn = gr.Button("✨ Lucky Vicky 魔法!", variant="primary")
    output = gr.Textbox(label="📣 員瑛式貼文", lines=10)
    
    gr.Examples(
        examples=[
            ["今天咖啡灑了", "⚡ Groq (推荐)"],
            ["出門忘記帶傘", "🤗 Hugging Face"],
        ],
        inputs=[user_input, provider]
    )
    
    btn.click(lucky_vicky_app, [user_input, provider], output)

demo.launch(share=True, debug=True)
""")

print("\n" + "="*60)
print("📝 总结")
print("="*60)
print("""
您现在知道如何:

✅ 在 Jupyter Notebook 中使用 Hugging Face
✅ 配置和使用 Hugging Face Token
✅ 创建 Lucky Vicky 生成器
✅ 整合多个 AI 提供商 (Groq + Hugging Face)
✅ 创建 Gradio Web App

💡 建议:
- 在 Notebook 中优先使用 Groq (快速且免费)
- Hugging Face 免费账户有模型限制
- 可以同时配置多个提供商作为备选

📁 相关文件:
- HuggingFace_使用指南.md - 详细教程
- 测试结果总结.md - 测试结果和建议
- Token使用说明.md - Token 配置说明

🎉 恭喜!您已经掌握了 Hugging Face 的基本使用!
""")

input("\n按 Enter 键退出...")
