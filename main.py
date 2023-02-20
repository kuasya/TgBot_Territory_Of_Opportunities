# -*- coding: utf-8 -*-
from asyncio import wait

import telebot
from telebot import types

bot = telebot.TeleBot('5748799991:AAGMrwwUlIVgR7pj5u5lRUuU2dWej25SskQ')


@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Политика конфиденциальности", url='https://rosstat.gov.ru/politika-konfidencialnosti')
    markup.add(button1)
    button2 = types.InlineKeyboardButton("Правила нашего сервиса",
                                         url='https://rosstat.gov.ru/politika-konfidencialnosti')
    markup.add(button2)
    bot.send_message(message.from_user.id,
                     "Привет! Рады, что Вы с нами!\nДля начала, пожалуйста, ознакомьтесь с правилами нашего сервиса и подтвердите согласие на обработку персональных данных.", reply_markup=markup)
    start2(message)

@bot.message_handler(content_types=['text'])
def start2(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Подтверждаю ознакомление и даю согласие на обработку персональных данных")
    markup1.add(btn1)
    bot.send_message(message.from_user.id, ' ', reply_markup=markup1)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Подтверждаю ознакомление и даю согласие на обработку персональных данных":
        wait(5)
        markup1 = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'Договорились!', reply_markup=markup1)
    elif message.text.lower() == "Привет!":
        bot.send_message(message.from_user.id, "Привет, чем могу тебе помочь?")
        menu1(message)
    elif message.text.lower() == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю напиши /help.")


def menu1(message):
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    bot.send_message(message.from_user.id, text="Привет!", reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
