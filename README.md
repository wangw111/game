# 游戏开发智能体

基于Streamlit和Agno的游戏开发智能体，专门用于生成儿童教育游戏。

## 功能特点

- 🎮 **多种游戏类型**：支持数字游戏、汉字游戏、英语游戏
- 🎨 **自定义场景**：根据动作逻辑生成游戏场景
- 🤖 **多AI支持**：集成OpenAI、Qwen、Claude等AI提供商
- 📱 **Web界面**：基于Streamlit的友好用户界面
- 📚 **教育导向**：专门为儿童学习设计

## 快速开始

### 1. 环境要求

- Python 3.7+
- 互联网连接（用于AI服务）

### 2. 安装和运行

```bash
# 克隆或下载项目
cd game

# 运行启动脚本
./start.sh
```

### 3. 配置API密钥

复制 `.env.example` 为 `.env` 并配置至少一个AI提供商的API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# OpenAI配置
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# Anthropic配置
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Qwen配置
QWEN_API_KEY=your_qwen_api_key_here
```

### 4. 访问应用

启动后，浏览器会自动打开 `http://localhost:8501`

## 使用指南

### 数字游戏

1. 选择"数字游戏"类型
2. 输入游戏标题
3. 选择数学运算类型（加法、减法、乘法、除法、混合运算）
4. 设置难度级别和适合年龄
5. 点击"生成数字游戏"
6. 预览游戏内容并下载游戏数据

### 汉字游戏

1. 选择"汉字游戏"类型
2. 输入游戏标题
3. 选择汉字类型（基础汉字、常用词语、成语）
4. 设置难度级别和适合年龄
5. 点击"生成汉字游戏"
6. 预览游戏内容并下载游戏数据

### 英语游戏

1. 选择"英语游戏"类型
2. 输入游戏标题
3. 选择英语学习类型（字母学习、单词记忆、简单对话、语法练习）
4. 设置难度级别和适合年龄
5. 点击"生成英语游戏"
6. 预览游戏内容并下载游戏数据

### 自定义游戏场景

1. 选择"自定义游戏场景"类型
2. 输入游戏标题和描述
3. 详细描述动作逻辑
4. 设置适合年龄
5. 点击"生成自定义游戏"
6. 查看生成的场景设计并下载场景数据

## 项目结构

```
game/
├── app.py                 # 主应用文件
├── requirements.txt       # Python依赖包
├── start.sh              # 启动脚本
├── .env.example          # 环境变量示例
├── config/               # 配置模块
│   ├── __init__.py
│   └── settings.py       # 应用配置
├── agents/               # 智能体模块
│   ├── __init__.py
│   ├── base_agent.py     # 基础智能体
│   └── game_agent.py     # 游戏智能体
├── games/                # 游戏模块
│   ├── __init__.py
│   ├── math_game.py      # 数字游戏生成器
│   ├── chinese_game.py   # 汉字游戏生成器
│   ├── english_game.py   # 英语游戏生成器
│   └── scene_generator.py # 场景生成器
├── utils/                # 工具模块
│   ├── __init__.py
│   ├── logger.py         # 日志工具
│   ├── ai_providers.py   # AI提供商
│   └── ai_manager.py     # AI管理器
├── logs/                 # 日志目录
└── output/               # 输出目录
```

## 技术特性

### AI提供商支持

- **OpenAI**: 支持GPT系列模型
- **Anthropic**: 支持Claude系列模型
- **Qwen**: 支持通义千问系列模型

### 游戏生成功能

- **智能题目生成**: 根据难度和年龄自动生成合适的题目
- **多种题型**: 选择题、填空题、匹配题等
- **自适应难度**: 根据用户表现调整题目难度
- **丰富的反馈**: 即时反馈和奖励机制

### 场景设计功能

- **角色设计**: 自动生成适合的角色设定
- **环境构建**: 根据描述创建游戏环境
- **交互设计**: 设计用户交互方式
- **视听设计**: 提供视觉和音频设计建议

## 开发说明

### 添加新游戏类型

1. 在 `games/` 目录下创建新的游戏生成器
2. 继承基础游戏生成器模式
3. 在 `app.py` 中集成新游戏类型
4. 更新用户界面

### 扩展AI提供商

1. 在 `utils/ai_providers.py` 中添加新的AI提供商类
2. 实现 `AIProvider` 接口
3. 在 `AIProviderManager` 中注册新提供商

### 自定义游戏模板

1. 在 `templates/` 目录下创建游戏模板
2. 定义游戏结构和规则
3. 集成到相应的游戏生成器中

## 许可证

本项目仅供学习和研究使用。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 创建Issue
- 发送邮件
- 提交Pull Request