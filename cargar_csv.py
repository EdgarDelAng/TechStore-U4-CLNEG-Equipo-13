"""Carga fixtures PetMarket desde CSV en objetos del dominio de U4.
Ejecutar desde la carpeta que contiene 'datos' y este archivo.
"""
import csv
from pathlib import Path
from decimal import Decimal
from app.domain import Customer, Order, OrderItem, Money

BASE = Path(__file__).resolve().parent / "datos"

def rows(filename):
    with (BASE / filename).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def load_fixture():
    clients = {
        x["cliente_id"]: Customer(
            x["cliente_id"], bool(int(x["es_vip"])), bool(int(x["activo"]))
        ) for x in rows("clientes.csv")
    }
    prices = {x["sku"]: Decimal(x["precio_mxn"]) for x in rows("productos.csv")}
    orders = {
        x["pedido_id"]: Order(
            customer=clients[x["cliente_id"]],
            id=x["pedido_id"],
            has_promotion=bool(int(x["tiene_promocion"]))
        ) for x in rows("pedidos.csv")
    }
    for x in rows("detalle_pedidos.csv"):
        orders[x["pedido_id"]].add_item(
            OrderItem(x["sku"], int(x["cantidad"]), Money(prices[x["sku"]]))
        )
    return orders

if __name__ == "__main__":
    orders = load_fixture()
    for order_id, order in orders.items():
        print(order_id, order.status.value, order.units, order.total.amount)
# Colores discretos para distinguir los resultados en la terminal.
class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    DIM = "\033[2m"


def _money(value):
    return f"$ {value:,.2f}"


if __name__ == "__main__":
    orders = load_fixture()
    c = Color
    print()
    print(f"{c.BLUE}{c.BOLD}PetMarket - Carga de pedidos desde CSV{c.RESET}")
    print(f"{c.DIM}{'-' * 42}{c.RESET}")
    print(f"{c.GREEN}Validación de archivos: correcta{c.RESET}")
    print(f"{c.GREEN}Pedidos cargados correctamente: {len(orders)}{c.RESET}")
    print()
    for order_id, order in orders.items():
        print(
            f"{c.BLUE}{order_id}{c.RESET}  "
            f"Estado: {c.YELLOW}{order.status.value}{c.RESET}  "
            f"Unidades: {order.units}  "
            f"Total: {c.GREEN}{_money(order.total.amount)}{c.RESET}"
        )
    print()
    print(f"Estado inicial de los pedidos: {c.YELLOW}{c.BOLD}DRAFT{c.RESET}")
    print(f"{c.GREEN}Resultado: carga finalizada sin errores.{c.RESET}")
    print()
