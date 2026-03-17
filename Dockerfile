# Dockerfile - 就像一份食谱，告诉电脑怎么“烹饪”这个运行环境

# 1. 基础镜像：用微软提供的官方 Playwright 镜像（它里面已经装好了 Python 和各种浏览器依赖）
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# 2. 设置工作目录：在容器内部创建一个叫 /app 的文件夹，咱们的代码都放这
WORKDIR /app

# 3. 复制菜单：把咱们写好的依赖清单 requirements.txt 考进去
COPY requirements.txt .

# 4. 安装插件：用 pip 安装那些 Python 库
# --no-cache-dir 意思是：装完别留垃圾，让镜像尽量瘦一点
RUN pip install --no-cache-dir -r requirements.txt

# 5. 安装浏览器：Playwright 特有的步骤，安装 Chromium 浏览器内核
RUN playwright install chromium

# 6. 复制源码：把当前文件夹下剩下的所有代码（monitor.py 等）全部拷贝进去
COPY . .

# 7. 启动指令：当容器启动时，执行 monitor.py 这个文件
CMD ["python", "monitor.py"]
