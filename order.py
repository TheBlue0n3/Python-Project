import csv
import os
from datetime import datetime


class OrderItem:
    """Siparişin içindeki tek bir ürün kalemini temsil eder."""

    def __init__(self, item, qty):
        self.item = item
        self.qty = qty

    def get_total(self):
        """Bu kalemin toplam fiyatını hesaplar."""
        return self.item.price * self.qty

    def __str__(self):
        """Kalemi yazı olarak döndürür."""
        return f"{self.item.name} x{self.qty} = {self.get_total():.2f}€"


class Order:
    """Bir siparişi temsil eder."""

    def __init__(self, id, customer):
        self.id = id
        self.customer = customer
        self.lines = []
        self.date = datetime.now()
        self.done = False

    def add_item(self, item, qty=1):
        """Siparişe ürün ekler. Ürün mevcut değilse veya adet geçersizse eklemez."""
        if not item.available:
            print(f"{item.name} is not available right now.")
            return False
        if qty <= 0:
            print("Quantity must be at least 1.")
            return False

        for line in self.lines:
            if line.item.id == item.id:
                line.qty += qty
                print(f"{item.name} quantity updated to {line.qty}.")
                return True

        self.lines.append(OrderItem(item, qty))
        print(f"{item.name} added to order.")
        return True

    def remove_item(self, item_id):
        """Siparişten ürün çıkarır."""
        for i in range(len(self.lines)):
            if self.lines[i].item.id == item_id:
                removed = self.lines.pop(i)
                print(f"{removed.item.name} removed from order.")
                return True
        print("Item not found in order.")
        return False

    def get_total(self):
        """Siparişin toplam tutarını hesaplar."""
        total = 0.0
        for line in self.lines:
            total += line.get_total()
        return total

    def show(self):
        """Sipariş detaylarını ekrana yazdırır."""
        print(f"\nOrder #{self.id}")
        print(f"  Customer: {self.customer.name}")
        print(f"  Date: {self.date.strftime('%d/%m/%Y %H:%M')}")
        print(f"  Status: {'Done' if self.done else 'Pending'}")
        print("  Items:")
        if len(self.lines) == 0:
            print("  (empty)")
        else:
            for line in self.lines:
                print(f"  - {line}")
        print(f"  Total: {self.get_total():.2f}€")

    def complete(self):
        """Siparişi tamamlandı olarak işaretler ve müşteri harcamasını günceller."""
        if len(self.lines) == 0:
            print("Order is empty, cannot complete.")
            return False
        self.done = True
        self.customer.add_spending(self.get_total())
        print(f"Order #{self.id} completed. Total: {self.get_total():.2f}€")
        return True


class OrderManager:
    """Tüm siparişleri yönetir."""

    def __init__(self):
        self.orders = []
        self.next_id = 1

    def create(self, customer):
        """Yeni sipariş oluşturur."""
        o = Order(self.next_id, customer)
        self.orders.append(o)
        self.next_id += 1
        print(f"Order #{o.id} created.")
        return o

    def find(self, id):
        """ID'ye göre sipariş arar, bulamazsa None döner."""
        for o in self.orders:
            if o.id == id:
                return o
        return None

    def show_active(self):
        """Tamamlanmamış siparişleri listeler."""
        active = []
        for o in self.orders:
            if not o.done:
                active.append(o)

        if len(active) == 0:
            print("No pending orders.")
        else:
            print("\nActive orders:")
            for o in active:
                print(f"  [{o.id}] {o.customer.name} - {o.get_total():.2f}€")

    def daily_report(self):
        """Günlük sipariş özetini ekrana yazdırır."""
        done_orders = []
        for o in self.orders:
            if o.done:
                done_orders.append(o)

        total_revenue = 0.0
        for o in done_orders:
            total_revenue += o.get_total()

        print("\nDaily Report:")
        print(f"  Total orders: {len(self.orders)}")
        print(f"  Completed: {len(done_orders)}")
        print(f"  Revenue: {total_revenue:.2f}€")

    def save_csv(self, path="data/orders.csv"):
        """Siparişleri CSV dosyasına kaydeder."""
        try:
            os.makedirs("data", exist_ok=True)
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["id", "customer", "date", "total", "done"])
                for o in self.orders:
                    w.writerow([o.id, o.customer.name, o.date.strftime("%d/%m/%Y %H:%M"), o.get_total(), o.done])
            print("Orders saved.")
        except Exception as e:
            print(f"Error: {e}")
