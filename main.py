import asyncio
import logging

from config import dp, bot
from handlers import acquaintance, commands, find_people

logging.basicConfig(level=logging.INFO)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )

    dp.include_router(commands.router)
    dp.include_router(acquaintance.router)
    dp.include_router(find_people.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
