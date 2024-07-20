from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from gpt.gpt import prompt
rt = Router()

lexicon = LEXICON_RU
@rt.message(Command('prompt'))
async def prompt_handler(msg: Message):
    payload = msg.text.replace("/prompt", '')
    if not payload.replace(' ',''):
        await msg.answer(lexicon["prompt_message_empty"])
        return
    await msg.answer(prompt(payload).choices[0].message.content)