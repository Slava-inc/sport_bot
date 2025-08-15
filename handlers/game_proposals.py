from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from utils.keyboards import Keyboards
from database.models import SessionLocal, GameProposal, User

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
    session = SessionLocal()
    try:
        user_data = context.user_data
        proposal = GameProposal(
            user_id=context.user_data.get("user_id"),
            city=user_data.get("city"),
            district=user_data.get("district"),
            date=user_data.get("date"),
            time=user_data.get("time"),
            game_type=user_data.get("game_type"),
            payment=user_data.get("payment"),
            comment=user_data.get("comment"),
            published=True,
        )
        session.add(proposal)
        session.commit()
        await update.message.reply_text("Предложение игры успешно создано!")
    except Exception as e:
        session.rollback()
        await update.message.reply_text(f"Ошибка при создании предложения: {e}")
    finally:
        session.close()
    return ConversationHandler.END

async def filter_game_proposals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Фильтрация предложений игр."""
    session = SessionLocal()
    sport = context.user_data.get("sport")
    level = context.user_data.get("level")
    time = context.user_data.get("time")

    proposals = session.query(GameProposal).join(User).filter(
        User.sport == sport,
        User.level.between(level - 1, level + 1),
        GameProposal.time.like(f"%{time}%")
    ).all()

    if proposals:
        for proposal in proposals:
            await update.message.reply_text(
                f"{proposal.user.first_name} {proposal.user.last_name}\n"
                f"Город: {proposal.city}\n"
                f"Время: {proposal.time}\n"
                f"Тип игры: {proposal.game_type}\n"
                f"Комментарий: {proposal.comment}"
            )
    else:
        await update.message.reply_text("По вашему запросу предложения не найдены.")
    session.close()


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