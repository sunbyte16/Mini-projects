import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime

@dataclass
class MenuItem:
    id: str
    name: str
    price: float
    category: str
    description: str = ""
    available: bool = True
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'description': self.description,
            'available': self.available
        }

@dataclass
class OrderItem:
    menu_item_id: str
    quantity: int
    price: float
    notes: str = ""
    
    def to_dict(self) -> dict:
        return {
            'menu_item_id': self.menu_item_id,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.quantity * self.price,
            'notes': self.notes
        }

@dataclass
class Order:
    order_id: str
    table_number: int
    items: List[Dict]
    status: str = "pending"  # pending, preparing, ready, served, paid, cancelled
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    served_at: str = ""
    paid_at: str = ""
    payment_method: str = ""
    discount: float = 0.0
    tax_rate: float = 8.0  # 8% tax
    tip: float = 0.0
    
    def calculate_subtotal(self) -> float:
        return sum(item['subtotal'] for item in self.items)
    
    def calculate_tax(self) -> float:
        return (self.calculate_subtotal() - self.discount) * (self.tax_rate / 100)
    
    def calculate_total(self) -> float:
        return self.calculate_subtotal() + self.calculate_tax() + self.tip - self.discount
    
    def to_dict(self) -> dict:
        return {
            'order_id': self.order_id,
            'table_number': self.table_number,
            'items': self.items,
            'status': self.status,
            'created_at': self.created_at,
            'served_at': self.served_at,
            'paid_at': self.paid_at,
            'payment_method': self.payment_method,
            'discount': self.discount,
            'tax_rate': self.tax_rate,
            'tip': self.tip,
            'subtotal': self.calculate_subtotal(),
            'tax': self.calculate_tax(),
            'total': self.calculate_total()
        }

class RestaurantBillingSystem:
    def __init__(self):
        self.menu: Dict[str, MenuItem] = {}
        self.orders: Dict[str, Order] = {}
        self.tables = {i: "available" for i in range(1, 21)}  # 20 tables
        self.load_data()
    
    def load_data(self):
        if os.path.exists('menu.json'):
            try:
                with open('menu.json', 'r') as f:
                    data = json.load(f)
                    self.menu = {k: MenuItem(**v) for k, v in data.items()}
            except (json.JSONDecodeError, FileNotFoundError):
                self.menu = {}
        
        if os.path.exists('orders.json'):
            try:
                with open('orders.json', 'r') as f:
                    data = json.load(f)
                    self.orders = {k: Order(**v) for k, v in data.items()}
            except (json.JSONDecodeError, FileNotFoundError):
                self.orders = {}
        
        # Update table status based on active orders
        for order in self.orders.values():
            if order.status not in ["paid", "cancelled"]:
                self.tables[order.table_number] = "occupied"
    
    def save_data(self):
        with open('menu.json', 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.menu.items()}, f, indent=2)
        
        with open('orders.json', 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.orders.items()}, f, indent=2)
    
    def add_menu_item(self, name: str, price: float, category: str, description: str = "") -> str:
        item_id = f"M{len(self.menu) + 1:03d}"
        self.menu[item_id] = MenuItem(item_id, name, price, category, description)
        self.save_data()
        return item_id
    
    def update_menu_item(self, item_id: str, **kwargs) -> bool:
        if item_id not in self.menu:
            return False
        
        item = self.menu[item_id]
        for key, value in kwargs.items():
            if hasattr(item, key):
                setattr(item, key, value)
        
        self.save_data()
        return True
    
    def create_order(self, table_number: int) -> Optional[Order]:
        if table_number not in self.tables or self.tables[table_number] != "available":
            return None
        
        order_id = f"ORD{len(self.orders) + 1:04d}"
        order = Order(order_id, table_number, [])
        self.orders[order_id] = order
        self.tables[table_number] = "occupied"
        self.save_data()
        return order
    
    def add_to_order(self, order_id: str, menu_item_id: str, quantity: int = 1, notes: str = "") -> bool:
        if order_id not in self.orders or menu_item_id not in self.menu or quantity <= 0:
            return False
        
        menu_item = self.menu[menu_item_id]
        if not menu_item.available:
            return False
        
        # Check if item already in order
        for item in self.orders[order_id].items:
            if item['menu_item_id'] == menu_item_id and item['notes'] == notes:
                item['quantity'] += quantity
                item['subtotal'] = item['quantity'] * item['price']
                self.save_data()
                return True
        
        # Add new item to order
        order_item = OrderItem(menu_item_id, quantity, menu_item.price, notes).to_dict()
        self.orders[order_id].items.append(order_item)
        self.save_data()
        return True
    
    def update_order_status(self, order_id: str, status: str) -> bool:
        if order_id not in self.orders or status not in ["pending", "preparing", "ready", "served", "paid", "cancelled"]:
            return False
        
        order = self.orders[order_id]
        order.status = status
        
        if status == "served":
            order.served_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif status == "paid":
            order.paid_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.tables[order.table_number] = "available"
        elif status == "cancelled":
            self.tables[order.table_number] = "available"
        
        self.save_data()
        return True
    
    def apply_discount(self, order_id: str, discount: float) -> bool:
        if order_id not in self.orders or discount < 0:
            return False
        
        self.orders[order_id].discount = discount
        self.save_data()
        return True
    
    def add_tip(self, order_id: str, tip: float) -> bool:
        if order_id not in self.orders or tip < 0:
            return False
        
        self.orders[order_id].tip = tip
        self.save_data()
        return True
    
    def process_payment(self, order_id: str, payment_method: str, amount: float) -> Tuple[bool, float]:
        if order_id not in self.orders or payment_method not in ["cash", "card", "mobile"]:
            return False, 0.0
        
        order = self.orders[order_id]
        total = order.calculate_total()
        
        if amount < total:
            return False, total - amount  # Return remaining amount
        
        order.payment_method = payment_method
        order.status = "paid"
        order.paid_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tables[order.table_number] = "available"
        self.save_data()
        
        return True, amount - total  # Return change

