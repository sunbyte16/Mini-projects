import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class Product:
    id: str
    name: str
    price: float
    description: str = ""
    category: str = ""
    stock: int = 0
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'category': self.category,
            'stock': self.stock
        }

@dataclass
class CartItem:
    product_id: str
    quantity: int
    price: float
    
    def to_dict(self) -> dict:
        return {
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.quantity * self.price
        }

@dataclass
class Order:
    order_id: str
    customer_name: str
    items: List[Dict]
    total: float
    status: str = "pending"
    order_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def to_dict(self) -> dict:
        return {
            'order_id': self.order_id,
            'customer_name': self.customer_name,
            'items': self.items,
            'total': self.total,
            'status': self.status,
            'order_date': self.order_date
        }

class EcommerceSystem:
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.cart: Dict[str, CartItem] = {}
        self.orders: Dict[str, Order] = {}
        self.load_data()
    
    def load_data(self):
        if os.path.exists('products.json'):
            try:
                with open('products.json', 'r') as f:
                    data = json.load(f)
                    self.products = {k: Product(**v) for k, v in data.items()}
            except (json.JSONDecodeError, FileNotFoundError):
                self.products = {}
        
        if os.path.exists('orders.json'):
            try:
                with open('orders.json', 'r') as f:
                    data = json.load(f)
                    self.orders = {k: Order(**v) for k, v in data.items()}
            except (json.JSONDecodeError, FileNotFoundError):
                self.orders = {}
    
    def save_data(self):
        with open('products.json', 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.products.items()}, f, indent=2)
        
        with open('orders.json', 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.orders.items()}, f, indent=2)
    
    def add_product(self, name: str, price: float, description: str = "", category: str = "", stock: int = 0) -> str:
        pid = f"P{len(self.products) + 1:04d}"
        self.products[pid] = Product(pid, name, price, description, category, stock)
        self.save_data()
        return pid
    
    def update_product_stock(self, product_id: str, quantity: int) -> bool:
        if product_id not in self.products:
            return False
        self.products[product_id].stock += quantity
        self.save_data()
        return True
    
    def add_to_cart(self, product_id: str, quantity: int = 1) -> bool:
        if product_id not in self.products or quantity <= 0:
            return False
        
        product = self.products[product_id]
        if product.stock < quantity:
            return False
        
        if product_id in self.cart:
            self.cart[product_id].quantity += quantity
        else:
            self.cart[product_id] = CartItem(product_id, quantity, product.price)
        
        return True
    
    def remove_from_cart(self, product_id: str, quantity: int = None) -> bool:
        if product_id not in self.cart:
            return False
        
        if quantity is None or quantity >= self.cart[product_id].quantity:
            del self.cart[product_id]
        else:
            self.cart[product_id].quantity -= quantity
        
        return True
    
    def get_cart_total(self) -> float:
        return sum(item.quantity * item.price for item in self.cart.values())
    
    def checkout(self, customer_name: str) -> Optional[Order]:
        if not self.cart:
            return None
        
        # Check stock availability
        for item in self.cart.values():
            if self.products[item.product_id].stock < item.quantity:
                return None
        
        # Process order
        order_id = f"ORD{len(self.orders) + 1:06d}"
        items = [{
            'product_id': item.product_id,
            'name': self.products[item.product_id].name,
            'quantity': item.quantity,
            'price': item.price,
            'subtotal': item.quantity * item.price
        } for item in self.cart.values()]
        
        total = self.get_cart_total()
        order = Order(order_id, customer_name, items, total)
        self.orders[order_id] = order
        
        # Update stock
        for item in self.cart.values():
            self.products[item.product_id].stock -= item.quantity
        
        # Clear cart
        self.cart.clear()
        self.save_data()
        
        return order
    
    def list_products(self, category: str = None) -> List[Product]:
        if category:
            return [p for p in self.products.values() if p.category.lower() == category.lower()]
        return list(self.products.values())
    
    def get_product(self, product_id: str) -> Optional[Product]:
        return self.products.get(product_id)

