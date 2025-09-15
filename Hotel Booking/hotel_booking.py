import json
import os
from datetime import datetime, timedelta

class Room:
    def __init__(self, room_number, room_type, price_per_night, capacity):
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.capacity = capacity
        self.amenities = []
        self.is_available = True
        self.bookings = []
    
    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)
    
    def is_room_available(self, check_in, check_out):
        if not self.is_available:
            return False
            
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        
        for booking in self.bookings:
            booking_start = datetime.strptime(booking['check_in'], "%Y-%m-%d")
            booking_end = datetime.strptime(booking['check_out'], "%Y-%m-%d")
            
            # Check for date overlap
            if (check_in_date < booking_end and check_out_date > booking_start):
                return False
        return True
    
    def book_room(self, guest_name, check_in, check_out, num_guests):
        if not self.is_room_available(check_in, check_out):
            return False
            
        if num_guests > self.capacity:
            return False
            
        booking = {
            'guest_name': guest_name,
            'check_in': check_in,
            'check_out': check_out,
            'num_guests': num_guests,
            'booking_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'confirmed'
        }
        
        self.bookings.append(booking)
        return True
    
    def cancel_booking(self, guest_name, check_in):
        for booking in self.bookings:
            if booking['guest_name'] == guest_name and booking['check_in'] == check_in:
                booking['status'] = 'cancelled'
                return True
        return False
    
    def to_dict(self):
        return {
            'room_number': self.room_number,
            'room_type': self.room_type,
            'price_per_night': self.price_per_night,
            'capacity': self.capacity,
            'amenities': self.amenities,
            'is_available': self.is_available,
            'bookings': self.bookings
        }

