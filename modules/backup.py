import datetime
import os
from decimal import Decimal

from rich.console import Console

from .db_client import get_connection

console = Console()


def create_backup(output_file=None):
    if not output_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"backup_ShopDB_{timestamp}.sql"

    try:
        conn = get_connection()
        cur = conn.cursor()
    except Exception:
        return

    try:
        console.print(f"[blue]начало резервного копирования базы данных...[/blue]")

        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY
                CASE table_name
                    WHEN 'categories' THEN 1
                    WHEN 'products' THEN 2
                    WHEN 'customers' THEN 3
                    WHEN 'orders' THEN 4
                    WHEN 'order_items' THEN 5
                    ELSE 6
                END;
        """)
        tables = [row[0] for row in cur.fetchall()]

        if not tables:
            console.print(
                "[yellow]в базе данных нет таблиц для резервного копирования.[/yellow]"
            )
            cur.close()
            conn.close()
            return

        backup_lines = [
            "-- ==========================================",
            f"-- резервная копия базы данных ShopDB",
            f"-- создано утилитой pg-buddy",
            f"-- дата создания: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "-- ==========================================\n",
            "SET session_replication_role = 'replica';\n",
        ]

        for table in reversed(tables):
            backup_lines.append(f"DROP TABLE IF EXISTS {table} CASCADE;")
        backup_lines.append("")

        for table in tables:
            console.print(f"Экспорт таблицы [cyan]{table}[/cyan]...")

            cur.execute(
                """
                SELECT column_name, data_type, character_maximum_length, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = %s AND table_schema = 'public'
                ORDER BY ordinal_position;
            """,
                (table,),
            )
            columns = cur.fetchall()

            cur.execute(
                """
                SELECT kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                  AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type = 'PRIMARY KEY' AND tc.table_name = %s;
            """,
                (table,),
            )
            pks = [row[0] for row in cur.fetchall()]

            ddl = f"CREATE TABLE {table} (\n"
            col_definitions = []

            for col_name, data_type, char_len, is_null, col_default in columns:
                col_type = data_type.upper()
                if col_type == "CHARACTER VARYING" and char_len:
                    col_type = f"VARCHAR({char_len})"
                elif col_type == "NUMERIC":
                    col_type = (
                        "NUMERIC(12, 2)"
                        if table in ("orders", "products", "order_items")
                        else "NUMERIC"
                    )

                is_serial = False
                if (
                    col_default
                    and "nextval" in col_default
                    and col_type in ("INTEGER", "BIGINT")
                ):
                    col_type = "SERIAL" if col_type == "INTEGER" else "BIGSERIAL"
                    is_serial = True

                definition = f"    {col_name} {col_type}"

                if col_name in pks and len(pks) == 1:
                    definition += " PRIMARY KEY"
                elif is_null == "NO":
                    definition += " NOT NULL"

                if col_default and not is_serial:
                    clean_default = col_default.split("::")[0]
                    definition += f" DEFAULT {clean_default}"

                col_definitions.append(definition)

            if len(pks) > 1:
                pks_str = ", ".join(pks)
                col_definitions.append(f"    PRIMARY KEY ({pks_str})")

            ddl += ",\n".join(col_definitions)
            ddl += "\n);"

            backup_lines.append(f"-- Структура таблицы {table}")
            backup_lines.append(ddl)
            backup_lines.append("")

            cur.execute(f"SELECT * FROM {table};")
            rows = cur.fetchall()

            if rows:
                col_names_list = [col[0] for col in columns]
                col_names_str = ", ".join(col_names_list)

                backup_lines.append(f"-- Данные таблицы {table}")
                for row in rows:
                    values_formatted = []
                    for val in row:
                        if val is None:
                            values_formatted.append("NULL")
                        elif isinstance(val, (int, float, Decimal)):
                            values_formatted.append(str(val))
                        elif isinstance(val, bool):
                            values_formatted.append("TRUE" if val else "FALSE")
                        elif isinstance(val, (datetime.datetime, datetime.date)):
                            values_formatted.append(f"'{val.isoformat()}'")
                        else:
                            escaped_str = str(val).replace("'", "''")
                            values_formatted.append(f"'{escaped_str}'")

                    vals_str = ", ".join(values_formatted)
                    backup_lines.append(
                        f"INSERT INTO {table} ({col_names_str}) VALUES ({vals_str});"
                    )
                backup_lines.append("")

        backup_lines.append("SET session_replication_role = 'origin';")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(backup_lines))

        console.print(
            f"[green]Резервная копия успешно создана и сохранена в файл: [bold]{output_file}[/bold][/green]"
        )

        cur.close()
        conn.close()
    except Exception as e:
        console.print(f"[red]Ошибка при создании резервной копии: {e}[/red]")
