from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from gpt.gpt import prompt
from gpt.prompts import PROMPTS_RU
from keyboards.set_menu import set_brainstorm_menu
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
    answer = prompt([{"role": MessagesRole.USER, "content": payload}])
    await msg.answer(answer["content"])
    await state.clear()


@rt.message(StateFilter(FSMStates.prompt_payload_empty))
async def prompt_adding_message(msg: Message, state: FSMContext):
    await prompt_handler(msg, state)



@rt.message(Command('brainstorm'), StateFilter(default_state))
async def brainstorm_init_handler(msg: Message, state: FSMContext):
    await set_brainstorm_menu()
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
    ctx = await state.get_data()
    ctx["brainstorm_payload"] = payload
    ctx["paused"] = False
    await msg.answer(answer["content"])
    await state.set_data(ctx)
    await state.set_state(FSMStates.brainstorming)


@rt.message(StateFilter(FSMStates.brainstorming_adding_topic))
async def brainstorm_adding_topic(msg: Message, state: FSMContext):
    await brainstorm_init_handler(msg, state)


@rt.message(Command('stop'), StateFilter(FSMStates.brainstorming))
async def conclude_brainstorm(msg: Message, state: FSMContext):
    ctx: dict[str, list] = await state.get_data()
    ctx["brainstorm_payload"].pop(0)
    brainstorm_messages: str = "".join([f"\n{message['role']}: {message['content']}" for message in ctx["brainstorm_payload"]])
    prompt_ = [dict(role=MessagesRole.SYSTEM,
                   content=prompts["conclude_brainstorm"] % brainstorm_messages)]
    res = prompt(prompt_)
    await state.clear()
    await msg.answer(res["content"])
    

@rt.message(Command('pause'), StateFilter(FSMStates.brainstorming))
async def pause_bot_in_brainstorm(msg: Message, state: FSMContext):
    ctx = await state.get_data()
    if ctx["paused"]:
        await msg.answer(lexicon["brainstorm_bot_unpaused"])
    else:
        await msg.answer(lexicon["brainstorm_bot_paused"])
    ctx["paused"] = not ctx["paused"]
    await state.set_data(ctx)


@rt.message(StateFilter(FSMStates.brainstorming))
async def brainstorm_handler(msg: Message, state: FSMContext):
    ctx: dict[str, list] = await state.get_data()
    ctx["brainstorm_payload"].append(dict(role=MessagesRole.USER,
                                                       content=msg.text))
    if not ctx["paused"]:
        answer = prompt(ctx["brainstorm_payload"])
        ctx["brainstorm_payload"].append(dict(role=MessagesRole.ASSISTANT,
                                            content=answer["content"]))
        await msg.answer(answer["content"])
    await state.set_data(ctx)