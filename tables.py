from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройка базы данных
DATABASE_URL = "sqlite:///sports_bot.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Модель пользователя
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    sport = Column(String, nullable=False)
    role = Column(String, nullable=False)
    photo_path = Column(String, nullable=True)
    telegram_id = Column(String, nullable=False)

# Инициализация базы данных
def init_db():
    Base.metadata.create_all(bind=engine)

# Сохранение данных пользователя
def save_to_database(user_data):
    db = SessionLocal()
    try:
        # Проверяем, существует ли пользователь с таким telegram_id и sport
        existing_user = db.query(User).filter_by(
            telegram_id=user_data.get("telegram_id"),
            sport=user_data.get("sport")
        ).first()

        if existing_user:
            print("Ошибка: Пользователь уже зарегистрирован в этом виде спорта.")
            return
                
        user = User(
            sport=user_data.get("sports"),
            role=user_data.get("role"),
            photo_path=user_data.get("photo"),
            telegram_id=user_data.get("telegram_id")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Пользователь сохранен в базу данных: {user.id}")
    except Exception as e:
        db.rollback()
        print(f"Ошибка при сохранении пользователя: {e}")
    finally:
        db.close()