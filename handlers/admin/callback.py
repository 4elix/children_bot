import requests as requests
from aiogram.dispatcher import FSMContext
from data.loader import db, dp, bot
from aiogram.types import CallbackQuery, ContentType, Message

from handlers.utils import convert_price
from keyboards.inline import generate_product_detail, generate_cart_buttons, generate_category_create_buttons, \
    generate_firms_admin_buttons, generate_products_admin_buttons, generate_product_detail_for_admin
from languages.langs import langs
from handlers.users.text_handlers import show_menu, show_menu_again
from states.states import LocationForm, AddNewCategory, AddNewSubCategory, AddNewFirm, EditPriceState, \
    EditProductPriceState, EditProductPhotoState, EditProductTitleRuState, EditProductTitleUzState, \
    EditProductDescRuState, EditProductDescUzState
from keyboards.reply import generate_location
from keyboards.inline import generate_commit_order, generate_commit, generate_cancel, \
    generate_subcategories_admin_buttons


@dp.callback_query_handler(lambda call: call.data == 'add_new_category')
async def reaction_to_add_new_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    await AddNewCategory.category_ru.set()
    await bot.send_message(chat_id, 'Введите название новой категории 🇷🇺: ')


@dp.message_handler(state=AddNewCategory.category_ru)
async def process_add_new_category_ru(message: Message, state: FSMContext):
    await state.update_data(category_ru=message.text)
    await AddNewCategory.category_uz.set()
    await message.answer('Введите название новой категории 🇺🇿: ')


@dp.message_handler(state=AddNewCategory.category_uz)
async def process_add_new_category_uz(message: Message, state: FSMContext):
    data = await state.get_data()

    db.create_new_category(data['category_ru'], message.text)
    await state.finish()
    await message.reply("Категория успешно создана. Перейдите в /admin")


@dp.callback_query_handler(lambda call: call.data.startswith('goto_category_'))
async def show_category_inside(call: CallbackQuery):
    category_id = int(call.data.replace('goto_category_', ''))
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.delete_message(chat_id, message_id)
    subcategories = db.get_subcategories_for_admin(category_id)
    print(subcategories)
    await bot.send_message(chat_id, 'Выберите подкатегорию: ',
                           reply_markup=generate_subcategories_admin_buttons(subcategories, category_id))


@dp.callback_query_handler(lambda call: call.data.startswith('delete_category_'))
async def reaction_to_delete_category_(call: CallbackQuery):
    category_id = int(call.data.replace('delete_category_', ''))
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.delete_message(chat_id, message_id)
    db.delete_category(category_id)
    await bot.send_message(chat_id, "Категория успешно УДАЛЕНА. Перейдите в /admin")


@dp.callback_query_handler(lambda call: call.data == 'back_to_all_categories')
async def reaction_to_back_to_all_categories(call: CallbackQuery):
    chat_id = call.message.chat.id
    await bot.delete_message(chat_id, call.message.message_id)
    categories = db.get_all_categories()
    await bot.send_message(chat_id, 'Выберите категорию или добавьте новую',
                           reply_markup=generate_category_create_buttons(categories))


@dp.callback_query_handler(lambda call: call.data.startswith('add_new_subcategory'))
async def reaction_to_add_new_subcategory(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.replace('add_new_subcategory_', ''))
    category = db.get_category(category_id)
    chat_id = call.message.chat.id
    await state.update_data(category_id=category_id)
    await AddNewSubCategory.category_ru.set()
    await bot.send_message(chat_id, f'Введите название новой подкатегории для категории "{category[1]}"  🇷🇺: ')


@dp.message_handler(state=AddNewSubCategory.category_ru)
async def process_add_new_subcategory_ru(message: Message, state: FSMContext):
    await state.update_data(category_ru=message.text)
    await AddNewSubCategory.category_uz.set()
    await message.answer(f'Введите название новой подкатегории  🇺🇿: ')


@dp.message_handler(state=AddNewSubCategory.category_uz)
async def process_add_new_subcategory(message: Message, state: FSMContext):
    data = await state.get_data()
    db.create_new_subcategory(data['category_ru'], message.text, data['category_id'])
    await state.finish()
    await message.reply("Подкатегория успешно создана. Перейдите в /admin")


@dp.callback_query_handler(lambda call: call.data.startswith('delete_subcategory_'))
async def reaction_to_delete_subcategory_(call: CallbackQuery):
    category_id = int(call.data.replace('delete_subcategory_', ''))
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.delete_message(chat_id, message_id)
    db.delete_subcategory(category_id)
    await bot.send_message(chat_id, "Подкатегория успешно УДАЛЕНА. Перейдите в /admin")


@dp.callback_query_handler(lambda call: call.data.startswith('back_to_subcategory_'))
@dp.callback_query_handler(lambda call: call.data.startswith('goto_subcategory_'))
async def show_subcategory_inside(call: CallbackQuery):
    if call.data.startswith('back_to_subcategory_'):
        firm_id = int(call.data.replace('back_to_subcategory_', ''))
        subcategory_id = db.get_subcategory_by_firm_id(firm_id)
    else:
        subcategory_id = int(call.data.replace('goto_subcategory_', ''))
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.delete_message(chat_id, message_id)
    firms = db.get_firms_for_admin(subcategory_id)
    await bot.send_message(chat_id, 'Выберите фирму или добавьте новую: ',
                           reply_markup=generate_firms_admin_buttons(firms, subcategory_id))


