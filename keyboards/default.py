from telebot.types import KeyboardButton, ReplyKeyboardMarkup

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    order = KeyboardButton('Catalog 📇')
    card = KeyboardButton('Card 🛒')
    feedback = KeyboardButton('Feedback 📲')
    settings = KeyboardButton('Settings ⚙️')
    markup.add(order, card, feedback, settings)
    return markup


def register_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton('Register ✍️')
    markup.add(btn)
    return markup

def share_contact():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton('Share my contact', request_contact=True)
    markup.add(btn)
    return markup

def submit_user_data_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    yes = KeyboardButton('All right!')
    no = KeyboardButton('I will change')
    markup.add(yes, no)
    return markup


def get_categories_buttons(category_list):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for item in category_list:
        btn = KeyboardButton(item[0])
        markup.add(btn)
    return markup


