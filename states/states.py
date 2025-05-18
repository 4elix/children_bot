from aiogram.dispatcher.filters.state import State, StatesGroup

class Form(StatesGroup):
    phone = State()


class LocationForm(StatesGroup):
    cart_id = State()
    waiting_to_money_tipe = State()
    waiting_for_location = State()


class AddProductStates(StatesGroup):
    waiting_for_firm_id = State()
    waiting_for_name_ru = State()
    waiting_for_name_uz = State()
    waiting_for_description_ru = State()
    waiting_for_description_uz = State()
    waiting_for_image = State()
    waiting_for_price = State()
    waiting_to_commit = State()

class SendMessageStates(StatesGroup):
    text = State()
    photo = State()


class AddNewCategory(StatesGroup):
    category_ru = State()
    category_uz = State()


class AddNewSubCategory(StatesGroup):
    main = State()
    category_ru = State()
    category_uz = State()

class AddNewFirm(StatesGroup):
    main = State()
    category_ru = State()
    category_uz = State()


class EditPriceState(StatesGroup):
    price = State()


class EditProductPriceState(StatesGroup):
    product_id = State()
    price = State()


class EditProductPhotoState(StatesGroup):
    product_id = State()
    photo = State()


class EditProductTitleRuState(StatesGroup):
    product_id = State()
    title_ru = State()

class EditProductTitleUzState(StatesGroup):
    product_id = State()
    title_uz = State()


class EditProductDescRuState(StatesGroup):
    product_id = State()
    desc_ru = State()


class EditProductDescUzState(StatesGroup):
    product_id = State()
    desc_uz = State()