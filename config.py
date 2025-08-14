from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Настройки приложения
    BOT_TOKEN: str
    DATABASE_URL: str

    class Config:
        env_file = "env_vars"  # Укажите файл с переменными окружения
        env_file_encoding = "utf-8"

# Создание экземпляра настроек
settings = Settings()