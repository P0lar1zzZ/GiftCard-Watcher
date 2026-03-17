import os
import asyncio
import time
from datetime import datetime, timedelta, timezone
from playwright.async_api import async_playwright
from telegram import Bot
from dotenv import load_dotenv

# 1. 载入配置
load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
INTERVAL_MIN = int(os.getenv('INTERVAL', 120))
INTERVAL = INTERVAL_MIN * 60

# --- 小工具：获取北京时间字符串 ---
def get_beijing_time():
    # 强制获取东八区时间
    tz = timezone(timedelta(hours=8))
    return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

# --- 定义：发送消息的功能 ---
async def send_msg(text):
    try:
        if not TG_TOKEN or not CHAT_ID:
            print(f"[{get_beijing_time()}] ❌ 错误：未在 .env 中找到配置！")
            return
        bot = Bot(token=TG_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=text)
        print(f"[{get_beijing_time()}] ✅ Telegram 消息已送达")
    except Exception as e:
        print(f"[{get_beijing_time()}] ❌ 消息发送失败: {e}")

# --- 定义：核心监控逻辑 ---
async def check_amazon():
    async with async_playwright() as p:
        # 加上 User-Agent 伪装，防止被亚马逊拦截
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # 搜索链接
        url = "https://www.amazon.com/s?k=Google+Play+Gift+Card+Digital"
        
        print(f"[{get_beijing_time()}] 侦察兵正在前往亚马逊...")
        
        try:
            # 增加超时到 60 秒，并等待网络静默
            await page.goto(url, wait_until="networkidle", timeout=60000)
            
            # --- 亲自扒出来的“狙击逻辑” ---
            
            # 1. 检查限时秒杀标签 (Limited time deal)
            limited_deal = await page.query_selector(".a-badge-text:has-text('Limited time deal')")
            
            # 2. 检查额外优惠券 (Extra % off / Coupon)
            # 使用老大定位的绿色高亮类名
            coupon = await page.query_selector(".s-coupon-highlight-color")
            
            # 3. 检查划线价 (List Price)
            # 只要源码里出现了带 "List:" 的隐藏标签，说明现在有折扣
            list_price = await page.query_selector("span.a-offscreen:has-text('List:')")

            if limited_deal or coupon or list_price:
                reason = "🔥 发现限时秒杀！" if limited_deal else ("🟢 发现额外优惠券！" if coupon else "📉 发现价格直降！")
                print(f"[{get_beijing_time()}] 🚨 {reason}")
                await send_msg(f"🌟 老大！真正的促销出现了！\n原因：{reason}\n链接: {url}")
            else:
                print(f"[{get_beijing_time()}] 💤 排除干扰，暂无真实折扣。")
                
        except Exception as e:
            print(f"[{get_beijing_time()}] ❌ 侦察任务失败: {e}")
            
        await browser.close()

# --- 主程序 ---
async def main():
    print(f"🚀 GoogleGiftcard Sniper 已成功启动！")
    print(f"📍 监控频率：每 {INTERVAL_MIN} 分钟巡逻一次")
    
    await send_msg("🫡 老大好！狙击手已在 Docker 阵地就位，正在用北京时间巡逻！")
    
    while True:
        try:
            await check_amazon()
        except Exception as e:
            print(f"⚠️ 循环任务报错: {e}")
        
        # 计算下次巡逻的北京时间
        next_ts = datetime.now(timezone(timedelta(hours=8))) + timedelta(seconds=INTERVAL)
        print(f"😴 进入休眠，下次巡逻时间：{next_ts.strftime('%H:%M:%S')}")
        await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
