import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor

from bot_find_people.config import PostgresDsl


from dotenv import load_dotenv
load_dotenv()


class PostgresExtration:

    def __init__(self, config: PostgresDsl):

        self.config = config
        self.connect = self._connection()

    def _connection(self) -> connection:
        """Создает соединение с Postgres"""
        return psycopg2.connect(**self.config.dict(), cursor_factory=RealDictCursor)

    def extract(self, name_table, _from):
        """Получение данных из Postgres"""
        with self.connect.cursor() as cursor:
            cursor.execute('SELECT * from users limit;')
            cur = cursor.fetchall()
            for records in cur:
                yield records

    def add_user(self, data):
        pass