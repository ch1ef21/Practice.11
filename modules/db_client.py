import os
import json
import psycopg2

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'connection.json')

def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Файл конфигурации не найден по пути: {CONFIG_PATH}")
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_connection():
    config = load_config()
    try:
        conn = psycopg2.connect(
            host=config.get('host', 'localhost'),
            port=config.get('port', 5432),
            database=config.get('database', 'ShopDB'),
            user=config.get('user', 'postgres'),
            password=config.get('password', '')
        )
        return conn
    except psycopg2.OperationalError as e:
        print("\n[!] Ошибка подключения к базе данных PostgreSQL!")
        print("Пожалуйста, проверьте:")
        print("  1. Запущен ли сервер PostgreSQL локально.")
        print("  2. Правильность логина/пароля в config/connection.json.")
        print(f"Детали ошибки: {e}\n")
        raise e
