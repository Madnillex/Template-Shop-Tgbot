from telebot.types import Message, ReplyKeyboardRemove
from loader import bot
from keyboards.default import *
from keyboards.inline import *
from states.states import RegisterStates


@bot.message_handler(regexp='Catalog 📇')
def reaction_to_catalog(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    check = db.check_user_info(user_id)
    if None in check:
        text = "You are not registered please register"
        markup = register_button()
    else:
        text = "Let's choose category"
        markup = get_categories_buttons(db.get_all_categories())
    bot.send_message(chat_id, text, reply_markup=markup)

# Registration PART
@bot.message_handler(regexp='Register ✍️')
def reaction_to_register(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.set_state(user_id, RegisterStates.full_name, chat_id)
    bot.send_message(chat_id, "Write your full name please", reply_markup=ReplyKeyboardRemove())

@bot.message_handler(content_types=['text'], state=RegisterStates.full_name)
def reaction_to_full_name(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        data['full_name'] = message.text.title()
    bot.set_state(user_id, RegisterStates.contact, chat_id)
    bot.send_message(chat_id, "Share your contact please", reply_markup=share_contact())

@bot.message_handler(content_types=['contact'], state=RegisterStates.contact)
def reaction_to_contact(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        data['contact'] = message.contact.phone_number
    bot.set_state(user_id, RegisterStates.birthdate, chat_id)
    bot.send_message(chat_id, 'Write your birthday please as: yyyy.mm.dd',
                     reply_markup=ReplyKeyboardRemove())

@bot.message_handler(content_types=['text'], state=RegisterStates.birthdate)
def reaction_to_birthdate(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        data['birthdate'] = message.text
    full_name = data['full_name']
    contact = data['contact']
    bot.set_state(user_id, RegisterStates.submit, chat_id)
    bot.send_message(chat_id, f'''PLEASE CHECK YOUR DATA:
Full name: {full_name}
Contact: {contact}
Birthday: {message.text}''', reply_markup=submit_user_data_btn())


@bot.message_handler(content_types=['text'], state=RegisterStates.submit)
def reaction_to_submit_user_info(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        birthdate = data['birthdate']
    full_name = data['full_name']
    contact = data['contact']
    if message.text == 'All right!':
        db.update_user_info(full_name, contact, birthdate, user_id)
        bot.delete_state(user_id, chat_id)
        bot.send_message(chat_id, 'You are registered 😊',
                         reply_markup=get_categories_buttons(db.get_all_categories()))
    else:
        bot.delete_state(user_id, chat_id)
        bot.set_state(user_id, RegisterStates.full_name, chat_id)
        bot.send_message(chat_id, 'Ok, please write your full name:',
                         reply_markup=ReplyKeyboardRemove())


# Category handler
@bot.message_handler(func=lambda message: message.text in [item[0] for item in db.get_all_categories()])
def reaction_to_category(message: Message):
    chat_id = message.chat.id
    category_name = message.text
    bot.send_message(chat_id, category_name,
                     reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id, category_name, reply_markup=get_products_by_pagination(category_name))


