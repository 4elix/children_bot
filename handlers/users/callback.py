import requests as requests
from aiogram.dispatcher import FSMContext
from data.loader import db, dp, bot
from aiogram.types import CallbackQuery, ContentType, Message, InputFile

from handlers.utils import convert_price
from keyboards.inline import generate_product_detail, generate_cart_buttons, generate_subcategories_for_user, \
    generate_firms_for_user, generate_products_for_user, generate_categories_for_user, \
    generate_product_detail_available_0
from languages.langs import langs
from handlers.users.text_handlers import show_menu, show_menu_again, show_main_menu
from states.states import LocationForm
from keyboards.reply import generate_location, generate_money
from keyboards.inline import generate_commit_order, generate_commit, generate_cancel


@dp.callback_query_handler(lambda call: call.data.startswith('back_category'))
async def back_to_categories(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    lang = db.get_user_lang(call.message.chat.id)
    await bot.delete_message(chat_id, message_id)
    categories = db.get_all_categories()
    await bot.send_message(chat_id, langs[lang]["today_menu"],
                           reply_markup=generate_categories_for_user(categories, lang))


@dp.callback_query_handler(lambda call: call.data.startswith('back_subcategory_'))
@dp.callback_query_handler(lambda call: call.data.startswith('user_category_'))
async def reaction_to_user_category(call: CallbackQuery):
    if call.data.startswith('user_category_'):
        category_id = int(call.data.replace('user_category_', ''))
    else:
        print(call.data)
        category_id = int(call.data.replace('back_subcategory_', ''))
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    lang = db.get_user_lang(call.message.chat.id)
    await bot.delete_message(chat_id, message_id)
    subcategories = db.get_subcategories_for_admin(category_id)
    await bot.send_message(chat_id, langs[lang]['subcategory_select'],
                           reply_markup=generate_subcategories_for_user(subcategories, category_id, lang))


@dp.callback_query_handler(lambda call: call.data.startswith('user_subcategory_'))
async def reaction_to_user_subcategory(call: CallbackQuery):
    subcategory_id = int(call.data.split('_')[2])  # user_subcategory_2_1
    category_id = int(call.data.split('_')[3])  # user_subcategory_2_1
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    lang = db.get_user_lang(call.message.chat.id)
    try:
        await bot.delete_message(chat_id, message_id)
        await bot.delete_message(chat_id, message_id - 1)
        await bot.delete_message(chat_id, message_id - 2)
    except:
        pass
    firms = db.get_firms_for_user(subcategory_id)
    print(firms)
    await bot.send_message(chat_id, langs[lang]['firm_select'],
                           reply_markup=generate_firms_for_user(firms, category_id, lang))


@dp.callback_query_handler(lambda call: call.data.startswith('back_firm_'))
async def reaction_to_back_firm(call: CallbackQuery):
    firm_id = int(call.data.replace('back_firm_', ''))
    subcategory_id = db.get_subcategory_by_firm_id(firm_id)
    category_id = db.get_category_id_by_subcategory_id(subcategory_id)
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    lang = db.get_user_lang(call.message.chat.id)
    try:
        await bot.delete_message(chat_id, message_id)
        await bot.delete_message(chat_id, message_id - 1)
        await bot.delete_message(chat_id, message_id - 2)
    except:
        pass
    firms = db.get_firms_for_user(subcategory_id)
    print(firms)
    await bot.send_message(chat_id, langs[lang]['firm_select'],
                           reply_markup=generate_firms_for_user(firms, category_id, lang))


@dp.callback_query_handler(lambda call: call.data.startswith('user_firms_'))
async def reaction_to_user_firm(call: CallbackQuery):
    try:
        if call.data.startswith('user_firms_'):
            firm_id = int(call.data.replace('user_firms_', ''))
        else:
            print(call.data)
            firm_id = int(call.data.replace('back_firm_', ''))
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        lang = db.get_user_lang(call.message.chat.id)
        try:
            await bot.delete_message(chat_id, message_id)
            await bot.delete_message(chat_id, message_id - 1)
            await bot.delete_message(chat_id, message_id - 2)
        except:
            pass
        products = db.get_products_for_admin(firm_id)

        await bot.send_message(chat_id, 'Выберите товар: ',
                               reply_markup=generate_products_for_user(products, firm_id, lang))
    except Exception as e:
        await bot.send_message(chat_id, e)


@dp.callback_query_handler(lambda call: call.data.startswith('all_products_back_'))
async def reaction_to_back_list_products(call: CallbackQuery):
    chat_id = call.message.chat.id
    product_id = call.data.replace('all_products_back_', '')
    firm_id = db.get_firm_id_by_product_id(product_id)
    lang = db.get_user_lang(chat_id)
    message_id = call.message.message_id
    await bot.delete_message(chat_id, message_id)
    products = db.get_products_for_users(firm_id)
    await bot.send_message(chat_id, 'Выберите товар: ',
                           reply_markup=generate_products_for_user(products, firm_id, lang))


@dp.callback_query_handler(lambda call: call.data.startswith('user_product_detail_'))
async def show_product_detail(call: CallbackQuery):
    product_id = int(call.data.replace('user_product_detail_', ''))
    lang = db.get_user_lang(call.message.chat.id)
    product = db.get_product_detail_by_id(product_id)
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        await bot.delete_message(call.message.chat.id, call.message.message_id - 2)
    except:
        pass
    available = product[::-1][0]
    if available == 1:
        if lang == 'ru':
            caption = f'Товар: {product[1]}\n\n{product[3]}\n\nЦена {convert_price(product[5])}'
        else:
            caption = f'Mahsulot: {product[2]}\n\n{product[4]}\n\nNarx {convert_price(product[5])}'

        await bot.send_photo(call.message.chat.id, photo=product[6], caption=caption,
                             reply_markup=generate_product_detail(product[0], lang))
    elif available == 0:
        if lang == 'ru':
            caption = f'Товар: {product[1]}\n\n{product[3]}\n\nЦена {convert_price(product[5])}\n\nТовара нету в наличии'
        else:
            caption = f'Mahsulot: {product[2]}\n\n{product[4]}\n\nNarx {convert_price(product[5])}\n\nTovar mavjud emas'

        await bot.send_photo(call.message.chat.id, photo=product[6], caption=caption,
                             reply_markup=generate_product_detail_available_0(product[0], lang))


@dp.callback_query_handler(lambda call: call.data == 'plus')
async def reaction_to_plus(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    lang = db.get_user_lang(call.message.chat.id)
    buttons = call.message.reply_markup.inline_keyboard
    quantity = int(buttons[0][1].text)
    product_id = buttons[0][1].callback_data.split('_')[1]
    if quantity < 100:
        quantity += 1
        await bot.edit_message_reply_markup(chat_id, message_id,
                                            reply_markup=generate_product_detail(product_id, lang, quantity))
    else:
        await bot.answer_callback_query(call.id,
                                        'Вы не можете купить больше 100 товаров одного наименования')


@dp.callback_query_handler(lambda call: call.data == 'minus')
async def reaction_to_minus(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    buttons = call.message.reply_markup.inline_keyboard
    quantity = int(buttons[0][1].text)
    lang = db.get_user_lang(call.message.chat.id)
    product_id = buttons[0][1].callback_data.split('_')[1]
    if quantity > 1:
        quantity -= 1
        await bot.edit_message_reply_markup(chat_id, message_id,
                                            reply_markup=generate_product_detail(product_id, lang, quantity))
    else:
        await bot.answer_callback_query(call.id,
                                        langs[lang]["error_less_1"])


@dp.callback_query_handler(lambda call: 'buy' in call.data)
async def add_product_to_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    lang = db.get_user_lang(chat_id)
    _, product_id, quantity = call.data.split('_')  # buy_1_2
    product_id, quantity = int(product_id), int(quantity)
    product_title_ru, product_title_uz, price = db.get_product_by_id(product_id)
    if lang == 'ru':
        product_name = product_title_ru
    else:
        product_name = product_title_uz
    final_price = quantity * price
    if db.get_cart_id(chat_id):
        cart_id = db.get_cart_id(chat_id)[0]
    else:
        db.create_cart_for_user(chat_id)
        cart_id = db.get_cart_id(chat_id)[0]

    try:
        '''Пытаемся закинуть новый товар в корзину'''
        db.insert_cart_product(cart_id, product_name, quantity, final_price)
        await bot.delete_message(chat_id, call.message.message_id)
        await bot.send_message(chat_id, langs[lang]["add_commit"])
    except:
        '''Если такой товар был, то обновляем его кол-во и цену'''
        db.update_cart_product(cart_id, product_name, quantity, final_price)
        await bot.delete_message(chat_id, call.message.message_id)
        await bot.send_message(chat_id, langs[lang]["change_commit"])
    await show_menu(call.message)


@dp.callback_query_handler(lambda call: 'cart' == call.data)
async def show_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    lang = db.get_user_lang(call.message.chat.id)
    try:
        await bot.delete_message(chat_id, call.message.message_id)
        await bot.delete_message(chat_id, call.message.message_id - 1)
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
        await show_menu(call.message)
    else:
        text = f'''{langs[lang]["your_cart"]}'''
        print(f'Пользователь: {call.message.from_user.full_name} - {call.message.chat.id}')
        print('Данные корзины: ', total_price, total_quantity, cart_products)

        print('Товары в корзине: ', cart_products)
        for cart_product in cart_products:
            text += f'{cart_product[2]} - {cart_product[4]} {langs[lang]["dona"]} - {convert_price(cart_product[3])} {langs[lang]["sum"]}\n\n'
        price = db.get_delivery_price()
        text += f'''{langs[lang]["total_quantity_start"]} {total_quantity} {langs[lang]["dona"]}
{langs[lang]["total_price_start"]} {convert_price(total_price)} {langs[lang]["sum"]}
{langs[lang]['delivery_price']} {price} {langs[lang]["sum"]}'''
        await bot.send_message(chat_id, text,
                               reply_markup=generate_cart_buttons(cart_products, cart_id, lang))


@dp.callback_query_handler(lambda call: "remove_" in call.data)
async def remove_cart_product_reaction(call: CallbackQuery):
    _, cart_product_id = call.data.split('_')  # remove_1
    message_id = call.message.message_id
    chat_id = call.message.chat.id
    db.delete_error(cart_product_id)
    lang = db.get_user_lang(call.message.chat.id)
    try:
        await bot.delete_message(chat_id, call.message.message_id)
        await bot.delete_message(chat_id, call.message.message_id - 1)
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
        await show_menu(call.message)
    else:
        text = f'''{langs[lang]["your_cart"]}'''
        print(f'Пользователь: {call.message.from_user.full_name} - {call.message.chat.id}')
        print('Данные корзины: ', total_price, total_quantity, cart_products)

        print('Товары в корзине: ', cart_products)
        for cart_product in cart_products:
            text += f'{cart_product[2]} - {cart_product[4]} {langs[lang]["dona"]} - {convert_price(cart_product[3])} {langs[lang]["sum"]}\n\n'
        price = db.get_delivery_price()
        text += f'''{langs[lang]["total_quantity_start"]} {total_quantity} {langs[lang]["dona"]}
{langs[lang]["total_price_start"]} {convert_price(total_price)} {langs[lang]["sum"]}
{langs[lang]['delivery_price']} {price} {langs[lang]["sum"]}'''
        await bot.send_message(chat_id, text,
                               reply_markup=generate_cart_buttons(cart_products, cart_id, lang))


@dp.callback_query_handler(lambda call: call.data == "clear")
async def clear_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    lang = db.get_user_lang(chat_id)
    cart_id = db.get_cart_id(chat_id)[0]
    cart_products = db.get_cart_products_by_cart_id(cart_id)
    for cart_product in cart_products:
        db.delete_error(cart_product[0])
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.send_message(call.message.chat.id, langs[lang]["you_clear_cart"])
    await show_menu(call.message)


@dp.callback_query_handler(lambda call: call.data == 'main_menu')
async def call_mail_menu_reaction(call: CallbackQuery):
    await show_menu(call.message)


@dp.callback_query_handler(lambda call: 'order_' in call.data)
async def commit_order_gey_money_type(call: CallbackQuery, state: FSMContext):
    _, cart_id = call.data.split('_')
    chat_id = call.message.chat.id
    await state.update_data(cart_id=cart_id)
    lang = db.get_user_lang(chat_id)
    await bot.send_message(chat_id, langs[lang]["choose_money"], reply_markup=generate_money(lang))
    await LocationForm.waiting_to_money_tipe.set()


@dp.message_handler(state=LocationForm.waiting_to_money_tipe)
async def commit_order_gey_money_type(message: Message, state: FSMContext):
    money = message.text
    chat_id = message.chat.id
    await state.update_data(money_type=money)
    lang = db.get_user_lang(chat_id)
    await LocationForm.waiting_for_location.set()
    await bot.send_message(chat_id, langs[lang]["send_location"], reply_markup=generate_location(lang))


@dp.message_handler(content_types=ContentType.LOCATION, state=LocationForm.waiting_for_location)
async def process_location(message: Message, state: FSMContext):
    location = message.location
    chat_id = message.chat.id
    lang = db.get_user_lang(chat_id)
    base_url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": 'de983ab4-e9a7-42ce-9154-81fa20293246',
        "format": "json",
        "geocode": f"{location.longitude},{location.latitude}",
    }

    response = requests.get(base_url, params=params)
    result = response.json()

    if "response" in result and "GeoObjectCollection" in result["response"]:
        features = result["response"]["GeoObjectCollection"]["featureMember"]
        if features:
            address = features[0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
        else:
            if lang == 'ru':
                address = "Адрес не найден"
            else:
                address = 'Manzil topilmadi'
    else:
        if lang == 'ru':
            address = "Адрес не найден"
        else:
            address = 'Manzil topilmadi'

    data = await state.get_data()
    cart_id = data.get('cart_id')
    money = data.get('money_type')
    await state.finish()
    # Сохранение заказа
    count_orders = len(db.get_count_orders_by_user(chat_id)) + 1
    cart = db.get_cart(cart_id)
    total_quantity, total_price = cart[2], cart[3]
    delivery_price = db.get_delivery_price()
    total_price += int(delivery_price)
    cart_products = db.get_cart_products_by_cart_id(cart_id)
    user = db.get_user_by_id(chat_id)
    db.create_order(chat_id, count_orders, total_quantity, total_price, address, money)
    order_id = db.get_order_id(chat_id, count_orders)[0]
    order = db.get_order(order_id)

    text = ''
    i = 1
    for cart_product in cart_products:
        product_name, final_price, quantity = cart_product[2], cart_product[3], cart_product[4]
        text += f'{i}. {product_name} - {quantity} шт - {convert_price(final_price)} сум\n'
        db.create_new_order_product(order_id, product_name, final_price, quantity)

    if lang == 'ru':
        await message.answer(f"""
Ваш заказ №{order[0]}
 
Ваш адрес: {address}

Ваш заказ:
{text}
Доставка: {delivery_price} сум
Большое спасибо. Ваш заказ принят. Вы увидите сообщение о статусе вашего заказа""")
    else:
        await message.answer(f"""
Buyurtmangiz №{order[0]}

Manzilingiz: {address}

Buyrtmangiz:
{text}
Yetkazib berish: {delivery_price} so'm
Katta rahmat. Buyurtmangiz qabul qilindi. Buyurtmangiz maqomini haqida xabarni ko‘rasiz.""")

    msg = await bot.send_message('-4185788925', f'''Заказ от клиента: {user[1]}
Общее количество заказов: {count_orders}
Оплата: {order[-1]}
Номер заказа: {order[0]}
Дата заказа: {order[5]}
Номер телефона: {user[2]}

Адрес: {address}

{text}

Доставка: {delivery_price} сум
        ''')
    await bot.send_location('-4185788925', reply_to_message_id=msg.message_id, latitude=location.latitude,
                            longitude=location.longitude,
                            reply_markup=generate_commit_order(order_id, location.latitude, location.longitude, chat_id,
                                                               cart_id))
    await show_main_menu(message)


@dp.callback_query_handler(lambda call: 'cancel' in call.data)
async def cancel_order(call: CallbackQuery):
    _, order_id, chat_id, cart_id = call.data.split('_')
    cart_products = db.get_cart_products_by_cart_id(cart_id)
    db.change_order_status(order_id, 'Отменен')
    for cart_product in cart_products:
        db.delete_error(cart_product[0])
    lang = db.get_user_lang(chat_id)
    message = call.message

    await bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=generate_cancel())

    if lang == 'ru':
        await bot.send_message(chat_id, f'Ваш заказ №{order_id} был отменен')
    else:
        await bot.send_message(chat_id, f'Sizning №{order_id} buyurtmangiz bekor qilongan')


@dp.callback_query_handler(lambda call: 'commit' in call.data)
async def commit_order(call: CallbackQuery):
    _, order_id, chat_id, cart_id = call.data.split('_')
    cart_products = db.get_cart_products_by_cart_id(cart_id)
    db.change_order_status(order_id, 'Подтвержден')
    for cart_product in cart_products:
        db.delete_error(cart_product[0])
    lang = db.get_user_lang(chat_id)
    message = call.message

    await bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=generate_commit())
    if lang == 'ru':
        await bot.send_message(chat_id,
                               f'Ваш заказ №{order_id} был подтвержден. С вами скоро свяжутся для уточнения информации')
    else:
        await bot.send_message(chat_id,
                               f"Sizning №{order_id} buyurtmangiz tasdiqlangan. Ma'lumotga aniqlik kiritish uchun tez orada siz bilan bog‘lanamiz")
