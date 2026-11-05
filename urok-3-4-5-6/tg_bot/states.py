from telebot.states import State, StatesGroup


class CategoryStates(StatesGroup):
    start = State()

    name = State()


class CategoryUpdateStates(StatesGroup):
    title = State()


class ProductStates(StatesGroup):
    start = State()

    title = State()
    quantity = State()
    price = State()
    category_id = State()



class ProductUpdateStates(StatesGroup):
    title = State()
    quantity = State()
    price = State()
    category_id = State()