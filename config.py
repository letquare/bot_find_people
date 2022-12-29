import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')


bot = Bot(token=API_TOKEN)
dp = Dispatcher()


class PostgresDsl(BaseSettings):
    dbname: str = Field(env='DB_NAME')
    user: str = Field(env='DB_USER')
    password: str = Field(env='DB_PASSWORD')
    host: str = Field(env='DB_HOST')
    port: str = Field(env='DB_PORT')


# POSTGRES = PostgresDsl()
