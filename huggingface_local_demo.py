y"""
Hugging Face Inference API - 本地 Windows 版本
可以直接在本地 Python 环境中运行
"""

from huggingface_hub import InferenceClient
import os

# ============================================
# 配置部分 - 请在这里设置您的 Token
# ============================================

# 方法 1: 直接设置 (不推荐,会暴露 token)
# HF_TOKEN = "hf_your_token_here"

# 方法 2: 从环境变量读取 (推荐)
# 在 PowerShell 中运行: $env:HF_TOKEN = "hf_your_token_here"
HF_TOKEN = os.getenv('HF_TOKEN', None)

# 方法 3: 从文件读取 (推荐)
# 创建一个 .env 文件,内容为: HF_TOKEN=hf_your_token_here
try:
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('HF_TOKEN='):
                HF_TOKEN = line.strip().split('=', 1)[1]
                break
except FileNotFoundError:
    pass

# ============================================
# 创建客户端
# ============================================

def create_client(token=None):
    """创建 Hugging Face Inference Client"""
    if token:
        return InferenceClient(token=token)
    else:
        print("⚠️  警告: 未提供 token,只能使用公开模型")
        return InferenceClient()


# ============================================
# 示例函数
# ============================================

def example_1_basic_chat(client):
    """示例 1: 基础对话"""
    print("\n" + "="*60)
    print("示例 1: 基础对话")
    print("="*60)
    
    messages = [
        {"role": "system", "content": "你是一个友善的 AI 助手,请用繁体中文回答。"},
        {"role": "user", "content": "你好!请介绍一下自己"}
    ]
    
    try:
        response = client.chat_completion(
            messages=messages,
            model="Qwen/Qwen2.5-7B-Instruct",
            max_tokens=200
        )
        
        result = response.choices[0].message.content
        print(f"\n回复:\n{result}\n")
        return result
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def example_2_lucky_vicky(client, event="今天咖啡灑到電腦上了!"):
    """示例 2: Lucky Vicky 生成器"""
    print("\n" + "="*60)
    print("示例 2: Lucky Vicky 生成器")
    print("="*60)
    
    system_prompt = """請用台灣習慣的中文來寫這段 po 文:
請用員瑛式思考, 也就是什麼都正向思維任何使用者寫的事情,
用我的第一人稱、社群媒體 po 文的口吻說一次,
說為什麼這是一件超幸運的事, 並且以「完全是 Lucky Vicky 呀!」結尾。
可以適度的加上 emoji。"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": event}
    ]
    
    try:
        response = client.chat_completion(
            messages=messages,
            model="Qwen/Qwen2.5-7B-Instruct",
            max_tokens=500,
            temperature=0.8
        )
        
        result = response.choices[0].message.content
        print(f"\n事件: {event}")
        print(f"\n📣 員瑛式貼文:\n{result}\n")
        return result
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def example_3_translation(client, text="Hello, how are you?"):
    """示例 3: 翻译"""
    print("\n" + "="*60)
    print("示例 3: 翻译")
    print("="*60)
    
    messages = [
        {"role": "system", "content": "你是专业翻译。将文本翻译成繁體中文。"},
        {"role": "user", "content": text}
    ]
    
    try:
        response = client.chat_completion(
            messages=messages,
            model="Qwen/Qwen2.5-7B-Instruct",
            max_tokens=200
        )
        
        result = response.choices[0].message.content
        print(f"\n原文: {text}")
        print(f"译文: {result}\n")
        return result
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def example_4_sentiment(client, text="這個產品真的太棒了!"):
    """示例 4: 情感分析"""
    print("\n" + "="*60)
    print("示例 4: 情感分析")
    print("="*60)
    
    messages = [
        {"role": "system", "content": "你是情感分析专家。分析文本情感,只回答:正面、负面或中性。"},
        {"role": "user", "content": f"分析情感: {text}"}
    ]
    
    try:
        response = client.chat_completion(
            messages=messages,
            model="Qwen/Qwen2.5-1.5B-Instruct",
            max_tokens=20
        )
        
        result = response.choices[0].message.content
        print(f"\n文本: {text}")
        print(f"情感: {result}\n")
        return result
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


# ============================================
# 主程序
# ============================================

def main():
    """主函数"""
    print("\n" + "🤗 "*20)
    print("Hugging Face Inference API - 本地演示")
    print("🤗 "*20 + "\n")
    
    # 检查 Token
    if not HF_TOKEN:
        print("⚠️  未找到 Hugging Face Token!")
        print("\n请选择以下方法之一设置 Token:\n")
        print("方法 1: 在代码中直接设置")
        print("   编辑此文件,找到 HF_TOKEN = ... 这一行")
        print("   改为: HF_TOKEN = 'hf_your_token_here'\n")
        print("方法 2: 使用环境变量")
        print("   在 PowerShell 中运行:")
        print("   $env:HF_TOKEN = 'hf_your_token_here'\n")
        print("方法 3: 创建 .env 文件")
        print("   在同一目录创建 .env 文件")
        print("   内容: HF_TOKEN=hf_your_token_here\n")
        print("获取 Token: https://huggingface.co/settings/tokens\n")
        
        # 询问是否继续
        choice = input("是否继续使用公开模型? (y/n): ")
        if choice.lower() != 'y':
            print("\n程序退出。")
            return
    
    # 创建客户端
    print("正在创建 Hugging Face 客户端...")
    client = create_client(HF_TOKEN)
    print("✅ 客户端创建成功!\n")
    
    # 运行示例
    try:
        # 示例 1: 基础对话
        example_1_basic_chat(client)
        
        # 示例 2: Lucky Vicky
        example_2_lucky_vicky(client, "今天出門忘記帶傘,結果下大雨")
        
        # 示例 3: 翻译
        example_3_translation(client, "Machine learning is amazing!")
        
        # 示例 4: 情感分析
        example_4_sentiment(client, "這個產品真的太棒了!")
        
        print("\n" + "="*60)
        print("✅ 所有示例运行完成!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ 运行错误: {e}")
        print("\n可能的原因:")
        print("1. Token 无效或已过期")
        print("2. 网络连接问题")
        print("3. API 速率限制")
        print("\n请检查后重试。\n")


# ============================================
# 交互式模式
# ============================================

def interactive_mode():
    """交互式 Lucky Vicky 生成器"""
    print("\n" + "🌈 "*20)
    print("Lucky Vicky 生成器 - 交互模式")
    print("🌈 "*20 + "\n")
    
    if not HF_TOKEN:
        print("❌ 需要 Hugging Face Token 才能使用交互模式")
        print("请先设置 Token (参考上面的说明)")
        return
    
    client = create_client(HF_TOKEN)
    print("✅ 客户端已就绪!\n")
    print("输入发生的事件,我会用 Lucky Vicky 的方式重新诠释!")
    print("输入 'quit' 或 'exit' 退出\n")
    
    while True:
        event = input("📝 发生了什么事? > ")
        
        if event.lower() in ['quit', 'exit', 'q']:
            print("\n再见! 🌈\n")
            break
        
        if not event.strip():
            continue
        
        example_2_lucky_vicky(client, event)


# ============================================
# 程序入口
# ============================================

if __name__ == "__main__":
    import sys
    
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_mode()
    else:
        main()
        
        # 询问是否进入交互模式
        print("\n是否进入交互式 Lucky Vicky 模式? (y/n): ", end="")
        choice = input()
        if choice.lower() == 'y':
            interactive_mode()
