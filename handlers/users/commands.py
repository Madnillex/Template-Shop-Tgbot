from telebot.types import Message
from loader import bot, db
from keyboards.default import main_menu


@bot.message_handler(commands=['start'])
def reaction_to_start(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    db.insert_telegram_id_user(user_id)
    bot.send_message(chat_id, f'Hi, {message.from_user.first_name}!', reply_markup=main_menu())