def display_menu(menu: Dict[str, MenuItem], category: str = None):
    items = [item for item in menu.values() 
             if (category is None or item.category.lower() == category.lower()) 
             and item.available]
    
    if not items:
        print("No items found in this category.")
        return
    
    print("\n{:<6} {:<30} {:<10} {:<30}".format("ID", "Name", "Price", "Description"))
    print("-" * 80)
    
    for item in items:
        print("{:<6} {:<30} ${:<9.2f} {:<30}".format(
            item.id, 
            item.name[:28], 
            item.price, 
            item.description[:28] + ("..." if len(item.description) > 28 else "")
        ))

def display_order(order: Order, menu: Dict[str, MenuItem]):
    print(f"\n=== Order {order.order_id} ===")
    print(f"Table: {order.table_number}")
    print(f"Status: {order.status.upper()}")
    print(f"Created: {order.created_at}")
    
    if order.served_at:
        print(f"Served: {order.served_at}")
    
    print("\n{:<5} {:<30} {:<10} {:<10} {:<10}".format(
        "Qty", "Item", "Price", "Subtotal", "Notes"))
    print("-" * 80)
    
    for item in order.items:
        menu_item = menu.get(item['menu_item_id'])
        item_name = menu_item.name if menu_item else "[Item not found]"
        print("{:<5} {:<30} ${:<9.2f} ${:<9.2f} {:<10}".format(
            item['quantity'],
            item_name[:28],
            item['price'],
            item['subtotal'],
            item['notes'][:10] + ("..." if len(item['notes']) > 10 else "")
        ))
    
    print("-" * 80)
    print(f"{'Subtotal:':>50} ${order.calculate_subtotal():.2f}")
    
    if order.discount > 0:
        print(f"{'Discount:':>50} -${order.discount:.2f}")
    
    print(f"{'Tax (' + str(order.tax_rate) + '%):':>50} ${order.calculate_tax():.2f}")
    
    if order.tip > 0:
        print(f"{'Tip:':>50} ${order.tip:.2f}")
    
    print(f"{'Total:':>50} ${order.calculate_total():.2f}")
    
    if order.status == "paid":
        print(f"\nPaid with {order.payment_method} at {order.paid_at}")

def display_table_status(tables: Dict[int, str]):
    print("\n=== Table Status ===")
    print("\nAvailable: ", end="")
    available = [str(t) for t, s in tables.items() if s == "available"]
    print(", ".join(available) if available else "None")
    
    print("Occupied: ", end="")
    occupied = [str(t) for t, s in tables.items() if s == "occupied"]
    print(", ".join(occupied) if occupied else "None")

def get_float_input(prompt: str, min_val: float = None) -> float:
    while True:
        try:
            value = float(input(prompt).strip() or "0")
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

