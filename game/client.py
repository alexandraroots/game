import requests
from user import User


class UserState:
    LOGIN = "LOGIN"
    GAME_SESSION = "GAME_SESSION"
    LOGOUT = "LOGOUT"
    BUY = "BUY"
    SELL = "SELL"
    SHOP = "SHOP"


class GameClient:
    SERVER_URL = "http://0.0.0.0:8000"

    ACTIONS = {
        0: "\nДоступные действия:",
        1: "1. Просмотр баланса",
        2: "2. Просмотр магазина снаряжения",
        3: "3. Просмотр лчиного снаряжения",
        4: "4. Купить предмет",
        5: "5. Продать предмет",
        6: "6. Выход",
    }

    def __init__(self):
        self.user = None
        self.state = UserState.LOGIN
        self.equipments = None

    def login(self):
        """
        Логиним пользователя по его никнейму
        """
        while not self.user:
            nickname = input("Введите ваш никнейм: ")
            response = requests.get(
                GameClient.SERVER_URL + f"/login/{nickname}"
            )

            if response.status_code == 200:
                user_data = response.json()
                self.user = User(**user_data)
                print(self.user)
            else:
                print(f"Произошла ошибка: {response.status_code}")

        self.state = UserState.GAME_SESSION

    def logout(self):
        """
        Разлогиниваем пользователя.
        Переводим в состояние выбора нового пользователя
        """
        self.user = None
        self.equipments = None
        self.state = UserState.LOGOUT

    def view_balance(self):
        """
        Просмотр текущего баланса на аккаунте игрока
        """
        print(f"Баланс аккаунта {self.user.credits} кредитов")

    def view_all_equipments(self):
        """
        Просмотр всего имущества, которое есть в магазине
        """
        response = requests.get(GameClient.SERVER_URL + f"/shop")
        if response.status_code == 200:
            self.equipments = response.json()
        else:
            print(
                f"Произошла ошибка получения equipments: {response.status_code}"
            )

        self.state = UserState.SHOP
        print("Всевозможное имущество:")
        for name, obj in self.equipments.items():
            print(f"{obj['name']}: {obj['price']} кредитов")
        print('\n')

        while self.state == UserState.SHOP:
            item_name = input(
                "Введите название предмета, о котором хотите узнать подробнее или 0, чтобы выйти из режима магазина: "
            )

            if item_name == '0':
                self.state = UserState.GAME_SESSION
                break

            found_item = self.equipments.get(item_name)

            if found_item is None:
                print("Такого товара не существует")
            else:
                print(f"{found_item['name']}: {found_item['price']} кредитов")
                print(found_item['description'])

    def view_equipments(self):
        """
        Просмотр всего имущества, которое есть у игрока
        """
        items = self.user.items
        if items:
            print(f"Имущество на аккаунте {self.user.nickname}:")
            for item in self.user.items:
                print(item)
        else:
            print("Имущества нет. Самое время закупиться в магазине!")

    def buy(self):
        """
        Покупаем имущество.
        Клиент проверяет ограничения на покупку:
            - наличие товара у игрока
            - наличие выбранного товара в магазине
        При выполнении всех условий, запрос на покупку идет на GameServer
        """
        self.state = UserState.BUY

        while self.state == UserState.BUY:
            item_name = input(
                "Введите название предмета, который вы хотите купить, или 0, чтобы выйти из режима попкупки: "
            )
            if item_name == '0':
                self.state = UserState.GAME_SESSION
                break

            found_item = self.equipments.get(item_name)

            if found_item is None:
                print("Такого товара не существует")
            elif item_name in self.user.items:
                print(
                    "У вас уже есть этот товар. Вы не можете купить его повторно"
                )
            else:
                self.server_request("/buy-item", item_name)

    def sell_item(self):
        """
        Продаем имущество.
        Клиент проверяет ограничения на покупку:
            - наличие товара у игрока
            - наличие выбранного товара в магазине
        При выполнении всех условий, запрос на продажу идет на GameServer
        """
        self.state = UserState.SELL
        while self.state == UserState.SELL:
            item_name = input(
                "Введите название предмета, который хотите продать, или 0, чтобы выйти из режима продажи: "
            )
            if item_name == '0':
                self.state = UserState.GAME_SESSION
                break

            if item_name in self.user.items:
                self.server_request("/sell-item", item_name)

            else:
                print(f"У вас нет товара '{item_name}' для продажи")
                self.state = UserState.GAME_SESSION

    def session(self):
        """
        Основная сессия взаимодействия игрока с магазином/балансом/своим имуществом
        """
        GameClient.actions()

        while self.state == UserState.GAME_SESSION:
            choice = input("Выберите действие (1-6) или 0 для справки: ")
            if choice == '0':
                GameClient.actions()
            if choice == '1':
                self.view_balance()
            elif choice == '2':
                self.view_all_equipments()
            elif choice == '3':
                self.view_equipments()
            elif choice == '4':
                self.buy()
            elif choice == '5':
                self.sell_item()
            elif choice == '6':
                self.logout()
            else:
                print(
                    "Неверный выбор. Пожалуйста, выберите действие от 1 до 6."
                )

    def server_request(self, endpoint: str, item_name: str):
        transaction_data = {
            "nickname": self.user.nickname,
            "item_name": item_name,
        }

        response = requests.post(
            GameClient.SERVER_URL + endpoint, json=transaction_data
        )
        if response.status_code == 200:
            resp = response.json()
            print(resp['message'])
            self.user.credits = int(resp['user_credits'])
            self.user.items = resp['user_items']
            self.state = UserState.GAME_SESSION
        else:
            print("Oooops! Что-то пошло не так, попробуйте позже")

    @staticmethod
    def actions():
        for _, value in GameClient.ACTIONS.items():
            print(value)


if __name__ == '__main__':
    client = GameClient()
    while True:
        client.login()
        client.session()
