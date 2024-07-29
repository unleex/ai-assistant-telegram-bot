from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from gpt.gpt import prompt
from gpt.prompts import PROMPTS_RU
from lexicon.lexicon import LEXICON_RU
from states.states import FSMStates
from gigachat.models import  MessagesRole


rt = Router()
lexicon = LEXICON_RU
prompts = PROMPTS_RU


@rt.message(Command('prompt'))
async def prompt_handler(msg: Message, state: FSMContext):
    payload = msg.text.replace("/prompt", '').replace("@evpatiy_ai_bot",'')
    if not payload.replace(' ',''):
        await msg.answer(lexicon["prompt_payload_empty"])
        await state.set_state(FSMStates.prompt_payload_empty)
        return
    answer = prompt([{"role": MessagesRole.USER, "content": prompts["prompt"] % payload}])
    await msg.answer(answer["content"])
    await state.clear()


@rt.message(StateFilter(FSMStates.prompt_payload_empty))
async def prompt_adding_message(msg: Message, state: FSMContext):
    await prompt_handler(msg, state)