def get_int_input(prompt: str, min_val: int = None, max_val: int = None) -> int:
    while True:
        try:
            value = int(input(prompt).strip() or "0")
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be at most {max_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer.")

def main():
    system = RestaurantBillingSystem()
    
    # Add sample menu items if none exist
    if not system.menu:
        system.add_menu_item("Margherita Pizza", 12.99, "Pizza", "Tomato sauce, mozzarella, basil")
        system.add_menu_item("Pepperoni Pizza", 14.99, "Pizza", "Tomato sauce, mozzarella, pepperoni")
        system.add_menu_item("Caesar Salad", 8.99, "Salads", "Romaine, croutons, parmesan, Caesar dressing")
        system.add_menu_item("Garlic Bread", 4.99, "Sides", "Freshly baked with garlic butter")
        system.add_menu_item("Pasta Carbonara", 13.99, "Pasta", "Spaghetti, eggs, pancetta, parmesan")
        system.add_menu_item("Tiramisu", 6.99, "Desserts", "Coffee-flavored Italian dessert")
        system.add_menu_item("Coke", 2.50, "Drinks", "12oz can")
        system.add_menu_item("Iced Tea", 2.50, "Drinks", "Freshly brewed")
    
    while True:
        print("\n=== Restaurant Billing System ===")
        print("1. View Menu")
        print("2. View Table Status")
        print("3. Create New Order")
        print("4. View/Edit Order")
        print("5. Process Payment")
        print("6. Admin: Manage Menu")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':  # View Menu
            categories = set(item.category for item in system.menu.values())
            print("\nCategories:", ", ".join(categories))
            category = input("Enter category (or press Enter for all): ").strip()
            display_menu(system.menu, category if category else None)
        
        elif choice == '2':  # View Table Status
            display_table_status(system.tables)
        
        elif choice == '3':  # Create New Order
            display_table_status(system.tables)
            table = get_int_input("\nEnter table number: ", 1, 20)
            
            if system.tables[table] != "available":
                print(f"Table {table} is currently occupied.")
            else:
                order = system.create_order(table)
                if order:
                    print(f"\n✅ Order {order.order_id} created for Table {table}")
                    
                    # Add items to order
                    while True:
                        display_menu(system.menu)
                        item_id = input("\nEnter item ID to add (or 'done' to finish): ").strip().upper()
                        
                        if item_id.lower() == 'done':
                            break
                        
                        if item_id not in system.menu:
                            print("Invalid item ID. Please try again.")
                            continue
                        
                        qty = get_int_input("Quantity: ", 1)
                        notes = input("Special instructions (press Enter if none): ").strip()
                        
                        if system.add_to_order(order.order_id, item_id, qty, notes):
                            print(f"Added {qty}x {system.menu[item_id].name} to order.")
                        else:
                            print("Failed to add item. It may be unavailable.")
                    
                    # Show order summary
                    display_order(order, system.menu)
                else:
                    print("Failed to create order. Please try again.")
        
        elif choice == '4':  # View/Edit Order
            order_id = input("Enter order ID (or press Enter to list all): ").strip().upper()
            
            if not order_id:
                if not system.orders:
                    print("No orders found.")
                    continue
                
                print("\nActive Orders:")
                for oid, order in system.orders.items():
                    if order.status != "paid" and order.status != "cancelled":
                        print(f"{oid} - Table {order.table_number} - {order.status.upper()}")
                
                order_id = input("\nEnter order ID to view/edit: ").strip().upper()
                if not order_id:
                    continue
            
            if order_id not in system.orders:
                print("Order not found.")
                continue
            
            order = system.orders[order_id]
            
            while True:
                display_order(order, system.menu)
                
                print("\n1. Add Item")
                print("2. Update Status")
                print("3. Apply Discount")
                print("4. Add Tip")
                print("5. Back to Main Menu")
                
                sub_choice = input("\nEnter your choice (1-5): ").strip()
                
                if sub_choice == '1':  # Add Item
                    display_menu(system.menu)
                    item_id = input("\nEnter item ID to add: ").strip().upper()
                    
                    if item_id not in system.menu:
                        print("Invalid item ID.")
                        continue
                    
                    qty = get_int_input("Quantity: ", 1)
                    notes = input("Special instructions (press Enter if none): ").strip()
                    
                    if system.add_to_order(order_id, item_id, qty, notes):
                        print(f"Added {qty}x {system.menu[item_id].name} to order.")
                    else:
                        print("Failed to add item. It may be unavailable.")
                
                elif sub_choice == '2':  # Update Status
                    print("\n1. Pending")
                    print("2. Preparing")
                    print("3. Ready")
                    print("4. Served")
                    print("5. Cancelled")
                    
                    status_choice = input("\nSelect status (1-5): ").strip()
                    status_map = {
                        '1': 'pending',
                        '2': 'preparing',
                        '3': 'ready',
                        '4': 'served',
                        '5': 'cancelled'
                    }
                    
                    if status_choice in status_map:
                        if system.update_order_status(order_id, status_map[status_choice]):
                            print("\n✅ Status updated successfully!")
                            order = system.orders[order_id]  # Refresh order
                        else:
                            print("\n❌ Failed to update status.")
                
                elif sub_choice == '3':  # Apply Discount
                    discount = get_float_input("Enter discount amount: $", 0)
                    if system.apply_discount(order_id, discount):
                        print(f"\n✅ ${discount:.2f} discount applied.")
                        order = system.orders[order_id]  # Refresh order
                    else:
                        print("\n❌ Failed to apply discount.")
                
                elif sub_choice == '4':  # Add Tip
                    tip = get_float_input("Enter tip amount: $", 0)
                    if system.add_tip(order_id, tip):
                        print(f"\n✅ ${tip:.2f} tip added.")
                        order = system.orders[order_id]  # Refresh order
                    else:
                        print("\n❌ Failed to add tip.")
                
                elif sub_choice == '5':  # Back to Main Menu
                    break
                
                else:
                    print("Invalid choice. Please try again.")
        
        elif choice == '5':  # Process Payment
            order_id = input("Enter order ID: ").strip().upper()
            
            if order_id not in system.orders:
                print("Order not found.")
                continue
            
            order = system.orders[order_id]
            
            if order.status == "paid":
                print("This order has already been paid.")
                continue
            
            display_order(order, system.menu)
            
            print("\nPayment Method:")
            print("1. Cash")
            print("2. Credit/Debit Card")
            print("3. Mobile Payment")
            
            method_choice = input("\nSelect payment method (1-3): ").strip()
            method_map = {'1': 'cash', '2': 'card', '3': 'mobile'}
            
            if method_choice not in method_map:
                print("Invalid choice.")
                continue
            
            method = method_map[method_choice]
            total = order.calculate_total()
            
            if method == 'cash':
                amount = get_float_input(f"Enter amount received (${total:.2f}): $", total)
                success, change = system.process_payment(order_id, method, amount)
                
                if success:
                    print(f"\n✅ Payment processed successfully!")
                    print(f"Change: ${change:.2f}")
                    print("Thank you for your business!")
                else:
                    print(f"\n❌ Insufficient payment. Remaining: ${change:.2f}")
            else:
                success, _ = system.process_payment(order_id, method, total)
                if success:
                    print("\n✅ Payment processed successfully!")
                    print("Thank you for your business!")
                else:
                    print("\n❌ Payment failed. Please try again.")
        
        elif choice == '6':  # Admin: Manage Menu
            while True:
                print("\n=== Menu Management ===")
                print("1. Add New Menu Item")
                print("2. Update Menu Item")
                print("3. Toggle Item Availability")
                print("4. View All Menu Items")
                print("5. Back to Main Menu")
                
                admin_choice = input("\nEnter your choice (1-5): ").strip()
                
                if admin_choice == '1':  # Add New Menu Item
                    print("\n=== Add New Menu Item ===")
                    name = input("Item Name: ").strip()
                    price = get_float_input("Price: $", 0.01)
                    category = input("Category: ").strip()
                    description = input("Description (press Enter if none): ").strip()
                    
                    item_id = system.add_menu_item(name, price, category, description)
                    print(f"\n✅ Menu item added successfully! ID: {item_id}")
                
                elif admin_choice == '2':  # Update Menu Item
                    display_menu(system.menu)
                    item_id = input("\nEnter item ID to update: ").strip().upper()
                    
                    if item_id not in system.menu:
                        print("Item not found.")
                        continue
                    
                    item = system.menu[item_id]
                    print(f"\nUpdating: {item.name}")
                    print("Leave field blank to keep current value.")
                    
                    name = input(f"Name [{item.name}]: ").strip()
                    price = input(f"Price [${item.price:.2f}]: $").strip()
                    category = input(f"Category [{item.category}]: ").strip()
                    description = input(f"Description [{item.description}]: ").strip()
                    
                    updates = {}
                    if name:
                        updates['name'] = name
                    if price:
                        try:
                            updates['price'] = float(price)
                        except ValueError:
                            print("Invalid price format. Update skipped.")
                    if category:
                        updates['category'] = category
                    if description:
                        updates['description'] = description
                    
                    if updates and system.update_menu_item(item_id, **updates):
                        print("\n✅ Menu item updated successfully!")
                    else:
                        print("\n❌ Failed to update menu item.")
                
                elif admin_choice == '3':  # Toggle Item Availability
                    display_menu(system.menu)
                    item_id = input("\nEnter item ID to toggle availability: ").strip().upper()
                    
                    if item_id in system.menu:
                        current = system.menu[item_id].available
                        system.update_menu_item(item_id, available=not current)
                        status = "available" if not current else "unavailable"
                        print(f"\n✅ Item is now {status}.")
                    else:
                        print("Item not found.")
                
                elif admin_choice == '4':  # View All Menu Items
                    display_menu(system.menu)
                
                elif admin_choice == '5':  # Back to Main Menu
                    break
                
                else:
                    print("Invalid choice. Please try again.")
        
        elif choice == '7':  # Exit
            print("\nThank you for using the Restaurant Billing System!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
