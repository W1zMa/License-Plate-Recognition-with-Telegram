from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Upload Photo/Video')],
        [KeyboardButton(text='Search')]
    ],
    resize_keyboard=True
)