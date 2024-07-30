import json

from aiogram.methods.get_chat_member import GetChatMember
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.config import bot
from lexicon.lexicon import LEXICON_RU




lexicon = LEXICON_RU

delegate_select_all_participants_butt = InlineKeyboardButton(
    text=lexicon["delegate_select_all_participants_butt"],
    callback_data="delegate_selected_all_participants"
)
delegate_add_new_participant_butt = InlineKeyboardButton(
    text=lexicon["delegate_add_new_participant_butt"],
    callback_data="delegate_selected_edit_cv"
)


async def build_delegate_selecting_user_kb(chat_id: int, except_for: list[str] = []):
    delegate_selecting_user_kb_builder = InlineKeyboardBuilder()
    delegate_selecting_user_kb_builder.row(delegate_add_new_participant_butt, delegate_select_all_participants_butt)
    with open("src/db/chat_database.json") as f:
        db = json.load(f)
    user_ids = db[str(chat_id)]["user_cvs"]
    user_nicknames = [(await bot.get_chat_member(chat_id, user_id)).user.username for user_id in user_ids]
    user_nicknames = list(filter(lambda x: x not in except_for, user_nicknames))
    add_user_butts = [InlineKeyboardButton(text=f"@{nickname}",
                                             callback_data=f"delegate_selected_{nickname}") 
                                            for nickname in user_nicknames]
    delegate_selecting_user_kb_builder.row(*add_user_butts, width = 1)
    return delegate_selecting_user_kb_builder.as_markup()