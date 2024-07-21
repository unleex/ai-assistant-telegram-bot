import asyncio
import logging.config
from config.config import dp, bot
from handlers import gpt_handlers, other_handlers
from keyboards.set_menu import set_main_menu
import logging
from logging_settings.logging_settings import logging_config


async def main() -> None:
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger()
    await bot.delete_webhook(drop_pending_updates = True) 
    await set_main_menu()   
    dp.include_router(other_handlers.rt)
    dp.include_router(gpt_handlers.rt)
    logger.info("starting")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())