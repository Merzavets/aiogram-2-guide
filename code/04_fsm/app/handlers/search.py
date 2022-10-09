from email import message
from turtle import st
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


# ageStage = [[str(i), "#" + str(i)] for i in range (0, 18)
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
# ]
# ageStage.append(['любой', "anyAgeFrom"])

amountStage = [
    ["от", "amountFrom"], 
    ["до", "amountTo"], 
    ["далее >>", "amountNext"]]
ChildAges = range(0, 18)


class MakeSearch(StatesGroup):
    waitForAgeTo = State()
    waitForAmountFrom = State()
    waitForAmountTo = State()


#######################################################################################
async def StartSearch(message: types.Message, state: FSMContext):
    ageStage = [[str(i), str(i)] for i in range (0, 18)]
    ageStage.append(["любой", "0"])

    ageBtns = []
    keyboard = types.InlineKeyboardMarkup(row_width=6)
    for name in ageStage:
        # ageBtns.add(types.InlineKeyboardButton(name, callback_data=name))
        ageBtns.append(types.InlineKeyboardButton(name[0], callback_data=name[1]))
    keyboard.add(*ageBtns)
    await message.answer("Выберите _нижнюю_ границу поиска возраста\nили нажмите *Любой*", reply_markup=keyboard, parse_mode="Markdown")
    await state.set_state(MakeSearch.waitForAgeTo.state)

#######################################################################################
### state: 'MakeSearch:waitForAgeTo'
### called when 'age from' button is pressed
async def SearchAgeTo(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(ageFrom=callback.data.lower())
    udata = await state.get_data()
    ageFrom = int(udata.get('ageFrom'))

### TODO: посчитать красивое количество рядов
    rowWidths = {
        "18" : 6,
        "17" : 4,
        "16" : 5,
        "15" : 7,
        "14" : 7,
        "13" : 6
    }
    
    rwidth = 6 #rowWidths[str(18 - ageFrom)]
    ageStage = [[str(i), str(i)] for i in  range (ageFrom, 18)]
    # ageStage.append(["любой", "17"])

    ageBtns = []
    keyboard = types.InlineKeyboardMarkup(row_width = rwidth)
    for name in ageStage:
        # ageBtns.add(types.InlineKeyboardButton(name, callback_data=name))
        ageBtns.append(types.InlineKeyboardButton(name[0], callback_data = name[1]))
    keyboard.add(*ageBtns)
    keyboard.row(types.InlineKeyboardButton("любой", callback_data="17"))
#    await callback.message.delete_reply_markup()

    await callback.message.edit_text(f"Ищем детишек от *{ageFrom}* до...\nВыберите _верхнюю_ границу поиска возраста\nили нажмите *Любой*",  reply_markup = keyboard, parse_mode = "Markdown")
    await state.set_state(MakeSearch.waitForAmountFrom.state)

#######################################################################################
### called when 'age to' button is pressed
### state: MakeSearch:waitForAmountFrom
async def SearchAmountFromCall(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(ageTo=callback.data.lower())
    udata = await state.get_data()

    amountChoices = [
        ["любая", "100"]
    ]
    amountBtns = []
    keyboard = types.InlineKeyboardMarkup(row_width=6)
    for choice in amountChoices:
        amountBtns.append(types.InlineKeyboardButton(choice[0], callback_data=choice[1]))
    keyboard.add(*amountBtns)
    await callback.message.edit_text(f"Ищем детишек от *{udata.get('ageFrom')}* до *{udata.get('ageTo')}*\nВведите _нижнюю_ границу поиска суммы от 100₽\nили нажмите *Любая*", reply_markup=keyboard, parse_mode="Markdown")
    await state.set_state(MakeSearch.waitForAmountTo.state)

#######################################################################################
async def SearchAmountFromMsg(message: types.Message, state: FSMContext):
    await state.update_data(ageTo=message.data.lower())
    udata = await state.get_data()

    amountChoices = [
        ["любая", "100"]
    ]
    amountBtns = []
    keyboard = types.InlineKeyboardMarkup(row_width=6)
    for choice in amountChoices:
        amountBtns.append(types.InlineKeyboardButton(choice[0], callback_data=choice[1]))
    keyboard.add(*amountBtns)
    await message.edit_text(f"Ищем детишек от *{udata.get('ageFrom')}* до *{udata.get('ageTo')}*\nВведите _нижнюю_ границу поиска суммы от 100₽\nили нажмите *Любая*", reply_markup=keyboard, parse_mode="Markdown")
    await state.set_state(MakeSearch.waitForAmountTo.state)


#######################################################################################
async def ValidateAgeTo(message: types.Message, state: FSMContext):
#    if not 0 <= int(message.text) <= 17:
#        await message.answer("ValidAgeTo Возраст должен быть от 0 до 17 лет.")
#        return
    await state.update_data(ageTo=message.data.lower())
    await state.update_data(ageFrom = '999')
    udata = await state.get_data()
    await message.answer(udata.get('ageTo'))

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    for size in amountStage:
        keyboard.add(size)
    await state.set_state(MakeSearch.waitForAmountFrom.state)
    await message.answer("Теперь выберите размер порции:", reply_markup=keyboard)


#######################################################################################
### если вводим текст на этапе нижней границы возраста
### state: 'MakeSearch:waitForAgeTo'
async def ValidateAgeFromInput(message: types.Message, state: FSMContext):
    if message.text.isnumeric() and (int(message.text) in ChildAges):
        await state.update_data(ageFrom=message.text.lower())
    else:
        await message.reply("ValidAgeFrom: Возраст должен быть от 0 до 17 лет.")
        await state.set_state(MakeSearch.waitForAmountFrom.state)
        return


    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    for size in amountStage:
        keyboard.add(size)
    ### await state.set_state(MakeSearch.waitForAmountFrom.state)
    ### TODO:какой тут "стейт" должен быть?
    # await message.answer("Теперь выберите размер порции:", reply_markup=keyboard)


#######################################################################################
### called when 'age to' is entered manually
### 'MakeSearch:waitForAmountFrom'
async def drinks_size_chosen(message: types.Message, state: FSMContext):
    if not (message.text.isnumeric() and (int(message.text) in ChildAges)):
        await message.answer("Пожалуйста, выберите размер порции, используя клавиатуру ниже.")
        return
    await state.update_data(ageTo=message.text)
    user_data = await state.get_data()
    await message.answer(f"Вы заказали {user_data['ageFrom']} объёмом {user_data['ageTo']}.\n"
                         f"Попробуйте теперь заказать еду: /food", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()



def register_handlers_search(dp: Dispatcher):
    dp.register_message_handler(StartSearch, commands="search", state="*")
#    dp.register_message_handler(SearchAgeTo, state=MakeSearch.waitForAgeTo)
    
#    dp.register_message_handler(ValidateAgeTo, state=MakeSearch.waitForAge, text="#1")
    dp.register_message_handler(ValidateAgeFromInput, state=MakeSearch.waitForAgeTo)
    dp.register_message_handler(drinks_size_chosen, state=MakeSearch.waitForAmountFrom)
#    dp.register_callback_query_handler(ValidateAgeTo, state=MakeSearch.waitForAgeTo )
    dp.register_callback_query_handler(SearchAgeTo, state=MakeSearch.waitForAgeTo)
    dp.register_callback_query_handler(SearchAmountFromCall, state=MakeSearch.waitForAmountFrom)