def display_menu():
    print("\n=== E-commerce System ===")
    print("1. Browse Products")
    print("2. View Product Details")
    print("3. Add to Cart")
    print("4. View Cart")
    print("5. Remove from Cart")
    print("6. Checkout")
    print("7. View Orders")
    print("8. Admin: Add Product")
    print("9. Admin: Update Stock")
    print("0. Exit")

def display_products(products: List[Product]):
    if not products:
        print("No products found.")
        return
    
    print("\n{:<8} {:<30} {:<10} {:<10} {:<20}".format(
        "ID", "Name", "Price", "Stock", "Category"))
    print("-" * 80)
    
    for p in products:
        print("{:<8} {:<30} ${:<9.2f} {:<10} {:<20}".format(
            p.id, p.name[:28], p.price, p.stock, p.category[:18]))

def display_cart(cart: Dict[str, CartItem], products: Dict[str, Product]):
    if not cart:
        print("Your cart is empty.")
        return
    
    print("\n{:<8} {:<30} {:<10} {:<10} {:<10}".format(
        "ID", "Name", "Price", "Qty", "Subtotal"))
    print("-" * 80)
    
    total = 0
    for item in cart.values():
        product = products[item.product_id]
        subtotal = item.quantity * item.price
        total += subtotal
        print("{:<8} {:<30} ${:<9.2f} {:<10} ${:<9.2f}".format(
            product.id, product.name[:28], item.price, item.quantity, subtotal))
    
    print("-" * 80)
    print(f"{'Total:':>58} ${total:.2f}")

def display_orders(orders: List[Order]):
    if not orders:
        print("No orders found.")
        return
    
    print("\n{:<12} {:<20} {:<12} {:<10} {:<20}".format(
        "Order ID", "Customer", "Total", "Status", "Date"))
    print("-" * 80)
    
    for order in sorted(orders, key=lambda x: x.order_date, reverse=True):
        print("{:<12} {:<20} ${:<11.2f} {:<10} {:<20}".format(
            order.order_id,
            order.customer_name[:18],
            order.total,
            order.status,
            order.order_date.split()[0]  # Just the date part
        ))

def display_order_details(order: Order, products: Dict[str, Product]):
    print(f"\n=== Order {order.order_id} ===")
    print(f"Customer: {order.customer_name}")
    print(f"Date: {order.order_date}")
    print(f"Status: {order.status}")
    
    print("\n{:<5} {:<30} {:<10} {:<10} {:<10}".format(
        "Qty", "Product", "Price", "Subtotal", "Status"))
    print("-" * 80)
    
    for item in order.items:
        print("{:<5} {:<30} ${:<9.2f} ${:<9.2f} {:<10}".format(
            item['quantity'],
            item['name'][:28],
            item['price'],
            item['subtotal'],
            "In Stock"  # Simplified for this example
        ))
    
    print("-" * 80)
    print(f"{'Total:':>58} ${order.total:.2f}")

