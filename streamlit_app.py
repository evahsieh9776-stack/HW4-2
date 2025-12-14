"""
員瑛式思考生成器 - Streamlit Web App
使用 Hugging Face Inference API
"""

import streamlit as st
from huggingface_hub import InferenceClient
import os

# ============================================
# 頁面配置
# ============================================

st.set_page_config(
    page_title="員瑛式思考生成器 - Lucky Vicky",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 自定義 CSS
# ============================================

st.markdown("""
<style>
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0.2em;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.3em;
        margin-bottom: 2em;
    }
    
    .stTextArea textarea {
        font-size: 1.1em;
    }
    
    .output-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2em;
        border-radius: 15px;
        margin-top: 1em;
        font-size: 1.1em;
        line-height: 1.8;
    }
    
    .footer {
        text-align: center;
        margin-top: 3em;
        padding: 2em;
        color: #888;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# Token 配置
# ============================================

@st.cache_resource
def get_hf_client():
    """獲取 Hugging Face 客戶端"""
    # 優先從 Streamlit secrets 讀取
    hf_token = None
    
    if hasattr(st, 'secrets') and 'HF_TOKEN' in st.secrets:
        hf_token = st.secrets['HF_TOKEN']
    else:
        # 從環境變數讀取
        hf_token = os.getenv('HF_TOKEN')
        
        # 從 .env 文件讀取
        if not hf_token:
            try:
                with open('.env', 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('HF_TOKEN='):
                            hf_token = line.strip().split('=', 1)[1]
                            break
            except FileNotFoundError:
                pass
    
    if hf_token:
        return InferenceClient(token=hf_token), True
    else:
        return None, False

client, token_available = get_hf_client()

# ============================================
# Lucky Vicky 生成函數
# ============================================

def generate_lucky_vicky(event, model_choice):
    """生成員瑛式思考貼文"""
    
    if not event or not event.strip():
        return "❌ 請輸入發生的事件!"
    
    system_prompt = """請用台灣習慣的中文來寫這段 po 文:
請用員瑛式思考, 也就是什麼都正向思維任何使用者寫的事情,
用我的第一人稱、社群媒體 po 文的口吻說一次,
說為什麼這是一件超幸運的事, 並且以「完全是 Lucky Vicky 呀!」結尾。
可以適度的加上 emoji。"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": event}
    ]
    
    # 模型映射
    model_map = {
        "Meta Llama 3.2-3B (推薦)": "meta-llama/Llama-3.2-3B-Instruct",
        "Meta Llama 3.2-1B": "meta-llama/Llama-3.2-1B-Instruct",
        "Microsoft Phi-3": "microsoft/Phi-3-mini-4k-instruct"
    }
    
    model = model_map.get(model_choice, "meta-llama/Llama-3.2-3B-Instruct")
    
    try:
        if not client:
            return "❌ 錯誤: 未配置 Hugging Face Token\n\n請在 Streamlit Cloud Secrets 中設置 HF_TOKEN"
        
        with st.spinner('🤔 Lucky Vicky 正在思考中...'):
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
            return f"❌ 模型 '{model_choice}' 在免費帳戶中不可用\n\n💡 建議:\n1. 嘗試其他模型\n2. 升級 Hugging Face 帳戶"
        elif "401" in error_msg or "Invalid token" in error_msg:
            return "❌ Token 無效或已過期\n\n請檢查:\n1. Token 是否正確\n2. Token 是否有 'Read' 權限\n3. 在 https://huggingface.co/settings/tokens 重新生成"
        else:
            return f"❌ 錯誤: {error_msg}\n\n💡 可能的原因:\n1. 網路連接問題\n2. API 速率限制\n3. 模型暫時不可用"

# ============================================
# 主界面
# ============================================

# 標題
st.markdown('<h1 class="main-title">🌈 員瑛式思考生成器</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Lucky Vicky - 把任何事情都變成幸運的事!</p>', unsafe_allow_html=True)

# Token 狀態提示
if token_available:
    st.success("✅ Hugging Face Token 已配置")
else:
    st.error("⚠️ 未找到 Hugging Face Token - 請在 Streamlit Cloud Secrets 中設置 HF_TOKEN")

# 側邊欄 - 使用說明
with st.sidebar:
    st.header("📖 使用說明")
    
    st.markdown("""
    ### 什麼是員瑛式思考?
    
    員瑛式思考是一種超級正向的思維方式,能把任何看似倒楣的事情,
    重新詮釋成幸運的事件!
    
    ### 如何使用?
    
    1. 在右側輸入框中描述發生的事情
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
    
    st.divider()
    
    st.markdown("### 💡 範例事件")
    examples = [
        "今天咖啡灑到電腦上了!",
        "出門忘記帶傘,結果下大雨",
        "考試考得不太好",
        "今天遲到了10分鐘",
        "手機掉到水裡了"
    ]
    
    for example in examples:
        if st.button(example, key=f"example_{example}", use_container_width=True):
            st.session_state.event_input = example

# 主要內容區域
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 發生了什麼事?")
    
    # 使用 session_state 來保存輸入
    if 'event_input' not in st.session_state:
        st.session_state.event_input = ""
    
    event_input = st.text_area(
        label="輸入事件",
        value=st.session_state.event_input,
        placeholder="例如:今天出門就下大雨,可是忘了帶傘...",
        height=200,
        label_visibility="collapsed"
    )
    
    st.subheader("🤖 選擇 AI 模型")
    model_choice = st.selectbox(
        label="模型選擇",
        options=[
            "Meta Llama 3.2-3B (推薦)",
            "Meta Llama 3.2-1B",
            "Microsoft Phi-3"
        ],
        label_visibility="collapsed"
    )
    
    generate_button = st.button("✨ 生成 Lucky Vicky 貼文", type="primary", use_container_width=True)

with col2:
    st.subheader("📣 員瑛式貼文")
    
    # 輸出區域
    output_container = st.container()
    
    if generate_button:
        if event_input:
            result = generate_lucky_vicky(event_input, model_choice)
            
            with output_container:
                st.markdown(f'<div class="output-box">{result}</div>', unsafe_allow_html=True)
                
                # 複製按鈕
                st.button("📋 複製貼文", key="copy_button")
        else:
            with output_container:
                st.warning("⚠️ 請先輸入發生的事件!")
    else:
        with output_container:
            st.info("👈 在左側輸入事件,然後點擊生成按鈕")

# 頁腳
st.markdown("""
<div class="footer">
    <p>🤗 Powered by Hugging Face Inference API</p>
    <p>💡 提示: 如果遇到問題,請檢查 Token 配置或嘗試其他模型</p>
    <p>📚 更多資訊請查看專案文檔</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# 會話狀態管理
# ============================================

# 初始化會話狀態
if 'generated_count' not in st.session_state:
    st.session_state.generated_count = 0

if generate_button and event_input:
    st.session_state.generated_count += 1
    
# 顯示統計
with st.sidebar:
    st.divider()
    st.metric("已生成貼文數", st.session_state.generated_count)
