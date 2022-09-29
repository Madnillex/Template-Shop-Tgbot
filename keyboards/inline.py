from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db


def get_products_by_pagination(category_name, page=1):
    markup = InlineKeyboardMarkup(row_width=1)
    limit = 5
    count_products = db.count_of_product(category_name)
    max_page =  count_products // limit if count_products % limit == 0 else count_products // limit + 1
    offset = 0 if page == 1 else (page - 1) * limit

    products = db.get_product_by_pagination(category_name, offset, limit)
    for item in products:
        markup.add(InlineKeyboardButton(item[1], callback_data=f"product|{item[0]}"))


    preview_btn = InlineKeyboardButton('⏮', callback_data='preview')
    page_btn = InlineKeyboardButton(page, callback_data=f'page|{category_name}')
    next_page = InlineKeyboardButton('⏭', callback_data='next')
    if page == 1:

        markup.row(page_btn, next_page)
    elif 1 < page < max_page:
        markup.row(preview_btn, page_btn, next_page)
    elif page == max_page:
        markup.row(preview_btn, page_btn)

    back = InlineKeyboardButton('Back 🔙', callback_data='back_categories')
    main_menu = InlineKeyboardButton('Main menu', callback_data='main_menu')
    markup.row(back, main_menu)
    return markup

def product_items_btns(category_id, product_id, page, quantity=1):
    items = [
        InlineKeyboardButton('➖', callback_data='minus'),
        InlineKeyboardButton(quantity, callback_data=f'quantity|{page}'),
        InlineKeyboardButton('➕', callback_data='plus')
    ]
    add_card = InlineKeyboardButton('Add to card', callback_data=f'add_card|{product_id}')
    card = InlineKeyboardButton('My card 🛒', callback_data='show_card')
    back = InlineKeyboardButton('Back 🔙', callback_data=f'back_cat_id|{category_id}')
    main_menu = InlineKeyboardButton('Main menu', callback_data='main_menu')
    return InlineKeyboardMarkup(keyboard=[
        items,
        [add_card, card],
        [back, main_menu]
    ])


def get_card_items(data:dict):
    markup = InlineKeyboardMarkup(row_width=1)
    for product_name, items in data.items():
        product_id = items['product_id']
        btn = InlineKeyboardButton(f"❌ {product_name}",
                                   callback_data=f"remove|{product_id}")
        markup.add(btn)
    back = InlineKeyboardButton('Categories', callback_data='back_categories')
    clear = InlineKeyboardButton('🔄 Clear card', callback_data='clear_card')
    order = InlineKeyboardButton('Submit ✅', callback_data='submit')
    markup.row(clear, order)
    markup.row(back)
    return markup