def main():
    system = EcommerceSystem()
    
    # Add sample products if none exist
    if not system.products:
        system.add_product("Wireless Earbuds", 99.99, "Noise cancelling", "Electronics", 50)
        system.add_product("Smart Watch", 199.99, "Fitness tracker", "Electronics", 30)
        system.add_product("Running Shoes", 79.99, "Lightweight", "Footwear", 100)
        system.add_product("Backpack", 49.99, "Waterproof", "Accessories", 75)
        system.add_product("Coffee Mug", 12.99, "Ceramic, 12oz", "Home", 200)
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (0-9): ").strip()
        
        if choice == '0':
            print("Thank you for shopping with us!")
            break
            
        elif choice == '1':  # Browse Products
            categories = set(p.category for p in system.products.values() if p.category)
            print("\nCategories:", ", ".join(categories) if categories else "No categories")
            category = input("Enter category (or press Enter for all): ").strip()
            products = system.list_products(category) if category else system.list_products()
            display_products(products)
        
        elif choice == '2':  # View Product Details
            pid = input("Enter product ID: ").strip().upper()
            product = system.get_product(pid)
            if product:
                print(f"\n=== {product.name} ===")
                print(f"ID: {product.id}")
                print(f"Price: ${product.price:.2f}")
                print(f"Category: {product.category}")
                print(f"In Stock: {product.stock}")
                print(f"\nDescription:\n{product.description}")
            else:
                print("Product not found.")
        
        elif choice == '3':  # Add to Cart
            pid = input("Enter product ID: ").strip().upper()
            try:
                qty = int(input("Quantity: ").strip() or "1")
                if qty <= 0:
                    print("Quantity must be positive.")
                    continue
                
                if system.add_to_cart(pid, qty):
                    print(f"Added {qty} x {system.get_product(pid).name} to cart.")
                else:
                    print("Failed to add to cart. Check product ID and stock.")
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == '4':  # View Cart
            display_cart(system.cart, system.products)
        
        elif choice == '5':  # Remove from Cart
            if not system.cart:
                print("Your cart is empty.")
                continue
                
            display_cart(system.cart, system.products)
            pid = input("\nEnter product ID to remove: ").strip().upper()
            
            if pid not in system.cart:
                print("Product not in cart.")
                continue
                
            try:
                qty = input(f"Quantity to remove (max {system.cart[pid].quantity}, or press Enter for all): ").strip()
                if qty:
                    qty = int(qty)
                    if qty <= 0:
                        print("Quantity must be positive.")
                        continue
                else:
                    qty = None
                
                if system.remove_from_cart(pid, qty):
                    print("Item updated in cart.")
                else:
                    print("Failed to update cart.")
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == '6':  # Checkout
            if not system.cart:
                print("Your cart is empty.")
                continue
                
            display_cart(system.cart, system.products)
            confirm = input("\nProceed to checkout? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                name = input("Your name: ").strip()
                if not name:
                    print("Name is required.")
                    continue
                
                order = system.checkout(name)
                if order:
                    print(f"\n✅ Order placed successfully!")
                    print(f"Order ID: {order.order_id}")
                    print(f"Total: ${order.total:.2f}")
                    print("Thank you for your purchase!")
                else:
                    print("Failed to process order. Please try again.")
        
        elif choice == '7':  # View Orders
            customer = input("Enter customer name (or press Enter for all): ").strip()
            orders = [o for o in system.orders.values() 
                     if not customer or o.customer_name.lower() == customer.lower()]
            
            if not orders:
                print("No orders found.")
                continue
            
            display_orders(orders)
            
            order_id = input("\nEnter Order ID to view details (or press Enter to go back): ").strip()
            if order_id and order_id in system.orders:
                display_order_details(system.orders[order_id], system.products)
        
        elif choice == '8':  # Admin: Add Product
            print("\n=== Add New Product ===")
            name = input("Product Name: ").strip()
            if not name:
                print("Name is required.")
                continue
                
            try:
                price = float(input("Price: $").strip())
                if price <= 0:
                    print("Price must be positive.")
                    continue
                    
                description = input("Description: ").strip()
                category = input("Category: ").strip()
                stock = int(input("Initial Stock: ").strip() or "0")
                
                pid = system.add_product(name, price, description, category, stock)
                print(f"\n✅ Product added successfully! ID: {pid}")
            except ValueError:
                print("Invalid input. Please try again.")
        
        elif choice == '9':  # Admin: Update Stock
            pid = input("Enter product ID: ").strip().upper()
            product = system.get_product(pid)
            
            if not product:
                print("Product not found.")
                continue
                
            print(f"\nCurrent stock for {product.name}: {product.stock}")
            
            try:
                change = int(input("Enter quantity to add (negative to remove): ").strip())
                if system.update_product_stock(pid, change):
                    print(f"Stock updated. New stock: {system.get_product(pid).stock}")
                else:
                    print("Failed to update stock.")
            except ValueError:
                print("Please enter a valid number.")
        
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
