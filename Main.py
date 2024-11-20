from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import re
import prices
import buttons
import crud_functions

API_TOKEN = ''

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


WELCOME_MESSAGE = "Здравствуйте! Добро пожаловать в нашу компанию. Мы рады предложить вам качественные услуги!"
ABOUT_US_MESSAGE = (
    "Наша компания предоставляет разнообразные услуги, включая профессиональные консультации и техническую помощь.\n"
    "Мы работаем на рынке уже несколько лет и заслужили доверие наших клиентов.\n"
    "Выберите интересующую вас услугу из меню ниже."
)


@dp.callback_query_handler(lambda call: call.data == "registration")
async def sing_up(call: types.CallbackQuery):
    await call.message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text
    if crud_functions.is_included(username):
        await message.answer("Пользователь существует, введите другое имя:")
    else:
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        await message.answer("Введите корректный email (пример: example@mail.com):")
        return

    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age <= 0:
            raise ValueError("Возраст должен быть больше 0.")
    except ValueError:
        await message.answer("Введите корректный возраст (целое число больше 0):")
        return

    await state.update_data(age=age)
    data = await state.get_data()

    try:
        crud_functions.add_user(data['username'], data['email'], data['age'])
    except Exception as e:
        await message.answer(f"Произошла ошибка при регистрации: {e}")
        return

    await message.answer("Регистрация завершена! Добро пожаловать!", reply_markup=buttons.main_menu)
    await state.finish()



@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(WELCOME_MESSAGE, reply_markup=buttons.main_menu)


@dp.message_handler(commands=['about'])
async def about_command(message: types.Message):
    await message.answer(ABOUT_US_MESSAGE, reply_markup=buttons.back_button_menu)


@dp.message_handler(lambda message: message.text == "Купить")
async def get_buying_list(message: types.Message):
    products = crud_functions.get_all_products()
    if not products:
        await message.answer("В базе данных пока нет товаров.")
        return

    for product in products:
        product_info = (
            f"**Название:** {product[1]}\n"
            f"**Описание:** {product[2]}\n"
            f"**Цена:** {product[3]} рублей"
        )
        await message.answer(product_info, parse_mode=ParseMode.MARKDOWN)

    await message.answer("Выберите продукт для покупки:", reply_markup=buttons.inline_product_menu)


async def fetch_products_with_images(message: types.Message):
    for i in range(1, 5):
        product = prices.services[i]
        product_info = (
            f"**Название:** {product['name']}\n"
            f"**Описание:** {product['description']}\n"
            f"**Цена:** {product['price']} рублей"
        )
        await message.answer(product_info, parse_mode=ParseMode.MARKDOWN)
        await message.answer_photo(photo=product["image_url"])


@dp.callback_query_handler(lambda call: call.data in ["buy", "about"])
async def main_menu_callback_handler(call: types.CallbackQuery):
    if call.data == "buy":
        await fetch_products_with_images(call.message)
    elif call.data == "about":
        await call.message.answer(ABOUT_US_MESSAGE, reply_markup=buttons.back_button_menu)
    await call.answer()


@dp.callback_query_handler(lambda call: call.data.startswith("product_buying"))
async def callback_buying_handler(call: types.CallbackQuery):
    await send_confirm_message(call)
    await call.answer()


@dp.callback_query_handler(lambda call: call.data == "go_back")
async def callback_back_handler(call: types.CallbackQuery):
    await call.message.answer("Вы вернулись в главное меню.", reply_markup=buttons.main_menu)
    await call.answer()


async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")


if __name__ == '__main__':
    crud_functions.initiate_db()
    executor.start_polling(dp, skip_updates=True)
