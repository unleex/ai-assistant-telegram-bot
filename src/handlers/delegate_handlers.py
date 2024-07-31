from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from gigachat.models import MessagesRole

from config.config import bot, BOT_USERNAME
from gpt.gpt import prompt
from gpt.prompts import PROMPTS_RU
from keyboards.keyboards import build_delegate_selecting_user_kb
from lexicon.lexicon import LEXICON_RU
from states.states import FSMStates


rt = Router()
lexicon = LEXICON_RU
prompts = PROMPTS_RU


@rt.message(Command("delegate"), StateFilter(default_state))
async def delegate_init_handler(msg: Message, state: FSMContext, chat_data: dict):
    task = msg.text.replace("/delegate", '').replace(BOT_USERNAME,'')
    if not task.replace(' ',''):
        await msg.answer(lexicon["delegate_task_empty"])
        await state.set_state(FSMStates.delegate_adding_task)
        return
    if not chat_data["user_cvs"]:
        await msg.answer(lexicon["delegate_no_user_cvs"])
        await FSMStates.set_chat_state(msg.chat.id, FSMStates.delegate_adding_user_cvs)
        return
    await msg.answer(lexicon["delegate_select_participants"],
                     reply_markup= await build_delegate_selecting_user_kb(msg.chat.id))
    await state.set_data({"delegate_task": task})
    await state.set_state(FSMStates.delegate_selecting_participants) 


@rt.message(Command("finish"), StateFilter(FSMStates.delegate_adding_user_cvs,
                                           FSMStates.delegate_selecting_participants))
async def delegate_finished_adding_user_cvs(msg: Message, state: FSMContext):
    ctx = await state.get_data()
    await msg.answer(lexicon["delegate_finished_adding_user_cvs"])
    prompt_ = prompts["init_delegate"] % (len(ctx["cvs"]), ctx["delegate_task"], '\n'.join(ctx["cvs"]))
    answer = prompt([{"role": MessagesRole.USER, "content": prompt_}])
    await msg.answer(answer["content"])
    await FSMStates.clear_chat_state(msg.chat.id)
    await FSMStates.clear_chat_data(msg.chat.id)
    await FSMStates.clear_chat_state(FSMStates.delegate_selecting_participants)

@rt.message(StateFilter(FSMStates.delegate_adding_user_cvs))
async def delegate_adding_user_cv(msg: Message, chat_data: dict, state: FSMContext):
    tag_index = msg.text.find("@")
    if tag_index != -1:
        # get user id by username
        username = msg.text[tag_index + 1 : msg.text.find(' ', tag_index + 1)]
        if username not in chat_data["users"].values():
            await msg.answer(lexicon["unknown_user"] % ("@" + username))
            return
        user_id = dict(zip(
            chat_data["users"].values(), 
            chat_data["users"].keys())
            )[username]
        cv = msg.text.replace('@', '').replace(username, '')
    else:
        user_id = msg.from_user.id
        username = msg.from_user.username
        cv = msg.text
    chat_data["user_cvs"][user_id] = cv
    ctx = await state.get_data()
    if "cvs" not in ctx:
        ctx["cvs"] = []
    ctx["cvs"].append(lexicon["delegate_cv_template"] % (
        username, chat_data["user_cvs"][user_id]))
    if "selected_users" not in ctx:
        ctx["selected_users"] = []
    ctx["selected_users"].append(username)
    await msg.answer(lexicon["delegate_user_cv_added"])
    await FSMStates.set_chat_data(msg.chat.id, ctx)
    

@rt.message(StateFilter(FSMStates.delegate_adding_task))
async def delegate_adding_task(msg: Message, state: FSMContext, chat_data: dict):
    await delegate_init_handler(msg, state, chat_data)


@rt.callback_query(F.data=="delegate_selected_all_participants", 
                   StateFilter(FSMStates.delegate_selecting_participants))
async def delegate_select_all_participants(clb: CallbackQuery, state: FSMContext, chat_data: dict):
    ctx = await state.get_data()
    ctx["cvs"] = [
        lexicon["delegate_cv_template"] %
        ((await bot.get_chat_member(clb.message.chat.id, user_id)).user.username, chat_data["user_cvs"][user_id])
        for user_id in chat_data["user_cvs"]
        ]
    prompt_ = prompts["init_delegate"] % (len(ctx["cvs"]), ctx["delegate_task"], '\n'.join(ctx["cvs"]))
    answer = prompt([{"role": MessagesRole.USER, "content": prompt_}])
    await bot.send_message(clb.message.chat.id, answer["content"])
    await state.clear()


@rt.callback_query(F.data=="delegate_selected_edit_cv", 
                   StateFilter(FSMStates.delegate_selecting_participants))
async def delegate_select_edit_cv(clb: CallbackQuery):
    await bot.send_message(clb.message.chat.id, lexicon["delegate_adding_user_cv"])
    await FSMStates.set_chat_state(clb.message.chat.id, FSMStates.delegate_adding_user_cvs)


@rt.callback_query(F.data.startswith("delegate_selected_"), 
                   StateFilter(FSMStates.delegate_selecting_participants))
async def delegate_select_user(clb: CallbackQuery, state: FSMContext, chat_data: dict):
    ctx = await state.get_data()
    if "cvs" not in ctx:
        ctx["cvs"] = []
    username = clb.data.replace("delegate_selected_", '')
    user_id = dict(zip(
        chat_data["users"].values(), 
        chat_data["users"].keys())
        )[username]
    ctx["cvs"].append(lexicon["delegate_cv_template"] % (
        username, chat_data["user_cvs"][user_id]))
    if "selected_users" not in ctx:
        ctx["selected_users"] = []
    ctx["selected_users"].append(username)
    text = clb.message.text
    await clb.message.edit_text(
        text + '\n' + lexicon["delegate_selected_user"] % username, 
        reply_markup=await build_delegate_selecting_user_kb(clb.message.chat.id, except_for=ctx["selected_users"]))
    await state.set_data(ctx)