from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from gpt.gpt import prompt
from gpt.prompts import PROMPTS_RU
from keyboards.set_menu import set_brainstorm_menu, set_main_menu
from lexicon.lexicon import LEXICON_RU
from states.states import FSMStates
from gigachat.models import  MessagesRole


rt = Router()
lexicon = LEXICON_RU
prompts = PROMPTS_RU


@rt.message(Command('conclude'), StateFilter(FSMStates.brainstorming))
async def conclude_brainstorm(msg: Message, chat_data: dict):
    chat_data["brainstorm_payload"].pop(0) # remove system message
    brainstorm_messages: str = "".join([f"\n{message['role']}: {message['content']}" for message in chat_data["brainstorm_payload"]])
    prompt_ = [dict(role=MessagesRole.SYSTEM,
                   content=prompts["conclude_brainstorm"] % brainstorm_messages)]
    res = prompt(prompt_)
    await FSMStates.clear_chat_state(msg.chat.id)
    chat_data["brainstorm_payload"].clear()
    chat_data["brainstorm_bot_paused"] = False
    await msg.answer(res["content"])
    await set_main_menu(msg.chat.id)
    

@rt.message(Command('pause'), StateFilter(FSMStates.brainstorming))
async def pause_bot_in_brainstorm(msg: Message, chat_data: dict):
    if chat_data["brainstorm_paused"]:
        await msg.answer(lexicon["brainstorm_bot_unpaused"])
    else:
        await msg.answer(lexicon["brainstorm_bot_paused"])
    chat_data["brainstorm_paused"] = not chat_data["brainstorm_paused"]


@rt.message(StateFilter(FSMStates.brainstorming))
async def brainstorm_handler(msg: Message, chat_data: dict):
    chat_data["brainstorm_payload"].append(dict(role=MessagesRole.USER,
                                                       content=msg.text))
    if not chat_data["brainstorm_paused"]:
        answer = prompt(chat_data["brainstorm_payload"])
        chat_data["brainstorm_payload"].append(dict(role=MessagesRole.ASSISTANT,
                                            content=answer["content"]))
        await msg.answer(answer["content"])


@rt.message(Command('brainstorm'), StateFilter(default_state))
async def brainstorm_init_handler(msg: Message, state: FSMContext, chat_data: dict):
    await set_brainstorm_menu(msg.chat.id)
    topic = msg.text.replace("/brainstorm", '').replace("@evpatiy_ai_bot",'')
    if not topic.replace(' ',''):
        await msg.answer(lexicon["brainstorm_topic_empty"])
        await state.set_state(FSMStates.brainstorming_adding_topic)
        return
    payload = [
            dict(
                role = MessagesRole.SYSTEM,
                content=prompts["init_brainstorm"] % topic
                )
    ]
    answer = prompt(payload)
    payload.append(dict(
        role=MessagesRole.ASSISTANT,
        content=answer["content"]))
    chat_data["brainstorm_payload"] = payload
    await msg.answer(answer["content"])
    await FSMStates.set_chat_state(msg.chat.id,FSMStates.brainstorming)


@rt.message(StateFilter(FSMStates.brainstorming_adding_topic))
async def brainstorm_adding_topic(msg: Message, state: FSMContext, chat_data: dict):
        await brainstorm_init_handler(msg, state, chat_data)