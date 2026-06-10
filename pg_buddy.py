import argparse
import sys

from modules.status import show_status


def main():
    parser = argparse.ArgumentParser(
        description="pg-buddy — консольный мультиинструмент для СУБД PostgreSQL (ShopDB)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # Команда status
    subparsers.add_parser(
        "status", help="Показать статус подключения и бизнес-метрики ShopDB"
    )

    # Если запуск без аргументов, выводим help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.command == "status":
        show_status()


if __name__ == "__main__":
    main()
