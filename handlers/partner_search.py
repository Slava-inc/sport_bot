from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from database.models import User, SessionLocal  # Импортируем модели и сессию базы данных
from utils.keyboards import Keyboards

# Определяем состояния диалога
FILTER_CITY, FILTER_LEVEL, FILTER_TIME = range(3)

async def start_partner_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало поиска партнера."""
    await update.message.reply_text("Выберите город:", reply_markup=Keyboards.get_partner_search_filters())
    return FILTER_CITY

async def get_filter_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение фильтра по городу."""
    context.user_data['filter_city'] = update.message.text
    await update.message.reply_text("Выберите уровень игры (например, 1-7):")
    return FILTER_LEVEL

async def get_filter_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение фильтра по уровню игры."""
    try:
        level = float(update.message.text)
        if 1.0 <= level <= 7.0:
            context.user_data['filter_level'] = level
            await update.message.reply_text("Выберите время игры (например, утро/день/вечер):")
            return FILTER_TIME
        else:
            await update.message.reply_text("Уровень должен быть от 1.0 до 7.0. Попробуйте снова:")
            return FILTER_LEVEL
    except ValueError:
        await update.message.reply_text("Введите корректный уровень игры (например, 5.0):")
        return FILTER_LEVEL

async def get_filter_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение фильтра по времени игры."""
    context.user_data['filter_time'] = update.message.text

    # Логика поиска партнеров в базе данных
    session = SessionLocal()
    city = context.user_data['filter_city']
    level = context.user_data['filter_level']
    time = context.user_data['filter_time']

    # Фильтрация пользователей по заданным критериям
    partners = session.query(User).filter(
        User.city == city,
        User.level.between(level - 1, level + 1),  # Поиск игроков с близким уровнем
        User.preferred_time.like(f"%{time}%")      # Поиск по времени игры
    ).all()

    # Отправка результатов пользователю
    if partners:
        await update.message.reply_text("Вот список найденных партнеров:")
        for partner in partners:
            await update.message.reply_text(
                f"{partner.first_name} {partner.last_name}\n"
                f"Уровень: {partner.level}\n"
                f"Город: {partner.city}\n"
                f"Время игры: {partner.preferred_time}"
            )
    else:
        await update.message.reply_text("По вашему запросу партнеры не найдены.")

    session.close()
    return ConversationHandler.END

# Конверсейшн-хендлер для поиска партнеров
partner_search_handler = ConversationHandler(
    entry_points=[CommandHandler('find_partner', start_partner_search)],
    states={
        FILTER_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_filter_city)],
        FILTER_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_filter_level)],
        FILTER_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_filter_time)],
    },
    fallbacks=[]
)