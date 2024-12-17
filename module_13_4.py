from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio


api =""
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())


@dp.message_handler(commands = ['start'])
async def start(message):
    print("Start message")
    await message.answer("Привет! Я бот помогающий твоему здоровью.")

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    calories = State()

@dp.message_handler(text = 'Calories')
async def set_age(message):
    await message.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message,state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer('Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weigth(message,state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message,state):
    await state.update_data(weigth=message.text)
    data = await state.get_data(['age', 'growth', 'weigth'])
    await message.answer('Выполнить расчет для мужчин или для женщин?')
    await UserState.calories.set()

    # """Обобщенная формула"""
    # calc = (10 * int(data['weigth'])) + (6.25 * int(data['growth'])) - (5 * int(data['age'])) - 161
    # await message.answer(f'Ваша норма калорий: {calc}')
    # await state.finish()  # завершаем состояние


@dp.message_handler(text = 'для женщин', state = UserState.calories)
async def calc_W(message, state):
    data = await state.get_data(['age', 'growth', 'weigth'])
    calc_W = (10 * int(data['weigth'])) + (6.25 * int(data['growth'])) - (5 * int(data['age'])) -161
    await message.answer(f'Ваша норма калорий: {calc_W}')
    await state.finish()  # завершаем состояние
#
@dp.message_handler(text = 'для мужчин', state = UserState.calories)
async def calc_M(message, state):
    data = await state.get_data(['age', 'growth', 'weigth'])
    calc_M = (10 * int(data['weigth'])) + (6.25 * int(data['growth'])) - (5 * int(data['age'])) + 5
    await message.answer(f'Ваша норма калорий: {calc_M}')
    await state.finish()  # завершаем состояние



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)