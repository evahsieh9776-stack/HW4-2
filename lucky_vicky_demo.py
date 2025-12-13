"""
員瑛式思考生成器 - Gradio Web Demo
使用 Hugging Face Inference API
"""

import gradio as gr
from huggingface_hub import InferenceClient
import os

# ============================================
# 配置
# ============================================

# 从 .env 文件读取 Token
HF_TOKEN = None
try:
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('HF_TOKEN='):
                HF_TOKEN = line.strip().split('=', 1)[1]
                break
except FileNotFoundError:
    pass

# 或从环境变量读取
if not HF_TOKEN:
    HF_TOKEN = os.getenv('HF_TOKEN')

# 创建客户端
if HF_TOKEN:
    client = InferenceClient(token=HF_TOKEN)
    print("✅ Hugging Face 客户端已创建")
else:
    client = None
    print("⚠️  未找到 Token,某些功能可能不可用")

# ============================================
# Lucky Vicky 生成函数
# ============================================

def generate_lucky_vicky(event, model_choice="Meta Llama 3.2-3B"):
    """生成員瑛式思考貼文"""
    
    if not event or not event.strip():
        return "❌ 请输入发生的事件!"
    
    system_prompt = """請用台灣習慣的中文來寫這段 po 文:
請用員瑛式思考, 也就是什麼都正向思維任何使用者寫的事情,
用我的第一人稱、社群媒體 po 文的口吻說一次,
說為什麼這是一件超幸運的事, 並且以「完全是 Lucky Vicky 呀!」結尾。
可以適度的加上 emoji。"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": event}
    ]
    
    # 根据选择的模型
    model_map = {
        "Meta Llama 3.2-3B": "meta-llama/Llama-3.2-3B-Instruct",
        "Meta Llama 3.2-1B": "meta-llama/Llama-3.2-1B-Instruct",
        "Microsoft Phi-3": "microsoft/Phi-3-mini-4k-instruct"
    }
    
    model = model_map.get(model_choice, "meta-llama/Llama-3.2-3B-Instruct")
    
    try:
        if not client:
            return "❌ 错误: 未配置 Hugging Face Token\n\n请在 .env 文件中设置 HF_TOKEN"
        
        response = client.chat_completion(
            messages=messages,
            model=model,
            max_tokens=500,
            temperature=0.8
        )
        
        result = response.choices[0].message.content
        return result
        
    except Exception as e:
        error_msg = str(e)
        
        if "not_supported" in error_msg or "doesn't support" in error_msg:
            return f"❌ 模型 '{model_choice}' 在免费账户中不可用\n\n💡 建议:\n1. 尝试其他模型\n2. 升级 Hugging Face 账户\n3. 或使用 Groq API (见 Notebook)"
        elif "401" in error_msg or "Invalid token" in error_msg:
            return "❌ Token 无效或已过期\n\n请检查:\n1. Token 是否正确\n2. Token 是否有 'Read' 权限\n3. 在 https://huggingface.co/settings/tokens 重新生成"
        else:
            return f"❌ 错误: {error_msg}\n\n💡 可能的原因:\n1. 网络连接问题\n2. API 速率限制\n3. 模型暂时不可用"

# ============================================
# 示例数据
# ============================================

examples = [
    ["今天咖啡灑到電腦上了!", "Meta Llama 3.2-3B"],
    ["出門忘記帶傘,結果下大雨", "Meta Llama 3.2-3B"],
    ["考試考得不太好", "Meta Llama 3.2-1B"],
    ["今天遲到了10分鐘", "Meta Llama 3.2-3B"],
    ["手機掉到水裡了", "Microsoft Phi-3"],
]

# ============================================
# Gradio 界面
# ============================================

# 自定义 CSS
custom_css = """
.gradio-container {
    font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
}

.title {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5em;
    font-weight: bold;
    margin-bottom: 0.5em;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 1.1em;
    margin-bottom: 2em;
}

