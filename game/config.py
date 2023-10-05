def get_config_from_env() -> dict:
    return {
        'storage': {
            'host': 'localhost',
            'port': 5432,
            'database': 'postgres',
            'user': 'postgres',
            'password': 'test',
        },
        'user': {'min_credits': 100, 'max_credits': 10000},
        'equipments': {
            'ship_1': {
                'name': 'ship_1',
                'description': 'Корабль "Ветерок"',
                'price': 1000,
            },
            'ship_2': {
                'name': 'ship_2',
                'description': 'Корабль "Морской Орел"',
                'price': 1500,
            },
            'equipment_1': {
                'name': 'equipment_1',
                'description': 'Снаряжение "Магическая сфера"',
                'price': 200,
            },
            'equipment_2': {
                'name': 'equipment_2',
                'description': 'Снаряжение "Красная Пушка"',
                'price': 300,
            },
            'treasure_map': {
                'name': 'treasure_map',
                'description': 'Сокровищница',
                'price': 500,
            },
            'compass': {
                'name': 'compass',
                'description': 'Компас "Звездное Руководство"',
                'price': 50,
            },
            'spyglass': {
                'name': 'spyglass',
                'description': 'Спутник "Око Предвидения"',
                'price': 100,
            },
            'rum_bottle': {
                'name': 'rum_bottle',
                'description': 'Бутылка рома',
                'price': 10,
            },
            'tropical_fruit': {
                'name': 'tropical_fruit',
                'description': 'Тропический фрукт',
                'price': 5,
            },
            'treasure_chest': {
                'name': 'treasure_chest',
                'description': 'Сундук с сокровищами',
                'price': 10000,
            },
        },
    }
