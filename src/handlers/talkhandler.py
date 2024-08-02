from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from gpt.gpt import prompt
from gigachat.models import  MessagesRole
from gpt.prompts import PROMPTS_RU
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON_RU


rt = Router()
prompts = PROMPTS_RU

@rt.message(StateFilter(default_state), F.text, F.chat.type=='private')
async def talking(message: Message, state: FSMContext):
    ctx = await state.get_data()
    if 'dialog' not in ctx:
        ctx['dialog'] = [{"role": MessagesRole.SYSTEM, "content": prompts["prompt"]}]
    ctx['dialog'].append(dict(role=MessagesRole.USER, content=message.text))
    answer = prompt(ctx['dialog'])
    ctx['dialog'].append(dict(role=MessagesRole.ASSISTANT, content=answer['content']))
    await message.answer(answer["content"])
    await state.set_data(ctx)

@rt.message(StateFilter(default_state), ~F.text, F.chat.type=='private')
async def talking(message: Message, state: FSMContext):
    await message.answer(LEXICON_RU['unknown_type_of_media'])