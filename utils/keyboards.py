from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class Keyboards:
    @staticmethod
    def get_main_menu():
        """Основное меню бота."""
        keyboard = [
            [InlineKeyboardButton("Регистрация", callback_data="menu_register")],
            [InlineKeyboardButton("Поиск партнера", callback_data="menu_find_partner")],
            [InlineKeyboardButton("Предложения игр", callback_data="menu_game_proposals")],
            [InlineKeyboardButton("Туры", callback_data="menu_tours")],
            [InlineKeyboardButton("Внести счет", callback_data="menu_submit_score")],
            [InlineKeyboardButton("Купить подписку", callback_data="menu_subscribe")],
            [InlineKeyboardButton("Моя анкета", callback_data="menu_my_profile")],
            [InlineKeyboardButton("Другие разделы", callback_data="menu_other_sections")]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_sport_types():
        """Клавиатура выбора вида спорта."""
        sports = [
            "Большой теннис", "Сквош", "Настольный теннис",
            "Бадминтон", "Футбол", "Баскетбол", "Волейбол"
        ]
        keyboard = [[InlineKeyboardButton(sport, callback_data=f"sport_{sport}")] for sport in sports]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_role_selection():
        """Клавиатура выбора роли."""
        roles = ["Игрок", "Тренер"]
        keyboard = [[InlineKeyboardButton(role, callback_data=f"role_{role}")] for role in roles]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_game_type():
        """Клавиатура выбора типа игры."""
        game_types = ["Одиночная игра", "Парная игра", "Микст", "Тренировка"]
        keyboard = [[InlineKeyboardButton(game_type, callback_data=f"game_type_{game_type}")] for game_type in game_types]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_payment_type():
        """Клавиатура выбора оплаты корта."""
        payment_types = [
            "Пополам",
            "Я оплачиваю корт",
            "Соперник оплачивает корт",
            "Проигравший оплачивает корт"
        ]
        keyboard = [[InlineKeyboardButton(payment_type, callback_data=f"payment_{payment_type}")] for payment_type in payment_types]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_confirmation_buttons():
        """Клавиатура подтверждения действия."""
        keyboard = [
            [InlineKeyboardButton("Да", callback_data="confirm_yes")],
            [InlineKeyboardButton("Нет", callback_data="confirm_no")]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_partner_search_filters():
        """Клавиатура фильтров поиска партнера."""
        filters = ["По городу", "По уровню игры", "По времени игры", "По типу игры"]
        keyboard = [[InlineKeyboardButton(filter_option, callback_data=f"filter_{filter_option}")] for filter_option in filters]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_subscription_plans():
        """Клавиатура выбора подписки."""
        keyboard = [
            [InlineKeyboardButton("Купить подписку за 300₽", callback_data="subscribe_buy")],
            [InlineKeyboardButton("Подробнее о подписке", callback_data="subscribe_details")]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_back_button(callback_data="back"):
        """Кнопка 'Назад'."""
        keyboard = [[InlineKeyboardButton("Назад", callback_data=callback_data)]]
        return InlineKeyboardMarkup(keyboard)