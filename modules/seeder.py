import random

from faker import Faker
from rich.console import Console

from .db_client import get_connection

console = Console()


def seed_database(num_customers=0, num_orders=0):
    fake = Faker("ru_RU")

    if num_customers == 0 and num_orders == 0:
        console.print(
            "[yellow]Укажите количество генерируемых данных: --customers N и/или --orders M[/yellow]"
        )
        return

    try:
        conn = get_connection()
        cur = conn.cursor()
    except Exception:
        return

    if num_customers > 0:
        console.print(f"[blue]Генерация {num_customers} клиентов...[/blue]")
        customers_data = []
        for _ in range(num_customers):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            phone = fake.phone_number()[:20]  # обрезаем до длины поля
            address = fake.address().replace("\n", ", ")
            customers_data.append((first_name, last_name, email, phone, address))

        try:
            cur.executemany(
                "INSERT INTO customers (first_name, last_name, email, phone, address) VALUES (%s, %s, %s, %s, %s);",
                customers_data,
            )
            conn.commit()
            console.print(
                f"[green]Успешно сгенерировано и вставлено клиентов: {num_customers}[/green]"
            )
        except Exception as e:
            conn.rollback()
            console.print(f"[red]Ошибка при генерации клиентов: {e}[/red]")
            cur.close()
            conn.close()
            return

    if num_orders > 0:
        console.print(f"[blue]Генерация {num_orders} случайных заказов...[/blue]")

        cur.execute("SELECT id FROM customers;")
        customer_ids = [row[0] for row in cur.fetchall()]

        if not customer_ids:
            console.print(
                "[red]Ошибка: В базе нет клиентов. Сначала сгенерируйте клиентов (--customers N)![/red]"
            )
            cur.close()
            conn.close()
            return

        cur.execute("SELECT id, price FROM products;")
        products = cur.fetchall()  # список кортежей (id, price)

        if not products:
            console.print(
                "[red]Ошибка: В таблице 'products' нет товаров. Невозможно создать заказы.[/red]"
            )
            cur.close()
            conn.close()
            return

        statuses = ["Новый", "Оплачен", "Доставляется", "Доставлен", "Отменен"]
        orders_created = 0

        try:
            for _ in range(num_orders):
                customer_id = random.choice(customer_ids)
                status = random.choice(statuses)
                created_at = fake.date_time_between(start_date="-30d", end_date="now")

                cur.execute(
                    "INSERT INTO orders (customer_id, status, total_amount, created_at) VALUES (%s, %s, 0, %s) RETURNING id;",
                    (customer_id, status, created_at),
                )
                order_id = cur.fetchone()[0]

                num_items = random.randint(1, 4)
                chosen_products = random.sample(products, min(num_items, len(products)))

                total_amount = 0
                for prod_id, prod_price in chosen_products:
                    qty = random.randint(1, 3)
                    item_price = float(prod_price)
                    total_amount += item_price * qty

                    cur.execute(
                        "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s);",
                        (order_id, prod_id, qty, item_price),
                    )

                cur.execute(
                    "UPDATE orders SET total_amount = %s WHERE id = %s;",
                    (total_amount, order_id),
                )
                orders_created += 1

            conn.commit()
            console.print(
                f"[green]Успешно сгенерировано заказов: {orders_created}[/green]"
            )

        except Exception as e:
            conn.rollback()
            console.print(f"[red]Ошибка при генерации заказов: {e}[/red]")

    cur.close()
    conn.close()
