# 🤗 Hugging Face Inference API 使用指南

## 📋 目录
1. [安装与设置](#安装与设置)
2. [获取 API Token](#获取-api-token)
3. [基础使用](#基础使用)
4. [Lucky Vicky 集成](#lucky-vicky-集成)
5. [完整示例代码](#完整示例代码)

---

## 1️⃣ 安装与设置

### 在 Jupyter Notebook 新 Cell 中运行:

```python
# 安装 Hugging Face Hub 库
!pip install huggingface_hub
```

---

## 2️⃣ 获取 API Token

### 步骤:
1. 访问 [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. 点击 "New token"
3. 选择 "Read" 权限即可
4. 复制生成的 token

### 在 Google Colab 中保存 Token:
1. 点击左侧 🔑 图标 (Secrets)
2. 添加新的 Secret:
   - Name: `HuggingFace`
   - Value: 粘贴你的 token

---

## 3️⃣ 基础使用

### Cell 1: 导入库并创建客户端

```python
from huggingface_hub import InferenceClient
import os

# 方法 A: 从 Colab Secrets 读取 (推荐)
from google.colab import userdata
hf_token = userdata.get('HuggingFace')

# 方法 B: 直接设置 (不推荐,会暴露 token)
# hf_token = "hf_your_token_here"

# 创建客户端
client = InferenceClient(token=hf_token)

print("✅ Hugging Face 客户端创建成功!")
```

### Cell 2: 简单测试

```python
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
```

---

## 4️⃣ Lucky Vicky 集成

### Cell 3: 创建 Hugging Face 版本的 Lucky Vicky

```python
def lucky_post_hf(event, client):
    """
    使用 Hugging Face 的員瑛式思考生成器
    
    参数:
        event: 发生的事件
        client: HuggingFace InferenceClient
    
    返回:
        Lucky Vicky 风格的正向贴文
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
        model="Qwen/Qwen2.5-7B-Instruct",  # 中文能力强的模型
        max_tokens=500,
        temperature=0.8  # 更有创意
    )
    
    return response.choices[0].message.content

# 测试
event = "今天出門忘記帶傘,結果下大雨"
result = lucky_post_hf(event, client)
print(f"事件: {event}\n")
print(f"📣 員瑛式貼文:\n{result}")
```

---

## 5️⃣ 完整示例代码

### Cell 4: 多功能示例

```python
# ============================================
# 示例 1: 文本生成
# ============================================
def hf_text_generation(prompt, client):
    response = client.text_generation(
        prompt=prompt,
        model="Qwen/Qwen2.5-1.5B-Instruct",
        max_new_tokens=200
    )
    return response

# 测试
print("示例 1: 文本生成")
print(hf_text_generation("台灣最有名的夜市是", client))
print("\n" + "="*50 + "\n")


# ============================================
# 示例 2: 对话补全
# ============================================
def hf_chat(user_message, client, system_message="你是一个友善的助手"):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    response = client.chat_completion(
        messages=messages,
        model="Qwen/Qwen2.5-7B-Instruct",
        max_tokens=300
    )
    
    return response.choices[0].message.content

# 测试
print("示例 2: 对话补全")
print(hf_chat("請推薦三個台北的景點", client))
print("\n" + "="*50 + "\n")


# ============================================
# 示例 3: 情感分析
# ============================================
def hf_sentiment(text, client):
    messages = [
        {
            "role": "system",
            "content": "你是情感分析专家。分析文本情感,只回答:正面、负面或中性。"
        },
        {
            "role": "user",
            "content": f"分析情感: {text}"
        }
    ]
    
    response = client.chat_completion(
        messages=messages,
        model="Qwen/Qwen2.5-1.5B-Instruct",
        max_tokens=20
    )
    
    return response.choices[0].message.content

# 测试
print("示例 3: 情感分析")
print(f"文本: 這個產品真的太棒了!")
print(f"情感: {hf_sentiment('這個產品真的太棒了!', client)}")
print("\n" + "="*50 + "\n")


# ============================================
# 示例 4: 翻译
# ============================================
def hf_translate(text, target_lang, client):
    messages = [
        {
            "role": "system",
            "content": f"你是专业翻译。将文本翻译成{target_lang}。"
        },
        {
            "role": "user",
            "content": text
        }
    ]
    
    response = client.chat_completion(
        messages=messages,
        model="Qwen/Qwen2.5-7B-Instruct",
        max_tokens=200
    )
    
    return response.choices[0].message.content

# 测试
print("示例 4: 翻译")
original = "Machine learning is transforming the world"
translated = hf_translate(original, "繁體中文", client)
print(f"原文: {original}")
print(f"译文: {translated}")
print("\n" + "="*50 + "\n")


# ============================================
# 示例 5: 流式响应 (逐字输出)
# ============================================
def hf_stream(prompt, client):
    messages = [{"role": "user", "content": prompt}]
    
    print(f"提示: {prompt}\n回复: ", end="")
    
    for token in client.chat_completion(
        messages=messages,
        model="Qwen/Qwen2.5-1.5B-Instruct",
        max_tokens=200,
        stream=True
    ):
        chunk = token.choices[0].delta.content
        print(chunk, end="", flush=True)
    
    print("\n")

# 测试
print("示例 5: 流式响应")
hf_stream("請用一句話介紹台灣", client)
```

---

## 6️⃣ 整合到 Gradio App

### Cell 5: 添加 Hugging Face 选项到现有 App

```python
import gradio as gr

# 定义系统提示
system = """請用台灣習慣的中文來寫這段 po 文:
請用員瑛式思考, 也就是什麼都正向思維任何使用者寫的事情,
用我的第一人稱、社群媒體 po 文的口吻說一次,
說為什麼這是一件超幸運的事, 並且以「完全是 Lucky Vicky 呀!」結尾。
可以適度的加上 emoji。"""

# 多提供商支持
def lucky_post_multi(prompt, provider_choice):
    """支持多个 AI 提供商"""
    
    if provider_choice == "Hugging Face":
        # 使用 Hugging Face
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
    
    elif provider_choice == "Groq":
        # 使用原有的 Groq
        return reply(system=system, prompt=prompt, 
                    provider="groq", model="openai/gpt-oss-120b")
    
    else:
        return "请选择一个提供商"

# 创建 Gradio 界面
with gr.Blocks(title="員瑛式思考產生器 - 多模型版") as demo:
    gr.Markdown("### ꒰*ˊᵕˋ꒱ 員瑛式思考產生器 Lucky Vicky 🌈")
    gr.Markdown("支持多个 AI 提供商!请选择你想使用的模型")
    
    with gr.Row():
        user_input = gr.Textbox(
            label="今天發生的事情是…", 
            placeholder="例如:今天出門就下大雨, 可是忘了帶傘...",
            lines=3
        )
    
    # 模型选择
    provider_dropdown = gr.Dropdown(
        choices=["Groq", "Hugging Face"],
        value="Hugging Face",
        label="🤖 選擇 AI 提供商"
    )
    
    submit_btn = gr.Button("✨ Lucky Vicky 魔法!", variant="primary")
    output = gr.Textbox(label="📣 員瑛式貼文", lines=10)
    
    # 添加示例
    gr.Examples(
        examples=[
            ["今天咖啡灑到電腦上了!", "Hugging Face"],
            ["出門忘記帶傘,結果下大雨", "Hugging Face"],
            ["考試考得不太好", "Groq"],
        ],
        inputs=[user_input, provider_dropdown]
    )
    
    submit_btn.click(
        fn=lucky_post_multi, 
        inputs=[user_input, provider_dropdown], 
        outputs=output
    )

demo.launch(share=True, debug=True)
```

---

## 📊 推荐的 Hugging Face 模型

| 模型名称 | 大小 | 特点 | 适用场景 |
|---------|------|------|---------|
| `Qwen/Qwen2.5-1.5B-Instruct` | 1.5B | 轻量快速 | 简单对话、测试 |
| `Qwen/Qwen2.5-7B-Instruct` | 7B | 中文能力强 | Lucky Vicky、翻译 |
| `Qwen/Qwen2.5-72B-Instruct` | 72B | 最强性能 | 复杂任务 |
| `meta-llama/Llama-3.1-8B-Instruct` | 8B | 多语言 | 通用对话 |
| `google/gemma-2-9b-it` | 9B | Google 出品 | 平衡性能 |

---

## 💡 使用技巧

### 1. Temperature 参数
- `0.1-0.3`: 更确定、一致的回复
- `0.7-0.9`: 更有创意、多样的回复
- `1.0+`: 非常随机

### 2. Max Tokens
- 简短回复: 50-100
- 中等回复: 200-300
- 长文本: 500-1000

### 3. 错误处理
```python
try:
    response = client.chat_completion(...)
except Exception as e:
    print(f"错误: {e}")
    # 可以切换到备用模型
```

---

## 🔗 相关链接

- [Hugging Face Hub](https://huggingface.co/)
- [模型库](https://huggingface.co/models)
- [API 文档](https://huggingface.co/docs/huggingface_hub)
- [获取 Token](https://huggingface.co/settings/tokens)

---

## ✅ 完成!

现在您已经学会了如何在 Jupyter Notebook 中使用 Hugging Face Inference API!

**下一步:**
1. 获取您的 API Token
2. 在 Colab Secrets 中保存
3. 运行上面的示例代码
4. 尝试不同的模型和参数

祝您使用愉快! 🎉
