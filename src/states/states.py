import json

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.base import StorageKey

from config.config import storage, bot


class FSMStates(StatesGroup):
    brainstorming = State()
    brainstorming_adding_topic = State()
    prompt_payload_empty = State()
    
    @staticmethod
    async def set_chat_state(chat_id: int, state: State | None):
        print(f"setting state {state} for chat {chat_id}")
        with open("src/db/chat_database.json") as f:
            db = json.load(f)
            for user_id in db[str(chat_id)]["user_ids"]:
                print(f"for users {db[str(chat_id)]["user_ids"]}")
                new_storage_key = StorageKey(bot.id, chat_id, user_id)
                ctx = FSMContext(storage,new_storage_key)
                await ctx.set_state(state)
    
    @staticmethod
    async def clear_chat_state(chat_id: int):
        await FSMStates.set_chat_state(chat_id, None)