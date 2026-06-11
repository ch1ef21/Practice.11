import csv
import json
import os

from rich.console import Console

from .db_client import get_connection

console = Console()


def export_data(table_name=None, query_text=None, file_format="csv", output_file=None):
    if not table_name and not query_text:
        console.print(
            "[red]Ошибка: Укажите либо имя таблицы (--table), либо SQL-запрос (--query) для экспорта.[/red]"
        )
        return

    sql = query_text if query_text else f"SELECT * FROM {table_name};"

    if not output_file:
        name = table_name if table_name else "export_result"
        output_file = f"{name}.{file_format.lower()}"

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql)

        if not cur.description:
            console.print(
                "[red]Ошибка: Запрос не возвращает данные (нет колонок). Экспорт невозможен.[/red]"
            )
            cur.close()
            conn.close()
            return

        colnames = [desc[0] for desc in cur.description]
        rows = cur.fetchall()

        if not rows:
            console.print(
                "[yellow]Запрос вернул 0 строк. Создается пустой файл с заголовками.[/yellow]"
            )

        file_format = file_format.lower()

        if file_format == "csv":
            with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(colnames)
                writer.writerows(rows)
            console.print(
                f"[green]Данные успешно экспортированы в CSV файл: [bold]{output_file}[/bold] (Строк: {len(rows)})[/green]"
            )

        elif file_format == "json":
            data = []
            for row in rows:
                row_dict = {}
                for col, val in zip(colnames, row):
                    if hasattr(val, "isoformat"):
                        val = val.isoformat()
                    elif (
                        hasattr(val, "to_eng_string") or type(val).__name__ == "Decimal"
                    ):
                        val = float(val)
                    row_dict[col] = val
                data.append(row_dict)

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            console.print(
                f"[green]Данные успешно экспортированы в JSON файл: [bold]{output_file}[/bold] (Записей: {len(rows)})[/green]"
            )

        else:
            console.print(
                f"[red]Ошибка: Неподдерживаемый формат '{file_format}'. Используйте 'csv' или 'json'.[/red]"
            )

        cur.close()
        conn.close()
    except Exception as e:
        console.print(f"[red]Ошибка при экспорте данных: {e}[/red]")


def import_data(table_name, file_path):
    if not os.path.exists(file_path):
        console.print(f"[red]Ошибка: Файл '{file_path}' для импорта не найден.[/red]")
        return

    ext = os.path.splitext(file_path)[1].lower()

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';"
        )
        db_cols = [row[0] for row in cur.fetchall()]

        if not db_cols:
            console.print(
                f"[red]Ошибка: Таблица '{table_name}' не найдена в базе данных.[/red]"
            )
            cur.close()
            conn.close()
            return

        records_inserted = 0

        if ext == ".csv":
            with open(file_path, "r", encoding="utf-8-sig") as f:
                sample = f.read(2048)
                f.seek(0)
                delimiter = ";" if ";" in sample else ","
                reader = csv.reader(f, delimiter=delimiter)

                header = next(reader)
                valid_cols = [col.strip() for col in header if col.strip() in db_cols]

                if not valid_cols:
                    console.print(
                        "[red]Ошибка: Ни одна колонка из CSV файла не совпадает с колонками таблицы БД.[/red]"
                    )
                    cur.close()
                    conn.close()
                    return

                col_indices = [header.index(col) for col in valid_cols]

                cols_str = ", ".join(valid_cols)
                placeholders = ", ".join(["%s"] * len(valid_cols))
                insert_query = (
                    f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders});"
                )

                for row in reader:
                    if not row:
                        continue
                    val_to_insert = [
                        row[idx].strip() if row[idx].strip() != "" else None
                        for idx in col_indices
                    ]
                    cur.execute(insert_query, val_to_insert)
                    records_inserted += 1

        elif ext == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list):
                console.print(
                    "[red]Ошибка: JSON файл для импорта должен содержать список объектов.[/red]"
                )
                cur.close()
                conn.close()
                return

            if len(data) == 0:
                console.print("[yellow]Предупреждение: JSON файл пуст.[/yellow]")
                cur.close()
                conn.close()
                return

            for idx, item in enumerate(data):
                if not isinstance(item, dict):
                    console.print(
                        f"[red]Ошибка: Элемент списка под индексом {idx} не является объектом.[/red]"
                    )
                    continue

                valid_cols = [col for col in item.keys() if col in db_cols]
                if not valid_cols:
                    continue

                cols_str = ", ".join(valid_cols)
                placeholders = ", ".join(["%s"] * len(valid_cols))
                insert_query = (
                    f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders});"
                )

                val_to_insert = [item[col] for col in valid_cols]
                cur.execute(insert_query, val_to_insert)
                records_inserted += 1
        else:
            console.print(
                f"[bold red]Ошибка:[/bold red] Неподдерживаемый тип файла '{ext}'. Используйте файлы .csv или .json."
            )
            cur.close()
            conn.close()
            return

        conn.commit()
        console.print(
            f"[green]Импорт завершен! Успешно добавлено строк в таблицу '{table_name}': {records_inserted}[/green]"
        )
        cur.close()
        conn.close()

    except Exception as e:
        console.print(f"[red]Ошибка при импорте данных: {e}[/red]")
