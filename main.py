from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)
from handlers.registration import start_registration, get_sport, get_role, save_profile, confirm_profile
from handlers.game_proposals import game_proposals_handler
from handlers.partner_search import partner_search_handler
from handlers.match_results import match_results_handler
from handlers.subscription import subscription_handler
from config import settings
import os
from database.models import init_db

# Убедитесь, что папка для хранения фото существует
PHOTOS_DIR = "user_photos"
os.makedirs(PHOTOS_DIR, exist_ok=True)

def main():

    
    # Создаем экземпляр приложения
    application = Application.builder().token(settings.BOT_TOKEN).build()

    # Регистрация команд и обработчиков
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_registration)],
        states={
            0: [CallbackQueryHandler(get_sport)],
            1: [CallbackQueryHandler(get_role)],
            2: [MessageHandler(filters.PHOTO & ~filters.COMMAND, save_profile)],
            3: [CallbackQueryHandler(confirm_profile)]
        },
        fallbacks=[]
    )

    # Добавляем обработчики
    application.add_handler(conv_handler)
    application.add_handler(game_proposals_handler)
    application.add_handler(partner_search_handler)
    application.add_handler(match_results_handler)
    application.add_handler(subscription_handler)

    # Обработчик inline-кнопок
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Запускаем бота
    application.run_polling()

# Пример обработчика inline-кнопок
async def handle_callback(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "confirm_yes":
        await query.edit_message_text("Подтверждено!")
    elif query.data == "confirm_no":
        await query.edit_message_text("Отменено!")

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")

    main()