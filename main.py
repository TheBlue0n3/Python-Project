from menu import Menu
from client import CustomerManager
from order import OrderManager


def load_data(menu, cm):
    """Kaydedilmiş verileri dosyalardan yükler."""
    menu.load_csv()
    cm.load_csv()


def setup_sample_menu(menu):
    """Eğer menü boşsa örnek ürünler ekler."""
    menu.add("Espresso", 35.0, "Coffee")
    menu.add("Cappuccino", 45.0, "Coffee")
    menu.add("Latte", 50.0, "Coffee")
    menu.add("Americano", 40.0, "Coffee")
    menu.add("Orange Juice", 30.0, "Drinks")
    menu.add("Water", 10.0, "Drinks")
    menu.add("Cheesecake", 65.0, "Dessert")
    menu.add("Brownie", 55.0, "Dessert")
    menu.add("Croissant", 40.0, "Snacks")
    menu.add("Sandwich", 75.0, "Snacks")


def menu_management(menu):
    """Menü yönetim ekranını çalıştırır."""
    while True:
        print("\n--- MENU MANAGEMENT ---")
        print("1. Show all menu items")
        print("2. Add new item")
        print("3. Update item price")
        print("4. Toggle item availability")
        print("0. Back")

        choice = input("Choice: ").strip()

        if choice == "1":
            menu.show_all()

        elif choice == "2":
            name = input("Item name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            try:
                price = float(input("Price (€): "))
                if price < 0:
                    print("Price cannot be negative.")
                    continue
            except ValueError:
                print("Invalid price.")
                continue
            category = input("Category: ").strip()
            menu.add(name, price, category)
            menu.save_csv()

        elif choice == "3":
            menu.show_all()
            try:
                id = int(input("Item ID to update: "))
                item = menu.find(id)
                if item is None:
                    print("Item not found.")
                    continue
                new_price = float(input(f"New price (current: {item.price:.2f}€): "))
                item.update_price(new_price)
                menu.save_csv()
            except ValueError:
                print("Invalid input.")

        elif choice == "4":
            menu.show_all()
            try:
                id = int(input("Item ID: "))
                item = menu.find(id)
                if item is None:
                    print("Item not found.")
                    continue
                item.toggle_available()
                menu.save_csv()
            except ValueError:
                print("Invalid input.")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def customer_management(cm):
    """Müşteri yönetim ekranını çalıştırır."""
    while True:
        print("\n--- CUSTOMER MANAGEMENT ---")
        print("1. List all customers")
        print("2. Add new customer")
        print("3. View customer details")
        print("4. Show VIP customers")
        print("0. Back")

        choice = input("Choice: ").strip()

        if choice == "1":
            cm.show_all()

        elif choice == "2":
            name = input("Customer name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            phone = input("Phone: ").strip()
            cm.add(name, phone)
            cm.save_csv()

        elif choice == "3":
            cm.show_all()
            try:
                id = int(input("Customer ID: "))
                c = cm.find(id)
                if c is None:
                    print("Customer not found.")
                else:
                    c.show()
            except ValueError:
                print("Invalid input.")

        elif choice == "4":
            cm.show_vip()

        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def order_management(menu, cm, om):
    """Sipariş yönetim ekranını çalıştırır."""
    while True:
        print("\n--- ORDER MANAGEMENT ---")
        print("1. New order")
        print("2. Show active orders")
        print("3. Complete an order")
        print("4. Daily report")
        print("0. Back")

        choice = input("Choice: ").strip()

        if choice == "1":
            cm.show_all()
            try:
                cid = int(input("Customer ID (0 for new customer): "))
                if cid == 0:
                    name = input("Name: ").strip()
                    phone = input("Phone: ").strip()
                    c = cm.add(name, phone)
                else:
                    c = cm.find(cid)
                    if c is None:
                        print("Customer not found.")
                        continue
            except ValueError:
                print("Invalid input.")
                continue

            o = om.create(c)

            while True:
                menu.show_all()
                print("\nEnter item ID to add, 0 to finish.")
                try:
                    iid = int(input("Item ID: "))
                    if iid == 0:
                        break
                    item = menu.find(iid)
                    if item is None:
                        print("Item not found.")
                        continue
                    qty = int(input("Quantity: "))
                    o.add_item(item, qty)
                    o.show()
                except ValueError:
                    print("Invalid input.")

            o.show()
            om.save_csv()

        elif choice == "2":
            om.show_active()

        elif choice == "3":
            om.show_active()
            try:
                oid = int(input("Order ID to complete: "))
                o = om.find(oid)
                if o is None:
                    print("Order not found.")
                elif o.done:
                    print("Order already completed.")
                else:
                    o.complete()
                    om.save_csv()
                    cm.save_csv()
            except ValueError:
                print("Invalid input.")

        elif choice == "4":
            om.daily_report()

        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def main():
    """Programın ana giriş noktası. Menüyü başlatır."""
    print("Welcome to Yildiz Cafe Management System")

    menu = Menu()
    cm = CustomerManager()
    om = OrderManager()

    print("\nLoading data...")
    load_data(menu, cm)

    if len(menu.items) == 0:
        print("No menu found. Loading sample menu...")
        setup_sample_menu(menu)
        menu.save_csv()

    while True:
        print("\nMain Menu:")
        print("1. Menu Management")
        print("2. Customer Management")
        print("3. Order Management")
        print("0. Exit")

        choice = input("Choice: ").strip()

        if choice == "1":
            menu_management(menu)
        elif choice == "2":
            customer_management(cm)
        elif choice == "3":
            order_management(menu, cm, om)
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Enter 0-3.")


if __name__ == "__main__":
    main()
