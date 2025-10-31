from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def inline_keyboard(number: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Reset count', callback_data=f'reset_count:{number}')]
    ])
    return keyboard