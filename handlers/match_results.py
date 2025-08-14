from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from utils.keyboards import Keyboards

# Определяем состояния диалога
MATCH_TYPE, PARTNER_NAME, SCORE = range(3)

async def start_match_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало внесения результата матча."""
    await update.message.reply_text("Выберите тип матча:", reply_markup=Keyboards.get_game_type())
    return MATCH_TYPE

async def get_match_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение типа матча."""
    context.user_data['match_type'] = update.message.text
    await update.message.reply_text("Введите имя или фамилию партнера:")
    return PARTNER_NAME

async def get_partner_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение имени партнера."""
    context.user_data['partner_name'] = update.message.text
    await update.message.reply_text("Введите счет матча (например, 6:4, 7:5):")
    return SCORE

async def save_match_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохранение результата матча."""
    context.user_data['score'] = update.message.text

    # Логика сохранения результата в базу данных
    # Например: save_match_result_to_db(context.user_data)

    await update.message.reply_text("Результат матча успешно сохранен!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена диалога."""
    await update.message.reply_text("Действие отменено.")
    return ConversationHandler.END

# Конверсейшн-хендлер для внесения результатов матчей
match_results_handler = ConversationHandler(
    entry_points=[CommandHandler('submit_score', start_match_result)],
    states={
        MATCH_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_match_type)],
        PARTNER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_partner_name)],
        SCORE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_match_result)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)