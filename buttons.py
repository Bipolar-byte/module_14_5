from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

main_menu = InlineKeyboardMarkup(row_width=2)

main_menu.add(
    InlineKeyboardButton(text="Регистрация", callback_data="registration")
)
main_menu.add(
    InlineKeyboardButton(text="Купить", callback_data="buy"),
    InlineKeyboardButton(text="О компании", callback_data="about"),
    InlineKeyboardButton(text="Наш сайт",
                         url="https://urban-university.ru/members/courses/course999421818026/20240131-0000domasnee-zadanie-po-teme-dorabotka-bota-439726756760"),
    InlineKeyboardButton(text="Контакты",
                         url="https://urban-university.ru/members/courses/course999421818026/20240131-0000domasnee-zadanie-po-teme-dorabotka-bota-439726756760")
)

inline_product_menu = InlineKeyboardMarkup(row_width=2)
inline_product_menu.add(
    InlineKeyboardButton(text="Product1", callback_data="product_buying_1"),
    InlineKeyboardButton(text="Product2", callback_data="product_buying_2"),
    InlineKeyboardButton(text="Product3", callback_data="product_buying_3"),
    InlineKeyboardButton(text="Product4", callback_data="product_buying_4"),
    InlineKeyboardButton(text="Назад", callback_data="go_back")
)

back_button_menu = ReplyKeyboardMarkup(resize_keyboard=True)
