from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


ageStage = [[str(i), "#" + str(i)] for i in range (0, 18)
#    ["от", "ageFrom"], 
#    ["до", "ageTo"], 
#    ["далее >>", "ageNext"]
#    ["0", "0"],
#    ["1", "1"],
#    ["2", "2"],
#    ["3", "3"],
#    ["4", "4"],
#    ["5", "5"],
#    ["6", "6"],
#    ["7", "7"],
#    ["8", "8"],
#    ["9", "9"],
#    ["10", "10"],
#    ["11", "11"],
#    ["12", "12"],
#    ["13", "13"],
#    ["14", "14"],
#    ["15", "15"],
#    ["16", "16"],
#    ["17", "17"],
#    ["любой", "любой"]
]
# ageStage.append(['любой', "anyAgeFrom"])

amountStage = [
    ["от", "amountFrom"], 
    ["до", "amountTo"], 
    ["далее >>", "amountNext"]]


class MakeSearch(StatesGroup):
    waitForAge = State()
    waitForAmount = State()


async def SearchForAge(message: types.Message, state: FSMContext):
    ageBtns = []
    keyboard = types.InlineKeyboardMarkup(row_width=6)
    for name in ageStage:
        # ageBtns.add(types.InlineKeyboardButton(name, callback_data=name))
        ageBtns.append(types.InlineKeyboardButton(name[0], callback_data=name[1]))
    keyboard.add(*ageBtns)
    await message.answer("Задайте возраст поиска от 0 до 17.\nНажмите Далее для перехода к следующему этапу.", reply_markup=keyboard)
    await state.set_state(MakeSearch.waitForAge.state)


async def ValidateAgeFrom(message: types.Message, state: FSMContext):
    if not 0 <= int(message.text) <= 17:
        await message.answer("ValidAgeFrom: Возраст должен быть от 0 до 17 лет.")
        return
    await state.update_data(ageFrom=message.text.lower())

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    for size in amountStage:
        keyboard.add(size)
    await state.set_state(MakeSearch.waitForAmount.state)
    await message.answer("Теперь выберите размер порции:", reply_markup=keyboard)

async def ValidateAgeTo(message: types.Message, state: FSMContext):
    if not 0 <= int(message.text) <= 17:
        await message.answer("ValidAgeTo Возраст должен быть от 0 до 17 лет.")
        return
    await state.update_data(ageTo=message.text.lower())

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    for size in amountStage:
        keyboard.add(size)
    await state.set_state(MakeSearch.waitForAmount.state)
    await message.answer("Теперь выберите размер порции:", reply_markup=keyboard)


async def drinks_size_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in amountStage:
        await message.answer("Пожалуйста, выберите размер порции, используя клавиатуру ниже.")
        return
    user_data = await state.get_data()
    await message.answer(f"Вы заказали {user_data['ageFrom']} объёмом {message.text.lower()}.\n"
                         f"Попробуйте теперь заказать еду: /food", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_search(dp: Dispatcher):
    dp.register_message_handler(SearchForAge, commands="search", state="*")
    dp.register_message_handler(ValidateAgeFrom, state=MakeSearch.waitForAge)
    dp.register_message_handler(ValidateAgeTo, state=MakeSearch.waitForAge)
    dp.register_message_handler(drinks_size_chosen, state=MakeSearch.waitForAmount)
