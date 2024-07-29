from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Chat, User

from typing import Callable, Any
import json
import logging
logger = logging.getLogger(__name__)
class DataBaseAccessor(BaseMiddleware):
    async def __call__(self, 
                       handler: Callable, 
                       event: TelegramObject, 
                       data: dict[str,Any]) -> Any:
        chat: Chat|None = data['event_chat'] 
        user: User|None = data["event_from_user"]
        with open("src/db/chat_database.json", mode='r') as fp:
            db: dict = json.load(fp)
        if str(chat.id) in db.keys():
            data['chat_data'] =  db[str(chat.id)]
        else:
            db[str(chat.id)] = {"brainstorm_payload": [], "users_cv": [], "brainstorm_paused": False, "user_ids": []}
            logger.info(f"New chat: {chat.id}.\nInfo: {chat.active_usernames}\n{chat.bio}")

        if user.id not in db[str(chat.id)]["user_ids"]:
            db[str(chat.id)]["user_ids"].append(user.id)
            logger.info(f"New user in chat: {chat.id}.\Id: {user.id}")

        result = await handler(event, data)

        with open('src/db/chat_database.json', mode='w') as fp:
            json.dump(db, fp, indent='\t')
        return result