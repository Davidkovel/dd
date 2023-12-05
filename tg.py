#!/usr/bin/env python
# -*- coding: utf-8 -*-


# import json
import re

import telebot
from telebot import types

TOKEN = '5761705554:AAHbYs51iR8R_DzOWC9Sx4QCzBAgMqINkLY'
bot = telebot.TeleBot(TOKEN)
# Женя - 6002938397
admins = ['6002938397']

user_conversations = {}

type_of_question = ""

keyboard = types.InlineKeyboardMarkup()
cooperation_button = types.InlineKeyboardButton("🫱 Сотрудничество", callback_data="cooperation")
suggestions_button = types.InlineKeyboardButton("⚖️ Предложения", callback_data="suggestions")
help_button = types.InlineKeyboardButton("🆘 Помощь", callback_data="help")
keyboard.add(cooperation_button, suggestions_button, help_button)


# def save_to_json():
#     with open('user_conversations.json', 'w') as file:
#         json.dump(user_conversations, file)


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    user_id = message.from_user.id
    user_name = message.from_user.username

    # del user_conversations[user_id]
    if str(user_id) in admins:
        greeting = f"Привет, вы администратор техподержка. Ждите вопросы от клиентов"
        bot.send_message(user_id, greeting)
    else:
        # if user_id in user_conversations:
        #     del user_conversations[user_id]
        greeting = (
            f"Приветствую, {user_name}! 👋 Добро пожаловать в онлайн-поддержку! Я здесь, чтобы помочь вам решить любые технические вопросы и предоставить необходимую поддержку."
            "\n\n🤖 Я - ваш виртуальный ассистент, готовый помочь с вопросами о сотрудничестве, предложениями и, конечно же, технической помощью. Выберите одну из опций ниже, чтобы начать:"
            "\n\n🫱 Сотрудничество - если у вас есть предложения о партнерстве или сотрудничестве."
            "\n⚖️ Предложения - поделитесь своими идеями и предложениями для улучшения наших услуг."
            "\n🆘 Помощь - если у вас возникли проблемы или вопросы, связанные с техническими вопросами."
            "\n\nНе стесняйтесь задавать вопросы - я здесь для вас! 🚀"
        )

        with open('photo_5429099130891916490_y.jpg',
                  'rb') as photo:
            bot.send_photo(user_id, photo, caption=greeting, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    global type_of_question
    user_id = call.from_user.id
    button_text = call.data

    if button_text == "cooperation":
        bot.send_message(user_id, "Если у вас есть вопрос, отправьте его мне")
        type_of_question = "🫱 Сотрудничество"
    elif button_text == "suggestions":
        bot.send_message(user_id, "Если у вас есть вопрос, отправьте его мне")
        type_of_question = "⚖️ Предложения"
    elif button_text == "help":
        bot.send_message(user_id, "Если у вас есть вопрос, отправьте его мне")
        type_of_question = "🆘 Помощь"


@bot.message_handler(func=lambda message: str(message.from_user.id) not in admins)
def handle_user_messages(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_message = message.text

    if user_id not in user_conversations and user_id not in admins:
        user_conversations[user_id] = {"questions": [], "responses": []}

    if user_id not in admins:
        user_conversations[user_id]["questions"].append(f"{user_name}: {user_message}")
        if message.reply_to_message:
            print(message.reply_to_message.text)
            user_id_str = get_id_from_text(message.reply_to_message.text)
            if user_id_str:
                user_id = int(user_id_str)
                print('-', user_id)
                answer_adminstrator = 'Ответ от администратора: '
                answer_adminstrator += message.text
                bot.send_message(user_id, answer_adminstrator)
                bot.send_message(user_id, 'Если у вас есть еще вопросы, то задавайте =)')
            else:
                print(user_id)
        else:
            print('47239743284', user_id)
            bot.send_message(user_id, "Ваш вопрос получен. Администратор скоро ответит.")
            for admin_id in admins:
                print(admin_id)
                bot.send_message(6002938397,
                                 f"{type_of_question}\nНовый вопрос от пользователя {user_name} (ID: {user_id}):\n{user_message}")
                # save_to_json()
    # if message.reply_to_message:
    #     print('33333')
    #     if user_id in admins:
    #         print('admin2 ')
    #
    #         user_id_str = get_id_from_text(message.reply_to_message.text)
    #         user_id = int(user_id_str)
    #
    #         bot.send_message(user_id, f"Администратор ответил: {message.text}")
    # else:
    #     print('admin 3')
    #     if admins[0] in user_conversations:
    #         questions = user_conversations[admins[0]]["questions"]
    #         if questions:
    #             question = questions[-1]
    #             bot.send_message(admins[0],
    #                              f"Последний вопрос от пользователя:\n{question}\n\nОтветите на вопрос, используя /respond.")
    #


def get_id_from_text(txt: str):
    match = re.search(r'ID: (\d+)', txt)
    if match:
        return match.group(1)
    else:
        return None


@bot.message_handler(func=lambda message: str(message.from_user.id) in admins)
def handle_admin_messages(message):
    admin_id = message.from_user.id
    admin_name = message.from_user.username

    print('admin 1')
    if message.reply_to_message:
        print('admin2 ')
        user_id_str = get_id_from_text(message.reply_to_message.text)
        print(f"Admin {admin_name} is responding to user with ID: {user_id_str}")

        bot.send_message(user_id_str, f"Администратор ответил: {message.text}")
        bot.send_message(user_id_str, "Чтобы задать еще раз вопрос то нажмите на /start")
    else:
        print('admin 3')
        if admin_id in user_conversations:
            questions = user_conversations[admin_id]["questions"]
            if questions:
                question = questions[-1]
                bot.send_message(admin_id,
                                 f"Последний вопрос от пользователя:\n{question}\n\nОтветите на вопрос, используя /respond.")


# @bot.message_handler(commands=['respond'])
# def handle_admin_response(message):
#     admin_id = message.from_user.id
#     admin_name = message.from_user.username
#
#     if admin_id in user_conversations:
#         responses = user_conversations[admin_id]["responses"]
#         if responses:
#             response = responses[-1]
#             user_id = response["user_id"]
#             bot.send_message(admin_id, f"Пользователь с ID {user_id} спрашивал:\n{response['message']}")
#             bot.send_message(admin_id, f"Ваш последний ответ:\n{response}\n\nОтвет отправлен пользователю.")
#             bot.send_message(user_id, f"Ответ от администратора {admin_name}:\n{response['message']}")
#         else:
#             bot.send_message(admin_id, "У вас нет ответов для отправки.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
