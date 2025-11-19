import telebot
import random
from telebot import types
import os
import time
import flask

TOKEN = os.environ.get('BOT_TOKEN', '8521270073:AAEqN3uLgjls9IzQ1bJjTJdIn-2Z75cGKB0')
bot = telebot.TeleBot(TOKEN)

# Хранилище данных пользователей
user_data = {}

# Списки ответов
answers_simple = [
    "Бесспорно", "Предрешено", "Никаких сомнений", "Определённо да", "Можешь быть уверен в этом",
    "Мне кажется — «да»", "Вероятнее всего", "Хорошие перспективы", "Знаки говорят — «да»", "Да",
    "Пока не ясно, попробуй снова", "Спроси позже", "Лучше не рассказывать", "Сейчас нельзя предсказать", 
    "Сконцентрируйся и спроси опять", "Даже не думай", "Мой ответ — «нет»", "По моим данным — «нет»", 
    "Перспективы не очень хорошие", "Весьма сомнительно"
]

answers_mystic = [
    "⭐ Звезды сошлись в твою пользу. Да.",
    "🌑 Луна скрывает ответ. Попробуй еще раз",
    "🔮 Магический шар говорит: Безусловно ДА!",
    "✨ Энергии Вселенной подтверждают твои ожидания",
    "🌠 По звездному пути - да, смело вперед!",
    "💫 Космические вибрации говорят НЕТ",
    "🔭 Галактики выстроились против этого"
]

answers_funny = [
    "🤔 Хмм... ДА, но только если принесешь печенек!",
    "🎉 ОДНОЗНАЧНО ДА! Танцуем от радости! 💃",
    "🙈 Я бы сказал нет, но мой хвост виляет да!",
    "🍕 Пицца с ананасами? Нет. А на твой вопрос - ДА!",
    "🤖 01000100 01000001 (это ДА в двоичном коде!)",
    "🐱 Кот сказал: мур-нет!",
    "🎯 Ты удачлив! Ответ - ДА!"
]

# Главное меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🎯 Режим выбора')
    btn2 = types.KeyboardButton('🎲 Режим ответа')
    btn3 = types.KeyboardButton('ℹ️ О боте')
    markup.add(btn1, btn2, btn3)
    return markup

# Кнопка Назад
def back_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('⬅️ Назад')
    markup.add(btn)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_data[user_id] = {'mode': 'main'}
    
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Я бот-рандомайзер с двумя режимами:\n\n"
        "🎯 *Режим выбора* - помогу выбрать между вариантами\n"
        "🎲 *Режим ответа* - отвечу на любой твой вопрос\n\n"
        "Выбери режим:",
        reply_markup=main_menu(),
        parse_mode='Markdown'
    )

# Обработка кнопки Назад
@bot.message_handler(func=lambda message: message.text == '⬅️ Назад')
def handle_back(message):
    user_id = message.from_user.id
    user_data[user_id] = {'mode': 'main'}
    
    bot.send_message(
        message.chat.id,
        "🔙 Возвращаемся в главное меню:\n\n"
        "🎯 *Режим выбора* - помогу выбрать между вариантами\n"
        "🎲 *Режим ответа* - отвечу на любой твой вопрос",
        reply_markup=main_menu(),
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text == '🎯 Режим выбора')
def start_choice_mode(message):
    user_id = message.from_user.id
    user_data[user_id] = {
        'mode': 'choice',
        'step': 1,
        'options': []
    }
    
    bot.send_message(
        message.chat.id,
        "🌟 *Режим выбора активирован!*\n\n"
        "Я помогу тебе выбрать между двумя вариантами.\n\n"
        "Напиши мне *первый вариант*:",
        reply_markup=back_button(),
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text == '🎲 Режим ответа')
def start_answer_mode(message):
    user_id = message.from_user.id
    user_data[user_id] = {'mode': 'answer_waiting_question'}
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('🔮 Мистический', callback_data='style_mystic')
    btn2 = types.InlineKeyboardButton('📊 Простой', callback_data='style_simple')
    btn3 = types.InlineKeyboardButton('😄 Шуточный', callback_data='style_funny')
    btn4 = types.InlineKeyboardButton('🎲 Случайный стиль', callback_data='style_random')
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(
        message.chat.id,
        "🎲 *Режим ответа активирован!*\n\n"
        "Задай мне любой вопрос, а затем выбери стиль ответа:\n\n"
        "🔮 *Мистический* - таинственные ответы\n"
        "📊 *Простой* - прямые ответы\n"
        "😄 *Шуточный* - веселые ответы\n"
        "🎲 *Случайный стиль* - сюрприз!",
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text == 'ℹ️ О боте')
def about_bot(message):
    bot.send_message(
        message.chat.id,
        "🤖 *Обо мне:*\n\n"
        "Я - умный бот-рандомайзер!\n\n"
        "✨ *Что я умею:*\n"
        "• Отвечать на вопросы в разных стилях\n"
        "• Помогать выбирать между вариантами\n"
        "• Поддерживать беседу\n\n"
        "Просто напиши мне что-нибудь! 😊",
        reply_markup=back_button(),
        parse_mode='Markdown'
    )

