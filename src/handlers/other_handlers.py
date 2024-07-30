from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU


rt = Router()
lexicon = LEXICON_RU


@rt.message(Command("start"), StateFilter(default_state))
async def start(msg: Message):
    await msg.answer(lexicon["start_command"])


@rt.message(Command("help"))
async def start(msg: Message):
    await msg.answer(lexicon["help_command"])


@rt.message(Command("cancel"))
async def cancel(msg: Message, state: FSMContext):
    await msg.answer(lexicon["cancel_command"])
    await state.clear()
