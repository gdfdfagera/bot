import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from io import BytesIO
import process


TOKEN = "6670441542:AAGnU4k3CGdvZ5klDM7a6jnb_w_iJZy2duc"
ALLOWED_USERS = [801866076, 439638583]


def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in ALLOWED_USERS:
        update.message.reply_text('Привет! Отправь мне Excel файл для обработки.')
    else:
        update.message.reply_text('Вы не авторизованы для использования этого бота.')

def handle_text(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in ALLOWED_USERS:
        received_text = update.message.text
        processed_text = process.process_input(received_text)
        result_message = "\n\n".join(
            [f"{i + 1}. {name}. {description}. Official site: {website}. Country: {country}" for
             i, (name, [description, website, country]) in enumerate(processed_text.items())])
        update.message.reply_text(result_message)
    else:
        update.message.reply_text('Вы не авторизованы для использования этого бота.')

def handle_excel(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in ALLOWED_USERS:
        file_id = update.message.document.file_id
        file = context.bot.get_file(file_id)

        file_path = os.path.join("temp", f"{file_id}.xlsx")
        file.download(file_path)

        global last_processed_excel_info
        new_companies_info, last_processed_excel_info = process.process_excel(file_path)

        result_message = "\n\n".join([f"{i + 1}. {name}. {description}. Official site: {website}. Country: {country}" for i, (name, [description, website, country]) in enumerate(new_companies_info.items())])
        update.message.reply_text(result_message)
    else:
        update.message.reply_text('Вы не авторизованы для использования этого бота.')

def find_more_companies(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in ALLOWED_USERS:
        global last_processed_excel_info
        if last_processed_excel_info:
            file_path = last_processed_excel_info["file_path"]

            new_companies_info, last_processed_excel_info = process.process_excel(file_path)

            result_message = "\n\n".join(
                [f"{i + 1}. {name}. {description}. Official site: {website}. Country: {country}" for i, (name, [description, website, country]) in enumerate(new_companies_info.items())])
            update.message.reply_text(result_message)
        else:
            update.message.reply_text('Пожалуйста, сначала отправьте Excel файл для обработки.')
    else:
        update.message.reply_text('Вы не авторизованы для использования этого бота.')

def start_find_by_country(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in ALLOWED_USERS:
        keyboard = [[InlineKeyboardButton("Найти компанию по стране", callback_data='find_by_country')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Введите страну:", reply_markup=reply_markup)
    else:
        update.message.reply_text('Вы не авторизованы для использования этого бота.')

def handle_country_input(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in ALLOWED_USERS:
        global last_processed_excel_info
        if last_processed_excel_info:
            file_path = last_processed_excel_info["file_path"]

            country = update.message.text

            new_companies_info = process.process_input(file_path, country)

            result_message = "\n\n".join(
                [f"{i + 1}. {name}. {description}. Official site: {website}. Country: {country}" for i, (name, [description, website, country]) in enumerate(new_companies_info.items())])
            update.message.reply_text(result_message)
        else:
            update.message.reply_text('Пожалуйста, сначала отправьте Excel файл для обработки.')
    else:
        update.message.reply_text('Вы не авторизованы для использования этого бота.')

def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == 'find_by_country':
        start_find_by_country(update, context)
    else:
        pass

def main() -> None:
    os.makedirs("temp", exist_ok=True)

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document.mime_type("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"), handle_excel))
    dp.add_handler(CommandHandler("find", find_more_companies))
    dp.add_handler(CommandHandler("find_by_country", start_find_by_country))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_country_input))
    dp.add_handler(CallbackQueryHandler(button_callback))
    dp.add_handler(CallbackQueryHandler(handle_country_input, pattern='find_by_country'))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
