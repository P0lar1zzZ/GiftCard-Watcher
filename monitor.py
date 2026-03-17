# monitor.py - 它是整个项目的核心，负责读取配置、访问亚马逊并发送 Telegram 提醒
import os
import asyncio
import time
from playwright.async_api import async_playwright # 引入模拟浏览器的“高级间谍”
from telegram import Bot # 引入发消息的机器人
from dotenv import load_dotenv # 引入读取配置文件的工具

# load_dotenv 会去寻找同文件夹下的 .env 文件，并把里面的 Token 读出来
load_dotenv()

# 从环境变量（也就是 .env 里）拿走老大刚才填的信息
TG_TOKEN = os.getenv('TG_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
# 如果没设频率，默认 120 分钟检查一次
INTERVAL = int(os.getenv('INTERVAL', 120)) * 60

# --- 定义：发送消息的功能 ---
async def send_msg(text):
    # 用你的 Token 初始化机器人
    bot = Bot(token=TG_TOKEN)
    # await 的意思是：发消息需要时间，程序会在这里等一下直到发成功
    await bot.send_message(chat_id=CHAT_ID, text=text)

# --- 定义：检查亚马逊的功能 ---
async def check_amazon():
    # 启动浏览器引擎（playwright）
    async with async_playwright() as p:
        # headless=True 意思是：在后台悄悄跑，不弹出浏览器窗口
        browser = await p.chromium.launch(headless=True)
        # 创建一个新页面，就像你在 Chrome 里点“新建标签页”
        page = await browser.new_page()
        
        # 亚马逊搜索“Google Play 礼品卡 数字版”的链接
        url = "https://www.amazon.com/s?k=Google+Play+Gift+Card+Digital"
        
        print(f"[{time.strftime('%H:%M:%S')}] 老大，侦察兵正在前往亚马逊...")
        # 让浏览器跳到这个 URL
        await page.goto(url)
        
        # 获取网页里的所有文字内容
        content = await page.content()
        
        # 逻辑判断：如果页面出现了“Deal”（优惠）或“Discount”（折扣）
        if "Deal" in content or "Discount" in content or "off" in content:
            print("🚨 发现情况！正在给总裁发报...")
            await send_msg(f"🌟 老大！亚马逊礼品卡疑似有促销活动啦！\n链接: {url}")
        else:
            print("💤 风平浪静，暂无促销。")
            
        # 任务完成，关闭浏览器节省 M4 的内存
        await browser.close()

# --- 主程序：让它一直循环跑下去 ---
async def main():
    print("🚀 GoogleGiftcard Sniper 已成功启动！正在守护您的 Ultra 梦想...")
    while True:
        try:
            # 执行一次检查
            await check_amazon()
        except Exception as e:
            # 万一断网了或者出错了，打印出报错，防止程序崩溃
            print(f"⚠️ 哎呀出错了: {e}")
        
        # 休息设定的时间，然后再次出发
        await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    # 启动异步主程序
    asyncio.run(main())
