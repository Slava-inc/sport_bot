from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Настройка базы данных (SQLite в данном примере)
DATABASE_URL = "sqlite:///sports_bot.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Модель пользователя
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)  # Уникальный ID Telegram
    sport = Column(String, nullable=False)  # Вид спорта
    role = Column(String, nullable=False)  # Роль: Игрок или Тренер
    photo_path = Column(String, nullable=True)  # Путь к фото профиля
    level = Column(Float, default=1.0)  # Уровень игрока (по умолчанию 1.0)
    rating_points = Column(Integer, default=500)  # Рейтинговые очки
    subscription = Column(Boolean, default=False)  # Подписка (PRO или нет)

# Модель предложения игры
class GameProposal(Base):
    __tablename__ = "game_proposals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Связь с пользователем
    city = Column(String, nullable=False)  # Город
    district = Column(String, nullable=True)  # Район
    date = Column(DateTime, nullable=False)  # Дата игры
    time = Column(String, nullable=False)  # Время игры
    game_type = Column(String, nullable=False)  # Тип игры (Одиночная, Парная, Микст, Тренировка)
    payment = Column(String, nullable=False)  # Оплата (Пополам, Я оплачиваю корт и т.д.)
    comment = Column(String, nullable=True)  # Комментарий
    published = Column(Boolean, default=True)  # Опубликовано ли предложение

# Модель тура
class Tour(Base):
    __tablename__ = "tours"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Связь с пользователем
    city = Column(String, nullable=False)  # Город
    district = Column(String, nullable=True)  # Район
    start_date = Column(DateTime, nullable=False)  # Начало поездки
    end_date = Column(DateTime, nullable=False)  # Конец поездки
    game_type = Column(String, nullable=False)  # Тип игры
    payment = Column(String, nullable=False)  # Оплата
    comment = Column(String, nullable=True)  # Комментарий

# Модель результата матча
class MatchResult(Base):
    __tablename__ = "match_results"
    id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Первый игрок
    player2_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Второй игрок
    score = Column(String, nullable=False)  # Счет
    game_type = Column(String, nullable=False)  # Тип игры
    timestamp = Column(DateTime, nullable=False)  # Время матча
    photo = Column(String, nullable=True)  # Фото матча
    video = Column(String, nullable=True)  # Видео матча

# Инициализация таблиц
def init_db():
    Base.metadata.create_all(bind=engine)