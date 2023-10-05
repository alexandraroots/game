from typing import List, Optional

import psycopg2
from config import get_config_from_env
from psycopg2.extras import Json
from pydantic import BaseModel

config = get_config_from_env()
DB_PARAMS = config['storage']


class TransactionData(BaseModel):
    nickname: str
    item_name: str


class User(BaseModel):
    nickname: str
    credits: int
    items: List[str]

    def __str__(self):
        return f"\nИмя пользователя: {self.nickname}\n Баланс: {self.credits}\n Снаряжение: {self.items}"

    def to_dict(self):
        return {
            'nickname': self.nickname,
            'credits': self.credits,
            'items': Json({"items": self.items}),
        }


def get_user(nickname: str) -> tuple[bool, Optional[User]]:
    """
    Получаем игрока из бд. Если игрока с таким именем нет, вернется None
    """
    with psycopg2.connect(**DB_PARAMS) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT * from users where nickname = %s""", (nickname,))
        existing_user = cur.fetchone()

    if existing_user:
        return True, User(
            nickname=nickname,
            credits=int(existing_user[2]),
            items=existing_user[3]['items'],
        )
    else:
        return False, None


def update_user(user: User):
    """
    Обновляем информацию об игроке в бд.
    """
    user_data = user.to_dict()

    update_query = """
            UPDATE users 
            SET credits = %(credits)s, items = %(items)s
            WHERE nickname = %(nickname)s
        """

    with psycopg2.connect(**DB_PARAMS) as conn:
        cur = conn.cursor()
        cur.execute(update_query, user_data)
        conn.commit()
