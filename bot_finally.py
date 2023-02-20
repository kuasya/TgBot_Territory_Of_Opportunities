# -*- coding: utf-8 -*-
from asyncio import wait

import time

import telebot
from telebot import types

# Внимание!!! Введите ключ доступа!
bot = telebot.TeleBot('') # чтобы подключить бота, укажите токен

# Создаем переменные, где будут храниться промежуточные данные
# Заявка студента
student_name = ''
student_email = ''
student_info = ''
student_phone = ''
student_teg = []
student_city = ''
student_edu = ''
student_portfolio = ''

# Заявка проекта
project_name = ''
project_email = ''
project_info = ''
project_phone = ''
project_teg = []
project_fio = ''
project_skill = ''

# Создаем словари, где будут храниться все заявки
dict_student = {1: [['#ИТ'], 'Миронов Евгений Антонович', 'mironov@mail.ru', '89119001000', 'Екатеринбург',
                    'Сибирский федеральный университет', 'Дипломант олимпиады «Я-профессионал» по Программной инженирии'
                    ' и Искусственному интеллекту 2021', 'Программированием занимаюсь ещё со школы. Учился в Яндекс '
                    'Лицее. Регулярно участвую в хакатонах. Работаю в среде Microsoft Visual Studio 2017 с Python и C# '
                    '(основной). Увлекаюсь шахматами, походами и компьютерными играми.'],
                2: [['#энергетика', '#ИТ'], 'Петрова Дарья Алексеевна', 'dariapa@mail.ru', '88001000000', 'Москва',
                    'МГУ, Энергетика', 'Призер Олимпиады Я-профессионал', 'В прошлом году проходила стажировку в '
                    'Сколковском институте науки и технологий (Сколтех). Программирую на Python, C++']}
# Формат данных [номер заявки]: [[тег], фио, почта, телефон, город, образование, достижения, о себе]
n_student = 2  # счетчик заявок, в словаре как номер заявки

dict_project = {1: [['#ИТ', '#гуманитарныенауки'], 'TalkNow', 'TalkNow – инновационное дейтинг приложение, где пользователи в основном '
                    'принимают решения по голосу. Вместо обычного пролистывания профилей, идея TalkNow сделать упор '
                    'на аудио. Так ты находишь по-настоящему интересного собеседника, а не просто внешне '
                    'привлекательного.', 'mail.ru', '89119500010', 'Зарубин Юрий Александрович', 'Ищем веб-дизайнера, '
                    'а также человека, готового продвигать проект, писать посты, налаживать связи с общественностью.'],
                2: [['#медицина', '#ИТ'], 'Домаптека', '«Домаптека» - приложение для управления домашней аптечкой. Для того, чтобы семья '
                        'не выбрасывала просроченные лекарства и всегда знала, что есть в домашней аптечке, сразу после'
                        ' покупки препаратов при помощи приложения «Домаптека» необходимо просканировать штрихкоды с '
                        'упаковок медикаментов. Приложение само рассортирует их по показаниям к применению, срокам '
                        'годности. ', 'mail.ru', '88005001020', 'Любимова Софья Владимировна',
                    'Ищем Бэкэнд-разработчика и специалистов в обасти фармацевтики']}
n_project = 2
# [номер заявки]: [[тег], название, о проекте, почта, телефон, фио руководителя, необходимые навыки]


