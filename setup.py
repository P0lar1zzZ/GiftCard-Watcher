# setup.py - 这是一个交互式脚本，用来帮你生成后续运行所需的配置文件
import os

def setup():
    # print 就是在屏幕上打出字来，给老大看的提示
    print("--- 🌟 GoogleGiftcard Sniper 自动配置程序 🌟 ---")
    print("请按照提示输入配置信息：\n")
    
    # input 会暂停程序，等待你在键盘上敲字并回车
    # 敲的内容会被存进等号左边的“变量”里
    token = input("1. 请输入您的 Telegram Bot Token: ")
    chat_id = input("2. 请输入您的 Telegram Chat ID: ")
    
    # or "120" 的意思是：如果总裁直接按回车不输入，就默认设置为 120 分钟
    interval = input("3. 监控频率（分钟，建议 120）: ") or "120"
    
    # with open(...) as f 是“打开文件”的标准写法
    # "w" 代表 Write（写入模式），会自动创建或覆盖名为 .env 的文件
    with open(".env", "w") as f:
        # f.write 就是把内容写进文件里
        f.write(f"TG_TOKEN={token}\n")
        f.write(f"CHAT_ID={chat_id}\n")
        f.write(f"INTERVAL={interval}\n")
    
    # 接着我们自动生成 docker-compose.yml，它是 Docker 的启动说明书
    with open("docker-compose.yml", "w") as f:
        # 下面这段三引号里的内容，会原封不动地写进文件
        f.write(f"""
version: '3.8'
services:
  sniper:
    build: .
    container_name: GoogleGiftcard_sniper
    restart: always # 意思是：如果电脑重启了，这个容器也会自动跟着启动
    env_file: .env   # 告诉 Docker 去读刚才生成的那个 .env 文件里的变量
""")
    
    print("\n✅ 配置完成！您现在可以运行 'docker-compose up --build -d' 启动了！")

# 这一行是 Python 的固定写法，意思是：如果这个文件是被直接运行的，就执行 setup() 函数
if __name__ == "__main__":
    setup()
