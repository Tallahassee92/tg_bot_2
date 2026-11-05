from tg_bot.loader import bot
from telebot import types
from tg_bot.keyboards import reply, inline
from tg_bot.states import CategoryStates, CategoryUpdateStates, ProductStates, ProductUpdateStates
from telebot.states.sync import StateContext
from database.managers.base import BaseManager

db_manager = BaseManager()


@bot.message_handler(commands=['start'], is_admin=True)
def user_start(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'hello, admin', reply_markup=reply.admin_kb())


@bot.message_handler(is_admin=True, func=lambda msg: msg.text == 'категории')
def handle_categories(message: types.Message, state: StateContext):
    state.set(CategoryStates.start)
    bot.send_message(message.chat.id, 'Выберите действие ниже', reply_markup=reply.admin_actions_kb())


# Добавить
@bot.message_handler(
    is_admin=True,
    func=lambda msg: msg.text == 'добавить',
    state=CategoryStates.start
)
def get_category_name(message: types.Message, state: StateContext):
    state.set(CategoryStates.name)
    bot.send_message(message.chat.id, 'напишите название категории', reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(is_admin=True, state=CategoryStates.name)
def insert_category(message: types.Message, state: StateContext):
    db_manager.manage('insert into categories(title) values (%s);', message.text, commit=True)
    bot.send_message(message.chat.id, f'Категория "{message.text}" добавлена')
    state.delete()


@bot.message_handler(
    is_admin=True,
    func=lambda message: message.text == 'получить',
    state=CategoryStates.start
)
def show_categories(message: types.Message, state: StateContext):
    chat_id = message.chat.id

    categories = db_manager.manage('select * from categories;', fetchall=True)
    for category in categories:
        bot.send_message(
            chat_id,
            f'ID: {category["id"]}\nName: {category["title"]}',
            reply_markup=inline.category_actions_kb(category.get('id'))
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('category_update'))
def start_category_update(call: types.CallbackQuery, state: StateContext):
    print(call.data)
    category_id = int(call.data.split(':')[-1])
    state.add_data(category_id=category_id)
    state.set(CategoryUpdateStates.title)
    bot.send_message(call.message.chat.id, 'Напишите новое название категории')


@bot.message_handler(is_admin=True, state=CategoryUpdateStates.title)
def update_category(message: types.Message, state: StateContext):
    chat_id = message.chat.id

    with bot.retrieve_data(chat_id) as data:
        category_id = data.get('category_id')

    db_manager.manage('update categories set title = %s where id = %s', message.text, category_id, commit=True)
    bot.send_message(chat_id, "Название категории обновлено", reply_markup=reply.admin_kb())
    state.delete()


@bot.callback_query_handler(func=lambda call: call.data.startswith('category_delete'))
def delete_category(call: types.CallbackQuery):
    category_id = int(call.data.split(':')[-1])
    db_manager.manage('delete from categories where id = %s;', category_id, commit=True)
    bot.send_message(call.message.chat.id, "Категория удалена", reply_markup=reply.admin_kb())


@bot.message_handler(is_admin=True, func=lambda msg: msg.text == 'продукты')
def handle_products(message: types.Message, state: StateContext):
    state.set(ProductStates.start)
    bot.send_message(message.chat.id, 'Выберите действие ниже', reply_markup=reply.admin_actions_kb())

@bot.message_handler(is_admin=True, func=lambda msg: msg.text == 'добавить', state=ProductStates.start)
def product_creation(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    state.set(ProductStates.title)
    bot.send_message(chat_id, "Напишите название продукта")


@bot.message_handler(is_admin=True, state=ProductStates.title)
def get_title_set_quantity(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    state.set(ProductStates.quantity)
    state.add_data(title=message.text)
    bot.send_message(chat_id, "Количество: ")

@bot.message_handler(is_admin=True, state=ProductStates.quantity)
def get_quantity_set_price(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    state.set(ProductStates.price)
    state.add_data(quantity=message.text)
    bot.send_message(chat_id, "Цена: ")


@bot.message_handler(is_admin=True, state=ProductStates.price)
def get_quantity_set_price(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    state.set(ProductStates.category_id)
    state.add_data(price=message.text)
    categories = db_manager.manage('select * from categories;', fetchall=True)

    bot.send_message(chat_id, "Категория: ", reply_markup=reply.categories_kb(categories))

@bot.message_handler(is_admin=True, state=ProductStates.category_id)
def add_product(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    category_id = db_manager.manage('select id from categories where title = %s', message.text, fetchone=True)  # RealDictCursor
    with bot.retrieve_data(chat_id) as data:
        p_title = data.get('title')
        p_quantity = data.get('quantity')
        p_price = data.get('price')

        db_manager.manage('''
        insert into products(title, quantity, price, category_id)
        values (%s,%s,%s,%s);
        ''', p_title, p_quantity, p_price, category_id.get('id'), commit=True)
        bot.send_message(chat_id, f'''
TITLE: <i>{p_title}</i>
QUANTITY: <b>{p_quantity}</b>
PRICE: <b>{p_price}</b>
CATEGORY: <i>{message.text}</i>
''', reply_markup=reply.admin_kb())
        state.delete()


@bot.message_handler(is_admin=True, func=lambda message: message.text == 'получить',
                     state=ProductStates.start)
def get_products(message: types.Message, state: StateContext):
    chat_id = message.chat.id

    products = db_manager.manage('''
    select p.id, p.title, p.quantity, p.price, c.title as category_title
    from products p
    join categories c on p.category_id = c.id;
    ''', fetchall=True)

    for product in products:
        p_id, p_title, p_quantity, p_price, category = product.values()

        bot.send_message(chat_id, f'''
ID: <b>{p_id}</b>
TITLE: <i>{p_title}</i>
QUANTITY: <b>{p_quantity}</b>
PRICE: <b>{p_price}</b>
CATEGORY: <i>{category}</i>
''', reply_markup=inline.product_actions_kb(p_id))


@bot.callback_query_handler(func=lambda call: call.data.startswith('product_delete'))
def delete_product(call: types.CallbackQuery, state: StateContext):
    product_id = int(call.data.split(':')[-1])
    chat_id = call.message.chat.id

    db_manager.manage('delete from products where id = %s;', product_id, commit=True)
    bot.send_message(chat_id, 'Продукт удален', reply_markup=reply.admin_kb())


@bot.callback_query_handler(func=lambda call: call.data.startswith('product_update'))
def update_product(call: types.CallbackQuery, state: StateContext):
    product_id = int(call.data.split(':')[-1]) # ['product_delete', 1]
    chat_id = call.message.chat.id

    message_id = call.message.message_id

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text='Выберите поле для обновления',
        reply_markup=inline.product_update_kb(product_id)
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('update_product_name'))
def get_new_name(call: types.CallbackQuery, state: StateContext):
    product_id = int(call.data.split(':')[-1]) # ['product_delete', 1]
    chat_id = call.message.chat.id

    state.add_data(product_id=product_id)
    state.set(ProductUpdateStates.title)

    bot.send_message(chat_id, 'Напишите новое название продукта')


@bot.message_handler(is_admin=True, state=ProductUpdateStates.title)
def update_name(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    with bot.retrieve_data(chat_id) as data:
        product_id = data.get('product_id')

    product = db_manager.manage('''
    update products set title = %s
    where id = %s returning id, title, quantity, price, category_id;
    ''', message.text, product_id, commit=True, fetchone=True)

    p_id, p_title, p_quantity, p_price, category = product.values()

    category = db_manager.manage('select title from categories where id = %s;', category, fetchone=True).get('title')

    bot.send_message(chat_id, f'''
ID: <b>{p_id}</b>
TITLE: <i>{p_title}</i>
QUANTITY: <b>{p_quantity}</b>
PRICE: <b>{p_price}</b>
CATEGORY: <i>{category}</i>
''', reply_markup=reply.admin_kb())
    state.delete()


@bot.callback_query_handler(func=lambda call: call.data.startswith('update_product_category'))
def get_new_category(call: types.CallbackQuery, state: StateContext):
    product_id = int(call.data.split(':')[-1])
    chat_id = call.message.chat.id

    state.add_data(product_id=product_id)
    state.set(ProductUpdateStates.category_id)

    categories = db_manager.manage('select title from categories;', fetchall=True)

    bot.send_message(chat_id, 'выберите категорию', reply_markup=reply.categories_kb(categories))


@bot.message_handler(is_admin=True, state=ProductUpdateStates.category_id)
def update_category(message: types.Message, state: StateContext):
    chat_id = message.chat.id

    with bot.retrieve_data(chat_id) as data:
        product_id = data.get('product_id')

    category_id = db_manager.manage('select id from categories where title = %s;', message.text, fetchone=True).get('id')
    product = db_manager.manage('''
    update products set category_id = %s
    where id = %s returning id, title, quantity, price; 
    ''', category_id, product_id, commit=True, fetchone=True)
    p_id, p_title, p_quantity, p_price = product.values()

    bot.send_message(chat_id, f'''
ID: <b>{p_id}</b>
TITLE: <i>{p_title}</i>
QUANTITY: <b>{p_quantity}</b>
PRICE: <b>{p_price}</b>
CATEGORY: <i>{message.text}</i>
''', reply_markup=reply.admin_kb())
    state.delete()

@bot.callback_query_handler(func=lambda call: call.data.startswith('update_product_quantity'))
def get_new_quantity(call: types.CallbackQuery, state: StateContext):
    product_id = int(call.data.split(':')[-1])
    chat_id = call.message.chat.id

    state.add_data(product_id=product_id)
    state.set(ProductUpdateStates.quantity)

    bot.send_message(chat_id, 'Напишите новое количество продукта')


@bot.message_handler(is_admin=True, state=ProductUpdateStates.quantity)
def update_quantity(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    with bot.retrieve_data(chat_id) as data:
        product_id = data.get('product_id')

    product = db_manager.manage('''
    update products set quantity = %s
    where id = %s returning id, title, quantity, price, category_id;
    ''', message.text, product_id, commit=True, fetchone=True)

    p_id, p_title, p_quantity, p_price, category_id = product.values()
    category = db_manager.manage('select title from categories where id = %s;', category_id, fetchone=True).get('title')

    bot.send_message(chat_id, f'''
ID: <b>{p_id}</b>
TITLE: <i>{p_title}</i>
QUANTITY: <b>{p_quantity}</b>
PRICE: <b>{p_price}</b>
CATEGORY: <i>{category}</i>
''', reply_markup=reply.admin_kb())
    state.delete()


@bot.callback_query_handler(func=lambda call: call.data.startswith('update_product_price'))
def get_new_price(call: types.CallbackQuery, state: StateContext):
    product_id = int(call.data.split(':')[-1])
    chat_id = call.message.chat.id

    state.add_data(product_id=product_id)
    state.set(ProductUpdateStates.price)

    bot.send_message(chat_id, 'Напишите новую стоимость продукта')



@bot.message_handler(is_admin=True, state=ProductUpdateStates.price)
def update_price(message: types.Message, state: StateContext):
    chat_id = message.chat.id
    with bot.retrieve_data(chat_id) as data:
        product_id = data.get('product_id')

    product = db_manager.manage('''
    update products set price = %s
    where id = %s returning id, title, quantity, price, category_id;
    ''', message.text, product_id, commit=True, fetchone=True)

    p_id, p_title, p_quantity, p_price, category_id = product.values()
    category = db_manager.manage('select title from categories where id = %s;', category_id, fetchone=True).get('title')

    bot.send_message(chat_id, f'''
ID: <b>{p_id}</b>
TITLE: <i>{p_title}</i>
QUANTITY: <b>{p_quantity}</b>
PRICE: <b>{p_price}</b>
CATEGORY: <i>{category}</i>
''', reply_markup=reply.admin_kb())
    state.delete()








@bot.message_handler(is_admin=True, func=lambda msg: msg.text == 'пользователи')
def handle_users(message: types.Message):
    bot.send_message(message.chat.id, 'Выберите действие ниже', reply_markup=reply.admin_actions_kb(True))


