from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from gpt.gpt import prompt
from gigachat.models import  MessagesRole
from gpt.prompts import PROMPTS_RU


rt = Router()
prompts = PROMPTS_RU

@rt.message(StateFilter(default_state))
async def talking(message: Message):
    payload = message.text
    answer = prompt([{"role": MessagesRole.USER, "content": prompts["prompt"] % payload}])
    await message.answer(answer["content"])
