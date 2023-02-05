import telebot
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, KeyboardButton
import random
from vocab import *
from threading import Thread
from gtts import gTTS

TOKEN = "5844845850:AAFtYpG4tboBH0mvJ7oMHipwK1KTYkrmqxc"

bot = telebot.TeleBot(TOKEN)

myid =  1062599312

again = normal = ez = []
with open("./Data/vocab.json",'r') as f:
    toeic = json.load(f)["TOEIC"]

with open("./Data/question.json") as f:
    excecise = json.load(f)["questions"]

def markup_inline():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(
        InlineKeyboardButton("Ez", callback_data="Ez"),
        InlineKeyboardButton("Normal", callback_data="Nm"),
        InlineKeyboardButton("Again", callback_data="Ag"),
        InlineKeyboardButton("Example", callback_data="Example")
    )
    return markup

def random_words():
    return random.choice(toeic)    

def random_question():
    order = random.randint(0,3625)
    return order,excecise[order]

def reminder():
    while True:
        try:
            words = random_words()
            bot.send_message(myid, (fetch_cambridge(words)), reply_markup=markup_inline())
            tts = gTTS(words, lang='en')
            tts.save('output.mp3')
            audio = open('output.mp3', 'rb')
            bot.send_audio(chat_id=myid, audio=audio, title= words)
            countdown(60*15)
        except:
            pass

@bot.message_handler(commands=['search'])
def search_handler(message):
	msg = message.text
	words = msg.replace("/search ","").strip()
	bot.reply_to(message,fetch_cambridge(words), reply_markup = markup_inline())
	tts = gTTS(words, lang='en')
	tts.save('output.mp3')
	audio = open('output.mp3', 'rb')
	bot.send_audio(chat_id=message.chat.id, audio=audio, title= words)
	

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
    word = call.json['message']['text'].split("\n")[0].strip()
    try:
        order = int(call.json['message']['text'].split("/")[0].strip().lower())
        ex = excecise[order]
        ans = ex['answer']
        da = ""
        tmp = {"1":"A","2":"B","3":"C","4":"D"}
        for k,v in ex.items():
            if k == "answer":
                continue
            if v == ans:
                ans = da + ": " + ans
                da = tmp[k]
    except: pass
    if call.data == "Ez":
        ez.append(word)
        toeic.remove(word)
    elif call.data == "Ag":
        again.append(word)
        toeic.remove(word)
    elif call.data == "Nm":
        normal.append(word)
        toeic.remove(word)
    elif call.data == "vocab":
        words = random_words()
        bot.send_message(chatid,fetch_cambridge(words),reply_markup=markup_inline())
        tts = gTTS(words, lang='en')
        tts.save('output.mp3')
        audio = open('output.mp3', 'rb')
        bot.send_audio(chat_id=chatid, audio=audio, title= words)
    elif call.data == "ex":
        order, qs = random_question()
        question = str(order) + "/ " + qs["question"]
        ans = qs["answer"]
        markup = InlineKeyboardMarkup()
        markup.row_width = 5
        markup.row(InlineKeyboardButton("A: " + qs['1'],callback_data= "A"))
        markup.row(InlineKeyboardButton("B: " + qs['2'],callback_data= "B"))
        markup.row(InlineKeyboardButton("C: " + qs['3'],callback_data= "C"))
        markup.row(InlineKeyboardButton("D: " + qs['4'],callback_data= "D"))
        markup.row(InlineKeyboardButton("Answer",callback_data= "answer"))
        bot.send_message(chatid,question,reply_markup=markup)
    elif call.data == "answer":
        bot.reply_to(call.message, ans)
        
    elif call.data == "A":
        if da == "A":
            bot.send_message(chatid,"Exactly!!\nA: " + ans)
        else:
            bot.send_message(chatid,f"Wrong!!\nAnswer is '{ans}'")
    elif call.data == "B":
        if da == "B":
            bot.send_message(chatid,"Exactly!!\nB: " + ans)
        else:
            bot.send_message(chatid,f"Wrong!!\nAnswer is '{ans}'")
    elif call.data == "C":
        if da == "C":
            bot.send_message(chatid,"Exactly!!\nC: " + ans)
        else:
            bot.send_message(chatid,f"Wrong!!\nAnswer is '{ans}'")
    elif call.data == "D":
        if da == "D":
            bot.send_message(chatid,"Exactly!!\nD: " + ans)
        else:
            bot.send_message(chatid,f"Wrong!!\nAnswer is '{ans}'")
        
    if call.data == "Example":
        word = call.json['message']['text'].split("\n")[0].strip().lower()
        bot.send_message(chatid,show_full_from_cache(word))
        
t2 = Thread(target=bot.infinity_polling)
t2.start()
t1 = Thread(target=reminder)
t1.start()