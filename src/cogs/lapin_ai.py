from discord.ext import commands
from src.handlers.chat import GeminiChatBot


# TODO:測試講幾句之後最初的 prompt 會不見
# TODO:寫指令的說明

class LapinAI(commands.Cog):
    prompt: str = "你是一名兔兔管家，請你對使用者的問題做出回答。\n" \
                  "請使用**繁體中文**回答。\n" \
                  "請簡短回答。"
    error_message: str = "現在忙線中，嗶嗶\n" \
                         "如果持續無法回應，請洽詢領主"
    chat_handler = GeminiChatBot(prompt=prompt, error_message=error_message)

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def chat(self, ctx, user_input: str):
        res = self.chat_handler.gen_response(user_input)
        await ctx.send(res)


async def setup(bot):
    await bot.add_cog(LapinAI(bot))
