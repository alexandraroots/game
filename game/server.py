import random

import psycopg2
from fastapi import FastAPI

from game.config import get_config_from_env
from game.user import User, get_user, update_user, TransactionData

config = get_config_from_env()
STORAGE = config['storage']
DB_PARAMS = config['storage']

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в сервер игры"}


@app.get("/shop")
def shop():
    return config['equipments']


@app.get("/login/{nickname}", response_model=User)
def login(nickname: str):
    flag, user = get_user(nickname)

    if flag:
        return user
    else:
        random_credits = random.randint(
            config['user']['min_credits'], config['user']['max_credits']
        )
        new_user = User(nickname=nickname, credits=random_credits, items=[])

        user_data = new_user.to_dict()

        insert_query = """
            INSERT INTO users (nickname, credits, items)
            VALUES (%(nickname)s, %(credits)s, %(items)s)
        """

        with psycopg2.connect(**DB_PARAMS) as conn:
            cur = conn.cursor()
            cur.execute(insert_query, user_data)
            conn.commit()

        return new_user


@app.post("/buy-item")
async def buy_item(data: TransactionData):
    flag, user = get_user(data.nickname)

    item_name = data.item_name

    item = config['equipments'][item_name]

    if user.credits >= item['price']:
        user.credits -= item['price']
        user.items.append(item_name)

        update_user(user)

        return {
            "message": f"Товар '{item_name}' куплен за {item['price']} кредитов",
            "user_credits": user.credits,
            "user_items": user.items,
        }
    else:
        return {
            "message": "У вас недостаточно средств для покупки",
            "user_credits": user.credits,
            "user_items": user.items,
        }


@app.post("/sell-item")
async def sell_item(data: TransactionData):
    flag, user = get_user(data.nickname)

    item_name = data.item_name

    item = config['equipments'][item_name]

    user.credits += item['price']
    user.items.remove(item_name)

    update_user(user)

    return {
        "message": f"Товар '{item_name}' продан за {item['price']} кредитов",
        "user_credits": user.credits,
        "user_items": user.items,
    }