class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = {}
        self.load_data()
    
    def load_data(self):
        if os.path.exists('hotel_data.json'):
            try:
                with open('hotel_data.json', 'r') as f:
                    data = json.load(f)
                    for room_num, room_data in data.items():
                        room = Room(
                            room_data['room_number'],
                            room_data['room_type'],
                            room_data['price_per_night'],
                            room_data['capacity']
                        )
                        room.amenities = room_data.get('amenities', [])
                        room.is_available = room_data.get('is_available', True)
                        room.bookings = room_data.get('bookings', [])
                        self.rooms[room_num] = room
            except (json.JSONDecodeError, FileNotFoundError):
                self.rooms = {}
    
    def save_data(self):
        data = {room.room_number: room.to_dict() for room in self.rooms.values()}
        with open('hotel_data.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    def add_room(self, room_number, room_type, price_per_night, capacity):
        if room_number in self.rooms:
            return False
        self.rooms[room_number] = Room(room_number, room_type, price_per_night, capacity)
        self.save_data()
        return True
    
    def find_available_rooms(self, check_in, check_out, room_type=None, min_capacity=1):
        available_rooms = []
        for room in self.rooms.values():
            if room_type and room.room_type != room_type:
                continue
            if room.capacity < min_capacity:
                continue
            if room.is_room_available(check_in, check_out):
                available_rooms.append(room)
        return available_rooms
    
    def book_room(self, room_number, guest_name, check_in, check_out, num_guests):
        if room_number not in self.rooms:
            return False, "Room not found"
        
        room = self.rooms[room_number]
        if room.book_room(guest_name, check_in, check_out, num_guests):
            self.save_data()
            total_nights = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
            total_cost = total_nights * room.price_per_night
            return True, f"Booking successful! Total cost: ${total_cost:.2f} for {total_nights} nights."
        return False, "Room not available for the selected dates"
    
    def cancel_booking(self, room_number, guest_name, check_in):
        if room_number not in self.rooms:
            return False, "Room not found"
        
        room = self.rooms[room_number]
        if room.cancel_booking(guest_name, check_in):
            self.save_data()
            return True, "Booking cancelled successfully"
        return False, "Booking not found"
    
    def get_room_details(self, room_number):
        if room_number not in self.rooms:
            return None
        return self.rooms[room_number]

def display_menu():
    print("\n=== Hotel Booking System ===")
    print("1. View Available Rooms")
    print("2. Book a Room")
    print("3. Cancel Booking")
    print("4. View Room Details")
    print("5. Add New Room (Admin)")
    print("6. Exit")

def get_date_input(prompt):
    while True:
        date_str = input(prompt + " (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def main():
    hotel = Hotel("Grand Hotel")
    
    # Add some sample rooms if none exist
    if not hotel.rooms:
        hotel.add_room("101", "Single", 99.99, 1)
        hotel.add_room("102", "Double", 149.99, 2)
        hotel.add_room("201", "Deluxe", 199.99, 2)
        hotel.add_room("202", "Suite", 299.99, 4)
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':  # View Available Rooms
            print("\n=== Available Rooms ===")
            check_in = get_date_input("Enter check-in date")
            check_out = get_date_input("Enter check-out date")
            
            room_type = input("Enter room type (or press Enter for all types): ").strip()
            try:
                min_capacity = int(input("Enter minimum capacity (default 1): ") or "1")
            except ValueError:
                min_capacity = 1
            
            available_rooms = hotel.find_available_rooms(check_in, check_out, room_type or None, min_capacity)
            
            if not available_rooms:
                print("\nNo available rooms match your criteria.")
            else:
                print("\n{:<10} {:<15} {:<10} {:<10} {:<15}".format(
                    "Room #", "Type", "Price/Night", "Capacity", "Amenities"))
                print("-" * 70)
                for room in available_rooms:
                    print("{:<10} {:<15} ${:<9.2f} {:<10} {}".format(
                        room.room_number,
                        room.room_type,
                        room.price_per_night,
                        f"{room.capacity} person" + ("" if room.capacity == 1 else "s"),
                        ", ".join(room.amenities) if room.amenities else "None"
                    ))
        
        elif choice == '2':  # Book a Room
            print("\n=== Book a Room ===")
            room_number = input("Enter room number: ").strip()
            guest_name = input("Enter guest name: ").strip()
            check_in = get_date_input("Enter check-in date")
            check_out = get_date_input("Enter check-out date")
            
            try:
                num_guests = int(input("Enter number of guests: "))
            except ValueError:
                print("Invalid number of guests.")
                continue
            
            success, message = hotel.book_room(room_number, guest_name, check_in, check_out, num_guests)
            print(f"\n{'✅ ' if success else '❌ '}{message}")
        
        elif choice == '3':  # Cancel Booking
            print("\n=== Cancel Booking ===")
            room_number = input("Enter room number: ").strip()
            guest_name = input("Enter guest name: ").strip()
            check_in = input("Enter check-in date (YYYY-MM-DD): ").strip()
            
            success, message = hotel.cancel_booking(room_number, guest_name, check_in)
            print(f"\n{'✅ ' if success else '❌ '}{message}")
        
        elif choice == '4':  # View Room Details
            room_number = input("\nEnter room number: ").strip()
            room = hotel.get_room_details(room_number)
            
            if not room:
                print("Room not found!")
                continue
                
            print(f"\n=== Room {room.room_number} Details ===")
            print(f"Type: {room.room_type}")
            print(f"Price per night: ${room.price_per_night:.2f}")
            print(f"Capacity: {room.capacity} person" + ("" if room.capacity == 1 else "s"))
            print(f"Amenities: {', '.join(room.amenities) if room.amenities else 'None'}")
            
            if room.bookings:
                print("\n=== Booking History ===")
                for booking in room.bookings:
                    print(f"\nGuest: {booking['guest_name']}")
                    print(f"Check-in: {booking['check_in']}")
                    print(f"Check-out: {booking['check_out']}")
                    print(f"Guests: {booking['num_guests']}")
                    print(f"Status: {booking['status']}")
                    print(f"Booked on: {booking['booking_date']}")
        
        elif choice == '5':  # Add New Room (Admin)
            print("\n=== Add New Room (Admin Only) ===")
            room_number = input("Enter room number: ").strip()
            
            if room_number in hotel.rooms:
                print("Room already exists!")
                continue
                
            room_type = input("Enter room type (e.g., Single, Double, Suite): ").strip()
            
            try:
                price = float(input("Enter price per night: "))
                capacity = int(input("Enter room capacity: "))
            except ValueError:
                print("Invalid price or capacity!")
                continue
            
            if hotel.add_room(room_number, room_type, price, capacity):
                print(f"\n✅ Room {room_number} added successfully!")
            else:
                print("\n❌ Failed to add room!")
        
        elif choice == '6':  # Exit
            print("\nThank you for using the Hotel Booking System!")
            break
        
        else:
            print("\nInvalid choice! Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()
