

# GiftCard-Watcher

基于 Playwright + Docker 的轻量化自动监控方案。支持全平台部署（macOS arm/intel, Windows, Linux）。

感谢伟大的gemini的帮助。
所有代码都做了注释，发生问题的时候可以检查一下代码或者把报错发给ai问问ai。

---

## 核心逻辑
通过 Docker 运行 Chromium 浏览器，模拟真实用户访问目标页面。发现价格变动或符合预期时，通过 Telegram Bot 实时推送通知。

---

## 🛠️ 安装全流程

### 1. 环境准备
- **下载 Docker Desktop**：访问 [Docker 官网](https://www.docker.com/products/docker-desktop/)，根据你的操作系统下载并安装。安装后确保 Docker 已启动。

### 2. 获取 Telegram 推送凭证
1. 在 Telegram 搜索并关注 `@BotFather`。
2. 发送 `/newbot` 指令，按照提示为机器人起名，获取 **API TOKEN**。
3. 搜索并关注 `@userinfobot`，获取你的 **Chat ID** (一串数字)。
4. **重要**：先给你的 Bot 发送一条任意消息以激活对话。

### 3. 项目配置
1. 将本项目所有文件下载至本地同一文件夹。
2. 在该文件夹内新建一个文本文件，重命名为 `.env` (注意前面的点，不要有 .txt 后缀)。
3. 将以下内容粘贴进 `.env` 文件并保存：
   ```env
   API_TOKEN=你的Token
   CHAT_ID=你的数字ID
   CHECK_INTERVAL=120

### 4. 一键部署
1.打开终端 (macOS) 或 PowerShell (Windows)。
2.使用 cd 命令进入该项目文件夹。
3.执行命令`docker-compose up -d`

注：首次运行会下载约 4GB 的环境镜像，请耐心等待。

## 进阶说明
• 跨架构适配：已完美适配 Apple Silicon (M1/M2/M3/M4) 及传统 Intel/AMD 处理器。
• 资源占用：镜像较大是因为包含了完整的浏览器内核以绕过反爬虫，实际运行仅占用约 300MB 运存。
• 配置热更新：修改 monitor.py 后，执行 docker-compose up -d --build 即可应用更改。

## ⚠️免责声明
本工具仅供技术研究及学习使用。使用者因不当利用本工具进行违法操作或违反目标平台服务条款而导致的任何后果（如封号、法律责任等），由使用者自行承担，开发者概不负责。

