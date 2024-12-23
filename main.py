import asyncio
import logging
from bot.bot import bot, dp
from bot.database.connection import db


async def main():
    logging.basicConfig(level=logging.INFO)

    try:
        await dp.start_polling(bot, db=db)
    except Exception as e:
        logging.error(f"Error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
