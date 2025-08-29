#!/bin/bash

# 游戏开发智能体启动脚本

echo "🎮 游戏开发智能体启动中..."

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查是否存在虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔄 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📚 安装依赖包..."
pip install -r requirements.txt

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到.env文件，请复制.env.example并配置API密钥"
    echo "📝 配置说明："
    echo "   1. 复制配置文件: cp .env.example .env"
    echo "   2. 编辑.env文件，填入相应的AI提供商API密钥"
    echo "   3. 至少需要配置一个AI提供商的API密钥"
    echo ""
    echo "🔑 支持的AI提供商："
    echo "   - OpenAI (OPENAI_API_KEY)"
    echo "   - Anthropic (ANTHROPIC_API_KEY)"
    echo "   - Qwen (QWEN_API_KEY)"
    exit 1
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p logs
mkdir -p output

# 启动应用
echo "🚀 启动Streamlit应用..."
streamlit run app.py --server.port=8501 --server.address=0.0.0.0