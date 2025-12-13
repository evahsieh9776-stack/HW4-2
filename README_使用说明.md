# 🎯 Hugging Face 学习资料包 - 使用说明

## 📦 文件清单

您的 HW4 文件夹现在包含以下文件:

```
HW4/
├── 【HW4】用AISuite打造員瑛式思考生成器.ipynb  (原有文件)
├── HuggingFace_使用指南.md                    (详细教程)
├── HuggingFace_快速参考.txt                   (速查手册)
├── huggingface_demo.py                        (完整示例代码)
└── notebook_cells.py                          (Notebook Cell 代码)
```

---

## 🚀 快速开始指南

### 步骤 1: 获取 Hugging Face Token

1. 访问 https://huggingface.co/settings/tokens
2. 点击 "New token"
3. 选择 "Read" 权限
4. 复制生成的 token (格式: `hf_xxxxxxxxxxxxx`)

### 步骤 2: 在 Google Colab 中设置

1. 打开您的 Notebook: `【HW4】用AISuite打造員瑛式思考生成器.ipynb`
2. 点击左侧的 🔑 图标 (Secrets)
3. 添加新的 Secret:
   - **Name**: `HuggingFace`
   - **Value**: 粘贴您的 token
4. 点击保存

### 步骤 3: 运行代码

#### 方法 A: 使用 notebook_cells.py (推荐)

1. 打开 `notebook_cells.py`
2. 复制每个 Cell 的代码到您的 Notebook
3. 按顺序运行:
   - Cell 1: 安装库
   - Cell 2: 设置客户端
   - Cell 3: 测试连接
   - Cell 4: Lucky Vicky 函数
   - Cell 5: 测试示例
   - Cell 7: 启动 Gradio App

#### 方法 B: 直接导入 Python 模块

```python
# 在 Notebook 中运行
!pip install huggingface_hub

# 导入示例代码
import sys
sys.path.append('/content/drive/MyDrive/HW4')  # 根据实际路径调整

from huggingface_demo import *

# 创建客户端
from google.colab import userdata
hf_token = userdata.get('HuggingFace')
client = create_hf_client(hf_token)

# 运行示例
example_3_lucky_vicky(client, "今天咖啡灑了")
```

---

## 📚 文件详细说明

### 1. HuggingFace_使用指南.md

**用途**: 完整的学习教程

**内容**:
- 安装与设置步骤
- 获取 API Token 指南
- 6 个完整示例
- Gradio App 集成
- 推荐模型列表
- 使用技巧和最佳实践

**适合**: 第一次学习 Hugging Face 的用户

**如何使用**:
- 在 VS Code 或任何 Markdown 编辑器中打开
- 按照步骤逐步学习
- 复制代码到 Notebook 测试

---

### 2. HuggingFace_快速参考.txt

**用途**: 快速查找常用代码

**内容**:
- 常用代码片段
- 参数说明
- 模型对比表
- 常见问题解答

**适合**: 已经熟悉基础,需要快速查找代码的用户

**如何使用**:
- 用记事本或任何文本编辑器打开
- 搜索需要的功能 (Ctrl+F)
- 复制粘贴代码片段

---

### 3. huggingface_demo.py

**用途**: 完整的 Python 示例模块

**内容**:
- 6 个独立的示例函数
- 详细的注释说明
- 可以直接导入使用

**适合**: 想要模块化使用的用户

**如何使用**:

```python
# 方法 1: 在 Notebook 中导入
from huggingface_demo import *

# 创建客户端
client = create_hf_client(token="your_token")

# 使用各种示例
example_1_text_generation(client)
example_2_chat_completion(client)
example_3_lucky_vicky(client, "今天遲到了")

# 方法 2: 运行所有示例
run_all_examples(token="your_token")
```

---

### 4. notebook_cells.py

**用途**: 可以直接复制到 Notebook 的 Cell 代码

**内容**:
- 8 个独立的 Cell
- 从安装到完整 Gradio App
- 包含测试和示例

**适合**: 想要在 Jupyter Notebook 中逐步运行的用户

**如何使用**:
1. 打开 `notebook_cells.py`
2. 找到对应的 Cell (例如: Cell 1, Cell 2...)
3. 复制整个 Cell 的代码
4. 粘贴到 Notebook 的新 Cell 中
5. 运行

**Cell 说明**:
- **Cell 1**: 安装 huggingface_hub
- **Cell 2**: 导入库并创建客户端
- **Cell 3**: 简单测试
- **Cell 4**: Lucky Vicky 函数定义
- **Cell 5**: 测试多个示例
- **Cell 6**: 多提供商版本
- **Cell 7**: Gradio App (完整界面)
- **Cell 8**: 其他实用功能

---

## 🎯 推荐学习路径

### 初学者路径

1. **阅读** `HuggingFace_使用指南.md` (15分钟)
2. **获取** Hugging Face Token
3. **运行** `notebook_cells.py` 的 Cell 1-3 (测试连接)
4. **尝试** Cell 4-5 (Lucky Vicky)
5. **启动** Cell 7 (Gradio App)

