import asyncio
import sys

from settings import BASE_PATH
from src.bot import start_bot
from src.server import keep_alive

# 在 src 目錄底下運行
sys.path.insert(0, str(BASE_PATH / "src"))

if __name__ == '__main__':
    keep_alive()
    asyncio.run(start_bot())
