from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from languages.langs import langs

def generate_product_detail(product_id, lang, quantity=1):
    markup = InlineKeyboardMarkup()
    minus_btn = InlineKeyboardButton('➖', callback_data='minus')
    quan_btn = InlineKeyboardButton(str(quantity), callback_data=f'quantity_{product_id}')
    plus_btn = InlineKeyboardButton('➕', callback_data='plus')
    buy_btn = InlineKeyboardButton(text=langs[lang]["get_order_btn"], callback_data=f'buy_{product_id}_{quantity}')
    cart_btn = InlineKeyboardButton(text=langs[lang]["cart_btn"], callback_data='cart')
    back_btn = InlineKeyboardButton(text=langs[lang]['back'], callback_data=f'all_products_back_{product_id}')
    main_menu = InlineKeyboardButton(text=langs[lang]["main_menu"], callback_data='main_menu')
    markup.add(minus_btn, quan_btn, plus_btn)
    markup.add(buy_btn)

    markup.add(cart_btn)
    markup.add(back_btn)
    markup.add(main_menu)
    return markup


def generate_product_detail_available_0(product_id, lang):
    markup = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton(text=langs[lang]['back'], callback_data=f'all_products_back_{product_id}')
    markup.add(back_btn)
    return markup


def generate_cart_buttons(cart_products, cart_id, lang):
    markup = InlineKeyboardMarkup()
    print(cart_products)
    # (2, 1, 'Адана (Шашлык)', 60000, 1)
    clear = InlineKeyboardButton(text=langs[lang]["clear_btn"], callback_data='clear')
    order = InlineKeyboardButton(text=langs[lang]["buy_btn"], callback_data=f'order_{cart_id}')
    main_menu = InlineKeyboardButton(text=langs[lang]["main_menu"], callback_data='main_menu')
    markup.row(order)
    markup.row(main_menu, clear)
    for cart_product in cart_products:
        name = InlineKeyboardButton(text=f'❌{cart_product[2]}', callback_data=f'remove_{cart_product[0]}')
        markup.row(name)
    return markup


def generate_commit_order(order_id, lat, lon, chat_id, cart_id):
    markup = InlineKeyboardMarkup()
    yes = InlineKeyboardButton(text='Подтвердить', callback_data=f'commit_{order_id}_{chat_id}_{cart_id}')
    no = InlineKeyboardButton(text='Отмена', callback_data=f'cancel_{order_id}_{chat_id}_{cart_id}')
    loc = InlineKeyboardButton(text='Открыть яндекс', url=f'https://3.redirect.appmetrica.yandex.com/route?end-lat={lat}&end-lon={lon}&ref=telegrambot&appmetrica_tracking_id=1178268795219780156')
    markup.add(yes, no)
    markup.add(loc)
    return markup


def generate_commit():
    markup = InlineKeyboardMarkup()
    com = InlineKeyboardButton(text='✅✅✅Подтверждено!✅✅✅', callback_data='asd')
    markup.add(com)
    return markup


def generate_cancel():
    markup = InlineKeyboardMarkup()
    com = InlineKeyboardButton(text='❌❌❌Отменено!❌❌❌', callback_data='asd')
    markup.add(com)
    return markup



def generate_category_create_buttons(categories):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for category in categories:
        btn = InlineKeyboardButton(text=category[1], callback_data=f'goto_category_{category[0]}')
        buttons.append(btn)
    markup.add(*buttons)
    add = InlineKeyboardButton(text='✅ Добавить категорию ✅', callback_data='add_new_category')
    markup.add(add)
    return markup

def generate_subcategories_admin_buttons(subcategories, category_id):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for category in subcategories:
        btn = InlineKeyboardButton(text=category[1], callback_data=f'goto_subcategory_{category[0]}')
        buttons.append(btn)
    markup.add(*buttons)
    add = InlineKeyboardButton(text='✅ Добавить подкатегорию ✅', callback_data=f'add_new_subcategory_{category_id}')
    delete = InlineKeyboardButton(text='❌ Удалить эту категорию ❌', callback_data=f'delete_category_{category_id}')
    back = InlineKeyboardButton(text='🔙 Назад 🔙', callback_data='back_to_all_categories')
    markup.add(add)
    markup.add(delete)
    markup.add(back)
    return markup

def generate_firms_admin_buttons(firms, subcategory_id):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for firm in firms:
        btn = InlineKeyboardButton(text=firm[1], callback_data=f'goto_firm_{firm[0]}')
        buttons.append(btn)
    markup.add(*buttons)
    add = InlineKeyboardButton(text='✅ Добавить фирму ✅', callback_data=f'add_new_firm_{subcategory_id}')
    delete = InlineKeyboardButton(text='❌ Удалить эту подкатегорию ❌', callback_data=f'delete_subcategory_{subcategory_id}')
    back = InlineKeyboardButton(text='🔙 Назад 🔙', callback_data='back_to_all_categories')
    markup.add(add)
    markup.add(delete)
    markup.add(back)
    return markup

