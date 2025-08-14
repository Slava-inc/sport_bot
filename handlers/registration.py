from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
# from database.models import User, SessionLocal  # Импортируем модели базы данных
from utils.keyboards import Keyboards  # Импортируем клавиатуры
from tables import save_to_database

# Определяем состояния диалога
SPORT, ROLE, PHOTO, CONFIRM_PROFILE = range(4)

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Начало процесса регистрации.
    Запрашивает у пользователя выбор вида спорта.
    """
    await update.message.reply_text(
        "Добро пожаловать! Для начала регистрации выберите вид спорта:",
        reply_markup=Keyboards.get_sport_types()  # Клавиатура с видами спорта
    )
    return SPORT

async def get_sport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Получение выбранного вида спорта.
    Сохраняет вид спорта и запрашивает роль пользователя.
    """
    query = update.callback_query
    await query.answer()  # Подтверждаем получение callback-запроса

    sport = query.data  # Получаем данные из callback_data
    context.user_data['sport'] = sport  # Сохраняем вид спорта в контексте

    await query.edit_message_text(
        "Выберите вашу роль:", 
        reply_markup=Keyboards.get_role_selection()
    )
    return ROLE  # Переходим к следующему состоянию

async def get_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Подтверждаем получение callback-запроса

    role = query.data  # Получаем данные из callback_data
    context.user_data['role'] = role  # Сохраняем роль в контексте

    await query.edit_message_text(
        "Отлично! Теперь загрузите ваше фото профиля.",
        reply_markup=None  # Убираем клавиатуру после выбора
    )
    return PHOTO  # Переходим к следующему состоянию

async def save_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Обработка загрузки фото
    photo_file = await update.message.photo[-1].get_file()
    photo_path = f"user_photos/{update.message.from_user.id}.jpg"
    await photo_file.download_to_drive(photo_path)

    # Сохраняем путь к фото в контексте
    context.user_data['photo'] = photo_path
    context.user_data['telegram_id'] = str(update.message.from_user.id)

    # Отправляем сообщение с подтверждением
    await update.message.reply_text(
        "Ваш профиль сохранен! Хотите опубликовать его?",
        reply_markup=Keyboards.get_confirmation_buttons()
    )
    return CONFIRM_PROFILE  # Переходим к состоянию подтверждения


async def confirm_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Подтверждаем получение callback-запроса

    confirmation = query.data  # Получаем данные из callback_data

    if confirmation == "confirm_yes":
        # Логика сохранения профиля в базе данных
        user_data = context.user_data
        # sport = user_data.get('sport')
        # role = user_data.get('role')
        # photo = user_data.get('photo')

        # Пример сохранения в базу данных
        save_to_database(context.user_data)

        await query.edit_message_text("Профиль успешно опубликован!")
    else:
        await query.edit_message_text("Публикация отменена.")

    return ConversationHandler.END  # Завершаем диалог