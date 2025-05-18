import logging
from time import sleep
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, ContentTypes, ReplyKeyboardRemove
from data.loader import bot, dp, db
from handlers.utils import convert_price
from states.states import AddProductStates, SendMessageStates, EditPriceState
from handlers.users.commands import command_start
from keyboards.reply import generate_admin_start, generate_products_for_delete, generate_month_markup, \
     back_admin_product, generate_commit_create_product
from keyboards.inline import generate_category_create_buttons

# 2. Создать класс состояний (StatesGroup) и определить необходимые состояния:


@dp.message_handler(commands=['register_as_amirkhon'])
async def register_admin(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    try:
        db.insert_admin(chat_id, full_name)
        await message.answer('Вы зарегистрировались как администратор. Для входа в админ панель нажмите /admin')
    except Exception as e:
        print(e)
        await message.answer('Вы уже зарегистрировались. Для входа в админ панель нажмите /admin')


@dp.message_handler(commands=['admin'])
@dp.message_handler(regexp='◀Назад в админку')
async def admin_start(message: Message):
    chat_id = message.chat.id
    admin = db.get_admin_by_id(chat_id)
    if admin:
        await message.answer('Здравствуйте. Выберите что хотите сделать. Если хотите выйти из админ панели. назмите /start',
                             reply_markup=generate_admin_start())
    else:
        await command_start(message)



@dp.callback_query_handler(lambda call: call.data.startswith('add_new_product_'))
async def start_add_product(call, state: FSMContext):
    firm_id = int(call.data.replace('add_new_product_', ''))
    firm = db.get_firm(firm_id)
    chat_id = call.message.chat.id
    await state.update_data(firm_id=firm_id)
    await call.message.reply(f"Привет! Давай создадим новый товар фирмы: {firm[1]}.\nВведи название товара  🇷🇺:", reply_markup=ReplyKeyboardRemove())
    await AddProductStates.waiting_for_name_ru.set()


@dp.message_handler(state=AddProductStates.waiting_for_name_ru)
async def process_name_ru(message: Message, state: FSMContext):
    await state.update_data(name_ru=message.text)
    await message.reply("Отлично! Теперь введите название товара 🇺🇿:", reply_markup=back_admin_product())
    await AddProductStates.waiting_for_name_uz.set()


@dp.message_handler(state=AddProductStates.waiting_for_name_uz)
async def process_name_uz(message: Message, state: FSMContext):
    await state.update_data(name_uz=message.text)
    await message.reply("Отлично! Теперь введите описание товара 🇷🇺:", reply_markup=back_admin_product())
    await AddProductStates.waiting_for_description_ru.set()


@dp.message_handler(state=AddProductStates.waiting_for_description_ru)
async def process_desc_ru(message: Message, state: FSMContext):
    if message.text == '🔙 с начала':
        await message.answer('Начнем с начала')
        await state.finish()
        await admin_start(message)
    else:
        await state.update_data(description_ru=message.text)
        await message.reply("Отлично! Теперь введите описание товара 🇺🇿:", reply_markup=back_admin_product())
        await AddProductStates.waiting_for_description_uz.set()


@dp.message_handler(state=AddProductStates.waiting_for_description_uz)
async def process_description_uz(message: Message, state: FSMContext):
    if message.text == '🔙 с начала':
        await message.answer('Начнем с начала')
        await state.finish()
        await admin_start(message)
    else:
        await state.update_data(description_uz=message.text)
        await message.reply("Хорошо! Теперь отправь мне картинку товара:", reply_markup=back_admin_product())
        await AddProductStates.waiting_for_image.set()


@dp.message_handler(content_types=[ContentType.PHOTO, ContentType.TEXT], state=AddProductStates.waiting_for_image)
async def process_image(message: Message, state: FSMContext):
    if message.text == '🔙 с начала':
        await message.answer('Начнем с начала')
        await state.finish()
        await admin_start(message)
    else:
        photo_id = message.photo[-1].file_id
        await state.update_data(image=photo_id)
        await message.reply("Отлично! Теперь введи цену товара:", reply_markup=back_admin_product())
        await AddProductStates.waiting_for_price.set()


@dp.message_handler(state=AddProductStates.waiting_for_price)
async def process_price(message: Message, state: FSMContext):
    if message.text == '🔙 с начала':
        await message.answer('Начнем с начала')
        await state.finish()
        await admin_start(message)
    else:
        await state.update_data(price=message.text)
        data = await state.get_data()
        chat_id = message.chat.id
        # Вывод информации о товаре
        # Очистка состояния
        # db.create_products(data['name'], data['description'], data['price'], data['image'])
        # Отправка информации о товаре пользователю
        await bot.send_photo(chat_id,
                         photo=data['image'],
                         caption=f'''Посмотрите и подтвердите или отмените создание товара\n{data['name_ru']}\n{data['name_uz']}\n\n{data['description_ru']}\n{data['description_uz']}\n\nЦена: {convert_price(data['price'])} сум''',
                             reply_markup=generate_commit_create_product())
        await AddProductStates.waiting_to_commit.set()

        # await admin_start(message)

@dp.message_handler(regexp='(👍 Подтвердить|👎 Отмена)', state=AddProductStates.waiting_to_commit)
async def stop_product_create(message: Message, state: FSMContext):
    if message.text == '👍 Подтвердить':
        data = await state.get_data()
        chat_id = message.chat.id
        # Вывод информации о товаре
        # Очистка состояния
        await state.finish()
        db.create_products(data['name_ru'],data['name_uz'], data['description_ru'],data['description_uz'], data['price'], data['image'], data['firm_id'])
        # Отправка информации о товаре пользователю
        await bot.send_message(chat_id, text=f'''Товар успешно создан''')
    else:
        await state.finish()
        await message.answer('Отменено создание товара')
    await admin_start(message)



@dp.message_handler(regexp='🚮 [\s\S]*')
async def reaction_to_delete(message: Message):
    product = message.text
    product = product.replace('🚮 ', '')
    db.delete_product(product)
    await message.answer('Товар успешно удален')
    await admin_start(message)


@dp.message_handler(regexp='🗃 Статистика')
async def show_statistic(message: Message):
    await message.answer(f'''Выберите период статистики: ''', reply_markup=generate_month_markup())

@dp.message_handler(regexp='👨‍👩‍👦‍👦 Рассылка всем')
async def start_sending_all(message: Message):
    await SendMessageStates.text.set()
    await message.reply("Отправьте текст сообщения для рассылки:")


@dp.message_handler(state=SendMessageStates.text, content_types=ContentTypes.TEXT)
async def get_message_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await SendMessageStates.photo.set()
    await message.reply("Отправьте фото для рассылки:")


@dp.message_handler(state=SendMessageStates.photo, content_types=ContentTypes.PHOTO)
async def get_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    await send_broadcast(state)
    await admin_start(message)


async def send_broadcast(state: FSMContext):
    async with state.proxy() as data:
        message_text = data['text']
        message_photo = data['photo']
    users_to_send = db.get_all_users()
    for user_id in users_to_send:
        try:
            await bot.send_photo(user_id[0], message_photo, caption=message_text)
            sleep(0.5)
        except Exception as e:
            logging.exception(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

    # Сброс состояния после рассылки
    await state.finish()


@dp.message_handler(regexp='1️⃣ месяц')
async def show_1_m_stat(message: Message):
    count_orders = db.get_count_orders_1_month()[0]
    sum_orders = db.get_sum_of_price_orders1()[0]
    count_users = len(db.get_all_users())
    await message.answer(f'''Всего пользователей: {count_users}

За последний месяц было заказано: {count_orders} заказов

На общую сумму: {convert_price(sum_orders)} сум''')
    await admin_start(message)


@dp.message_handler(regexp='Сегодня с 01:00 до 12:00')
async def show_today_morning_stat(message: Message):
    orders = db.get_today_morning()
    text = '''Сегодня с 01:00 до 12:00:\n\n'''
    if len(orders) > 0:
        for order in orders:
            text += f'Заказ №{order[0]} - {order[6]}шт - {order[7]} сум\n\n'
            order_items = db.get_order_products(order[0])
            for order_item in order_items:
                text += f'\t{order_item[2]} - {order_item[4]}шт - {order_item[3]} сум\n'
    else:
        text += 'Ничего не было заказано'
    await message.answer(text)
    await admin_start(message)


@dp.message_handler(regexp='Сегодня с 12:00 до 01:00')
async def show_today_day_stat(message: Message):
    orders = db.get_today_day()
    text = '''Сегодня с 12:00 до 01:00:\n\n'''
    if len(orders) > 0:
        for order in orders:
            text += f'Заказ №{order[0]} - {order[6]}шт - {order[7]} сум\n\n'
            order_items = db.get_order_products(order[0])
            for order_item in order_items:
                text += f'\t{order_item[2]} - {order_item[4]}шт - {order_item[3]} сум\n'
    else:
        text += 'Ничего не было заказано'
    await message.answer(text)
    await admin_start(message)


@dp.message_handler(regexp='3️⃣ месяца')
async def show_3_m_stat(message: Message):
    count_orders = db.get_count_orders_3_month()[0]
    sum_orders = db.get_sum_of_price_orders3()[0]
    count_users = len(db.get_all_users())
    await message.answer(f'''Всего пользователей: {count_users}

За последние 3 месяца было заказано: {count_orders} заказов

На общую сумму: {convert_price(sum_orders)} сум''')
    await admin_start(message)


@dp.message_handler(regexp='6️⃣ месяцев')
async def show_6_m_stat(message: Message):
    count_orders = db.get_count_orders_6_month()[0]
    sum_orders = db.get_sum_of_price_orders6()[0]
    count_users = len(db.get_all_users())
    await message.answer(f'''Всего пользователей: {count_users}

За последние 6 месяцев было заказано: {count_orders} заказов

На общую сумму: {convert_price(sum_orders)} сум''')
    await admin_start(message)


@dp.message_handler(regexp='1️⃣2️⃣ месяцев')
async def show_12_m_stat(message: Message):
    count_orders = db.get_count_orders_12_month()[0]
    sum_orders = db.get_sum_of_price_orders12()[0]
    count_users = len(db.get_all_users())
    await message.answer(f'''Всего пользователей: {count_users}

За последние 12 месяцев было заказано: {count_orders} заказов

На общую сумму: {convert_price(sum_orders)} сум''')
    await admin_start(message)



@dp.message_handler(regexp='♻ Изменить меню')
async def change_menu(message: Message):
    chat_id = message.chat.id
    categories = db.get_all_categories()
    await bot.send_message(chat_id, 'Выберите категорию или добавьте новую', reply_markup=generate_category_create_buttons(categories))



@dp.message_handler(regexp='🚚 Изменить стоимость доставки')
async def start_change_price(message: Message):
    chat_id = message.chat.id
    await EditPriceState.price.set()
    await bot.send_message(chat_id, 'Введите новую цену доставки')


@dp.message_handler(state=EditPriceState.price)
async def get_new_price(message: Message, state: FSMContext):
    chat_id = message.chat.id
    price = message.text
    await state.finish()
    db.update_delivery_price(int(price))
    await bot.send_message(chat_id, 'Цена изменена у пользователей')
    await admin_start(message)



