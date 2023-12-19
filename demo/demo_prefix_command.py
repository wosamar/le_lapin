# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands

from settings import Settings

settings = Settings()

# intents是要求機器人的權限
intents = discord.Intents.all()
# command_prefix是前綴符號，可以自由選擇($, #, &...)
bot = commands.Bot(command_prefix="%", intents=intents)


# @commands.Cog.listener()
@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")


# @commands.command()
@bot.command()
# 輸入%Hello呼叫指令
async def hello(ctx):
    # 回覆Hello, world!
    await ctx.send("Hello, world!")


bot.run(settings.BOT_TOKEN)
