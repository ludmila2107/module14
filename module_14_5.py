from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.utils import executor
from crud_functions import initiate_db
from crud_functions import is_included
from crud_functions import add_user

bot = Bot(token='')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class RegistrationState(StatesGroup):
	username = State()
	email = State()
	age = State()

@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
	await message.answer("Добро пожаловать! Нажмите 'Регистрация' для создания аккаунта.")

@dp.message_handler(lambda message: message.text == 'Регистрация')
async def sing_up(message: types.Message):
	await message.answer("Введите имя пользователя (только латинский алфавит):")
	await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
	username = message.text
	if not username.isalpha():
		await message.answer("Имя пользователя должно содержать только латинские буквы.")
		return
	if is_included(username):
		await message.answer("Пользователь существует, введите другое имя:")
	else:
		await state.update_data(username=username)
		await message.answer("Введите свой email:")
		await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
	email = message.text
	await state.update_data(email=email)
	await message.answer("Введите свой возраст:")
	await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
	age = message.text
	await state.update_data(age=age)

	user_data = await state.get_data()
	add_user(user_data['username'], user_data['email'], age)

	await message.answer("Регистрация завершена! Добро пожаловать.")
	await state.finish()


if __name__ == '__main__':
	initiate_db()
	executor.start_polling(dp)