# запускать бот с команды /start!!!!!!!! (надо прописать это в описании к боту)

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Политика конфиденциальности",
                                         url='https://rosstat.gov.ru/politika-konfidencialnosti')
    markup.add(button1)
    button2 = types.InlineKeyboardButton("Правила нашего сервиса",
                                         url='https://rosstat.gov.ru/politika-konfidencialnosti')
    markup.add(button2)
    bot.send_message(message.from_user.id,
                     "Привет! Рады, что Вы с нами!\nДля начала, пожалуйста, ознакомьтесь с правилами нашего сервиса "
                     "и подтвердите согласие на обработку персональных данных.", reply_markup=markup)
    keyboard = types.InlineKeyboardMarkup()  # клавиатура
    key_yes = types.InlineKeyboardButton(text='Подтверждаю', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)
    question = 'Вы подтверждаете ознакомление и даете согласие на обработку персональных данных?'
    time.sleep(2)
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def main(message):
    global student_teg, project_teg

    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Напишите, пожалуйста, свое ФИО.\nНапример, Иванов Иван Иванович")
        bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name
    elif message.text == '/reg_project':
        bot.send_message(message.from_user.id, "Напишите, пожалуйста, название проекта.")
        bot.register_next_step_handler(message, get_project)  # следующий шаг – функция get_project
    elif message.text == '/project':
        if 1 not in dict_project:
            phrase = 'К сожалению, на данный момент нет новых проектов.'
            bot.send_message(message.from_user.id, "Проекты:\n"+phrase)
        else:
            for key in dict_project.keys():
                tegs = ''
                for teg in dict_project[key][0]:
                    tegs += ' ' + teg

                # Формат данных словаря
                # [номер заявки]: [[тег], название, о проекте, почта, телефон, город, необходимые навыки]
                phrase = 'Название: ' + dict_project[key][1] + '\nО проекте: ' + dict_project[key][2]+'\nEmail: ' + \
                         '***' + '\nТелефон: ' + '***' + '\nРуководитель: ' + dict_project[key][5] + \
                         '\nНеобходимые навыки: ' + dict_project[key][6] + '\n'\
                         + tegs
                bot.send_message(message.from_user.id, "\nПроект, " + '#заявка' + str(key) + '\n' + phrase +
                                 "\n\nВнимание! Для получения контактных данных необходимо оформить "
                                 "платную подписку")

    elif message.text == '/student':
        if 1 not in dict_student:
            phrase = 'К сожалению, на данный момент еще никто не зарегистрировался.'
            bot.send_message(message.from_user.id, "Студенты:\n"+phrase)
        else:
            for key in dict_student.keys():
                tegs = ''
                for teg in dict_student[key][0]:
                    tegs += ' ' + teg

                # Формат данных словаря
                # [номер заявки]: [[тег], фио, почта, телефон, город, образование, достижения, о себе]
                phrase = 'ФИО: ' + dict_student[key][1] + '\nEmail: ' +\
                         '***' + '\nТелефон: ' + '***' + '\nГород: ' + dict_student[key][4] + \
                         '\nОбразование: ' + dict_student[key][5] + '\nО себе: ' + dict_student[key][7] + \
                         '\nДостижения: ' + dict_student[key][6] + '\n'\
                         + tegs
                bot.send_message(message.from_user.id, "\nСтудент, " + '#заявка' + str(key) + '\n' + phrase +
                                 "\n\nВнимание! "
                                 "Для получения контактных данных необходимо оформить платную подписку")

    elif message.text.lower() == "/help":
        bot.send_message(message.from_user.id, "Если Вы студент нажмите /help_student \n"
                                               "Если Вы руководитель и хотите создать проект нажмите /help_project")
    elif message.text.lower() == "/help_student":
        bot.send_message(message.from_user.id, "Дорогие студенты! Вы можете оставить заявку с информацией о себе.\n"
                                               "Мы передадим Вашу "
                                               "заявку руководителям проектов. Если Ваша кандидатура будет "
                                               "соответствовать требованиям, руководитель свяжется с Вами.\nТакже Вам "
                                               "доступен просмотр проектов, на участие в которых ведется набор."
                                               "\n\nДля того, чтобы создать заявку, напишите /reg\n"
                                               "Чтобы посмотреть доступные проекты, нажмите /project ")
    elif message.text.lower() == "/help_project":
        bot.send_message(message.from_user.id, "Уважаемые сотрудники! Вы можете оставить заявку с информацией о Вашем "
                                               "проекте.\n"
                                               "Заинтересованные в теме студенты откликнутся и свяжутся с Вами по "
                                               "контактным данным, указанным в заявке.\nТакже Вы "
                                               "можете увидеть информацию о студентах, ищущих научного руководителя."
                                               "\n\nДля того, чтобы создать заявку, напишите /reg_project\n"
                                               "Чтобы посмотреть список студентов, нажмите /student ")

    # // Добавление тегов к заявке студента

    elif message.text == 'ИТ':
        student_teg += ['#ИТ']
    elif message.text == 'естественные науки':
        student_teg += ['#естественныенауки']
    elif message.text == 'энергетика':
        student_teg += ['#энергетика']
    elif message.text == 'экономика':
        student_teg += ['#экономика']
    elif message.text == 'медицина':
        student_teg += ['#медицина']
    elif message.text == 'спорт':
        student_teg += ['#спорт']
    elif message.text == 'образование':
        student_teg += ['#образование']
    elif message.text == 'гуманитарные науки':
        student_teg += ['#гуманитарныенауки']
    elif message.text == '/send':
        category = 'student'
        download(category, message)

    # Создание тегов к заявке проекта
    elif message.text == '- ИТ -':
        project_teg += ['#ИТ']
    elif message.text == '- естественные науки -':
        project_teg += ['#естественныенауки']
    elif message.text == '- энергетика -':
        project_teg += ['#энергетика']
    elif message.text == '- экономика -':
        project_teg += ['#экономика']
    elif message.text == '- медицина -':
        project_teg += ['#медицина']
    elif message.text == '- спорт -':
        project_teg += ['#спорт']
    elif message.text == '- образование -':
        project_teg += ['#образование']
    elif message.text == '- гуманитарные науки -':
        project_teg += ['#гуманитарныенауки']
    elif message.text == '/send_project':
        category = 'project'
        download(category, message)

    else:
        bot.send_message(message.from_user.id, "Я не понимаю, напишите /help.")


