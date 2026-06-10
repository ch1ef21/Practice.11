import os

from rich.console import Console
from rich.table import Table

from .db_client import get_connection

console = Console()


def execute_query(sql_text=None, file_path=None):
    if file_path:
        if not os.path.exists(file_path):
            console.print(f"[red]Ошибка: Файл '{file_path}' не найден.[/red]")
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                sql_text = f.read()
        except Exception as e:
            console.print(f"[red]Ошибка при чтении файла {file_path}: {e}[/red]")
            return

    if not sql_text or not sql_text.strip():
        console.print("[yellow]Предупреждение: Пустой SQL запрос.[/yellow]")
        return

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(sql_text)

        if cur.description:
            colnames = [desc[0] for desc in cur.description]
            rows = cur.fetchall()

            if not rows:
                console.print(
                    "[yellow]Запрос выполнен успешно, но не вернул строк.[/yellow]"
                )
                cur.close()
                conn.close()
                return

            table = Table(title="Результат запроса")
            for col in colnames:
                table.add_column(col, style="cyan")

            for row in rows:
                table.add_row(
                    *(str(item) if item is not None else "NULL" for item in row)
                )

            console.print(table)
            console.print(f"[green]Успешно получено строк: {len(rows)}[/green]")
        else:
            conn.commit()
            console.print(
                f"[green]Запрос выполнен успешно. Затронуто строк: {cur.rowcount}[/green]"
            )

        cur.close()
        conn.close()
    except Exception as e:
        console.print(f"[red]Ошибка выполнения SQL запроса: {e}[/red]")
