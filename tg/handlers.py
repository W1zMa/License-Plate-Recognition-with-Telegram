import os
import asyncio
from aiogram import Router, types, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from services import db
from tg.states import PhotoState
from recognition.detector import process_video
from tg.keyboard.replykey import main_menu
from tg.keyboard.inlinekey import inline_keyboard

rt = Router()

@rt.message(CommandStart())
async def handler_message_start(message: types.Message):
    #await state.set_state(PhotoState.wait_for_photo)
    await message.answer("Hello welcome", reply_markup=main_menu)


@rt.message(lambda message: message.text == "Upload Photo/Video")
async def handler_send_photo(message: types.Message, state: FSMContext):
    await state.set_state(PhotoState.wait_for_photo)
    await message.answer("Please send photo or video")

@rt.message(StateFilter(PhotoState.wait_for_photo))
async def handler_wait_photo(message: types.Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    #os.makedirs("photos", exist_ok=True)
    if message.photo:
        file_id = message.photo[-1].file_id
        ext = 'jpg'
    elif message.video: 
        file_id = message.video.file_id
        ext = 'mp4'
    else:
        await message.answer("Only photo or video")
        await state.clear
        return 

    file_path = f"data/photos/{user_id}_{file_id}.{ext}"
    await bot.download(file_id, destination=file_path)
    await message.answer("Please wait")

    numbers = await asyncio.to_thread(process_video, file_path)

    for num in numbers:
        db.save_plate(num['plate'], user_id, file_path, num['accuracy'])

    if numbers:
        text = "\n".join(f"{n['plate']} ({n['accuracy']}%)" for n in numbers)
        print(f"Find:\n{text}")
        #await message.answer(f"Find:\n{text}")
        for num in numbers:
            count = db.get_count(num['plate'])
            #avg_conf
            await message.answer(f'{num["plate"]} - Number (with Accuracy - {num["accuracy"]}), which was added {count} times')
    else:
        await message.answer("unf nothing found")
    try:
        os.remove(file_path)
    except Exception as e:
        print("file not found")

    await state.clear()

@rt.message(lambda message: message.text == "Search")
async def handler_search_input(message: types.Message, state: FSMContext):
    await state.set_state(PhotoState.wait_for_search)
    await message.answer("Please Enter the number!")

@rt.message(StateFilter(PhotoState.wait_for_search))
async def handeler_search_output(message: types.message, state: FSMContext):
    numbers_input = message.text
    rows = db.get_info(numbers_input)
    found = False
    for row in rows:
        if row["number"] == numbers_input:
            count = db.get_count(row['number'])
            await message.answer(f"Find {row['number']} which was added {count}", reply_markup=inline_keyboard(row['number']))
            found = True
            break
    if not found:
        await message.answer("Unf nothing found :( ") 
    await state.clear()



@rt.callback_query(lambda c: c.data.startswith("reset_count"))
async def callback_reset(callback: types.CallbackQuery):
    data = callback.data
    number = data.split(":")[1]

    db.reset_count(number)
    await callback.message.answer("Reseted")
    await callback.answer() 

