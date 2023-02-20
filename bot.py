# -*- coding: utf-8 -*-
from asyncio import wait

import time

import telebot
from telebot import types

bot = telebot.TeleBot('5748799991:AAGMrwwUlIVgR7pj5u5lRUuU2dWej25SskQ')

name = ''
message_email = ''
message_info = ''
message_phone = ''

# запускать бот с команды /start!!!!!!!! (надо прописать это в описании к боту)

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
    keyboard = types.InlineKeyboardMarkup()  # клавиатура
    key_yes = types.InlineKeyboardButton(text='Подтверждаю', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)
    question = 'Вы подтверждаете ознакомление и даете согласие на обработку персональных данных?'
    time.sleep(3)
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # сохранение данных
    if call.data == "yes":  # call.data == callback_data
        bot.send_message(call.message.chat.id, 'Спасибо! Для получения информации о боте напишите /help')
    elif call.data == "yes2":  # call.data == callback_data
        bot.send_message(call.message.chat.id, 'Ваша заявка сохранена :)')
    elif call.data == "no":

        bot.send_message(call.message.chat.id, 'Вы хотите заново внести данные? Тогда напишите, пожалуйста, /reg')


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Напишите, пожалуйста, свое ФИО.\nНапример, Иванов Иван Иванович")
        bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name
    elif message.text.lower() == "/help":
        bot.send_message(message.from_user.id, "Вы можете оставить заявку с информацией о себе.\nМы передадим Вашу "
                                               "заявку руководителям проектов. Если Ваша кандидатура будет "
                                               "соответствовать требованиям, руководитель свяжется с Вами.\n"
                                               "\nДля того, чтобы создать заявку, напишите /reg")
    else:
        bot.send_message(message.from_user.id, "Я не понимаю, напишите /help.")


def get_name(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Напишите, пожалуйста, свою элекронную почту')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global message_email
    message_email = message.text
    bot.send_message(message.from_user.id, 'Укажите номер телефона')
    bot.register_next_step_handler(message, get_group)


def get_group(message):
    global message_phone

    message_phone = message.text
    bot.send_message(message.from_user.id, 'Напишите, пожалуйста, вкратце о себе и своих навыках (2-3 предложения)')
    bot.register_next_step_handler(message, get_info)


def get_info(message):  # информация о себе
    global message_info
    message_info = message.text

    # bot.register_next_step_handler(message, get_info)

    keyboard = types.InlineKeyboardMarkup()  # клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes2')  # кнопка «Да»
    keyboard.add(key_yes)  # добавление кнопки в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)

    # проверка правильности заполнения заявки
    question = 'Ваша заявка\nФИО: ' + name + '\nEmail: '+message_email + '\nТелефон: '+message_phone+\
               '\nО себе: '+message_info+'\n \n Вы хотите сохранить заявку?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
