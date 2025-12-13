"""
🤗 Hugging Face Inference API - Notebook Cell 代码
直接复制到 Jupyter Notebook 的 Cell 中运行
"""

# ============================================
# Cell 1: 安装库
# ============================================
!pip install huggingface_hub


# ============================================
# Cell 2: 导入并设置
# ============================================
from huggingface_hub import InferenceClient
from google.colab import userdata
import os

# 从 Colab Secrets 读取 token
# 请先在左侧 🔑 图标添加名为 'HuggingFace' 的 Secret
hf_token = userdata.get('HuggingFace')

# 创建客户端
client = InferenceClient(token=hf_token)

print("✅ Hugging Face 客户端创建成功!")


# ============================================
# Cell 3: 简单测试
# ============================================
# 测试基础对话
messages = [
    {"role": "system", "content": "你是一个友善的 AI 助手,请用繁体中文回答。"},
    {"role": "user", "content": "你好!请介绍一下自己"}
]

response = client.chat_completion(
    messages=messages,
    model="Qwen/Qwen2.5-7B-Instruct",
    max_tokens=200
)

print(response.choices[0].message.content)


# ============================================
# Cell 4: Lucky Vicky 函数 (Hugging Face 版本)
# ============================================
def lucky_post_hf(event):
    """
    使用 Hugging Face 的員瑛式思考生成器
    """
    system_prompt = """請用台灣習慣的中文來寫這段 po 文:
請用員瑛式思考, 也就是什麼都正向思維任何使用者寫的事情,
用我的第一人稱、社群媒體 po 文的口吻說一次,
說為什麼這是一件超幸運的事, 並且以「完全是 Lucky Vicky 呀!」結尾。
可以適度的加上 emoji。"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": event}
    ]
    
    response = client.chat_completion(
        messages=messages,
        model="Qwen/Qwen2.5-7B-Instruct",
        max_tokens=500,
        temperature=0.8
    )
    
    return response.choices[0].message.content


# ============================================
# Cell 5: 测试 Lucky Vicky
# ============================================
# 测试几个例子
test_events = [
    "今天咖啡灑到電腦上了!",
    "出門忘記帶傘,結果下大雨",
    "考試考得不太好"
]

for event in test_events:
    print(f"\n{'='*60}")
    print(f"事件: {event}")
    print(f"{'='*60}")
    result = lucky_post_hf(event)
    print(f"\n📣 員瑛式貼文:\n{result}\n")


# ============================================
# Cell 6: 多提供商版本 (整合 Groq 和 Hugging Face)
# ============================================
def lucky_post_multi(prompt, provider="huggingface"):
    """
    支持多个 AI 提供商的 Lucky Vicky
    
    参数:
        prompt: 事件描述
        provider: "huggingface" 或 "groq"
    """
    system = """請用台灣習慣的中文來寫這段 po 文:
