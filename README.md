# x-poster

一个简单而强大的 X (Twitter) 自动发布工具。

## 功能特点

- 自动从 `xfile` 目录随机选择 Markdown 文件
- 智能追踪已发布文件，避免重复发布
- 可配置的发布时间间隔
- 支持添加时间戳和话题标签
- 完整的日志记录

## 安装

1. 克隆项目到本地
2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置

1. 复制 `.env` 文件并填入你的 Twitter API 凭证：
   - TWITTER_API_KEY
   - TWITTER_API_SECRET
   - TWITTER_ACCESS_TOKEN
   - TWITTER_ACCESS_TOKEN_SECRET
   - TWITTER_BEARER_TOKEN

2. 在 `settings.json` 中配置：
   - 发布时间间隔
   - 工作时间段
   - 时区设置
   - 内容格式选项
   - 文件目录设置

## 使用方法

1. 在 `xfile` 目录中放入要发布的 Markdown 文件
2. 运行程序：
```bash
python main.py
```

## 日志

程序运行日志保存在 `bot.log` 文件中，使用 JSON 格式记录所有操作和错误信息。

## 已发布历史

已发布的文件记录保存在 `posted_history.json` 中，避免重复发布。
