from src.logger import setup_logging
from src.views import compile_to_json

logger = setup_logging()


def main():
    file_path = 'operations.xls'
    user_settings = 'user_settings.json'
    # 13.08.2021 20:15:00
    # 18.01.2019 20:15:00

    user_input = input('ДД.ММ.ГГГГ HH:MM:SS -> ')
    compile_to_json(file_path, user_input, user_settings)
    print(f'Файл "user_information_set.json" создан в папке data')


if __name__ == '__main__':
    main()
