from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.loader import db
from languages.langs import langs
def generate_languages():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    ru = KeyboardButton(text='Русский 🇷🇺')
    uz = KeyboardButton(text="O'zbekcha 🇺🇿")
    markup.add(ru, uz)
    return markup

def generate_phone_number(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    phone = KeyboardButton(text=langs[lang]["share_contact"], request_contact=True)
    markup.add(phone)
    return markup


def generate_main_menu(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    order = KeyboardButton(text=langs[lang]["order_btn"])
    delivery = KeyboardButton(text=langs[lang]["delivery_btn"])
    feedback = KeyboardButton(text=langs[lang]["history_btn"])
    cart = KeyboardButton(text=langs[lang]["cart_btn"])
    settings = KeyboardButton(text=langs[lang]["settings_btn"])
    markup.row(order)
    markup.row(feedback, settings)
    markup.row(delivery, cart)
    return markup


def generate_settings(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    change_langs = KeyboardButton(text=langs[lang]['settings_reaction_langs'])
    main_menu = KeyboardButton(text=langs[lang]['main_menu'])
    markup.row(change_langs)
    markup.row(main_menu)
    return markup



def generate_products(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    cart = KeyboardButton(text=langs[lang]["cart_btn"])
    main_btn = KeyboardButton(text=langs[lang]["main_menu"])
    products = [i[0] for i in db.get_products_status_1()]
    for product in products:
        btn = KeyboardButton(text=product)
        markup.row(btn)
    markup.add(cart, main_btn)
    return markup


def generate_admin_start():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    change_menu = KeyboardButton(text='♻ Изменить меню')
    statistic = KeyboardButton(text='🗃 Статистика')
    send_to_all = KeyboardButton(text='👨‍👩‍👦‍👦 Рассылка всем')
    delivery_price = KeyboardButton(text='🚚 Изменить стоимость доставки')
    markup.row(change_menu)
    markup.row(statistic, send_to_all)
    markup.row(delivery_price)
    return markup

def generate_money(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    cart = KeyboardButton(text=langs[lang]["cart_money"])
    cash = KeyboardButton(text=langs[lang]["cash_money"])
    markup.add(cart, cash)
    return markup


def generate_location(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    loc = KeyboardButton(text=langs[lang]["location_btn"], request_location=True)
    markup.add(loc)
    return markup


def generate_products_for_delete():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    products = [i[0] for i in db.get_products_status_1()]
    for product in products:
        btn = KeyboardButton(text=f'🚮 {product}')
        markup.row(btn)
    main_btn = KeyboardButton(text=langs['ru']["main_menu"])
    markup.row(main_btn)
    return markup


def commit_location(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    yes = KeyboardButton(text=langs[lang]['yes_btn'])
    no = KeyboardButton(text=langs[lang]['no_btn'])
    markup.add(yes, no)
    return markup

def generate_products_again(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    cart = KeyboardButton(text=langs[lang]["cart_btn"])
    main_btn = KeyboardButton(text=langs[lang]["main_menu"])
    markup.add(cart)
    markup.add(main_btn)
    return markup

def generate_month_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = KeyboardButton(text='Сегодня с 01:00 до 12:00')
    btn2 = KeyboardButton(text='Сегодня с 12:00 до 01:00')
    month1 = KeyboardButton(text='1️⃣ месяц')
    month3 = KeyboardButton(text='3️⃣ месяца')
    month6 = KeyboardButton(text='6️⃣ месяцев')
    month12 = KeyboardButton(text='1️⃣2️⃣ месяцев')
    back_btn = KeyboardButton(text='◀Назад в админку')
    markup.row(btn1)
    markup.row(btn2)
    markup.add(month1, month3, month6)
    markup.add(month12, back_btn)
    return markup



def back_admin_product():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text='🔙 с начала')
    markup.add(btn)
    return markup


def generate_commit_create_product():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    good = KeyboardButton(text="👍 Подтвердить")
    bad = KeyboardButton(text="👎 Отмена")
    markup.add(good, bad)
    return markup