# Обработка шагов режима выбора
@bot.message_handler(func=lambda message: 
                    message.from_user.id in user_data and 
                    user_data[message.from_user.id].get('mode') == 'choice')
def handle_choice_steps(message):
    user_id = message.from_user.id
    user_state = user_data[user_id]
    current_step = user_state['step']
    
    if current_step == 1:
        user_state['options'].append(message.text)
        user_state['step'] = 2
        
        bot.send_message(
            message.chat.id,
            f"✅ Первый вариант: *{message.text}*\n\n"
            "Теперь напиши *второй вариант*:",
            parse_mode='Markdown'
        )
    
    elif current_step == 2:
        user_state['options'].append(message.text)
        user_state['step'] = 3
        show_confirmation(message.chat.id, user_state['options'])

def show_confirmation(chat_id, options):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_edit1 = types.InlineKeyboardButton('✏️ Изменить 1-й вариант', callback_data='edit_1')
    btn_edit2 = types.InlineKeyboardButton('✏️ Изменить 2-й вариант', callback_data='edit_2')
    btn_confirm = types.InlineKeyboardButton('✅ Всё верно! Выбирай!', callback_data='confirm_choice')
    markup.add(btn_edit1, btn_edit2)
    markup.add(btn_confirm)
    
    confirmation_text = (
        "📋 *Проверь свои варианты:*\n\n"
        f"1. {options[0]}\n"
        f"2. {options[1]}\n\n"
        "Всё верно или хочешь что-то изменить?"
    )
    
    bot.send_message(chat_id, confirmation_text, reply_markup=markup, parse_mode='Markdown')

# Обработка инлайн-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if call.data.startswith('edit_'):
        option_num = int(call.data.split('_')[1])
        user_data[user_id] = {
            'mode': 'editing',
            'editing_option': option_num,
            'options': user_data[user_id]['options']
        }
        
        bot.send_message(
            chat_id,
            f"✏️ *Режим редактирования*\n\n"
            f"Текущий {option_num}-й вариант: *{user_data[user_id]['options'][option_num-1]}*\n\n"
            f"Напиши новый текст для {option_num}-го варианта:",
            reply_markup=back_button(),
            parse_mode='Markdown'
        )
    
    elif call.data == 'confirm_choice':
        options = user_data[user_id]['options']
        chosen_option = random.choice(options)
        choose_with_style(chat_id, options, chosen_option, call.message.message_id)
        
        if user_id in user_data:
            del user_data[user_id]
    
    elif call.data.startswith('style_'):
        style = call.data.split('_')[1]
        user_data[user_id]['selected_style'] = style
        
        if style == 'random':
            style = random.choice(['mystic', 'simple', 'funny'])
        
        style_names = {
            'mystic': '🔮 Мистический',
            'simple': '📊 Простой', 
            'funny': '😄 Шуточный'
        }
        
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=f"✅ Выбран стиль: *{style_names[style]}*\n\n"
                 "Теперь задай мне свой вопрос!",
            parse_mode='Markdown'
        )

