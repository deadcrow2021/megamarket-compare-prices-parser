from aiogram import Bot, Dispatcher
import asyncio

from src.constants import TOKEN

bot = Bot(TOKEN)

disp = Dispatcher()

async def main():
    await disp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
