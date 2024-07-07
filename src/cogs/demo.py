import discord
from discord.ext import commands


class Demo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    # 關鍵字觸發
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.content.lower() == "welcome":
            await message.channel.send("Welcome to Lapin World!")


async def setup(bot):
    await bot.add_cog(Demo(bot))
