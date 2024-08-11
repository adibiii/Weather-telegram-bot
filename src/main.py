import json
import logging

import requests

from config import *
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import(
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,
    Application)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

with open('cities.json', 'r') as f:
    cities = json.loads(f.read())

PROVIENCE, CITY = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text ="""سلام به ربات هوا شناسی خوش امدید 
لطفا استان مورد نظر خود را انتخاب کنید:"""

    keyboard = []
    for i in cities.keys():
        keyboard.append([InlineKeyboardButton(i, callback_data=i)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text, reply_markup=reply_markup)
    return PROVIENCE


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f" your Province: {query.data}")
    keyboard = []
    for i in cities[query.data]:
        keyboard.append([InlineKeyboardButton(i, callback_data=i)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    text  = f"""لطفا یکی از شهر های استان {query.data} را انتخاب کنید:"""
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text =text, reply_markup=reply_markup,)
    return CITY


async def button2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"your city: {query.data}")
    location = f"{query.data}, iran/{date}?"
    url = BASE_PATH+location+API_KEY+API_OPTION
    response = requests.get(url)
    if response.status_code == 200:
        res = json.loads(response.text)
        current_weather = dict()
        current_weather['address'] = res['address']
        current_weather['date'] = res['days'][0]['datetime']
        current_weather['temp'] = int((res['days'][0]['temp'] - 32) * (5 / 9))
        current_weather['description'] = res['days'][0]['description']
        current_weather['icon'] = res['days'][0]['icon']
    text = f""" today: {res['days'][0]['datetime']}
weather in ({res['address']}) is:
temp: {int((res['days'][0]['temp'] - 32) * (5 / 9))}
description: {res['days'][0]['description']}
icon: {res['days'][0]['icon']}"""

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('thank you!!')
    return ConversationHandler.END


def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PROVIENCE: [CallbackQueryHandler(button)],
            CITY: [CallbackQueryHandler(button2)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
