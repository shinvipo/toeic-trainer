import telebot
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, KeyboardButton

TOKEN = "5844845850:AAFtYpG4tboBH0mvJ7oMHipwK1KTYkrmqxc"

bot = telebot.TeleBot(TOKEN)

def markup_inline():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("Ez", callback_data="Ez"),
        InlineKeyboardButton("Normal", callback_data="Nm"),
        InlineKeyboardButton("Again", callback_data="Ag")
    )
    return markup

@bot.message_handler(commands=['search'])
def search_handler(message):
	msg = message.text
	vocab = msg.split(" ")[1:]
	bot.reply_to(message,vocab, reply_markup = markup_inline())

@bot.message_handler(commands=['help','start'])
def help_kb(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Vocabulary", callback_data="vocab"),
        InlineKeyboardButton("Excercise", callback_data="ex")
    )
    bot.send_message(message.chat.id, "Vocabulary or Excercise", reply_markup=markup)

@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    chatid = call.json['from']['id']
    if call.data == "Ez":
        bot.send_message(chatid,"Ez")
    elif call.data == "Ag":
        bot.send_message(chatid,"Ag")
    elif call.data == "Nm":
        bot.send_message(chatid,"Nm")
    elif call.data == "vocab":
        bot.send_message(chatid,"Vocabulary")
    elif call.data == "ex":
        bot.send_message(chatid,"Excercise")

bot.infinity_polling()