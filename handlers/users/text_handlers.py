from aiogram.types import Message
from data.loader import bot, dp, db
from keyboards.reply import generate_main_menu, generate_settings, \
    generate_products, generate_languages, generate_products_again
from keyboards.inline import generate_product_detail, generate_categories_for_user
from languages.langs import langs
from keyboards.inline import generate_cart_buttons
from handlers.utils import convert_price


@dp.message_handler(regexp='🏠 (Главное меню|Bosh menyu)')
async def show_main_menu(message: Message):
    lang = db.get_user_lang(message.chat.id)
    if lang == 'ru':
        await message.answer(f'Здравствуйте {message.from_user.full_name}', reply_markup=generate_main_menu(lang))
    else:
        await message.answer(f'Assalomu alaykum {message.from_user.full_name}', reply_markup=generate_main_menu(lang))




#  🏠 Афросиаб

@dp.message_handler(regexp='🛍 (Заказать|Buyurtma berish)')
async def show_menu(message: Message):
    lang = db.get_user_lang(message.chat.id)
    categories = db.get_all_categories()
    print(categories, lang)
    await message.answer(langs[lang]["today_menu"], reply_markup=generate_categories_for_user(categories, lang))


async def show_menu_again(message: Message):
    lang = db.get_user_lang(message.chat.id)
    await message.answer(langs[lang]["today_menu"], reply_markup=generate_products_again(lang))



@dp.message_handler(regexp='⚙️ (Настройки|Sozlamalar)')
async def show_settings(message: Message):
    lang = db.get_user_lang(message.chat.id)
    await message.answer(message.text, reply_markup=generate_settings(lang))


@dp.message_handler(regexp="🌐 (Изменить язык|Tilni o'zgartirish)")
async def change_settings_langs(message: Message):
    lang = db.get_user_lang(message.chat.id)

    await message.answer(langs[lang]["change_lang_reaction"], reply_markup=generate_languages())


@dp.message_handler(regexp="🛵 (Условия доставки|Yetkazib berish shartlari)")
async def show_delivery_about(message: Message):
    lang = db.get_user_lang(message.chat.id)
    await message.answer(langs[lang]["delivery_reaction"])
    await show_main_menu(message)


@dp.message_handler(regexp="ℹ️ (О нас|Biz haqimizda)")
async def show_about(message: Message):
    lang = db.get_user_lang(message.chat.id)
    await message.answer(langs[lang]["about_reaction"])
    await show_main_menu(message)


@dp.message_handler(lambda message: message.text in [i[0] for i in db.get_products_status_1()])
async def show_product_detail(message: Message):
    lang = db.get_user_lang(message.chat.id)
    product = db.get_product_by_title(message.text)

    caption = f'Товар: {product[1]}\n\n{product[2]}\n\nЦена {convert_price(product[3])}'

    await bot.send_photo(message.chat.id,
                         photo=product[4],
                         caption=caption,
                         reply_markup=generate_product_detail(product[0], lang)
                         )


@dp.message_handler(regexp="📥 (Корзина|Savat)")
async def show_cart(message: Message):
    chat_id = message.chat.id
    lang = db.get_user_lang(message.chat.id)
    try:
        await bot.delete_message(chat_id, message.message_id)
    except:
        pass
    if db.get_cart_id(chat_id):
        cart_id = db.get_cart_id(chat_id)[0]
    else:
        db.create_cart_for_user(chat_id)
        cart_id = db.get_cart_id(chat_id)[0]
    db.update_cart_total_price_quantity(cart_id)
    total_price, total_quantity = db.get_cart_total_price_quantity(cart_id)
    try:
        total_price, total_quantity = int(total_price), int(total_quantity)
    except:
        total_price, total_quantity = 0, 0
    cart_products = db.get_cart_products_by_cart_id(cart_id)

    if len(cart_products) == 0:
        await bot.send_message(chat_id, langs[lang]["empty_cart_message"])
        await show_menu(message)
    else:
        text = f'''{langs[lang]["your_cart"]}'''
        print(total_price, total_quantity, cart_products)
        for cart_product in cart_products:
            text += f'{cart_product[2]} - {cart_product[4]} {langs[lang]["dona"]} - {convert_price(cart_product[3])} {langs[lang]["sum"]}\n\n'
        price = db.get_delivery_price()
        text += f'''{langs[lang]["total_quantity_start"]} {total_quantity} {langs[lang]["dona"]}
{langs[lang]["total_price_start"]} {convert_price(total_price)} {langs[lang]["sum"]}
{langs[lang]['delivery_price']} {price} {langs[lang]["sum"]}'''

        await bot.send_message(chat_id, text,
                               reply_markup=generate_cart_buttons(cart_products, cart_id, lang))



@dp.message_handler(regexp="📦 (Мои заказы|Buyurtmalarim)")
async def show_orders_history(message: Message):
    chat_id = message.chat.id
    lang = db.get_user_lang(chat_id)
    orders = db.get_last_orders(chat_id)
    if lang == 'ru':
        text = 'Ваши последние заказы:\n'
    else:
        text = 'Oxirgi buyurtmalaringiz:\n'
    for order in orders:
        if lang == 'ru':
            text += f'''Номер заказа: {order[0]}
Адрес: {order[3]}
Статус: {order[4]}
Время заказа: {order[5]}
На сумму: {convert_price(order[7])}\n\n'''
        else:
            text += f'''Buyurtma raqami: {order[0]}
<b>Manzil:</b> {order[3]}
<b>Maqomi:</b> {order[4]}
<b>Вuyurtma vaqti:</b> {order[5]}
<b>Miqdorga:</b> {convert_price(order[7])}\n\n'''
        order_products = db.get_order_products(order[0])
        for ord_product in order_products:
            text += f'{ord_product[2]} - {ord_product[4]} - {ord_product[3]}\n'

    await message.answer(text)
    await show_main_menu(message)


