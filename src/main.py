import asyncio
from config.config import dp, bot
from handlers import gpt_handlers, other_handlers
from keyboards.set_menu import set_main_menu


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates = True) 
    await set_main_menu()   
    dp.include_router(other_handlers.rt)
    dp.include_router(gpt_handlers.rt)
    print("starting")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())