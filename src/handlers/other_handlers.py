from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from keyboards.set_menu import set_main_menu
from lexicon.lexicon import LEXICON_RU
from states.states import FSMStates


rt = Router()
lexicon = LEXICON_RU


@rt.message(Command("start"), StateFilter(default_state))
async def start(msg: Message):
    await msg.answer(lexicon["start_command"])
    await set_main_menu(msg.chat.id)


@rt.message(Command("help"))
async def start(msg: Message):
    await msg.answer(lexicon["help_command"])


@rt.message(Command("cancel"))
async def cancel(msg: Message):
    await msg.answer(lexicon["cancel_command"])
    await FSMStates.clear_chat_data(msg.chat.id)
    await FSMStates.clear_chat_state(msg.chat.id)
