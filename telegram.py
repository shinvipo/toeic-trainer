import telebot
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, KeyboardButton
import random
from vocab import *
from threading import Thread

TOKEN = "5844845850:AAFtYpG4tboBH0mvJ7oMHipwK1KTYkrmqxc"

bot = telebot.TeleBot(TOKEN)

myid =  1062599312


def markup_inline():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("Ez", callback_data="Ez"),
        InlineKeyboardButton("Normal", callback_data="Nm"),
        InlineKeyboardButton("Again", callback_data="Ag")
    )
    return markup

def Example_inline():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Example", callback_data="Example")
    )
    return markup

def random_words():
    return random.choice(toeic)

def reminder():
    while True:
        words = random_words()
        bot.send_message(myid, (fetch_cambridge(words)))
        countdown(60*15)

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
        words = random_words()
        bot.send_message(chatid,fetch_cambridge(words),reply_markup=Example_inline())
    elif call.data == "ex":
        bot.send_message(chatid,"Excercise")
    if call.data == "Example":
        word = call.json['message']['text'].split("\n")[0]
        bot.send_message(chatid,show_full_from_cache(word))
        
t1 = Thread(target=reminder)
t1.start()
t1.join()
t2 = Thread(target=bot.infinity_polling)
t2.start()
t2.join()
