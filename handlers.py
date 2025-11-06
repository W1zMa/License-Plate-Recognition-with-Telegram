import os
import asyncio
from dotenv import load_dotenv
from aiogram import Router, types, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from services import db
from states import PhotoState
from recognition.detector import process_video
from keyboard.replykey import main_menu
from keyboard.inlinekey import resetcounts, delete_number

load_dotenv()
rt = Router()

@rt.message(CommandStart())
async def handler_message_start(message: types.Message):
    #await state.set_state(PhotoState.wait_for_photo)
    await message.answer("👋 Hi there! Welcome to PlateSaver. Send a clear photo of the vehicle license plate and I’ll read it, save the number, and show you the result. Fast, simple, and private. 📸➡️🗂️", reply_markup=main_menu)


@rt.message(lambda message: message.text == "Upload Photo/Video")
async def handler_send_photo(message: types.Message, state: FSMContext):
    await state.set_state(PhotoState.wait_for_photo)
    await message.answer("Please send photo or video 📸")

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
        await message.answer("📸 Please send a photo or video of the license plate only. 🚗✨")
        await state.clear
        return 

    file_path = f"data/photos/{user_id}_{file_id}.{ext}"
    await bot.download(file_id, destination=file_path)
    await message.answer("Please wait ⏳")

    numbers = await asyncio.to_thread(process_video, file_path)
    
    if numbers:
            text = "\n".join(f"{n['plate']} ({n['accuracy']}%), in {n['timecode']}" for n in numbers)
            
            print(f"Find:\n{text}")
            for num in numbers:
                count = db.get_count(num['plate']) + 1
                db.save_plate(num['plate'], count, file_path, num['accuracy'], num['timecode'])
                await message.answer(f'✅ Plate: {num["plate"]}. Accuracy: {num["accuracy"]}. Added: {count} times🚗. on {num["timecode"]} sec',
                    reply_markup=delete_number(num['plate'])
                )
            await state.clear()
    else:
        await message.answer("😕 Oops! Nothing found in this photo. Try again with a clearer image. 📸✨")
    os.remove(file_path)
@rt.message(lambda message: message.text == "Search")
async def handler_search_input(message: types.Message, state: FSMContext):
    await state.set_state(PhotoState.wait_for_search)
    await message.answer("🚘 Enter the license plate number you’d like to find. 🔍")

@rt.message(StateFilter(PhotoState.wait_for_search))
async def handeler_search_output(message: types.message, state: FSMContext):
    numbers_input = message.text
    rows = db.get_info(numbers_input)
    found = False
    for row in rows:
        if row["number"] == numbers_input:
            count = db.get_count(row['number'])
            await message.answer(f"Find {row['number']} which was added {count}", reply_markup=resetcounts(row['number']))
            found = True
            break
    if not found:
        await message.answer("😕 Oops! Nothing found") 
    await state.clear()

@rt.callback_query(lambda c: c.data.startswith("delete_number"))
async def callback_delnum(callback: types.CallbackQuery):
    data = callback.data
    plate = data.split(":")[1]
    db.delet_plate(plate)
    await callback.message.delete()
    await callback.message.answer(f"✅ {plate} deleted successfully ")
    await callback.answer()

    

@rt.callback_query(lambda c: c.data.startswith("reset_count"))
async def callback_reset(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if str(user_id) == os.getenv("ADMIN_ID"):
        data = callback.data
        number = data.split(":")[1]
        count = db.get_count(number)
        if count == 0:
            await callback.message.answer("Already reseted ❌")
            await callback.answer()
        else:
            db.reset_count(number)
            await callback.message.answer("Reseted ✅")
            await callback.answer()
    else:
        await callback.message.answer("🚫 You’re not an admin")
        await callback.answer()

