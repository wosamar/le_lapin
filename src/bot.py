import os
import asyncio
import discord
from discord.ext import commands

from settings import Settings, BASE_PATH

settings = Settings()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)


# 當機器人完成啟動時
@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")


# 重新載入所有Cog檔案
@bot.command()
async def reload_all(ctx):
    await load_extensions()
    await ctx.send("Reload all done.")


# 載入指令程式檔案
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")


# 卸載指令檔案
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")


# 重新載入程式檔案
@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")


# 一開始bot開機需載入全部程式檔案
async def load_extensions():
    path = BASE_PATH / "src" / "cogs"
    for filename in os.listdir(path):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")


async def start_bot():
    async with bot:
        await load_extensions()
        await bot.start(settings.DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(start_bot())
