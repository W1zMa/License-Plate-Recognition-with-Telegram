from aiogram.fsm.state import State, StatesGroup
class PhotoState(StatesGroup):
    wait_for_photo = State()
