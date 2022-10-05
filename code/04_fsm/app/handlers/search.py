from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


ageStage = [
    ["от", "ageFrom"], 
    ["до", "ageTo"], 
    ["далее >>", "ageNext"]
]
amountStage = [
    ["от", "amountFrom"], 
    ["до", "amountTo"], 
    ["далее >>", "amountNext"]]


class MakeSearch(StatesGroup):
    waitForAge = State()
    waintForAmount = State()


async def drinks_start(message: types.Message, state: FSMContext):
    ageBtns = []
    keyboard = types.InlineKeyboardMarkup()
    for name in ageStage:
        # ageBtns.add(types.InlineKeyboardButton(name, callback_data=name))
        ageBtns.append(types.InlineKeyboardButton(name[0], callback_data=name[1]))
    keyboard.add(*ageBtns)
    await message.answer("Задайте возраст поиска от 0 до 17.\nНажмите Далее для перехода к следующему этапу.", reply_markup=keyboard)
    await state.set_state(MakeSearch.waitForAge.state)


async def drinks_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in ageStage:
        await message.answer("Пожалуйста, выберите напиток, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_food=message.text.lower())

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    for size in amountStage:
        keyboard.add(size)
    await state.set_state(MakeSearch.waintForAmount.state)
    await message.answer("Теперь выберите размер порции:", reply_markup=keyboard)


async def drinks_size_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in amountStage:
        await message.answer("Пожалуйста, выберите размер порции, используя клавиатуру ниже.")
        return
    user_data = await state.get_data()
    await message.answer(f"Вы заказали {user_data['chosen_food']} объёмом {message.text.lower()}.\n"
                         f"Попробуйте теперь заказать еду: /food", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_search(dp: Dispatcher):
    dp.register_message_handler(drinks_start, commands="search", state="*")
    dp.register_message_handler(drinks_chosen, state=MakeSearch.waitForAge)
    dp.register_message_handler(drinks_size_chosen, state=MakeSearch.waintForAmount)
