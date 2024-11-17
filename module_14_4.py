from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import initiate_db, get_all_products

api = ""
bot = Bot(token = api)
dp = Dispatcher(bot,storage= MemoryStorage())

class UserState(StatesGroup):
	age = State()
	growth = State()
	weight = State()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.add(button)
kb.add(button2)
kb.add(button3)
inline_kb_product = InlineKeyboardMarkup()
for i in range(1,5):
    inline_kb_product.add(InlineKeyboardButton(text=f'Product{i}', callback_data='product_buying'))
@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    products = get_all_products()
    count_ = 1
    product_list = []
    for product in products:
        product_list.append(product)
    for el in product_list:
        photo_path = f'Images/Products{count_}.jpg'
        await message.answer_photo(photo=open(photo_path, 'rb'),
                                caption=f'Название: {el[1]} | Описание: {el[2]} | Цена: {el[3]}',
                                reply_markup=inline_kb_product)
        count_+=1

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call:types.CallbackQuery):
    await call.message.answer('Вы успешно приобрели продукт!"')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	await message.answer("Привет! Я бот, помогающий твоему здоровью!", reply_markup=kb)

@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'))
    inline_kb.add(InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas'))
    await message.answer("Выберите опцию:", reply_markup=inline_kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    formulas_text = "Формула Миффлина-Сан Жеора:\n" \
                    "Для женщин: BMR = 10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(лет) - 161\n" \
                    "Для мужчин: BMR = 10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(лет) + 5"
    await call.message.answer(formulas_text)

@dp.callback_query_handler(text='calories')
async def set_age(call: types.CallbackQuery):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    recommendation = 10 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) - 161
    await message.answer(f"Ежедневно должны потреблять не более - {recommendation} калорий.")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)