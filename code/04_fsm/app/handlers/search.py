from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


ageSelect = ["от...", "до...", "пропустить"]
amountSelect = ["от...", "до...", "пропустить"]
diseaseSelect = ["грипп", "простуда"]
regionSelect = ["Москва", "Казань"]


class DoSearch(StatesGroup):
    waiting_for_age = State()
    waiting_for_drink_amount = State()
    waiting_for_desease = State()
    waiting_for_region = State()

### TODO: rename these functions
async def drinks_start(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    for name in ageSelect:
        keyboard.add(name)
    await message.answer("Выберите напиток:", reply_markup=keyboard)
    await state.set_state(DoSearch.waiting_for_age.state)


async def drinks_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in ageSelect:
        await message.answer("Пожалуйста, выберите напиток, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_food=message.text.lower())

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    for size in amountSelect:
        keyboard.add(size)
    await state.set_state(DoSearch.waiting_for_drink_size.state)
    await message.answer("Теперь выберите размер порции:", reply_markup=keyboard)


async def drinks_size_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in amountSelect:
        await message.answer("Пожалуйста, выберите размер порции, используя клавиатуру ниже.")
        return
    user_data = await state.get_data()
    await message.answer(f"Вы заказали {user_data['chosen_food']} объёмом {message.text.lower()}.\n"
                         f"Попробуйте теперь заказать еду: /food", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_drinks(dp: Dispatcher):
    dp.register_message_handler(drinks_start, commands="search", state="*")
    dp.register_message_handler(drinks_chosen, state=DoSearch.waiting_for_age)
    dp.register_message_handler(drinks_size_chosen, state=DoSearch.waiting_for_drink_size)
