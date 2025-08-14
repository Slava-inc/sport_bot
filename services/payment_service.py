import yookassa
from config import settings

class PaymentService:
    def __init__(self):
        yookassa.Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
        yookassa.Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    def create_payment(self, user_id: int):
        payment = yookassa.Payment.create({
            "amount": {
                "value": "300.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://yourboturl.com/success"
            },
            "capture": True,
            "description": f"PRO subscription for user {user_id}"
        })
        
        return payment.confirmation.confirmation_url, payment.id
    
    def check_payment_status(self, payment_id: str):
        payment = yookassa.Payment.find_one(payment_id)
        return payment.status