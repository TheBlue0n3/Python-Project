import csv
import os


class Customer:
    """Bir müşteriyi temsil eder."""

    def __init__(self, id, name, phone):
        self.id = id
        self.name = name
        self.phone = phone
        self.total_spent = 0.0
        self.order_count = 0

    def add_spending(self, amount):
        """Müşterinin toplam harcamasına yeni miktar ekler."""
        if amount < 0:
            print("Amount cannot be negative.")
            return
        self.total_spent += amount
        self.order_count += 1

    def show(self):
        """Müşteri bilgilerini ekrana yazdırır."""
        print(f"\n  ID     : {self.id}")
        print(f"  Name   : {self.name}")
        print(f"  Phone  : {self.phone}")
        print(f"  Orders : {self.order_count}")
        print(f"  Spent  : {self.total_spent:.2f}€")

    def update_phone(self, new_phone):
        """Müşterinin telefon numarasını günceller."""
        self.phone = new_phone
        print(f"{self.name} phone updated.")

    def is_vip(self):
        """Müşterinin VIP olup olmadığını kontrol eder (500€ üzeri harcama)."""
        if self.total_spent >= 500:
            return True
        return False

    def __str__(self):
        """Müşteriyi yazı olarak döndürür."""
        return f"{self.name} (ID: {self.id})"


class CustomerManager:
    """Tüm müşterileri yönetir."""

    def __init__(self):
        self.customers = []
        self.next_id = 1

    def add(self, name, phone):
        """Yeni müşteri ekler ve oluşturulan müşteriyi döndürür."""
        c = Customer(self.next_id, name, phone)
        self.customers.append(c)
        self.next_id += 1
        print(f"{name} added as customer.")
        return c

    def find(self, id):
        """ID'ye göre müşteri arar, bulamazsa None döner."""
        for c in self.customers:
            if c.id == id:
                return c
        return None

    def show_all(self):
        """Tüm müşterileri listeler."""
        if len(self.customers) == 0:
            print("No customers yet.")
            return

        print("\nCustomers:")
        for c in self.customers:
            vip = " [VIP]" if c.is_vip() else ""
            print(f"  [{c.id}] {c.name} - {c.phone}{vip}")

    def show_vip(self):
        """Sadece VIP müşterileri listeler."""
        vip_list = []
        for c in self.customers:
            if c.is_vip():
                vip_list.append(c)

        if len(vip_list) == 0:
            print("No VIP customers yet.")
        else:
            print("\nVIP Customers:")
            for c in vip_list:
                print(f"  {c.name} - {c.total_spent:.2f}€")

    def save_csv(self, path="data/customers.csv"):
        """Müşteri verilerini CSV dosyasına kaydeder."""
        try:
            os.makedirs("data", exist_ok=True)
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["id", "name", "phone", "total_spent", "order_count"])
                for c in self.customers:
                    w.writerow([c.id, c.name, c.phone, c.total_spent, c.order_count])
            print("Customers saved.")
        except Exception as e:
            print(f"Error: {e}")

    def load_csv(self, path="data/customers.csv"):
        """Müşteri verilerini CSV dosyasından yükler."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                r = csv.DictReader(f)
                self.customers = []
                for row in r:
                    c = Customer(int(row["id"]), row["name"], row["phone"])
                    c.total_spent = float(row["total_spent"])
                    c.order_count = int(row["order_count"])
                    self.customers.append(c)
                if len(self.customers) > 0:
                    self.next_id = max(c.id for c in self.customers) + 1
            print(f"Customers loaded. {len(self.customers)} found.")
        except FileNotFoundError:
            print(f"{path} not found. Starting empty.")
        except Exception as e:
            print(f"Error: {e}")