# Обработка режима редактирования
@bot.message_handler(func=lambda message: 
                    message.from_user.id in user_data and 
                    user_data[message.from_user.id].get('mode') == 'editing')
def handle_edit_mode(message):
    user_id = message.from_user.id
    user_state = user_data[user_id]
    
    # Сохраняем новый вариант
    option_num = user_state['editing_option']
    user_state['options'][option_num - 1] = message.text
    
    # Возвращаемся к подтверждению
    user_state['mode'] = 'choice'
    user_state['step'] = 3
    del user_state['editing_option']
    
    show_confirmation(message.chat.id, user_state['options'])

# Красивый выбор варианта
def choose_with_style(chat_id, options, chosen_option, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass
    
    emojis = ["🎯", "⭐", "✨", "🎊", "🏆"]
    spinning_emojis = ["⏳", "⌛", "🔮", "🎲"]
    
    msg = bot.send_message(
        chat_id,
        f"{random.choice(spinning_emojis)} *Запускаю магию выбора...*",
        parse_mode='Markdown'
    )
    
    time.sleep(1.5)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg.message_id,
        text=f"{random.choice(spinning_emojis)} *Анализирую варианты...*",
        parse_mode='Markdown'
    )
    
    time.sleep(1.5)
    
    result_text = (
        f"{random.choice(emojis)} *ВОТ МОЙ ВЫБОР!* {random.choice(emojis)}\n\n"
        f"📋 Из вариантов:\n"
        f"• {options[0]}\n"
        f"• {options[1]}\n\n"
        f"🎉 *Я выбираю:*\n"
        f"✨ **{chosen_option}** ✨\n\n"
        "_Удачи в твоём выборе!_"
    )
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg.message_id,
        text=result_text,
        parse_mode='Markdown'
    )

# Обработка ЛЮБОГО текстового сообщения (отвечает на всё)
@bot.message_handler(content_types=['text'])
def handle_any_message(message):
    user_id = message.from_user.id
    
    # Пропускаем сообщения, которые уже обрабатываются другими хендлерами
    if (user_id in user_data and 
        user_data[user_id].get('mode') in ['choice', 'editing', 'answer_waiting_question']):
        return
    
    # Если пользователь в режиме ожидания вопроса для ответа
    if user_id in user_data and user_data[user_id].get('mode') == 'answer_waiting_question':
        if 'selected_style' in user_data[user_id]:
            style = user_data[user_id]['selected_style']
            
            if style == 'mystic':
                answer = random.choice(answers_mystic)
            elif style == 'simple':
                answer = random.choice(answers_simple)
            elif style == 'funny':
                answer = random.choice(answers_funny)
            else:
                answer = random.choice(answers_simple)
            
            # Сбрасываем режим
            user_data[user_id] = {'mode': 'main'}
            
            bot.send_message(
                message.chat.id,
                f"❓ *Твой вопрос:* {message.text}\n\n"
                f"💫 *Мой ответ:* {answer}",
                reply_markup=main_menu(),
                parse_mode='Markdown'
            )
        else:
            bot.send_message(
                message.chat.id,
                "⚠️ Сначала выбери стиль ответа из кнопок выше!",
                reply_markup=back_button()
            )
    
    # Если пользователь просто написал сообщение (не в режиме)
    else:
        responses = [
            "Интересно! Хочешь задать вопрос или выбрать между вариантами?",
            "Хм... Используй кнопки ниже для выбора режима!",
            "Класс! Выбери, чем я могу тебе помочь 👇",
            "Отлично! Давай воспользуемся одним из моих режимов!",
            "Понял тебя! Выбери действие из меню ниже:"
        ]
        
        bot.send_message(
            message.chat.id,
            f"{random.choice(responses)}",
            reply_markup=main_menu()
        )

# ===== ДЛЯ RENDER =====
app = flask.Flask(__name__)

@app.route('/')
def index():
    return "🤖 Бот работает! Используйте Telegram для общения с ботом."

@app.route('/webhook', methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

# Установка webhook при запуске
def set_webhook():
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=webhook_url)

if __name__ == '__main__':
    # Для Render - устанавливаем webhook и запускаем Flask
    set_webhook()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
