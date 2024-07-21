from aiogram.fsm.state import State, StatesGroup
class FSMStates(StatesGroup):
    brainstorming = State()
    brainstorming_adding_topic = State()
    prompt_payload_empty = State()