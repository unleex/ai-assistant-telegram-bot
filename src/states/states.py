import json

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.base import StorageKey

from config.config import storage, bot


class FSMStates(StatesGroup):
    brainstorming = State()
    brainstorming_adding_topic = State()
    delegate_adding_task = State()
    delegate_adding_user_cvs = State()
    delegate_selecting_participants = State()
    prompt_payload_empty = State()
    
    @staticmethod
    async def set_chat_state(chat_id: int, state: State | None):
        with open("src/db/chat_database.json") as f:
            db = json.load(f)
        for user_id in db[str(chat_id)]["users"]:
            new_storage_key = StorageKey(bot.id, chat_id, int(user_id))
            ctx = FSMContext(storage,new_storage_key)
            await ctx.set_state(state)
    
    @staticmethod
    async def set_chat_data(chat_id: int, data: dict):
        with open("src/db/chat_database.json") as f:
            db = json.load(f)
        for user_id in db[str(chat_id)]["users"]:
            new_storage_key = StorageKey(bot.id, chat_id, int(user_id))
            ctx = FSMContext(storage,new_storage_key)
            await ctx.set_data(data)

    @staticmethod
    async def clear_chat_data(chat_id: int):
        await FSMStates.set_chat_data(chat_id, {})

    @staticmethod
    async def clear_chat_state(chat_id: int):
        await FSMStates.set_chat_state(chat_id, None)