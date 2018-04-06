#!/usr/bin/python3
from app.handler import BotHandler
import telebot

handler = BotHandler()
bot = telebot.TeleBot(handler.token)


@bot.message_handler(commands=['start'])
def start_command_handler(command):
    bot.send_message(command.chat.id, handler.help_message)


@bot.message_handler(content_types=['text'])
def message_handler(message):
    chat_id = message.chat.id
    response = handler.text_handler(message.text)
    bot.send_message(chat_id, response)

bot.polling(none_stop=True)