@dp.callback_query_handler(lambda call: call.data.startswith('add_new_firm'))
async def reaction_to_add_new_firm(call: CallbackQuery, state: FSMContext):
    subcategory_id = int(call.data.replace('add_new_firm_', ''))
    subcategory = db.get_subcategory(subcategory_id)
    chat_id = call.message.chat.id
    await state.update_data(subcategory_id=subcategory_id)
    await AddNewFirm.category_ru.set()
    await bot.send_message(chat_id, f'Введите название новой фирмы для категории "{subcategory[1]}"  🇷🇺: ')


@dp.message_handler(state=AddNewFirm.category_ru)
async def process_add_new_firm_ru(message: Message, state: FSMContext):
    await state.update_data(category_ru=message.text)
    await AddNewFirm.category_uz.set()
    await message.answer(f'Введите название новой фирмы для категории 🇺🇿: ')


@dp.message_handler(state=AddNewFirm.category_uz)
async def process_add_new_firm_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    db.create_new_firm(data['category_ru'], message.text, data['subcategory_id'])
    await state.finish()
    await message.reply("Фирма успешно создана. Перейдите в /admin")


@dp.callback_query_handler(lambda call: call.data.startswith('delete_firm_'))
async def reaction_to_delete_subcategory_(call: CallbackQuery):
    category_id = int(call.data.replace('delete_firm_', ''))
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.delete_message(chat_id, message_id)
    db.delete_firm(category_id)
    await bot.send_message(chat_id, "Фирма успешно УДАЛЕНА. Перейдите в /admin")


@dp.callback_query_handler(lambda call: call.data.startswith('back_to_products_list_'))
@dp.callback_query_handler(lambda call: call.data.startswith('goto_firm_'))
async def show_firms_inside(call: CallbackQuery):
    if call.data.startswith('back_to_products_list_'):
        product_id = int(call.data.replace('back_to_products_list_', ''))
        firm_id = db.get_firm_id_by_product_id(product_id)
    else:
        firm_id = int(call.data.replace('goto_firm_', ''))
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.delete_message(chat_id, message_id)
    products = db.get_products_for_admin(firm_id)
    await bot.send_message(chat_id, 'Выберите товар или добавьте новый: ',
                           reply_markup=generate_products_admin_buttons(products, firm_id))


@dp.callback_query_handler(lambda call: call.data.startswith('goto_product_'))
async def show_product_inside(call: CallbackQuery = None, given_product_id=None, given_chat_id=None):
    if given_product_id:
        product_id = given_product_id
        chat_id = given_chat_id
    else:
        product_id = int(call.data.replace('goto_product_', ''))
        chat_id = call.message.chat.id
    product = db.get_product_detail_by_id(product_id)
    if str(product[-1]) == '1':
        status = 'Доступен ✅'
    else:
        status = 'Не доступен ❌'
    caption = f'Товар:\n\n🇷🇺: {product[1]}\n\n🇺🇿: {product[2]}\n\n🇷🇺: {product[3]}\n\n🇺🇿: {product[4]}\n\nЦена {convert_price(product[5])}\n\nСтатус: {status}'
    try:
        await bot.send_photo(chat_id,
                             photo=product[6],
                             caption=caption,
                             reply_markup=generate_product_detail_for_admin(product_id)
                             )
    except Exception as e:
        await bot.send_message(chat_id,
                               f'{e}\n\nТовар: {product[1]}\n\n{product[3]}\n\nЦена {convert_price(product[5])}\n\nНет фото для этого товара. Вы можете это исправить',
                               reply_markup=generate_product_detail_for_admin(product[0]))


@dp.callback_query_handler(lambda call: call.data.startswith('edit_photo_'))
async def edit_photo_product(call: CallbackQuery, state: FSMContext):
    product_id = int(call.data.replace('edit_photo_', ''))
    await state.update_data(product_id=product_id)
    await EditProductPhotoState.photo.set()
    await bot.send_message(chat_id=call.message.chat.id, text='Отправь новое фото')


@dp.message_handler(state=EditProductPhotoState.photo, content_types=['photo'])
async def save_new_photo(message: Message, state: FSMContext):
    chat_id = message.chat.id
    image = message.photo[0].file_id
    data = await state.get_data()
    product_id = data['product_id']
    await state.finish()
    db.update_photo_product(product_id, image)
    await bot.send_message(chat_id, f'Фото успешно заменено')
    await show_product_inside(given_product_id=product_id, given_chat_id=chat_id)


@dp.callback_query_handler(lambda call: call.data.startswith('edit_price_'))
async def edit_price_product(call: CallbackQuery, state: FSMContext):
    product_id = int(call.data.replace('edit_price_', ''))
    await state.update_data(product_id=product_id)
    await EditProductPriceState.price.set()
    await bot.send_message(chat_id=call.message.chat.id, text='Введите новую цену для товара')


