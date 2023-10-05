import psycopg2

from game.config import get_config_from_env

config = get_config_from_env()
DB_PARAMS = config['storage']


if __name__ == '__main__':
    create_users = """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            nickname VARCHAR(255) UNIQUE NOT NULL,
            credits INT,
            items JSONB
    )
    """
    with psycopg2.connect(**DB_PARAMS) as conn:
        cur = conn.cursor()
        res = cur.execute(create_users)
