# Star Cafe Management System

A simple cafe management program I built with Python. It lets you manage the menu, customers and orders from the terminal.

## How to run

```bash
python main.py
```

No installation needed, just Python 3.

## What it can do

- Add/update menu items and toggle availability
- Add customers and track their spending
- Create orders, add items, and complete them
- See a daily revenue report
- Everything is saved to CSV files so data is not lost when you close the program

## Files

- `main.py` – starts the program and handles the menus
- `menu.py` – MenuItem and Menu classes
- `client.py` – Customer and CustomerManager classes
- `order.py` – Order, OrderItem and OrderManager classes
- `data/` – CSV files are saved here automatically
