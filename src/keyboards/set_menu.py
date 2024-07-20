from aiogram.types import BotCommand
from aiogram import Bot
from lexicon.lexicon import LEXICON_RU

lexicon = LEXICON_RU
async def set_main_menu(bot: Bot) -> None:
    main_menu_commands = [
        BotCommand(command="prompt",
                   description=lexicon["prompt_command_description"])
    ]
    await bot.set_my_commands(main_menu_commands)