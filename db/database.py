import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./f1_wiki.db")

# SQLite потребує цього аргументу для роботи в багатопотоковому режимі FastAPI
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
# Фабрика сесій — кожен запит отримує свою сесію
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Базовий клас для всіх ORM-моделей
Base = declarative_base()


def get_db():
    # Dependency для FastAPI: відкриває сесію і закриває після запиту
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from db import models  # noqa: F401 — ensures models are registered before create_all
    # Створює всі таблиці в БД за визначеними моделями
    Base.metadata.create_all(bind=engine)
