from aiogram.fsm.state import State, StatesGroup
class PhotoState(StatesGroup):
    wait_for_photo = State()
    wait_for_info = State()
