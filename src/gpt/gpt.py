from typing import List
from config.config import giga
from gigachat.models import Chat, Messages, MessagesRole


MAX_TOKENS = 3000


def prompt(chat: list[dict[str, str | MessagesRole]],
           max_tokens: int = MAX_TOKENS) -> dict[str, str | MessagesRole]:
    chat = Chat(
        messages=[Messages(role=i["role"],
                           content=i["content"]) for i in chat],
        max_tokens=max_tokens
    )
    #for serialization in context
    res = giga.chat(chat)
    return dict(role=MessagesRole.ASSISTANT,
                content=res.choices[0].message.content)