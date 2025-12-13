"""
检查敏感信息脚本
扫描项目中是否还有真实的 Token
"""

import os
import re

# 要检查的 Token 模式
TOKEN_PATTERN = r'hf_[a-zA-Z0-9]{34}'

# 要扫描的文件类型
FILE_EXTENSIONS = ['.py', '.md', '.txt', '.json', '.yaml', '.yml']

# 排除的目录
EXCLUDE_DIRS = ['.git', '.venv', '__pycache__', 'node_modules']

def scan_file(filepath):
    """扫描单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 查找 Token
        matches = re.findall(TOKEN_PATTERN, content)
        
        if matches:
            return list(set(matches))  # 去重
        return []
        
    except Exception as e:
        return []

def scan_directory(directory='.'):
    """扫描整个目录"""
    findings = {}
    
    for root, dirs, files in os.walk(directory):
        # 排除特定目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            # 检查文件扩展名
            if any(file.endswith(ext) for ext in FILE_EXTENSIONS):
                filepath = os.path.join(root, file)
                tokens = scan_file(filepath)
                
                if tokens:
                    findings[filepath] = tokens
    
    return findings

def main():
    """主函数"""
    print("="*60)
    print("🔍 扫描敏感信息")
    print("="*60)
    print("\n正在扫描项目文件...\n")
    
    findings = scan_directory()
    
    if not findings:
        print("✅ 未发现真实 Token!")
        print("\n项目可以安全上传到 GitHub")
        print("\n下一步:")
        print("1. 运行: git status")
        print("2. 确认 .env 文件不在列表中")
        print("3. 运行: git add .")
        print("4. 运行: git commit -m 'Add project'")
        print("5. 运行: git push origin main")
    else:
        print("⚠️  发现以下文件包含真实 Token:")
        print()
        
        for filepath, tokens in findings.items():
            print(f"📄 {filepath}")
            for token in tokens:
                print(f"   Token: {token[:10]}...")
            print()
        
        print("="*60)
        print("🔧 建议操作")
        print("="*60)
        print("\n1. 运行清理脚本:")
        print("   python clean_tokens.py")
        print("\n2. 或手动编辑上述文件,替换真实 Token")
        print("\n3. 如果已上传到 GitHub:")
        print("   - 立即撤销 Token: https://huggingface.co/settings/tokens")
        print("   - 生成新 Token")
        print("   - 更新 .env 文件")
    
    print("\n" + "="*60)
    print()

if __name__ == "__main__":
    main()
    input("\n按 Enter 键退出...")
