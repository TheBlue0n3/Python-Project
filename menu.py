import csv
import os


class MenuItem:
    """Menüdeki bir ürünü temsil eder."""

    def __init__(self, id, name, price, category):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.available = True

    def update_price(self, new_price):
        """Ürünün fiyatını günceller."""
        if new_price < 0:
            print("Price cannot be negative.")
            return False
        self.price = new_price
        print(f"{self.name} price is now {self.price:.2f}€.")
        return True

    def toggle_available(self):
        """Ürünün mevcut/mevcut değil durumunu değiştirir."""
        self.available = not self.available
        if self.available:
            print(f"{self.name} is now available.")
        else:
            print(f"{self.name} is now unavailable.")

    def show(self):
        """Ürün bilgilerini ekranda gösterir."""
        status = "yes" if self.available else "no"
        print(f"  [{self.id}] {self.name} - {self.price:.2f}€ - available: {status}")

    def __str__(self):
        """Ürünü yazı olarak döndürür."""
        return f"{self.name} ({self.price:.2f}€)"


class Menu:
    """Cafe menüsünü yönetir."""

    def __init__(self):
        self.items = []
        self.next_id = 1

    def add(self, name, price, category):
        """Menüye yeni ürün ekler."""
        x = MenuItem(self.next_id, name, price, category)
        self.items.append(x)
        self.next_id += 1
        print(f"{name} added to menu.")
        return x

    def find(self, id):
        """Verilen ID'ye sahip ürünü döndürür, yoksa None döner."""
        for i in self.items:
            if i.id == id:
                return i
        return None

    def show_all(self):
        """Tüm menüyü kategorilere göre ekrana yazdırır."""
        if len(self.items) == 0:
            print("Menu is empty.")
            return

        print("\nCafe Menu:")

        categories = []
        for i in self.items:
            if i.category not in categories:
                categories.append(i.category)

        for cat in categories:
            print(f"\n{cat}:")
            for i in self.items:
                if i.category == cat and i.available:
                    i.show()

    def save_csv(self, path="data/menu.csv"):
        """Menüyü CSV dosyasına kaydeder."""
        try:
            os.makedirs("data", exist_ok=True)
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["id", "name", "price", "category", "available"])
                for i in self.items:
                    w.writerow([i.id, i.name, i.price, i.category, i.available])
            print(f"Menu saved.")
        except Exception as e:
            print(f"Error: {e}")

    def load_csv(self, path="data/menu.csv"):
        """Menüyü CSV dosyasından yükler."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                r = csv.DictReader(f)
                self.items = []
                for row in r:
                    x = MenuItem(int(row["id"]), row["name"], float(row["price"]), row["category"])
                    x.available = row["available"] == "True"
                    self.items.append(x)
                if len(self.items) > 0:
                    self.next_id = max(i.id for i in self.items) + 1
            print(f"Menu loaded. {len(self.items)} items.")
        except FileNotFoundError:
            print(f"{path} not found. Starting empty.")
        except Exception as e:
            print(f"Error: {e}")