# Создание заявки для студента
def get_name(message):  # получаем фио, затем запрашиваем почту
    global student_name
    student_name = message.text
    bot.send_message(message.from_user.id, 'Напишите, пожалуйста, свою элекронную почту')
    bot.register_next_step_handler(message, get_email)


def get_email(message):
    global student_email
    student_email = message.text
    bot.send_message(message.from_user.id, 'Укажите номер телефона')
    bot.register_next_step_handler(message, get_group)


def get_group(message):
    global student_phone
    student_phone = message.text
    bot.send_message(message.from_user.id, 'Введите свой город')
    bot.register_next_step_handler(message, get_city)


def get_city(message):
    global student_city
    student_city = message.text
    bot.send_message(message.from_user.id, 'Заполните, пожалуйста, информацию о своем образовании')
    bot.register_next_step_handler(message, get_edu)


def get_edu(message):
    global student_edu
    student_edu = message.text
    bot.send_message(message.from_user.id, 'Укажите свои достижения, если есть')
    bot.register_next_step_handler(message, get_portfolio)


def get_portfolio(message):
    global student_portfolio
    student_portfolio = message.text
    bot.send_message(message.from_user.id, 'Напишите, пожалуйста, вкратце о себе, '
                                           'своих навыках и опыте работы (2-3 предложения)')
    bot.register_next_step_handler(message, get_info)


def get_info(message):  # информация о себе
    global student_info
    student_info = message.text

    # bot.register_next_step_handler(message, get_info)

    # Создание клавиатуры да-нет для подтверждения заявки
    keyboard = types.InlineKeyboardMarkup()  # клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes2')  # кнопка «Да»
    keyboard.add(key_yes)  # добавление кнопки в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)

    # проверка, что заявка заполнена правильно
    question = 'Ваша заявка\nФИО: ' + student_name + '\nEmail: ' + student_email + '\nТелефон: ' + student_phone +\
               '\nГород: '+student_city+'\nОбразование: '+student_edu +\
               '\nО себе: ' + student_info + '\nДостижения: '+student_portfolio+'\n \n Вы хотите сохранить заявку?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


# Создание заявки для проекта
def get_project(message):  # получаем название, затем запрашиваем информацию о проекте
    global project_name
    project_name = message.text
    bot.send_message(message.from_user.id, 'Напишите, пожалуйста, краткую информацию о проекте, указав цель '
                                           'и задачи проекта. (2-3 предложения)')
    bot.register_next_step_handler(message, get_info_project)


def get_info_project(message):  # информация о проекте
    global project_info
    project_info = message.text
    bot.send_message(message.from_user.id, 'Напишите, элекронную почту, по которой студенты смогут с Вами связаться')
    bot.register_next_step_handler(message, get_email_project)


def get_email_project(message):
    global project_email
    project_email = message.text
    bot.send_message(message.from_user.id, 'Введите, пожалуйста, номер телефона')
    bot.register_next_step_handler(message, get_phone_project)


def get_phone_project(message):
    global project_phone
    project_phone = message.text
    bot.send_message(message.from_user.id, 'Укажите, пожалуйста, ФИО руководителя прокта.\n'
                                           'Например, Иванов Иван Иванович')
    bot.register_next_step_handler(message, get_fio_project)


def get_fio_project(message):
    global project_fio
    project_fio = message.text
    bot.send_message(message.from_user.id, 'Укажите, пожалуйста, какими необходимыми навыками '
                                           'должен обладать участник проекта')
    bot.register_next_step_handler(message, get_skill_project)


