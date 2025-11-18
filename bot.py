import telebot
import random
from telebot import types
import json

TOKEN = '8521270073:AAEqN3uLgjls9IzQ1bJjTJdIn-2Z75cGKB0'
bot = telebot.TeleBot(TOKEN)

# Хранилище временных данных пользователей
user_data = {}

# Списки ответов (остаются из предыдущего кода)
answers_simple = ["Бесспорно", "Предрешено", "Никаких сомнений", "Определённо да", "Можешь быть уверен в этом"]
answers_mystic = ["⭐ Звезды сошлись в твою пользу. Да.", "🌑 Луна скрывает ответ. Попробуй еще раз"]
# ... остальные списки ответов

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🎯 Режим выбора')
    btn2 = types.KeyboardButton('🎲 Режим ответа')
    markup.add(btn1, btn2)
    
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Я бот-рандомайзер с двумя режимами:\n\n"
        "🎯 **Режим выбора** - помогу выбрать между вариантами\n"
        "🎲 **Режим ответа** - отвечу на любой твой вопрос\n\n"
        "Выбери режим:",
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text == '🎯 Режим выбора')
def start_choice_mode(message):
    user_id = message.from_user.id
    # Инициализируем данные пользователя
    user_data[user_id] = {
        'mode': 'choice',
        'step': 1,
        'options': []
    }
    
    bot.send_message(
        message.chat.id,
        "🌟 *Режим выбора активирован!*\n\n"
        "Напиши мне *первый вариант*:",
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text == '🎲 Режим ответа')
def start_answer_mode(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('🔮 Мистический', callback_data='mystic')
    btn2 = types.InlineKeyboardButton('📊 Простой', callback_data='simple')
    btn3 = types.InlineKeyboardButton('😄 Шуточный', callback_data='funny')
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(
        message.chat.id,
        "🎲 *Режим ответа активирован!*\n\n"
        "Задай мне вопрос и выбери стиль ответа:",
        reply_markup=markup,
        parse_mode='Markdown'
    )

# Обработчик текстовых сообщений для режима выбора
@bot.message_handler(func=lambda message: message.from_user.id in user_data and user_data[message.from_user.id]['mode'] == 'choice')
def handle_choice_steps(message):
    user_id = message.from_user.id
    user_state = user_data[user_id]
    current_step = user_state['step']
    
    if current_step == 1:
        # Сохраняем первый вариант
        user_state['options'].append(message.text)
        user_state['step'] = 2
        
        bot.send_message(
            message.chat.id,
            "📝 Отлично! Теперь напиши *второй вариант*:",
            parse_mode='Markdown'
        )
    
    elif current_step == 2:
        # Сохраняем второй вариант
        user_state['options'].append(message.text)
        user_state['step'] = 3
        
        # Показываем подтверждение
        show_confirmation(message.chat.id, user_state['options'])

def show_confirmation(chat_id, options):
    markup = types.InlineKeyboardMarkup()
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

# Обработчик инлайн-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if call.data.startswith('edit_'):
        # Режим редактирования
        option_num = int(call.data.split('_')[1])
        user_data[user_id]['editing'] = option_num
        
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=f"✏️ Напиши новый текст для *{option_num}-го варианта*:",
            parse_mode='Markdown'
        )
    
    elif call.data == 'confirm_choice':
        # Подтверждение и выбор варианта
        options = user_data[user_id]['options']
        chosen_option = random.choice(options)
        
        # Красивая анимация выбора
        choose_with_style(chat_id, options, chosen_option, call.message.message_id)
        
        # Очищаем данные пользователя
        if user_id in user_data:
            del user_data[user_id]
    
    elif call.data in ['mystic', 'simple', 'funny']:
        # Обработка стилей ответа (из предыдущего кода)
        handle_answer_style(call)

def choose_with_style(chat_id, options, chosen_option, message_id):
    # Удаляем предыдущее сообщение с кнопками
    bot.delete_message(chat_id, message_id)
    
    # Создаем красивый результат выбора
    emojis = ["🎯", "⭐", "✨", "🎊", "🏆"]
    spinning_emojis = ["⏳", "⌛", "⏳", "⌛"]
    
    # Отправляем сообщение с "анимацией"
    msg = bot.send_message(
        chat_id,
        f"{random.choice(spinning_emojis)} *Запускаю магию выбора...*",
        parse_mode='Markdown'
    )
    
    # Имитируем процесс выбора
    import time
    time.sleep(2)
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg.message_id,
        text=f"{random.choice(spinning_emojis)} *Анализирую варианты...*",
        parse_mode='Markdown'
    )
    
    time.sleep(2)
    
    # Финальное сообщение с результатом
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

# Обработчик редактирования вариантов
@bot.message_handler(func=lambda message: message.from_user.id in user_data and 'editing' in user_data[message.from_user.id])
def handle_edit_option(message):
    user_id = message.from_user.id
    user_state = user_data[user_id]
    option_num = user_state['editing']
    
    # Обновляем вариант
    user_state['options'][option_num - 1] = message.text
    del user_state['editing']
    
    # Снова показываем подтверждение
    show_confirmation(message.chat.id, user_state['options'])

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен!")
    bot.infinity_polling()
