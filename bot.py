import os
import telebot
from logic import generate_image   # наша функция из прошлого шага
from config import BOT_TOKEN
from telebot import apihelper
apihelper.proxy = {'https': 'socks5://127.0.0.1:9150'}



bot = telebot.TeleBot(BOT_TOKEN)



@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.reply_to(
        message,
        "Привет! 👋\n"
        "Отправь описание картинки — и я её сгенерирую.\n"
        "Например: «рыжий кот в космосе, акварель»."
    )


@bot.message_handler(content_types=['text'])
def handle_text(message):
    prompt = message.text.strip()
    if not prompt:
        bot.reply_to(message, "Пустой запрос 🤔 Напиши, что нарисовать.")
        return

    # Сообщаем пользователю, что запрос принят
    status_msg = bot.reply_to(message, "🎨 Генерирую изображение, подожди…")

    try:
        # 1) Вызываем функцию генерации
        filename = generate_image(prompt)

        # 2) Проверяем, что картинка получена
        if filename is None:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
                text="😔 Не удалось сгенерировать картинку. Попробуй другой промпт."
            )
            return

        # 3) Отправляем картинку в чат пользователю
        with open(filename, "rb") as photo:
            bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption="Готово! Промпт: %s" % prompt[:200]
            )

        # Удаляем служебное сообщение «генерирую…»
        bot.delete_message(message.chat.id, status_msg.message_id)

        # Чистим временный файл, чтобы не копились картинки
        try:
            os.remove(filename)
        except OSError:
            pass

    except Exception as e:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=status_msg.message_id,
            text="😔 Ошибка при генерации:\n%s" % e
        )


# ====== ЗАПУСК ======
if __name__ == "__main__":
    print("Бот запущен. Остановить — Ctrl+C.")
    bot.infinity_polling(timeout=60)