請用員瑛式思考, 也就是什麼都正向思維任何使用者寫的事情,
用我的第一人稱、社群媒體 po 文的口吻說一次,
說為什麼這是一件超幸運的事, 並且以「完全是 Lucky Vicky 呀!」結尾。
可以適度的加上 emoji。"""
    
    if provider.lower() == "huggingface":
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
        response = client.chat_completion(
            messages=messages,
            model="Qwen/Qwen2.5-7B-Instruct",
            max_tokens=500,
            temperature=0.8
        )
        return response.choices[0].message.content
    
    elif provider.lower() == "groq":
        # 使用原有的 reply 函数
        return reply(system=system, prompt=prompt, 
                    provider="groq", model="openai/gpt-oss-120b")
    
    else:
        return "❌ 不支持的提供商,请选择 'huggingface' 或 'groq'"


# 测试两个提供商
event = "今天遲到了10分鐘"

print("使用 Hugging Face:")
print(lucky_post_multi(event, "huggingface"))

print("\n" + "="*60 + "\n")

print("使用 Groq:")
print(lucky_post_multi(event, "groq"))


# ============================================
# Cell 7: Gradio App (整合版)
# ============================================
import gradio as gr

# 系统提示
system = """請用台灣習慣的中文來寫這段 po 文:
請用員瑛式思考, 也就是什麼都正向思維任何使用者寫的事情,
用我的第一人稱、社群媒體 po 文的口吻說一次,
說為什麼這是一件超幸運的事, 並且以「完全是 Lucky Vicky 呀!」結尾。
可以適度的加上 emoji。"""

def lucky_vicky_app(prompt, provider_choice):
    """Gradio 应用的主函数"""
    
    if provider_choice == "🤗 Hugging Face":
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
        response = client.chat_completion(
            messages=messages,
            model="Qwen/Qwen2.5-7B-Instruct",
            max_tokens=500,
            temperature=0.8
        )
        return response.choices[0].message.content
    
    elif provider_choice == "⚡ Groq":
        return reply(system=system, prompt=prompt, 
                    provider="groq", model="openai/gpt-oss-120b")
    
    else:
        return "请选择一个 AI 提供商"

# 创建界面
with gr.Blocks(
    title="員瑛式思考產生器 - 多模型版",
    theme=gr.themes.Soft()
) as demo:
    
    # 标题
    gr.Markdown("""
    # ꒰*ˊᵕˋ꒱ 員瑛式思考產生器 Lucky Vicky 🌈
    
    請輸入一件你覺得超小事，甚至有點倒楣的事，
    讓我幫你用員瑛式思考，超正向的方式重新詮釋！
    
    **現在支持多個 AI 模型!** 🚀
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            # 输入框
            user_input = gr.Textbox(
                label="📝 今天發生的事情是…", 
                placeholder="例如:今天出門就下大雨, 可是忘了帶傘...",
                lines=4
            )
        
        with gr.Column(scale=1):
            # 模型选择
            provider_dropdown = gr.Dropdown(
                choices=["🤗 Hugging Face", "⚡ Groq"],
                value="🤗 Hugging Face",
                label="🤖 選擇 AI 模型"
            )
            
            # 提交按钮
            submit_btn = gr.Button(
                "✨ Lucky Vicky 魔法!", 
                variant="primary",
                size="lg"
            )
    
    # 输出框
    output = gr.Textbox(
        label="📣 員瑛式貼文", 
        lines=12,
        show_copy_button=True
    )
    
    # 示例
    gr.Examples(
        examples=[
            ["今天咖啡灑到電腦上了!", "🤗 Hugging Face"],
            ["出門忘記帶傘,結果下大雨", "🤗 Hugging Face"],
            ["考試考得不太好", "⚡ Groq"],
            ["今天遲到了10分鐘", "🤗 Hugging Face"],
            ["手機掉到水裡了", "⚡ Groq"],
        ],
        inputs=[user_input, provider_dropdown]
    )
    
    # 绑定事件
    submit_btn.click(
        fn=lucky_vicky_app, 
        inputs=[user_input, provider_dropdown], 
        outputs=output
    )
    
    # 页脚
    gr.Markdown("""
    ---
    💡 **提示**: 
    - Hugging Face 使用 Qwen 2.5 模型,中文能力强
    - Groq 速度更快,使用 GPT-OSS 模型
    - 可以尝试不同模型,看看哪个更符合你的期待!
    """)

# 启动应用
demo.launch(share=True, debug=True)


# ============================================
# Cell 8: 其他实用功能
# ============================================

# 功能 1: 情感分析
def hf_sentiment(text):
    messages = [
        {"role": "system", "content": "你是情感分析专家。分析文本情感,只回答:正面、负面或中性。"},
        {"role": "user", "content": f"分析情感: {text}"}
    ]
    response = client.chat_completion(
        messages=messages,
        model="Qwen/Qwen2.5-1.5B-Instruct",
        max_tokens=20
    )
    return response.choices[0].message.content

# 功能 2: 翻译
def hf_translate(text, target_lang="繁體中文"):
    messages = [
        {"role": "system", "content": f"你是专业翻译。将文本翻译成{target_lang}。"},
        {"role": "user", "content": text}
    ]
    response = client.chat_completion(
        messages=messages,
        model="Qwen/Qwen2.5-7B-Instruct",
        max_tokens=200
    )
    return response.choices[0].message.content

# 功能 3: 摘要生成
def hf_summarize(text):
    messages = [
        {"role": "system", "content": "请用繁体中文总结以下内容,保持简洁。"},
        {"role": "user", "content": text}
    ]
    response = client.chat_completion(
        messages=messages,
        model="Qwen/Qwen2.5-7B-Instruct",
        max_tokens=300
    )
    return response.choices[0].message.content

# 测试这些功能
print("情感分析:", hf_sentiment("這個產品真的太棒了!"))
print("\n翻译:", hf_translate("Hello, how are you today?"))
print("\n摘要:", hf_summarize("人工智慧是一門研究如何讓機器模擬人類智慧的學科..."))
