"""
Hugging Face Inference API 示例
使用方案二:通过 Hugging Face Inference API 调用模型
无需下载模型,直接使用云端 API
"""

# ============================================
# 第一步:安装必要的库
# ============================================
# 在 Jupyter Notebook 中运行:
# !pip install huggingface_hub

# ============================================
# 第二步:导入库并设置 API Token
# ============================================
from huggingface_hub import InferenceClient
import os

# 如果在 Google Colab 中使用:
# from google.colab import userdata
# hf_token = userdata.get('HuggingFace')  # 从 Colab Secrets 读取

# 如果在本地 Jupyter 使用,直接设置:
# hf_token = "your_huggingface_token_here"  # 替换为你的 token

# 或者从环境变量读取:
# hf_token = os.getenv('HF_TOKEN')

# ============================================
# 第三步:创建 Inference Client
# ============================================
def create_hf_client(token=None):
    """
    创建 Hugging Face Inference Client
    
    参数:
        token: Hugging Face API token (可选,某些公开模型不需要)
    
    返回:
        InferenceClient 实例
    """
    if token:
        return InferenceClient(token=token)
    else:
        # 不使用 token,只能访问公开模型
        return InferenceClient()


# ============================================
# 第四步:定义不同的使用示例
# ============================================

def example_1_text_generation(client, prompt="你好,请介绍一下自己"):
    """
    示例 1: 基础文本生成
    """
    print("=" * 50)
    print("示例 1: 基础文本生成")
    print("=" * 50)
    
    response = client.text_generation(
        prompt=prompt,
        model="Qwen/Qwen2.5-1.5B-Instruct",  # 使用轻量级模型
        max_new_tokens=200,
        temperature=0.7
    )
    
    print(f"输入: {prompt}")
    print(f"输出: {response}")
    print()
    return response


def example_2_chat_completion(client, user_message="什么是机器学习?"):
    """
    示例 2: 对话补全 (推荐使用)
    """
    print("=" * 50)
    print("示例 2: 对话补全")
    print("=" * 50)
    
    messages = [
        {
            "role": "system", 
            "content": "你是一个友善的 AI 助手,请用繁体中文回答问题。"
        },
        {
            "role": "user", 
            "content": user_message
        }
    ]
    
    response = client.chat_completion(
        messages=messages,
        model="Qwen/Qwen2.5-7B-Instruct",  # 中文能力强的模型
        max_tokens=500,
        temperature=0.7
    )
    
    print(f"用户: {user_message}")
    print(f"AI: {response.choices[0].message.content}")
    print()
    return response.choices[0].message.content


def example_3_lucky_vicky(client, event="今天咖啡灑到電腦上了!"):
    """
    示例 3: 员瑛式思考生成器 (Lucky Vicky)
    """
    print("=" * 50)
    print("示例 3: 員瑛式思考生成器")
    print("=" * 50)
    
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
        temperature=0.8  # 稍高的温度让回复更有创意
    )
    
    lucky_post = response.choices[0].message.content
    
    print(f"事件: {event}")
    print(f"\n📣 員瑛式貼文:\n{lucky_post}")
    print()
    return lucky_post


def example_4_sentiment_analysis(client, text="今天天氣真好!"):
    """
    示例 4: 情感分析
    """
    print("=" * 50)
    print("示例 4: 情感分析")
    print("=" * 50)
    
    # 使用对话模型进行情感分析
    messages = [
        {
            "role": "system",
            "content": "你是一个情感分析专家。请分析用户输入的文本情感,只回答:正面、负面或中性。"
        },
        {
            "role": "user",
            "content": f"请分析这段文字的情感: {text}"
        }
    ]
    
    response = client.chat_completion(
        messages=messages,
        model="Qwen/Qwen2.5-1.5B-Instruct",
        max_tokens=50
    )
    
    sentiment = response.choices[0].message.content
    
    print(f"文本: {text}")
    print(f"情感: {sentiment}")
    print()
    return sentiment


def example_5_translation(client, text="Hello, how are you?", target_lang="繁體中文"):
    """
    示例 5: 翻译
    """
    print("=" * 50)
    print("示例 5: 翻译")
    print("=" * 50)
    
    messages = [
        {
            "role": "system",
            "content": f"你是一个专业的翻译助手。请将用户输入的文本翻译成{target_lang}。"
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
    
    translation = response.choices[0].message.content
    
    print(f"原文: {text}")
    print(f"译文: {translation}")
    print()
    return translation


def example_6_streaming_response(client, prompt="請講一個有趣的故事"):
    """
    示例 6: 流式响应 (逐字输出)
    """
    print("=" * 50)
    print("示例 6: 流式响应")
    print("=" * 50)
    print(f"提示: {prompt}\n回复: ", end="")
    
    messages = [
        {"role": "user", "content": prompt}
    ]
    
    full_response = ""
    
    for token in client.chat_completion(
        messages=messages,
        model="Qwen/Qwen2.5-1.5B-Instruct",
        max_tokens=300,
        stream=True
    ):
        chunk = token.choices[0].delta.content
        print(chunk, end="", flush=True)
        full_response += chunk
    
    print("\n")
    return full_response


# ============================================
# 第五步:主函数 - 运行所有示例
# ============================================
def run_all_examples(token=None):
    """
    运行所有示例
    
    参数:
        token: Hugging Face API token (可选)
    """
    print("\n🚀 开始运行 Hugging Face Inference API 示例\n")
    
    # 创建客户端
    client = create_hf_client(token)
    
    try:
        # 示例 1: 基础文本生成
        example_1_text_generation(client, "台灣最有名的小吃是什麼?")
        
        # 示例 2: 对话补全
        example_2_chat_completion(client, "請推薦三個台北的旅遊景點")
        
        # 示例 3: Lucky Vicky 生成器
        example_3_lucky_vicky(client, "今天出門忘記帶傘,結果下大雨")
        
        # 示例 4: 情感分析
        example_4_sentiment_analysis(client, "這個產品真的太棒了!")
        
        # 示例 5: 翻译
        example_5_translation(client, "Machine learning is amazing!", "繁體中文")
        
        # 示例 6: 流式响应
        # example_6_streaming_response(client, "請用一句話介紹人工智慧")
        
        print("✅ 所有示例运行完成!")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("\n💡 提示:")
        print("1. 确保已安装 huggingface_hub: pip install huggingface_hub")
        print("2. 某些模型可能需要 API token")
        print("3. 检查网络连接")


# ============================================
# 使用说明
# ============================================
"""
在 Jupyter Notebook 中使用:

# 方法 1: 不使用 token (仅公开模型)
from huggingface_hub import InferenceClient
client = InferenceClient()

# 方法 2: 使用 token (推荐)
from huggingface_hub import InferenceClient
client = InferenceClient(token="your_token_here")

# 运行单个示例
example_3_lucky_vicky(client, "今天遲到了10分鐘")

# 或运行所有示例
run_all_examples(token="your_token_here")
"""


# ============================================
# 如果直接运行此脚本
# ============================================
if __name__ == "__main__":
    print("请在 Jupyter Notebook 中导入并使用此模块")
    print("\n示例代码:")
    print("from huggingface_demo import *")
    print("client = create_hf_client()")
    print("example_3_lucky_vicky(client, '今天咖啡灑了')")
