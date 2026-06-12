import argparse
import sys

from modules.backup import create_backup
from modules.porter import export_data, import_data
from modules.query import execute_query
from modules.seeder import seed_database
from modules.status import show_status


def main():
    parser = argparse.ArgumentParser(
        description="pg-buddy — консольный мультиинструмент для СУБД PostgreSQL (ShopDB)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    subparsers.add_parser(
        "status", help="Показать статус подключения и бизнес-метрики ShopDB"
    )

    query_parser = subparsers.add_parser(
        "query", help="Выполнить произвольный SQL запрос"
    )
    query_parser.add_argument("sql", nargs="?", help="SQL запрос для выполнения")
    query_parser.add_argument("-f", "--file", help="Путь к SQL файлу со скриптом")

    export_parser = subparsers.add_parser(
        "export", help="Экспортировать данные таблицы или запроса в файл"
    )
    export_parser.add_argument("-t", "--table", help="Имя таблицы для экспорта")
    export_parser.add_argument(
        "-q", "--query", help="SQL-запрос, результат которого нужно экспортировать"
    )
    export_parser.add_argument(
        "-f",
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Формат файла (по умолчанию: csv)",
    )
    export_parser.add_argument(
        "-o",
        "--output",
        help="Путь к выходному файлу (по умолчанию: имя_таблицы.формат)",
    )

    import_parser = subparsers.add_parser(
        "import", help="Импортировать данные из CSV или JSON в таблицу"
    )
    import_parser.add_argument(
        "-t", "--table", required=True, help="Имя таблицы, куда импортировать данные"
    )
    import_parser.add_argument(
        "-i", "--input", required=True, help="Путь к файлу CSV или JSON для импорта"
    )

    seed_parser = subparsers.add_parser(
        "seed", help="Заполнить БД демонстрационными данными (Faker)"
    )
    seed_parser.add_argument(
        "-c",
        "--customers",
        type=int,
        default=0,
        help="Количество генерируемых клиентов",
    )
    seed_parser.add_argument(
        "-o", "--orders", type=int, default=0, help="Количество генерируемых заказов"
    )

    backup_parser = subparsers.add_parser(
        "backup", help="Создать резервную копию структуры и данных СУБД"
    )
    backup_parser.add_argument(
        "-o",
        "--output",
        help="Путь к выходному .sql файлу (по умолчанию: backup_ShopDB_дата_время.sql)",
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.command == "status":
        show_status()
    elif args.command == "query":
        execute_query(sql_text=args.sql, file_path=args.file)
    elif args.command == "export":
        export_data(
            table_name=args.table,
            query_text=args.query,
            file_format=args.format,
            output_file=args.output,
        )
    elif args.command == "import":
        import_data(table_name=args.table, file_path=args.input)
    elif args.command == "seed":
        seed_database(num_customers=args.customers, num_orders=args.orders)
    elif args.command == "backup":
        create_backup(output_file=args.output)


if __name__ == "__main__":
    main()
