from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.main.api.configs.config import Config

engine = create_engine(Config.fetch('dataBaseUrl'), echo=False)
SessionLocal = sessionmaker(bind=engine)