### 快速上手路径

1. **查看** `HuggingFace_快速参考.txt`
2. **复制** 基础设置代码
3. **复制** Lucky Vicky 代码片段
4. **直接运行**

### 深度学习路径

1. **研究** `huggingface_demo.py` 的源代码
2. **理解** 每个函数的实现
3. **修改** 参数进行实验
4. **创建** 自己的自定义函数

---

## 💡 实用技巧

### 技巧 1: 快速切换模型

```python
# 在 notebook_cells.py 的 Cell 7 中
# 修改 model 参数即可切换:

# 快速但简单
model="Qwen/Qwen2.5-1.5B-Instruct"

# 平衡性能 (推荐)
model="Qwen/Qwen2.5-7B-Instruct"

# 最强性能
model="Qwen/Qwen2.5-72B-Instruct"
```

### 技巧 2: 调整创意程度

```python
# 在 lucky_post_hf 函数中调整 temperature:

# 更一致的回复
temperature=0.3

# 平衡 (推荐)
temperature=0.7

# 更有创意
temperature=0.9
```

### 技巧 3: 错误处理

```python
try:
    result = lucky_post_hf(event)
except Exception as e:
    print(f"Hugging Face 错误: {e}")
    # 自动切换到 Groq
    result = reply(system=system, prompt=event, 
                  provider="groq", model="openai/gpt-oss-120b")
```

---

## 🔧 常见问题解决

### 问题 1: "No module named 'huggingface_hub'"

**解决**:
```python
!pip install huggingface_hub
```

### 问题 2: "Invalid token"

**解决**:
1. 检查 Token 是否正确复制
2. 确保 Token 有 "Read" 权限
3. 重新生成 Token

### 问题 3: "Rate limit exceeded"

**解决**:
1. 等待几分钟后重试
2. 使用较小的模型
3. 考虑升级到付费计划

### 问题 4: 响应太慢

**解决**:
1. 使用 1.5B 或 7B 模型
2. 减少 max_tokens
3. 或切换到 Groq (更快)

---

## 🎨 自定义示例

### 示例 1: 创建自己的提示词

```python
def my_custom_generator(event):
    my_system = """你是一个幽默的作家。
请用搞笑的方式重新描述用户的经历,
加入夸张的比喻和有趣的emoji。"""
    
    messages = [
        {"role": "system", "content": my_system},
        {"role": "user", "content": event}
    ]
    
    response = client.chat_completion(
        messages=messages,
        model="Qwen/Qwen2.5-7B-Instruct",
        max_tokens=300
    )
    
    return response.choices[0].message.content
```

### 示例 2: 批量处理

```python
events = [
    "今天咖啡灑了",
    "出門忘記帶傘",
    "考試考得不好"
]

results = []
for event in events:
    result = lucky_post_hf(event)
    results.append(result)
    print(f"處理: {event}")
    print(f"結果: {result}\n")
```

---

## 📊 性能对比

| 提供商 | 模型 | 速度 | 中文能力 | 免费额度 |
|--------|------|------|----------|----------|
| Hugging Face | Qwen 2.5-7B | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 有限制 |
| Groq | GPT-OSS-120B | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 较多 |
| OpenAI | GPT-4o | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 需付费 |

**建议**:
- 开发测试: Hugging Face (免费)
- 生产环境: Groq (快速) 或 OpenAI (质量高)
- Lucky Vicky: Hugging Face Qwen 2.5-7B (中文最佳)

---

## 🚀 下一步

### 完成基础后,您可以:

1. **部署到 Hugging Face Spaces**
   ```bash
   gradio deploy
   ```

2. **创建自己的模型微调**
   - 收集数据
   - 使用 transformers 训练
   - 上传到 Hugging Face Hub

3. **集成更多功能**
   - 图像生成
   - 语音识别
   - 多模态应用

4. **优化性能**
   - 使用缓存
   - 批量处理
   - 异步调用

---

## 📞 获取帮助

- **Hugging Face 文档**: https://huggingface.co/docs
- **社区论坛**: https://discuss.huggingface.co
- **Discord**: https://discord.gg/hugging-face

---

## ✅ 检查清单

在开始之前,确保您已经:

- [ ] 注册 Hugging Face 账号
- [ ] 获取 API Token
- [ ] 在 Colab 中添加 Secret
- [ ] 安装 huggingface_hub
- [ ] 测试基础连接
- [ ] 运行 Lucky Vicky 示例
- [ ] 启动 Gradio App

---

## 🎉 总结

您现在拥有:

1. ✅ 完整的学习指南
2. ✅ 快速参考手册
3. ✅ 可运行的示例代码
4. ✅ Notebook Cell 代码
5. ✅ Lucky Vicky 集成方案

**开始您的 Hugging Face 之旅吧!** 🚀

有任何问题,随时查阅这些文档或询问我! 😊
