# DeepSeek CLI Chat

一个基于 DeepSeek API 的简单命令行对话工具，让您可以通过终端与 AI 进行交互对话。

## ✨ 特性

- 🚀 **简单易用**: 纯命令行界面，启动即用
- 🔧 **配置灵活**: 独立的配置文件管理 API 密钥和参数
- 📝 **提示词管理**: 可自定义系统提示词，定制 AI 行为
- 💬 **多轮对话**: 支持上下文记忆的连续对话
- 🛡️ **安全设计**: API 密钥安全存储，不会泄露到版本控制
- 📊 **状态监控**: 实时显示响应时间和 token 使用情况

## 📋 系统要求

- Python 3.6 或更高版本
- 有效的 DeepSeek API 密钥
- 网络连接

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API 密钥

```bash
# 复制配置文件模板
cp config.json.example config.json

# 编辑配置文件，设置您的 API 密钥
# 在 config.json 中将 "your-deepseek-api-key-here" 替换为您的实际 API 密钥
```

### 3. 运行程序

```bash
python main.py
```

## 📁 项目结构

```
deepseek-cli-chat/
├── main.py                 # 主程序入口
├── config.py               # 配置管理模块
├── api_client.py           # DeepSeek API 客户端
├── prompt_manager.py       # 系统提示词管理
├── config.json.example     # 配置文件示例
├── config.json            # 实际配置文件（需要创建）
├── prompts/               # 提示词目录
│   └── system.txt         # 默认系统提示词
├── requirements.txt       # Python 依赖
├── README.md             # 项目说明
├── PRD.md                # 产品需求文档
└── .gitignore            # Git 忽略文件
```

## ⚙️ 配置说明

### config.json 配置文件

```json
{
  "deepseek": {
    "api_key": "your-deepseek-api-key-here",
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat",
    "max_tokens": 2000,
    "temperature": 0.7
  },
  "app": {
    "system_prompt_file": "prompts/system.txt",
    "max_history": 10
  }
}
```

**配置项说明:**

- `api_key`: 您的 DeepSeek API 密钥
- `base_url`: API 基础 URL（通常不需要修改）
- `model`: 使用的模型名称
- `max_tokens`: 单次回复的最大 token 数
- `temperature`: 回复的随机性（0-1，越高越随机）
- `system_prompt_file`: 系统提示词文件路径
- `max_history`: 保留的最大对话历史数

### 系统提示词

编辑 `prompts/system.txt` 文件可以自定义 AI 的行为风格：

```
你是一个有用的AI助手，请用简洁明了的方式回答用户的问题。
```

## 🎮 使用方法

### 基本对话

启动程序后，直接输入问题即可开始对话：

```
💭 您: 你好！
🤖 AI: 你好！我是 DeepSeek AI 助手，很高兴为您服务。有什么我可以帮助您的吗？
```

### 内置命令

程序支持以下内置命令：

- `help` - 显示帮助信息
- `clear` - 清空对话历史
- `history` - 显示对话统计信息
- `reload` - 重新加载系统提示词
- `quit` / `exit` / `q` - 退出程序

### 使用示例

```bash
💭 您: 解释一下什么是机器学习
🤖 AI: 机器学习是人工智能的一个分支...

💭 您: history
📊 对话统计:
  总消息数: 4
  用户消息: 2
  AI回复: 1
  系统消息: 1
  最大历史: 10

💭 您: clear
🗑️ 对话历史已清空

💭 您: quit
👋 感谢使用 DeepSeek CLI Chat，再见！
```

## 🔧 高级用法

### 自定义提示词

1. 编辑 `prompts/system.txt` 文件
2. 在程序中使用 `reload` 命令重新加载

### 调整 API 参数

编辑 `config.json` 文件中的参数：

- 调高 `temperature` 获得更有创意的回复
- 调高 `max_tokens` 获得更长的回复
- 调整 `max_history` 控制上下文记忆长度

## 🛠️ 开发说明

### 模块说明

- **config.py**: 负责配置文件的读取、验证和管理
- **prompt_manager.py**: 管理系统提示词的加载和更新
- **api_client.py**: 封装 DeepSeek API 调用逻辑
- **main.py**: 主程序，整合所有模块并提供 CLI 界面

### 扩展开发

项目采用模块化设计，易于扩展：

1. **添加新的 AI 模型**: 修改 `api_client.py`
2. **增强 CLI 界面**: 修改 `main.py`
3. **添加新功能**: 创建新模块并在 `main.py` 中集成

### 测试

每个模块都包含测试代码，可以单独运行：

```bash
python config.py          # 测试配置管理
python prompt_manager.py  # 测试提示词管理
python api_client.py      # 测试 API 客户端
```

## 🔒 安全注意事项

1. **API 密钥安全**: 
   - 不要将 `config.json` 提交到版本控制系统
   - 定期更换 API 密钥
   - 不要在公共场所展示包含密钥的配置文件

2. **网络安全**:
   - 确保网络连接安全
   - 注意 API 调用频率限制

## 🐛 故障排除

### 常见问题

**Q: 提示 "配置文件不存在"**
A: 请确保已复制 `config.json.example` 为 `config.json`

**Q: 提示 "API密钥无效"**
A: 请检查 `config.json` 中的 API 密钥是否正确

**Q: 网络连接失败**
A: 请检查网络连接和防火墙设置

**Q: 程序启动失败**
A: 请确保 Python 版本 >= 3.6 且已安装所需依赖

### 获取帮助

如果遇到问题，可以：

1. 查看程序输出的错误信息
2. 检查配置文件格式是否正确
3. 确认 API 密钥和网络连接
4. 查看 [DeepSeek API 文档](https://platform.deepseek.com/docs)

## 📄 许可证

本项目仅供学习和个人使用。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

---

**享受与 AI 的对话吧！** 🎉