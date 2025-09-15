import json
import os
from datetime import datetime

class Product:
    def __init__(self, product_id, name, price, quantity, category, reorder_level=5):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
        self.reorder_level = reorder_level
        self.date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_updated = self.date_added
    
    def update_quantity(self, amount):
        self.quantity += amount
        self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.quantity >= 0  # Returns False if quantity goes negative
    
    def needs_reorder(self):
        return self.quantity <= self.reorder_level
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'category': self.category,
            'reorder_level': self.reorder_level,
            'date_added': self.date_added,
            'last_updated': self.last_updated
        }

class Inventory:
    def __init__(self):
        self.products = {}
        self.categories = set()
        self.load_inventory()
    
    def load_inventory(self):
        if os.path.exists('inventory.json'):
            try:
                with open('inventory.json', 'r') as f:
                    data = json.load(f)
                    for product_id, product_data in data.items():
                        product = Product(
                            product_data['product_id'],
                            product_data['name'],
                            product_data['price'],
                            product_data['quantity'],
                            product_data['category'],
                            product_data.get('reorder_level', 5)
                        )
                        product.date_added = product_data.get('date_added', product.date_added)
                        product.last_updated = product_data.get('last_updated', product.last_updated)
                        self.products[product_id] = product
                        self.categories.add(product.category)
            except (json.JSONDecodeError, FileNotFoundError):
                self.products = {}
                self.categories = set()
    
    def save_inventory(self):
        data = {}
        for product_id, product in self.products.items():
            data[product_id] = product.to_dict()
        with open('inventory.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    def add_product(self, name, price, quantity, category, reorder_level=5):
        product_id = f"P{len(self.products) + 1:03d}"
        product = Product(product_id, name, price, quantity, category, reorder_level)
        self.products[product_id] = product
        self.categories.add(category)
        self.save_inventory()
        return product_id
    
    def update_product(self, product_id, **kwargs):
        if product_id not in self.products:
            return False
        
        product = self.products[product_id]
        
        # Update product attributes
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        product.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_inventory()
        return True
    
    def remove_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            # Rebuild categories set
            self.categories = set(product.category for product in self.products.values())
            self.save_inventory()
            return True
        return False
    
    def search_products(self, query):
        query = query.lower()
        results = []
        for product in self.products.values():
            if (query in product.name.lower() or 
                query in product.product_id.lower() or 
                query in product.category.lower()):
                results.append(product)
        return results
    
    def get_low_stock_items(self, threshold=None):
        if threshold is None:
            return [p for p in self.products.values() if p.needs_reorder()]
        return [p for p in self.products.values() if p.quantity <= threshold]
    
    def get_products_by_category(self, category):
        return [p for p in self.products.values() if p.category.lower() == category.lower()]

def display_menu():
    print("\n=== Inventory Management System ===")
    print("1. View All Products")
    print("2. Add New Product")
    print("3. Update Product")
    print("4. Remove Product")
    print("5. Search Products")
    print("6. View Low Stock Items")
    print("7. View Products by Category")
    print("8. Generate Inventory Report")
    print("9. Exit")

def display_product(product):
    print("\n" + "=" * 70)
    print(f"Product ID:     {product.product_id}")
    print(f"Name:           {product.name}")
    print(f"Category:       {product.category}")
    print(f"Price:          ${product.price:.2f}")
    print(f"Quantity:       {product.quantity}")
    print(f"Reorder Level:  {product.reorder_level}")
    print(f"Status:         {'🟢 In Stock' if product.quantity > 0 else '🔴 Out of Stock'}")
    if product.needs_reorder() and product.quantity > 0:
        print("                ⚠️  Low stock!")
    print(f"\nAdded:          {product.date_added}")
    print(f"Last Updated:   {product.last_updated}")
    print("=" * 70)

def display_products_list(products, title="Products"):
    if not products:
        print("\nNo products found!")
        return
    
    print(f"\n=== {title} ({len(products)}) ===")
    print("-" * 120)
    print("{:<10} {:<30} {:<15} {:<10} {:<10} {:<20} {:<15}".format(
        "ID", "Name", "Category", "Price", "Qty", "Status", "Last Updated"))
    print("-" * 120)
    
    for product in products:
        status = "✅ In Stock"
        if product.quantity == 0:
            status = "❌ Out of Stock"
        elif product.needs_reorder():
            status = "⚠️  Low Stock"
            
        print("{:<10} {:<30} {:<15} ${:<9.2f} {:<10} {:<20} {:<15}".format(
            product.product_id,
            product.name[:28] + '...' if len(product.name) > 28 else product.name,
            product.category[:13] + '...' if len(product.category) > 13 else product.category,
            product.price,
            product.quantity,
            status,
            product.last_updated.split()[0]  # Just the date part
        ))

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")

def main():
    inventory = Inventory()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '1':  # View All Products
            display_products_list(list(inventory.products.values()), "All Products")
            
            # Option to view details of a specific product
            view_details = input("\nEnter product ID to view details (or press Enter to go back): ").strip()
            if view_details and view_details in inventory.products:
                display_product(inventory.products[view_details])
                input("\nPress Enter to continue...")
        
        elif choice == '2':  # Add New Product
            print("\n=== Add New Product ===")
            name = input("Product Name: ").strip()
            if not name:
                print("Product name cannot be empty!")
                continue
                
            price = get_float_input("Price: $")
            quantity = get_int_input("Initial Quantity: ")
            category = input("Category: ").strip()
            reorder_level = get_int_input("Reorder Level (default 5): ") or 5
            
            product_id = inventory.add_product(name, price, quantity, category, reorder_level)
            print(f"\n✅ Product added successfully! Product ID: {product_id}")
        
        elif choice == '3':  # Update Product
            product_id = input("\nEnter product ID to update: ").strip()
            if product_id not in inventory.products:
                print("Product not found!")
                continue
                
            product = inventory.products[product_id]
            display_product(product)
            
            print("\nEnter new values (press Enter to keep current):")
            name = input(f"Name [{product.name}]: ").strip()
            price = input(f"Price [${product.price:.2f}]: $").strip()
            quantity = input(f"Quantity [{product.quantity}]: ").strip()
            category = input(f"Category [{product.category}]: ").strip()
            reorder_level = input(f"Reorder Level [{product.reorder_level}]: ").strip()
            
            updates = {}
            if name:
                updates['name'] = name
            if price:
                try:
                    updates['price'] = float(price)
                except ValueError:
                    print("Invalid price format. Price not updated.")
            if quantity:
                try:
                    updates['quantity'] = int(quantity)
                except ValueError:
                    print("Invalid quantity. Quantity not updated.")
            if category:
                updates['category'] = category
            if reorder_level:
                try:
                    updates['reorder_level'] = int(reorder_level)
                except ValueError:
                    print("Invalid reorder level. Reorder level not updated.")
            
            if updates:
                if inventory.update_product(product_id, **updates):
                    print("\n✅ Product updated successfully!")
                else:
                    print("\n❌ Failed to update product!")
            else:
                print("\nNo changes made.")
        
        elif choice == '4':  # Remove Product
            product_id = input("\nEnter product ID to remove: ").strip()
            if product_id in inventory.products:
                confirm = input(f"Are you sure you want to delete {inventory.products[product_id].name}? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    if inventory.remove_product(product_id):
                        print("\n✅ Product removed successfully!")
                    else:
                        print("\n❌ Failed to remove product!")
            else:
                print("\nProduct not found!")
        
        elif choice == '5':  # Search Products
            query = input("\nEnter search term (name, ID, or category): ").strip()
            if not query:
                print("Please enter a search term.")
                continue
                
            results = inventory.search_products(query)
            display_products_list(results, f"Search Results for '{query}'")
            
            # Option to view details of a specific product
            view_details = input("\nEnter product ID to view details (or press Enter to go back): ").strip()
            if view_details and view_details in inventory.products:
                display_product(inventory.products[view_details])
                input("\nPress Enter to continue...")
        
        elif choice == '6':  # View Low Stock Items
            threshold_input = input("\nEnter threshold (press Enter for default reorder level): ").strip()
            if threshold_input:
                try:
                    threshold = int(threshold_input)
                    low_stock = inventory.get_low_stock_items(threshold)
                    display_products_list(low_stock, f"Items with Quantity ≤ {threshold}")
                except ValueError:
                    print("Invalid threshold. Using default reorder levels.")
                    low_stock = inventory.get_low_stock_items()
                    display_products_list(low_stock, "Items at or Below Reorder Level")
            else:
                low_stock = inventory.get_low_stock_items()
                display_products_list(low_stock, "Items at or Below Reorder Level")
            
            if low_stock:
                input("\nPress Enter to continue...")
        
        elif choice == '7':  # View Products by Category
            print("\nAvailable Categories:")
            categories = sorted(inventory.categories)
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category}")
            
            category_choice = input("\nSelect a category number or enter category name: ").strip()
            if category_choice.isdigit() and 1 <= int(category_choice) <= len(categories):
                selected_category = categories[int(category_choice) - 1]
            else:
                selected_category = category_choice
                
            products = inventory.get_products_by_category(selected_category)
            display_products_list(products, f"Products in Category: {selected_category}")
            
            if products:
                input("\nPress Enter to continue...")
        
        elif choice == '8':  # Generate Inventory Report
            print("\n=== Inventory Report ===")
            total_products = len(inventory.products)
            total_quantity = sum(p.quantity for p in inventory.products.values())
            total_value = sum(p.price * p.quantity for p in inventory.products.values())
            low_stock_count = len(inventory.get_low_stock_items())
            out_of_stock = [p for p in inventory.products.values() if p.quantity == 0]
            
            print(f"Total Products:      {total_products}")
            print(f"Total Quantity:      {total_quantity}")
            print(f"Total Value:         ${total_value:,.2f}")
            print(f"Low Stock Items:     {low_stock_count}")
            print(f"Out of Stock Items:  {len(out_of_stock)}")
            
            if out_of_stock:
                print("\n=== Out of Stock Items ===")
                for product in out_of_stock:
                    print(f"- {product.name} ({product.product_id})")
            
            # Category-wise summary
            print("\n=== Categories Summary ===")
            categories_summary = {}
            for product in inventory.products.values():
                if product.category not in categories_summary:
                    categories_summary[product.category] = {
                        'count': 0,
                        'quantity': 0,
                        'value': 0.0
                    }
                categories_summary[product.category]['count'] += 1
                categories_summary[product.category]['quantity'] += product.quantity
                categories_summary[product.category]['value'] += product.price * product.quantity
            
            print("\n{:<20} {:<10} {:<15} {:<15}".format(
                "Category", "Products", "Total Qty", "Total Value"))
            print("-" * 60)
            for category, data in sorted(categories_summary.items()):
                print("{:<20} {:<10} {:<15} ${:<14,.2f}".format(
                    category[:18] + '..' if len(category) > 18 else category,
                    data['count'],
                    data['quantity'],
                    data['value']))
            
            input("\nPress Enter to continue...")
        
        elif choice == '9':  # Exit
            print("\nThank you for using the Inventory Management System!")
            break
        
        else:
            print("\nInvalid choice! Please enter a number from 1 to 9.")

if __name__ == "__main__":
    main()
