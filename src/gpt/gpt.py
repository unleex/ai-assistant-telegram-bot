from langchain.schema import HumanMessage, SystemMessage
from typing import List
from config.config import giga
from gigachat.models import Chat, Messages, MessagesRole
def prompt(messages: str | Chat):
    return giga.chat(messages)