@dp.message_handler(state=EditProductPriceState.price, regexp='\d+')
async def save_new_price(message: Message, state: FSMContext):
    chat_id = message.chat.id
    price = int(message.text)
    data = await state.get_data()
    product_id = data['product_id']
    await state.finish()
    db.update_price_product(product_id, price)
    await bot.send_message(chat_id, f'Цена успешно изменена на {price}')
    await show_product_inside(given_product_id=product_id, given_chat_id=chat_id)


# TODO проверить кнопки назад везде
# TODO Сделать подтверждение при регистрации админа


@dp.callback_query_handler(lambda call: call.data.startswith('delete_product_'))
async def delete_product_reaction(call: CallbackQuery):
    product_id = call.data.replace('delete_product_', '')
    db.delete_product(product_id)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.send_message(call.message.chat.id, 'Товар успешно удален.... Для продолжения нажмите кнопки внизу')


# ------------------------- Изменение названия -------------------------------------------- #

@dp.callback_query_handler(lambda call: call.data.startswith('edit_titleru_'))
async def edit_title_ru_product(call: CallbackQuery, state: FSMContext):
    product_id = int(call.data.replace('edit_titleru_', ''))
    await state.update_data(product_id=product_id)
    await EditProductTitleRuState.title_ru.set()
    await bot.send_message(chat_id=call.message.chat.id, text='Введите новое название товара 🇷🇺')


@dp.message_handler(state=EditProductTitleRuState.title_ru)
async def save_new_title_ru(message: Message, state: FSMContext):
    chat_id = message.chat.id
    title_ru = message.text
    data = await state.get_data()
    product_id = data['product_id']
    await state.finish()
    db.update_title_ru_product(product_id, title_ru)
    await bot.send_message(chat_id, f'Название успешно изменена на {title_ru}')
    await show_product_inside(given_product_id=product_id, given_chat_id=chat_id)

@dp.callback_query_handler(lambda call: call.data.startswith('edit_titleuz_'))
async def edit_title_uz_product(call: CallbackQuery, state: FSMContext):
    product_id = int(call.data.replace('edit_titleuz_', ''))
    await state.update_data(product_id=product_id)
    await EditProductTitleUzState.title_uz.set()
    await bot.send_message(chat_id=call.message.chat.id, text='Введите новое название товара 🇺🇿:')


@dp.message_handler(state=EditProductTitleUzState.title_uz)
async def save_new_title_uz(message: Message, state: FSMContext):
    chat_id = message.chat.id
    title_uz = message.text
    data = await state.get_data()
    product_id = data['product_id']
    await state.finish()
    db.update_title_uz_product(product_id, title_uz)
    await bot.send_message(chat_id, f'Название успешно изменена на {title_uz}')
    await show_product_inside(given_product_id=product_id, given_chat_id=chat_id)

# ------------------------- Изменение описания -------------------------------------------- #

@dp.callback_query_handler(lambda call: call.data.startswith('edit_descru_'))
async def edit_desc_ru_product(call: CallbackQuery, state: FSMContext):
    product_id = int(call.data.replace('edit_descru_', ''))
    await state.update_data(product_id=product_id)
    await EditProductDescRuState.desc_ru.set()
    await bot.send_message(chat_id=call.message.chat.id, text='Введите новое описание товара 🇷🇺')


@dp.message_handler(state=EditProductDescRuState.desc_ru)
async def save_new_desc_ru(message: Message, state: FSMContext):
    chat_id = message.chat.id
    desc_ru = message.text
    data = await state.get_data()
    product_id = data['product_id']
    await state.finish()
    db.update_desc_ru_product(product_id, desc_ru)
    await bot.send_message(chat_id, f'Описание успешно изменена на: {desc_ru}')
    await show_product_inside(given_product_id=product_id, given_chat_id=chat_id)

@dp.callback_query_handler(lambda call: call.data.startswith('edit_descuz_'))
async def edit_desc_uz_product(call: CallbackQuery, state: FSMContext):
    product_id = int(call.data.replace('edit_descuz_', ''))
    await state.update_data(product_id=product_id)
    await EditProductDescUzState.desc_uz.set()
    await bot.send_message(chat_id=call.message.chat.id, text='Введите новое описание товара 🇺🇿:')


@dp.message_handler(state=EditProductDescUzState.desc_uz)
async def save_new_desc_uz(message: Message, state: FSMContext):
    chat_id = message.chat.id
    desc_uz = message.text
    data = await state.get_data()
    product_id = data['product_id']
    await state.finish()
    db.update_desc_uz_product(product_id, desc_uz)
    await bot.send_message(chat_id, f'Описание успешно изменена на:  {desc_uz}')
    await show_product_inside(given_product_id=product_id, given_chat_id=chat_id)


@dp.callback_query_handler(lambda call: call.data.startswith('available_'))
async def change_status(call: CallbackQuery):
    product_id = call.data.replace('available_', '')
    db.change_available(product_id)
    await bot.send_message(call.message.chat.id, f'Статус успешно изменен')
    await show_product_inside(given_product_id=product_id, given_chat_id=call.message.chat.id)


