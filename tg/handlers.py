import os
import asyncio
from aiogram import Router, types, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from services import db
from tg.states import PhotoState
from recognition.detector import process_video
from tg.keyboard import main_menu

rt = Router()

@rt.message(CommandStart())
async def handler_message_start(message: types.Message, state: FSMContext):
    await state.set_state(PhotoState.wait_for_photo)
    await message.answer("Hello send photo")


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
    for row in rows:
        if row["number"] == numbers_input:
            await message.answer("true")
        else:
            await message.answer("false")
    await state.clear()
