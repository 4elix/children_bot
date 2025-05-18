from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentTypes
from data.loader import bot, dp, db
from .text_handlers import show_main_menu
from keyboards.reply import generate_languages, generate_phone_number
from states.states import Form
from languages.langs import langs



@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    print(message.chat.id)
    print(message.from_user.full_name)
    user = db.get_user_by_id(message.chat.id)
    if user:
        await show_main_menu(message)
    else:
        await message.answer('Добро пожаловать, выберете пожалуйста язык\n\nXush kelibsiz, tilni tanlang',
                             reply_markup=generate_languages())


@dp.message_handler(regexp=r"(Русский 🇷🇺|O'zbekcha 🇺🇿)")
async def get_lang_and_register(message: Message):
    lang = message.text
    chat_id = message.chat.id
    user = db.get_user_by_id(chat_id)
    l = 'ru' if lang == 'Русский 🇷🇺' else 'uz'
    if user:
        db.change_user_lang(telegram_id=chat_id, lang=l)
    else:
        full_name = message.from_user.full_name
        db.insert_user(chat_id, full_name, l)
        db.create_cart_for_user(chat_id)
    await Form.phone.set()
    await message.answer(langs[l]["share_contact_message"], reply_markup=generate_phone_number(l))


@dp.message_handler(content_types=ContentTypes.CONTACT, state=Form.phone)
async def process_phone(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone=phone_number)
    chat_id = message.chat.id
    # Выводим информацию о номере телефона
    lang = db.get_user_lang(chat_id)
    if lang == 'ru':
        await message.reply(f"Спасибо за номер телефона: {phone_number}.")
    else:
        await message.reply(f"Telefon raqami uchun rahmat: {phone_number}.")
    db.update_user_phone(chat_id, phone_number)
    # Завершаем состояние
    await state.finish()
    await show_main_menu(message)