def get_skill_project(message):
    global project_skill
    project_skill = message.text

    # Создание клавиатуры да-нет для подтверждения заявки
    keyboard = types.InlineKeyboardMarkup()  # клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes3')  # кнопка «Да»
    keyboard.add(key_yes)  # добавление кнопки в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no3')
    keyboard.add(key_no)

    # проверка, что заявка заполнена правильно

    question = 'Ваша заявка\nПроект: ' + project_name + '\nО проекте: ' + project_info + '\nEmail: ' + project_email +\
               '\nТелефон: ' + project_phone + '\nРуководитель: ' + project_fio + '\nНеобходимые навыки: ' + project_skill +\
               '\n \n Вы хотите сохранить заявку?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


def choose_teg_student(message):  # Выбор тега в заявке студента
    global student_teg
    student_teg = []
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton('ИТ')
    bt2 = types.KeyboardButton('естественные науки')
    bt3 = types.KeyboardButton('энергетика')
    bt4 = types.KeyboardButton('экономика')
    bt5 = types.KeyboardButton('медицина')
    bt6 = types.KeyboardButton('спорт')
    bt7 = types.KeyboardButton('образование')
    bt8 = types.KeyboardButton('гуманитарные науки')
    markup.add(bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8)
    bot.send_message(message.chat.id, text='Укажите, в какой области Вам будет интересен проект. Чтобы сохранить заявку'
                                           ' под данной темой, нажмите на соответствующий тег.\n'
                                           '\nВы можете выбрать несколько тегов.\n'
                                           'Чтобы окончательно отправить заявку, '
                                           'нажмите /send',
                     reply_markup=markup)


def choose_teg_project(message):  # Выбор тега в заявке проекта
    global project_teg
    project_teg = []
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton('- ИТ -')
    bt2 = types.KeyboardButton('- естественные науки -')
    bt3 = types.KeyboardButton('- энергетика -')
    bt4 = types.KeyboardButton('- экономика -')
    bt5 = types.KeyboardButton('- медицина -')
    bt6 = types.KeyboardButton('- спорт -')
    bt7 = types.KeyboardButton('- образование -')
    bt8 = types.KeyboardButton('- гуманитарные науки -')
    markup.add(bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8)
    bot.send_message(message.chat.id, text='Укажите, к какой категории относится Ваша заявка. Чтобы сохранить заявку'
                                           ' под данной темой, нажмите на соответствующий тег.\n'
                                           '\nВы можете выбрать несколько тегов.\n'
                                           'Чтобы окончательно отправить заявку, '
                                           'нажмите /send_project',
                     reply_markup=markup)


def download(category, message):  # Сохранение заявок
    global dict_student
    global dict_project
    if category == 'student':
        # Формат данных словаря [номер заявки]: [[тег], фио, почта, телефон, город, образование, достижения, о себе]

        global n_student, student_teg, student_name, student_email, student_info, student_phone,\
            student_edu, student_city, student_portfolio
        n_student += 1
        value = [student_teg, student_name, student_email, student_phone, student_city, student_edu, student_portfolio,
                 student_info]
        dict_student[n_student] = value
        print(dict_student)
        bot.send_message(message.chat.id, 'Ваша заявка сохранена :)\nДля выхода в главное меню нажмите /help')

    if category == 'project':
        # Формат данных словаря [номер заявки]: [[тег], название, о проекте, почта, телефон, город, необходимые навыки]
        global n_project, project_name, project_info, project_phone, project_email, project_teg
        n_project += 1
        value = [project_teg, project_name, project_info, project_email, project_phone, project_fio, project_skill]
        dict_project[n_project] = value
        print(dict_project)
        bot.send_message(message.chat.id, 'Заявка сохранена :)\nДля выхода в главное меню нажмите /help')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # сохранение данных
    if call.data == "yes":  # call.data == callback_data
        bot.send_message(call.message.chat.id, 'Спасибо! Для получения информации о боте напишите /help')
    elif call.data == "yes2":  # call.data == callback_data
        # переход к сохранению заявки в словарь + создание тегов
        choose_teg_student(call.message)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Вы хотите заново внести данные? Тогда напишите, пожалуйста, /reg')

    # заявки проектов
    elif call.data == "yes3":  # call.data == callback_data
        # переход к сохранению заявки в словарь + создание тегов
        choose_teg_project(call.message)
    elif call.data == "no3":
        bot.send_message(call.message.chat.id, 'Вы хотите заново внести данные? '
                                               'Тогда напишите, пожалуйста, /reg_project')


bot.polling(none_stop=True, interval=0)
