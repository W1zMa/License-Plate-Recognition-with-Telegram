from aiogram import Router, types, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from states import PhotoState

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
    await message.answer("Thx")
    await state.clear()
