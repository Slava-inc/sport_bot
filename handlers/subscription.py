from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes
)
from services.payment_service import PaymentService

async def buy_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка покупки подписки."""
    payment_service = PaymentService()
    payment_url, payment_id = payment_service.create_payment(update.effective_user.id)

    await update.message.reply_text(
        f"Для покупки подписки перейдите по ссылке: {payment_url}"
    )

    # Логика проверки статуса платежа
    status = payment_service.check_payment_status(payment_id)
    if status == "succeeded":
        await update.message.reply_text("Подписка успешно активирована!")
    else:
        await update.message.reply_text("Ошибка при оплате. Попробуйте снова.")

# Хендлер для покупки подписки
subscription_handler = CommandHandler('subscribe', buy_subscription)