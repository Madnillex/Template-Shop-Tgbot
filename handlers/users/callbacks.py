from telebot.types import CallbackQuery
from loader import bot
from keyboards.default import *
from keyboards.inline import *
from states.states import CardStates
from shipping_data.shipping_detail import generate_product_invoice


@bot.callback_query_handler(func=lambda call: call.data == 'next')
def reaction_to_next(call: CallbackQuery):
    chat_id = call.message.chat.id
    keyboards = call.message.reply_markup.keyboard[-2]
    for item in keyboards:
        if 'page' in item.callback_data:
            category_name = item.callback_data.split('|')[1]
            page = int(item.text)
            page += 1
            bot.edit_message_reply_markup(chat_id, call.message.id,
                                          reply_markup=get_products_by_pagination(category_name, page))


@bot.callback_query_handler(func=lambda call: call.data == 'preview')
def reaction_to_next(call: CallbackQuery):
    chat_id = call.message.chat.id
    keyboards = call.message.reply_markup.keyboard[-2]
    for item in keyboards:
        if 'page' in item.callback_data:
            category_name = item.callback_data.split('|')[1]
            page = int(item.text)
            if page > 1:
                page -= 1
                bot.edit_message_reply_markup(chat_id, call.message.id,
                                              reply_markup=get_products_by_pagination(category_name, page))


@bot.callback_query_handler(func=lambda call: 'page' in call.data)
def reaction_to_page(call: CallbackQuery):
    keyboards = call.message.reply_markup.keyboard[-2]
    for item in keyboards:
        if 'page' in item.callback_data:
            page = item.text
            bot.answer_callback_query(call.id, f"You are in {page} page")


@bot.callback_query_handler(func=lambda call: call.data == 'back_categories')
def reaction_to_categories(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    categories = [item for item in db.get_all_categories()]
    bot.send_message(chat_id, 'Categories', reply_markup=get_categories_buttons(categories))


@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def reaction_to_main_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, 'Categories', reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: 'product' in call.data)
def reaction_to_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    keyboards = call.message.reply_markup.keyboard[-2]
    page = 1
    for item in keyboards:
        if 'page' in item.callback_data:
            page = int(item.text)
    product_id = int(call.data.split('|')[1])
    product = db.get_product_info(product_id)
    price = product[2]
    product_name = product[1]
    image = product[3]
    link = product[4]
    category_id = product[5]
    bot.send_photo(chat_id, image, caption=f'''
Product name: {product_name}
Price: {price}
<a href='{link}'>More</a>
''', parse_mode='html', reply_markup=product_items_btns(category_id, product_id, page))


@bot.callback_query_handler(func=lambda call: call.data == 'plus')
def reaction_to_plus(call: CallbackQuery):
    chat_id = call.message.chat.id
    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    quantity += 1
    category_id = call.message.reply_markup.keyboard[-1][0].callback_data.split('|')[1]
    page = call.message.reply_markup.keyboard[0][1].callback_data.split('|')[1]
    product_id = call.message.reply_markup.keyboard[1][0].callback_data.split('|')[1]
    bot.edit_message_reply_markup(chat_id, call.message.id,
                                  reply_markup=product_items_btns(category_id, product_id, page, quantity))


@bot.callback_query_handler(func=lambda call: call.data == 'minus')
def reaction_to_minus(call: CallbackQuery):
    chat_id = call.message.chat.id
    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    if quantity > 1:
        quantity -= 1
    category_id = call.message.reply_markup.keyboard[-1][0].callback_data.split('|')[1]
    page = call.message.reply_markup.keyboard[0][1].callback_data.split('|')[1]
    product_id = call.message.reply_markup.keyboard[1][0].callback_data.split('|')[1]
    bot.edit_message_reply_markup(chat_id, call.message.id,
                                  reply_markup=product_items_btns(category_id, product_id, page, quantity))


@bot.callback_query_handler(func=lambda call: 'quantity' in call.data)
def reaction_to_quantity(call: CallbackQuery):
    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    bot.answer_callback_query(call.id, f"Quantity of product is {quantity}")


@bot.callback_query_handler(func=lambda call: 'add_card' in call.data)
def reaction_to_add_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    bot.set_state(user_id, CardStates.card, chat_id)
    product_id = int(call.data.split('|')[1])
    product = db.get_product_info(product_id)
    product_name = product[1]
    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    price = product[2]
    with bot.retrieve_data(user_id, chat_id) as data:
        if data.get('card'):
            data['card'][product_name] = {
                'product_id': product_id,
                'price': price,
                'quantity': quantity
            }
        else:
            data['card'] = {
                product_name: {
                    'product_id': product_id,
                    'price': price,
                    'quantity': quantity
                }
            }


@bot.callback_query_handler(func=lambda call: call.data == 'show_card')
def reaction_to_show_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        res = get_text_reply_markup(data)
    text = res['text']
    markup = res['markup']
    bot.send_message(chat_id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: 'remove' in call.data)
def reaction_to_remove(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    product_id = int(call.data.split('|')[1])
    with bot.retrieve_data(user_id, chat_id) as data:
        keys = [product_name for product_name in data['card'].keys()]
        for item in keys:
            if data['card'][item]['product_id'] == product_id:
                del data['card'][item]
    res = get_text_reply_markup(data)
    text = res['text']
    markup = res['markup']
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, text, reply_markup=markup)


def get_text_reply_markup(data: dict):
    text = "Card:\n"
    total_price = 0
    for product_name, item in data['card'].items():
        product_price = item['price']
        quantity = item['quantity']
        price = quantity * int(product_price)
        total_price += price
        text += f"""{product_name}
Price: {quantity} ✖️{product_price} = {price}"""
    if total_price == 0:
        text = "Your card is empty"
        markup = main_menu()
    else:
        text += f"\nTotal quantity: {total_price} UZS"
        markup = get_card_items(data['card'])
    return {'markup': markup, 'text': text, 'total_price': total_price}


@bot.callback_query_handler(func=lambda call: call.data == 'clear_card')
def reaction_clear_card_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    bot.delete_state(user_id, chat_id)
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, "Your card is empty", reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: 'back_cat_id' in call.data)
def reaction_to_back_cat_id(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    page = int(call.message.reply_markup.keyboard[0][1].callback_data.split('|')[1])
    category_id = int(call.message.reply_markup.keyboard[-1][0].callback_data.split('|')[1])
    category_name = db.get_category_name_by_category_id(category_id)
    markup = get_products_by_pagination(category_name, page)
    bot.send_message(chat_id, category_name, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'submit')
def submit_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        bot.send_invoice(chat_id, **generate_product_invoice(data['card']).generate_invoice(),
                         invoice_payload='shop_bot')

