import json
import os
import re
from datetime import datetime

class Contact:
    def __init__(self, name, phone, email=None, address=None, notes=None):
        self.name = name
        self.phone = self._clean_phone(phone)
        self.email = email
        self.address = address
        self.notes = notes
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = self.created_at
    
    def _clean_phone(self, phone):
        # Remove all non-digit characters
        return ''.join(filter(str.isdigit, phone))
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        return {
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'notes': self.notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def matches_search(self, query):
        query = query.lower()
        return (query in self.name.lower() or 
                query in self.phone or 
                (self.email and query in self.email.lower()) or
                (self.address and query in self.address.lower()) or
                (self.notes and query in self.notes.lower()))

class ContactBook:
    def __init__(self):
        self.contacts = {}
        self.load_contacts()
    
    def load_contacts(self):
        if os.path.exists('contacts.json'):
            try:
                with open('contacts.json', 'r') as f:
                    data = json.load(f)
                    for phone, contact_data in data.items():
                        contact = Contact(
                            contact_data['name'],
                            phone,
                            contact_data.get('email'),
                            contact_data.get('address'),
                            contact_data.get('notes')
                        )
                        contact.created_at = contact_data.get('created_at', contact.created_at)
                        contact.updated_at = contact_data.get('updated_at', contact.updated_at)
                        self.contacts[phone] = contact
            except (json.JSONDecodeError, FileNotFoundError):
                self.contacts = {}
    
    def save_contacts(self):
        data = {}
        for phone, contact in self.contacts.items():
            data[phone] = contact.to_dict()
        with open('contacts.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    def add_contact(self, name, phone, email=None, address=None, notes=None):
        contact = Contact(name, phone, email, address, notes)
        self.contacts[contact.phone] = contact
        self.save_contacts()
        return contact
    
    def update_contact(self, phone, **kwargs):
        if phone in self.contacts:
            self.contacts[phone].update(**kwargs)
            # If phone number was updated, we need to update the key
            if 'phone' in kwargs and kwargs['phone'] != phone:
                self.contacts[kwargs['phone']] = self.contacts.pop(phone)
            self.save_contacts()
            return True
        return False
    
    def delete_contact(self, phone):
        if phone in self.contacts:
            del self.contacts[phone]
            self.save_contacts()
            return True
        return False
    
    def search_contacts(self, query):
        results = []
        for contact in self.contacts.values():
            if contact.matches_search(query):
                results.append(contact)
        return results
    
    def get_all_contacts(self):
        return sorted(self.contacts.values(), key=lambda x: x.name.lower())

def display_contact(contact):
    print("\n" + "=" * 50)
    print(f"Name:    {contact.name}")
    print(f"Phone:   {contact.phone}")
    if contact.email:
        print(f"Email:   {contact.email}")
    if contact.address:
        print(f"Address: {contact.address}")
    if contact.notes:
        print(f"Notes:   {contact.notes}")
    print(f"\nCreated:  {contact.created_at}")
    print(f"Updated: {contact.updated_at}")
    print("=" * 50)

def get_valid_phone():
    while True:
        phone = input("Phone Number (digits only, 10+ digits): ").strip()
        if phone.isdigit() and len(phone) >= 10:
            return phone
        print("Please enter a valid phone number (at least 10 digits).")

def get_valid_email():
    while True:
        email = input("Email (or press Enter to skip): ").strip()
        if not email:
            return None
        if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return email
        print("Please enter a valid email address or press Enter to skip.")

def display_menu():
    print("\n=== Contact Book ===")
    print("1. Add New Contact")
    print("2. View All Contacts")
    print("3. Search Contacts")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Exit")

def main():
    contact_book = ContactBook()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':  # Add New Contact
            print("\n=== Add New Contact ===")
            name = input("Full Name: ").strip()
            if not name:
                print("Name cannot be empty!")
                continue
                
            phone = get_valid_phone()
            if phone in contact_book.contacts:
                print("A contact with this phone number already exists!")
                continue
                
            email = get_valid_email()
            address = input("Address (or press Enter to skip): ").strip() or None
            notes = input("Notes (or press Enter to skip): ").strip() or None
            
            contact = contact_book.add_contact(name, phone, email, address, notes)
            print(f"\n✅ Contact '{contact.name}' added successfully!")
            
        elif choice == '2':  # View All Contacts
            contacts = contact_book.get_all_contacts()
            if not contacts:
                print("\nNo contacts found!")
                continue
                
            print(f"\n=== All Contacts ({len(contacts)}) ===")
            for i, contact in enumerate(contacts, 1):
                print(f"{i}. {contact.name} - {contact.phone}")
            
            view_choice = input("\nEnter contact number to view details (or press Enter to go back): ").strip()
            if view_choice.isdigit() and 1 <= int(view_choice) <= len(contacts):
                display_contact(contacts[int(view_choice) - 1])
                
        elif choice == '3':  # Search Contacts
            query = input("\nSearch (name, phone, email, etc.): ").strip()
            if not query:
                print("Please enter a search term.")
                continue
                
            results = contact_book.search_contacts(query)
            if not results:
                print("\nNo matching contacts found!")
                continue
                
            print(f"\n=== Search Results ({len(results)}) ===")
            for i, contact in enumerate(results, 1):
                print(f"{i}. {contact.name} - {contact.phone}")
                
            view_choice = input("\nEnter contact number to view details (or press Enter to go back): ").strip()
            if view_choice.isdigit() and 1 <= int(view_choice) <= len(results):
                display_contact(results[int(view_choice) - 1])
                
        elif choice == '4':  # Update Contact
            search = input("\nEnter contact name or phone number to update: ").strip()
            if not search:
                continue
                
            results = contact_book.search_contacts(search)
            if not results:
                print("\nNo matching contacts found!")
                continue
                
            print("\n=== Matching Contacts ===")
            for i, contact in enumerate(results, 1):
                print(f"{i}. {contact.name} - {contact.phone}")
                
            contact_choice = input("\nSelect contact to update (or press Enter to cancel): ").strip()
            if not contact_choice or not contact_choice.isdigit() or not (1 <= int(contact_choice) <= len(results)):
                continue
                
            contact = results[int(contact_choice) - 1]
            display_contact(contact)
            
            print("\nEnter new details (press Enter to keep current value):")
            name = input(f"Name [{contact.name}]: ").strip() or contact.name
            
            while True:
                phone = input(f"Phone [{contact.phone}]: ").strip() or contact.phone
                if phone == contact.phone or phone not in contact_book.contacts:
                    break
                print("This phone number is already in use by another contact!")
                
            email = input(f"Email [{contact.email or 'None'}]: ").strip()
            if not email and contact.email is not None:
                email = contact.email
            elif email == '':
                email = None
                
            address = input(f"Address [{contact.address or 'None'}]: ").strip()
            if not address and contact.address is not None:
                address = contact.address
            elif address == '':
                address = None
                
            notes = input(f"Notes [{contact.notes or 'None'}]: ").strip()
            if not notes and contact.notes is not None:
                notes = contact.notes
            elif notes == '':
                notes = None
            
            updates = {
                'name': name if name != contact.name else None,
                'phone': phone if phone != contact.phone else None,
                'email': email if email != contact.email else None,
                'address': address if address != contact.address else None,
                'notes': notes if notes != contact.notes else None
            }
            
            if any(updates.values()):  # If any changes were made
                contact_book.update_contact(contact.phone, **{k: v for k, v in updates.items() if v is not None})
                print("\n✅ Contact updated successfully!")
            else:
                print("\nNo changes made to the contact.")
                
        elif choice == '5':  # Delete Contact
            search = input("\nEnter contact name or phone number to delete: ").strip()
            if not search:
                continue
                
            results = contact_book.search_contacts(search)
            if not results:
                print("\nNo matching contacts found!")
                continue
                
            print("\n=== Matching Contacts ===")
            for i, contact in enumerate(results, 1):
                print(f"{i}. {contact.name} - {contact.phone}")
                
            contact_choice = input("\nSelect contact to delete (or press Enter to cancel): ").strip()
            if not contact_choice or not contact_choice.isdigit() or not (1 <= int(contact_choice) <= len(results)):
                continue
                
            contact = results[int(contact_choice) - 1]
            confirm = input(f"\nAre you sure you want to delete {contact.name}? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                if contact_book.delete_contact(contact.phone):
                    print("\n✅ Contact deleted successfully!")
                else:
                    print("\nFailed to delete contact!")
                    
        elif choice == '6':  # Exit
            print("\nThank you for using the Contact Book!")
            break
            
        else:
            print("\nInvalid choice! Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()
