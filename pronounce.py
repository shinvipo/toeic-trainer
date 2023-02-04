import os
import random
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Define a list of TOEIC vocabulary words and their definitions
TOEIC_VOCAB = [
    {"term": "accelerate", "definition": "to increase speed"},
    {"term": "competitor", "definition": "a person or company that tries to win a competition or get the same thing as someone else"},
    {"term": "enthusiastic", "definition": "having or showing a lot of excitement and interest"},
    {"term": "innovative", "definition": "introducing new ideas or methods"},
    {"term": "persistent", "definition": "continuing to do something in a determined way, despite difficulties"},
    # Add more vocabulary words as needed
]

# Function to handle the /quiz command
def start_quiz(update, context):
    # Choose a random vocabulary word from the list
    word = random.choice(TOEIC_VOCAB)
    context.user_data['current_word'] = word
    update.message.reply_text(f"What is the definition of {word['term']}?")

# Function to handle user input
def answer_quiz(update, context):
    user_answer = update.message.text
    word = context.user_data['current_word']
    if user_answer.lower() == word['definition'].lower():
        update.message.reply_text("Correct! Well done.")
    else:
        update.message.reply_text(f"Incorrect. The correct answer is {word['definition']}.")

# Create the Updater and pass it the bot's token
updater = Updater(token=os.getenv('TELEGRAM_BOT_TOKEN'), use_context=True)
dispatcher = updater.dispatcher

# Add handler for the /quiz command
quiz_handler = CommandHandler('quiz', start_quiz)
dispatcher.add_handler(quiz_handler)

# Add handler for user input
answer_handler = MessageHandler(Filters.text, answer_quiz)
dispatcher.add_handler(answer_handler)

# Start the bot
updater.start_polling()