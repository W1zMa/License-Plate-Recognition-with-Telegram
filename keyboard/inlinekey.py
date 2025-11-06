from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def delete_number(plate: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Delete number', callback_data=f'delete_number:{plate}')]
    ])
    return keyboard

def resetcounts(number: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Reset count', callback_data=f'reset_count:{number}')]
    ])
    return keyboard
