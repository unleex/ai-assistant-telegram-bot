from aiogram.types import BotCommand
from config.config import bot
from lexicon.lexicon import LEXICON_RU


lexicon = LEXICON_RU


async def set_main_menu() -> None:
    main_menu_commands = [
        BotCommand(command="start",
                   description=lexicon["start_command_description"]),
        BotCommand(command="help",
                   description=lexicon["help_command_description"]),          
        BotCommand(command="prompt",
                   description=lexicon["prompt_command_description"]),
        BotCommand(command="brainstorm",
                   description=lexicon["brainstorm_command_description"]),
    ]
    await bot.set_my_commands(main_menu_commands)


async def set_brainstorm_menu():
    brainstorm_commands = [
        BotCommand(command="stop",
                   description=lexicon["stop_command_description"])
    ]
    await bot.set_my_commands(brainstorm_commands)