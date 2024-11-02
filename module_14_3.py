from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = '***'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(resize_keyboard=True)
but = KeyboardButton(text='Рассчитать')
but2 = KeyboardButton(text='Информация')
but3 = KeyboardButton(text='Купить')
kb.add(but)
kb.add(but2)
kb.add(but3)


ikb = InlineKeyboardMarkup()
inl = InlineKeyboardMarkup()
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button1 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
button2 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button3 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button4 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button5 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
ikb.add(button)
ikb.add(button1)
inl.add(button2)
inl.add(button3)
inl.add(button4)
inl.add(button5)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start_(message):
    await message.answer('Привет, я бот помогающий твоему здоровью', reply_markup=kb)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()



@dp.message_handler(text= 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=ikb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age= message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    formula = (10*int(data['weight']) + 6.25*int(data['growth']) - 5*int(data['age']) + 5)
    await message.answer(f"Ваша норма каллорий: {formula}")
    await state.finish()


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    products = [{'name':  'Product1', 'script': 'Описание 1', 'price': 100, 'img': '1.jpg'},
                {'name':  'Product2', 'script': 'Описание 2', 'price': 200, 'img': '2.jpg'},
                {'name':  'Product3', 'script': 'Описание 3', 'price': 300, 'img': '3.jpg'},
                {'name':  'Product4', 'script': 'Описание 4', 'price': 400, 'img': '4.jpg'}]
    for product in products:
        await message.answer(f'Название: {product ["name"]} | Описание: {product ["script"]} | Цена: {product ["price"]}')
        with open(product ['img'], 'rb') as photo:
            await message.answer_photo(photo)
        await message.answer("Выберите продукт для покупки:", reply_markup=inl)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler()
async def start(message: types.Message):
    await message.answer('Привет! Хочешь узнать свою норму калорий? Тогда напиши /start')









if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)








