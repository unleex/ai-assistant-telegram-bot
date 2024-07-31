import asyncio
import logging.config

from config.config import dp, bot, BOT_DESCRIPTION
from handlers import brainstorm_handlers, other_handlers, prompt_handlers, delegate_handlers
from logging_settings.logging_settings import logging_config
from middlewares.middlewares import DataBaseAccessor


async def main() -> None:
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger()
    await bot.delete_webhook(drop_pending_updates = True)
    dp.include_router(other_handlers.rt)
    dp.include_router(brainstorm_handlers.rt)
    dp.include_router(prompt_handlers.rt)
    dp.include_router(delegate_handlers.rt)
    dp.update.middleware(DataBaseAccessor())
    logger.info("starting")
    await bot.set_my_description(BOT_DESCRIPTION)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())