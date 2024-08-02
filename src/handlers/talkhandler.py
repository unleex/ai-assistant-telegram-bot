from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from gpt.gpt import prompt
from gigachat.models import  MessagesRole
from gpt.prompts import PROMPTS_RU
from aiogram.fsm.context import FSMContext


rt = Router()
prompts = PROMPTS_RU

@rt.message(StateFilter(default_state), F.chat.type=='private')
async def talking(message: Message, state: FSMContext):
    ctx = await state.get_data()
    if 'dialog' not in ctx:
        ctx['dialog'] = [{"role": MessagesRole.USER, "content": prompts["prompt"] % message.text}]
    else:
        ctx['dialog'].append(dict(role=MessagesRole.USER, content=message.text))
    answer = prompt(ctx['dialog'])
    ctx['dialog'].append(dict(role=MessagesRole.ASSISTANT, content=answer['content']))
    await message.answer(answer["content"])
    await state.set_data(ctx)