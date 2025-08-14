from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from utils.keyboards import Keyboards

# Определяем состояния диалога
CITY, DISTRICT, DATE, TIME, GAME_TYPE, PAYMENT, COMMENT = range(7)

async def start_game_proposal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало процесса создания предложения игры."""
    await update.message.reply_text("Введите город:", reply_markup=Keyboards.get_back_button())
    return CITY

async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение города."""
    context.user_data['city'] = update.message.text
    await update.message.reply_text("Введите район:")
    return DISTRICT

async def get_district(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение района."""
    context.user_data['district'] = update.message.text
    await update.message.reply_text("Введите дату игры (дд.мм.гггг):")
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение даты игры."""
    context.user_data['date'] = update.message.text
    await update.message.reply_text("Введите время игры (чч:мм):")
    return TIME

async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение времени игры."""
    context.user_data['time'] = update.message.text
    await update.message.reply_text("Выберите тип игры:", reply_markup=Keyboards.get_game_type())
    return GAME_TYPE

async def get_game_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение типа игры."""
    context.user_data['game_type'] = update.message.text
    await update.message.reply_text("Выберите способ оплаты корта:", reply_markup=Keyboards.get_payment_type())
    return PAYMENT

async def get_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение способа оплаты корта."""
    context.user_data['payment'] = update.message.text
    await update.message.reply_text("Добавьте комментарий (если нужно):")
    return COMMENT

async def save_game_proposal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохранение предложения игры."""
    context.user_data['comment'] = update.message.text

    # Логика сохранения в базу данных
    # Например: save_to_db(context.user_data)

    await update.message.reply_text("Предложение игры успешно создано!")
    return ConversationHandler.END

# Конверсейшн-хендлер для предложений игр
game_proposals_handler = ConversationHandler(
    entry_points=[CommandHandler('propose_game', start_game_proposal)],
    states={
        CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)],
        DISTRICT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_district)],
        DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
        TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)],
        GAME_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_game_type)],
        PAYMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_payment)],
        COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_game_proposal)],
    },
    fallbacks=[]
)