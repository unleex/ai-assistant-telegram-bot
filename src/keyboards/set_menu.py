from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

from config.config import bot
from lexicon.lexicon import LEXICON_RU


lexicon = LEXICON_RU


async def set_main_menu(chat_id: int | None = None) -> None:
    main_menu_commands = [
        BotCommand(command="start",
                   description=lexicon["start_command_description"]),
        BotCommand(command="help",
                   description=lexicon["help_command_description"]),    
        BotCommand(command="cancel",
                   description=lexicon["cancel_command_description"]),
        BotCommand(command="prompt",
                   description=lexicon["prompt_command_description"]),
        BotCommand(command="brainstorm",
                   description=lexicon["brainstorm_command_description"]),
        BotCommand(command="delegate",
                   description=lexicon["delegate_command_description"])
    ]
    await bot.set_my_commands(main_menu_commands, BotCommandScopeChat(chat_id=chat_id) if chat_id else BotCommandScopeDefault())


async def set_brainstorm_menu(chat_id: int | None = None):
    brainstorm_commands = [
        BotCommand(command="conclude",
                   description=lexicon["conclude_command_description"]),
        BotCommand(command="pause",
                   description=lexicon["pause_command_description"]),
        BotCommand(command="cancel",
                   description=lexicon["cancel_command_description"]) 
    ]
    await bot.set_my_commands(brainstorm_commands, BotCommandScopeChat(chat_id=chat_id) if chat_id else BotCommandScopeDefault())