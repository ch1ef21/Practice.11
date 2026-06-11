import psycopg2
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .db_client import get_connection

console = Console()


def show_status():
    try:
        conn = get_connection()
        cur = conn.cursor()
    except Exception:
        return

    cur.execute("SELECT version();")
    db_version = cur.fetchone()[0]

    cur.execute("SELECT current_database();")
    db_name = cur.fetchone()[0]

    cur.execute("SELECT pg_size_pretty(pg_database_size(current_database()));")
    db_size = cur.fetchone()[0]

    console.print(
        Panel.fit(
            f"[bold green]Подключено к СУБД PostgreSQL![/bold green]\n"
            f"[bold]База данных:[/bold] {db_name}\n"
            f"[bold]Размер базы данных:[/bold] {db_size}\n"
            f"[bold]Версия сервера:[/bold] {db_version.split(',')[0]}",
            title="[bold blue]Статус подключения[/bold blue]",
        )
    )

    try:
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """)
        tables = [row[0] for row in cur.fetchall()]

        table_stats = []
        for table in tables:
            cur.execute(f"SELECT COUNT(*) FROM {table};")
            row_count = cur.fetchone()[0]

            cur.execute(f"SELECT pg_size_pretty(pg_total_relation_size('{table}'));")
            table_size = cur.fetchone()[0]

            table_stats.append((table, row_count, table_size))

        table_stats.sort(key=lambda x: x[1], reverse=True)

        rich_table = Table(title="\n Статистика таблиц базы данных")
        rich_table.add_column("Имя таблицы", style="cyan")
        rich_table.add_column("Количество строк", justify="right", style="magenta")
        rich_table.add_column("Размер на диске", justify="right", style="green")

        for name, count, size in table_stats:
            rich_table.add_row(name, f"{count:,}", size)

        console.print(rich_table)

    except Exception as e:
        console.print(f"[red]Не удалось получить статистику таблиц: {e}[/red]")

    console.print("\n[bold yellow Аналитика интернет-магазина (ShopDB):[/bold yellow]")
    try:
        cur.execute(
            "SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM orders WHERE status != 'Отменен';"
        )
        order_count, total_revenue = cur.fetchone()

        cur.execute("SELECT COUNT(*) FROM customers;")
        customer_count = cur.fetchone()[0]

        cur.execute(
            "SELECT name, stock, price FROM products WHERE stock < 15 ORDER BY stock ASC LIMIT 3;"
        )
        low_stock = cur.fetchall()

        metric_table = Table(show_header=False, box=None)
        metric_table.add_row("[bold]Всего клиентов:[/bold]", f"{customer_count} чел.")
        metric_table.add_row(
            "[bold]Активных заказов (кроме отмененных):[/bold]", f"{order_count} шт."
        )
        metric_table.add_row(
            "[bold]Общая выручка:[/bold]",
            f"[bold green]{total_revenue:,.2f} руб.[/bold green]",
        )

        console.print(metric_table)

        if low_stock:
            low_stock_table = Table(
                title="\n Внимание! Товары на исходе (критический остаток)"
            )
            low_stock_table.add_column("Товар", style="yellow")
            low_stock_table.add_column(
                "Остаток на складе", justify="right", style="red"
            )
            low_stock_table.add_column("Цена", justify="right", style="green")

            for name, stock, price in low_stock:
                low_stock_table.add_row(name, str(stock), f"{price:,.2f} руб.")
            console.print(low_stock_table)

    except Exception as e:
        console.print(
            f"[red]Не удалось получить бизнес-метрики. Проверьте структуру таблиц: {e}[/red]"
        )

    cur.close()
    conn.close()