.footer {
    text-align: center;
    margin-top: 2em;
    padding: 1em;
    color: #888;
    font-size: 0.9em;
}
"""

# 创建界面
with gr.Blocks(
    title="員瑛式思考生成器 - Lucky Vicky",
    theme=gr.themes.Soft(
        primary_hue="purple",
        secondary_hue="pink",
    ),
    css=custom_css
) as demo:
    
    # 标题
    gr.HTML("""
        <div class="title">🌈 員瑛式思考生成器</div>
        <div class="subtitle">Lucky Vicky - 把任何事情都變成幸運的事!</div>
    """)
    
    # 说明
    with gr.Accordion("📖 使用說明", open=False):
        gr.Markdown("""
        ### 什麼是員瑛式思考?
        
        員瑛式思考是一種超級正向的思維方式,能把任何看似倒楣的事情,
        重新詮釋成幸運的事件!
        
        ### 如何使用?
        
        1. 在下方輸入框中描述發生的事情
        2. 選擇 AI 模型 (推薦使用 Meta Llama 3.2-3B)
        3. 點擊「✨ 生成 Lucky Vicky 貼文」
        4. 等待 AI 生成正向思考的社群媒體貼文
        
        ### 技術說明
        
        - 使用 Hugging Face Inference API
        - 支持多個免費 AI 模型
        - 專為繁體中文優化
        
        ### 注意事項
        
        - 免費模型可能有速率限制
        - 某些模型可能需要付費訂閱
        - 建議使用 Meta Llama 模型 (免費且效果好)
        """)
    
    # 主要内容
    with gr.Row():
        with gr.Column(scale=2):
            # 输入区
            event_input = gr.Textbox(
                label="📝 發生了什麼事?",
                placeholder="例如:今天出門就下大雨,可是忘了帶傘...",
                lines=4,
                max_lines=10
            )
            
            # 模型选择
            model_choice = gr.Dropdown(
                choices=[
                    "Meta Llama 3.2-3B",
                    "Meta Llama 3.2-1B",
                    "Microsoft Phi-3"
                ],
                value="Meta Llama 3.2-3B",
                label="🤖 選擇 AI 模型",
                info="推薦使用 Meta Llama 3.2-3B (免費且效果好)"
            )
            
            # 生成按钮
            generate_btn = gr.Button(
                "✨ 生成 Lucky Vicky 貼文",
                variant="primary",
                size="lg"
            )
        
        with gr.Column(scale=3):
            # 输出区
            output = gr.Textbox(
                label="📣 員瑛式貼文",
                lines=15,
                max_lines=20,
                placeholder="生成的 Lucky Vicky 貼文會顯示在這裡..."
            )
    
    # 示例
    gr.Examples(
        examples=examples,
        inputs=[event_input, model_choice],
        outputs=output,
        fn=generate_lucky_vicky,
        cache_examples=False,
        label="💡 試試這些例子"
    )
    
    # 绑定事件
    generate_btn.click(
        fn=generate_lucky_vicky,
        inputs=[event_input, model_choice],
        outputs=output
    )
    
    # 也支持按 Enter 键
    event_input.submit(
        fn=generate_lucky_vicky,
        inputs=[event_input, model_choice],
        outputs=output
    )
    
    # 页脚
    gr.HTML("""
        <div class="footer">
            <p>🤗 Powered by Hugging Face Inference API</p>
            <p>💡 提示: 如果遇到問題,請檢查 Token 配置或嘗試其他模型</p>
            <p>📚 更多資訊請查看 <code>學習總結.md</code></p>
        </div>
    """)

# ============================================
# 启动应用
# ============================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🌈 員瑛式思考生成器 - Lucky Vicky")
    print("="*60)
    
    if HF_TOKEN:
        print(f"✅ Token 已配置: {HF_TOKEN[:10]}...")
    else:
        print("⚠️  未找到 Token")
        print("請在 .env 文件中設置 HF_TOKEN")
    
    print("\n正在啟動 Gradio 應用...")
    print("應用將在瀏覽器中自動打開")
    print("\n按 Ctrl+C 停止應用\n")
    
    # 启动应用
    demo.launch(
        server_name="127.0.0.1",  # 本地访问
        server_port=7860,          # 端口
        share=False,               # 不创建公开链接
        show_error=True,           # 显示错误
        quiet=False                # 显示日志
    )
