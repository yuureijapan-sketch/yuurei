import discord
from discord.ext import commands
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import os


# Render用のダミーサーバー（これがないとRenderに止められます）
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    httpd = HTTPServer(('0.0.0.0', 8080), MyHandler)
    httpd.serve_forever()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

NOTIFICATION_CHANNEL_ID = 1492506054851039283   # あなたのID
MONITOR_CHANNEL_ID = 1492487369679572992     # あなたのID

@bot.event
async def on_ready():
    print(f'ログインしました: {bot.user}')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != MONITOR_CHANNEL_ID: return
    if payload.user_id == bot.user.id: return
    notif_channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
    if notif_channel is None: return
    try:
        origin_channel = bot.get_channel(payload.channel_id)
        origin_msg = await origin_channel.fetch_message(payload.message_id)
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        content = origin_msg.content if origin_msg.content else "(画像等)"
        msg = f"誰が：{member.display_name}さん\nギルド：{content}"
        await notif_channel.send(msg)
    except Exception as e:
        print(f"Error: {e}")

# ダミーサーバーを別スレッドで起動
threading.Thread(target=run_server, daemon=True).start()

# ボット起動
import os
# 直接トークンを書かずに、Renderの設定（DISCORD_TOKEN）を読み込む
bot.run(os.getenv('DISCORD_TOKEN'))