def generate_products_admin_buttons(products, firm_id):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for product in products:
        btn = InlineKeyboardButton(text=product[1], callback_data=f'goto_product_{product[0]}')
        buttons.append(btn)
    markup.add(*buttons)
    add = InlineKeyboardButton(text='✅ Добавить товар ✅', callback_data=f'add_new_product_{firm_id}')
    delete = InlineKeyboardButton(text='❌ Удалить эту фирму ❌', callback_data=f'delete_firm_{firm_id}')
    back = InlineKeyboardButton(text='🔙 Назад 🔙', callback_data=f'back_to_subcategory_{firm_id}')
    markup.add(add)
    markup.add(delete)
    markup.add(back)
    return markup


def generate_categories_for_user(categories, lang):
    markup = InlineKeyboardMarkup()
    for category in categories:
        if lang == 'ru':
            btn = InlineKeyboardButton(text=category[1], callback_data=f'user_category_{category[0]}')
        else:
            btn = InlineKeyboardButton(text=category[2], callback_data=f'user_category_{category[0]}')
        markup.add(btn)
    return markup


def generate_subcategories_for_user(subcategories, category_id, lang):
    markup = InlineKeyboardMarkup()
    for category in subcategories:
        if lang == 'ru':
            btn = InlineKeyboardButton(text=category[1], callback_data=f'user_subcategory_{category[0]}_{category_id}')
        else:
            btn = InlineKeyboardButton(text=category[2], callback_data=f'user_subcategory_{category[0]}_{category_id}')

        markup.add(btn)
    if lang == 'ru':
        back = InlineKeyboardButton(text='Назад', callback_data=f'back_category')
    else:
        back = InlineKeyboardButton(text='Orqaga', callback_data=f'back_category')
    markup.row(back)
    return markup

def generate_firms_for_user(firms, category_id, lang):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for firm in firms:
        if lang == 'ru':
            btn = InlineKeyboardButton(text=firm[1], callback_data=f'user_firms_{firm[0]}')
        else:
            btn = InlineKeyboardButton(text=firm[2], callback_data=f'user_firms_{firm[0]}')
        buttons.append(btn)
    if lang == 'ru':
        back = InlineKeyboardButton(text='Назад', callback_data=f'back_subcategory_{category_id}')
    else:
        back = InlineKeyboardButton(text='Orqaga', callback_data=f'back_subcategory_{category_id}')
    markup.add(*buttons)
    markup.row(back)
    return markup

def generate_products_for_user(products, firm_id, lang):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for product in products:
        if lang == 'ru':
            btn = InlineKeyboardButton(text=product[1], callback_data=f'user_product_detail_{product[0]}')
        else:
            btn = InlineKeyboardButton(text=product[2], callback_data=f'user_product_detail_{product[0]}')
        buttons.append(btn)
    markup.add(*buttons)
    if lang == 'ru':
        back = InlineKeyboardButton(text='Назад', callback_data=f'back_firm_{firm_id}')
    else:
        back = InlineKeyboardButton(text='Orqaga', callback_data=f'back_firm_{firm_id}')
    markup.row(back)

    return markup


def generate_product_detail_for_admin(product_id):
    markup = InlineKeyboardMarkup()
    edit_price = InlineKeyboardButton(text='🔁Изменить цену', callback_data=f'edit_price_{product_id}')
    add_photo = InlineKeyboardButton(text='🔁Изменить фото', callback_data=f'edit_photo_{product_id}')
    add_title_ru = InlineKeyboardButton(text='🔁Название 🇷🇺', callback_data=f'edit_titleru_{product_id}')
    add_title_uz = InlineKeyboardButton(text='🔁Название 🇺🇿', callback_data=f'edit_titleuz_{product_id}')
    add_desc_ru = InlineKeyboardButton(text='🔁Описание 🇷🇺', callback_data=f'edit_descru_{product_id}')
    add_desc_uz = InlineKeyboardButton(text='🔁Описание 🇺🇿', callback_data=f'edit_descuz_{product_id}')
    delete_product = InlineKeyboardButton(text='❌ Удалить этот товар ❌', callback_data=f'delete_product_{product_id}')
    available_product = InlineKeyboardButton(text='🔁✅❌Изменить статус', callback_data=f'available_{product_id}')
    back = InlineKeyboardButton(text='🔙 Назад 🔙', callback_data=f'back_to_products_list_{product_id}')
    markup.add(edit_price, add_photo)
    markup.add(add_title_ru, add_title_uz)
    markup.add(add_desc_ru, add_desc_uz)
    markup.add(available_product)
    markup.add(delete_product)
    markup.add(back)
    return markup


