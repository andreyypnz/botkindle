from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import subprocess

# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
available_book_types = ["да", "нет"]


class TransferBook(StatesGroup):
    waiting_for_book_type = State()


async def book_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_book_types:
        keyboard.add(name)
    await message.answer("Нужны ли виньетки?", reply_markup=keyboard)
    await message.document.download()
    await TransferBook.waiting_for_book_type.set()


async def book_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_book_types:
        await message.answer("Пожалуйста, выберите тип, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_type=message.text.lower())
    user_data = await state.get_data()
    await message.reply(f"Отлично!\n", reply_markup=types.ReplyKeyboardRemove())
    subprocess.call("./run.sh %s" % (str(user_data['chosen_type'])), shell=True)
    await message.answer("Отправлено!")
    await state.finish()


async def register_handlers_book(dp: Dispatcher):
    dp.register_message_handler(book_start, content_types=types.ContentTypes.DOCUMENT, state="*")
    dp.register_message_handler(book_chosen, state=TransferBook.waiting_for_book_type)
