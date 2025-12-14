"""
員瑛式思考生成器 - Streamlit 簡化版
用於測試部署
"""

import streamlit as st

# 頁面配置
st.set_page_config(
    page_title="Lucky Vicky 測試",
    page_icon="🌈",
    layout="wide"
)

# 標題
st.title("🌈 Lucky Vicky - 員瑛式思考生成器")
st.subheader("測試版本")

# 檢查 Token
token_status = "❌ 未配置"
try:
    token = st.secrets["HF_TOKEN"]
    if token:
        token_status = f"✅ Token 已配置 ({token[:10]}...)"
except:
    token_status = "❌ 無法讀取 Token"

st.info(token_status)

# 測試功能
st.write("---")
st.write("### 測試區域")

test_input = st.text_area("輸入測試文字", "這是測試")

if st.button("測試按鈕"):
    st.success(f"✅ 按鈕正常工作! 你輸入了: {test_input}")

# 顯示環境資訊
with st.expander("環境資訊"):
    import sys
    st.write(f"Python 版本: {sys.version}")
    st.write(f"Streamlit 版本: {st.__version__}")
    
st.write("---")
st.write("如果你看到這個頁面,表示 Streamlit 應用已成功部署! 🎉")
