import json
import os
from datetime import datetime, timedelta
import random

class Transport:
    def __init__(self, transport_type, number, source, destination, departure_time, arrival_time, total_seats, fare):
        self.transport_type = transport_type  # 'bus' or 'train'
        self.number = number  # Bus/Train number
        self.source = source
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.total_seats = total_seats
        self.available_seats = list(range(1, total_seats + 1))
        self.booked_seats = {}  # seat_number: booking_details
        self.fare = fare
    
    def is_seat_available(self, seat_number):
        return seat_number in self.available_seats
    
    def book_seat(self, seat_number, passenger_name, passenger_age, passenger_gender, contact_number):
        if not self.is_seat_available(seat_number):
            return False, "Seat not available"
        
        booking_id = f"{self.transport_type.upper()}{self.number}{seat_number:03d}{random.randint(100, 999)}"
        booking_details = {
            'booking_id': booking_id,
            'passenger_name': passenger_name,
            'passenger_age': passenger_age,
            'passenger_gender': passenger_gender,
            'contact_number': contact_number,
            'seat_number': seat_number,
            'booking_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'confirmed',
            'fare': self.fare
        }
        
        self.booked_seats[seat_number] = booking_details
        self.available_seats.remove(seat_number)
        return True, booking_details
    
    def cancel_booking(self, booking_id):
        for seat_number, booking in self.booked_seats.items():
            if booking['booking_id'] == booking_id:
                self.available_seats.append(seat_number)
                self.available_seats.sort()
                del self.booked_seats[seat_number]
                return True, "Booking cancelled successfully"
        return False, "Booking not found"
    
    def get_booking_details(self, booking_id):
        for booking in self.booked_seats.values():
            if booking['booking_id'] == booking_id:
                return booking
        return None
    
    def to_dict(self):
        return {
            'transport_type': self.transport_type,
            'number': self.number,
            'source': self.source,
            'destination': self.destination,
            'departure_time': self.departure_time,
            'arrival_time': self.arrival_time,
            'total_seats': self.total_seats,
            'available_seats': self.available_seats,
            'booked_seats': self.booked_seats,
            'fare': self.fare
        }

class TicketReservationSystem:
    def __init__(self):
        self.transports = {}
        self.load_data()
    
    def load_data(self):
        if os.path.exists('transport_data.json'):
            try:
                with open('transport_data.json', 'r') as f:
                    data = json.load(f)
                    for transport_id, transport_data in data.items():
                        transport = Transport(
                            transport_data['transport_type'],
                            transport_data['number'],
                            transport_data['source'],
                            transport_data['destination'],
                            transport_data['departure_time'],
                            transport_data['arrival_time'],
                            transport_data['total_seats'],
                            transport_data['fare']
                        )
                        transport.available_seats = transport_data['available_seats']
                        transport.booked_seats = transport_data['booked_seats']
                        self.transports[transport_id] = transport
            except (json.JSONDecodeError, FileNotFoundError):
                self.transports = {}
    
    def save_data(self):
        data = {transport_id: transport.to_dict() for transport_id, transport in self.transports.items()}
        with open('transport_data.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    def add_transport(self, transport_type, number, source, destination, departure_time, arrival_time, total_seats, fare):
        transport_id = f"{transport_type[0].upper()}{number}"  # B123, T456, etc.
        if transport_id in self.transports:
            return False, "Transport with this number already exists"
        
        transport = Transport(transport_type, number, source, destination, departure_time, arrival_time, total_seats, fare)
        self.transports[transport_id] = transport
        self.save_data()
        return True, f"{transport_type.capitalize()} {number} added successfully"
    
    def search_transports(self, source, destination, date=None, transport_type=None):
        results = []
        for transport in self.transports.values():
            if (transport.source.lower() == source.lower() and 
                transport.destination.lower() == destination.lower() and
                (transport_type is None or transport.transport_type == transport_type.lower())):
                
                if date:
                    transport_date = datetime.strptime(transport.departure_time, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d")
                    if transport_date != date:
                        continue
                
                results.append(transport)
        
        return sorted(results, key=lambda x: x.departure_time)
    
    def book_ticket(self, transport_id, seat_number, passenger_details):
        if transport_id not in self.transports:
            return False, "Transport not found"
        
        transport = self.transports[transport_id]
        success, result = transport.book_seat(
            seat_number,
            passenger_details['name'],
            passenger_details['age'],
            passenger_details['gender'],
            passenger_details['contact']
        )
        
        if success:
            self.save_data()
        
        return success, result
    
    def cancel_ticket(self, booking_id):
        for transport in self.transports.values():
            success, message = transport.cancel_booking(booking_id)
            if success:
                self.save_data()
                return True, message
        return False, "Booking not found"
    
    def get_booking_status(self, booking_id):
        for transport in self.transports.values():
            booking = transport.get_booking_details(booking_id)
            if booking:
                return booking
        return None

def display_menu():
    print("\n=== Ticket Reservation System ===")
    print("1. Search Buses/Trains")
    print("2. Book Ticket")
    print("3. Cancel Booking")
    print("4. View Booking Details")
    print("5. Add New Transport (Admin)")
    print("6. View All Transports (Admin)")
    print("7. Exit")

def display_transport(transport, show_seats=False):
    print("\n" + "=" * 80)
    print(f"{transport.transport_type.upper()} {transport.number}")
    print("-" * 80)
    print(f"From:    {transport.source}")
    print(f"To:      {transport.destination}")
    print(f"Dep:     {transport.departure_time}")
    print(f"Arr:     {transport.arrival_time}")
    print(f"Fare:    ${transport.fare}")
    print(f"Seats:   {len(transport.available_seats)}/{transport.total_seats} available")
    
    if show_seats:
        print("\nSeat Layout:")
        seats_per_row = 4
        seat_width = 5
        
        for i in range(0, transport.total_seats, seats_per_row):
            row = transport.available_seats[i:i + seats_per_row]
            for seat in range(1, seats_per_row + 1):
                seat_num = i + seat
                if seat_num > transport.total_seats:
                    break
                status = "[ ]" if seat_num in transport.available_seats else "[X]"
                print(f"{seat_num:02d}{status}", end="\t")
            print()
    
    print("=" * 80)

def get_passenger_details():
    print("\nEnter Passenger Details:")
    name = input("Full Name: ").strip()
    
    while True:
        try:
            age = int(input("Age: "))
            if age <= 0 or age > 120:
                print("Please enter a valid age (1-120)")
                continue
            break
        except ValueError:
            print("Please enter a valid number for age")
    
    gender = ""
    while gender.lower() not in ['m', 'f', 'male', 'female']:
        gender = input("Gender (M/F): ").strip().lower()
        if gender == 'm':
            gender = 'Male'
        elif gender == 'f':
            gender = 'Female'
    
    contact = ""
    while not contact.strip():
        contact = input("Contact Number: ").strip()
    
    return {
        'name': name,
        'age': age,
        'gender': gender,
        'contact': contact
    }

def main():
    system = TicketReservationSystem()
    
    # Add some sample data if none exists
    if not system.transports:
        system.add_transport("bus", "101", "New York", "Boston", "2023-12-01 08:00", "2023-12-01 12:00", 20, 29.99)
        system.add_transport("train", "201", "New York", "Washington DC", "2023-12-01 10:00", "2023-12-01 14:30", 50, 59.99)
        system.add_transport("bus", "102", "Boston", "New York", "2023-12-01 14:00", "2023-12-01 18:00", 20, 29.99)
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':  # Search Buses/Trains
            print("\n=== Search Transports ===")
            source = input("From: ").strip()
            destination = input("To: ").strip()
            date = input("Date (YYYY-MM-DD, press Enter for all dates): ").strip()
            transport_type = input("Type (bus/train, press Enter for all): ").strip().lower()
            
            if transport_type not in ['', 'bus', 'train']:
                print("Invalid transport type. Please enter 'bus' or 'train'.")
                continue
            
            results = system.search_transports(
                source, 
                destination, 
                date if date else None, 
                transport_type if transport_type else None
            )
            
            if not results:
                print("\nNo transports found matching your criteria.")
            else:
                print(f"\n=== Found {len(results)} Transports ===")
                for i, transport in enumerate(results, 1):
                    print(f"\n{i}. {transport.transport_type.upper()} {transport.number}")
                    print(f"   {transport.source} to {transport.destination}")
                    print(f"   Dep: {transport.departure_time} - Arr: {transport.arrival_time}")
                    print(f"   Fare: ${transport.fare} | Seats: {len(transport.available_seats)}/{transport.total_seats} available")
            
            input("\nPress Enter to continue...")
        
        elif choice == '2':  # Book Ticket
            transport_id = input("\nEnter Transport ID (e.g., B101, T201): ").strip().upper()
            
            if transport_id not in system.transports:
                print("Invalid Transport ID")
                continue
            
            transport = system.transports[transport_id]
            display_transport(transport, show_seats=True)
            
            try:
                seat_number = int(input("\nEnter seat number: "))
                if seat_number < 1 or seat_number > transport.total_seats:
                    print("Invalid seat number")
                    continue
            except ValueError:
                print("Please enter a valid seat number")
                continue
            
            passenger_details = get_passenger_details()
            
            print("\nConfirm Booking:")
            print(f"Transport: {transport.transport_type.upper()} {transport.number}")
            print(f"From: {transport.source} To: {transport.destination}")
            print(f"Date: {transport.departure_time.split()[0]}")
            print(f"Seat: {seat_number}")
            print(f"Fare: ${transport.fare}")
            print(f"Passenger: {passenger_details['name']} ({passenger_details['age']} {passenger_details['gender']})")
            
            confirm = input("\nConfirm booking? (yes/no): ").strip().lower()
            if confirm == 'yes':
                success, result = system.book_ticket(transport_id, seat_number, passenger_details)
                if success:
                    print("\n✅ Booking Successful!")
                    print(f"Booking ID: {result['booking_id']}")
                    print(f"Seat: {result['seat_number']}")
                    print(f"Status: {result['status'].upper()}")
                else:
                    print(f"\n❌ Error: {result}")
            else:
                print("\nBooking cancelled")
            
            input("\nPress Enter to continue...")
        
        elif choice == '3':  # Cancel Booking
            booking_id = input("\nEnter Booking ID to cancel: ").strip()
            booking = system.get_booking_status(booking_id)
            
            if not booking:
                print("Booking not found")
                input("\nPress Enter to continue...")
                continue
            
            print("\nBooking Details:")
            print(f"Booking ID: {booking['booking_id']}")
            print(f"Passenger: {booking['passenger_name']}")
            print(f"Seat: {booking['seat_number']}")
            print(f"Status: {booking['status'].upper()}")
            
            confirm = input("\nAre you sure you want to cancel this booking? (yes/no): ").strip().lower()
            if confirm == 'yes':
                success, message = system.cancel_ticket(booking_id)
                print(f"\n{message}")
            else:
                print("\nCancellation aborted")
            
            input("\nPress Enter to continue...")
        
        elif choice == '4':  # View Booking Details
            booking_id = input("\nEnter Booking ID: ").strip()
            booking = system.get_booking_status(booking_id)
            
            if booking:
                print("\n=== Booking Details ===")
                print(f"Booking ID:  {booking['booking_id']}")
                print(f"Status:      {booking['status'].upper()}")
                print(f"Booked On:   {booking['booking_time']}")
                print("\nPassenger Details:")
                print(f"Name:    {booking['passenger_name']}")
                print(f"Age:     {booking['passenger_age']}")
                print(f"Gender:  {booking['passenger_gender']}")
                print(f"Contact: {booking['contact_number']}")
                print(f"\nFare:    ${booking['fare']:.2f}")
            else:
                print("\nBooking not found")
            
            input("\nPress Enter to continue...")
        
        elif choice == '5':  # Add New Transport (Admin)
            print("\n=== Add New Transport (Admin) ===")
            transport_type = ""
            while transport_type.lower() not in ['bus', 'train']:
                transport_type = input("Transport Type (bus/train): ").strip().lower()
            
            number = input("Transport Number: ").strip()
            source = input("Source: ").strip()
            destination = input("Destination: ").strip()
            departure_time = input("Departure Time (YYYY-MM-DD HH:MM): ").strip()
            arrival_time = input("Arrival Time (YYYY-MM-DD HH:MM): ").strip()
            
            try:
                total_seats = int(input("Total Seats: "))
                fare = float(input("Fare: "))
            except ValueError:
                print("Invalid input for seats or fare")
                continue
            
            success, message = system.add_transport(
                transport_type, number, source, destination,
                departure_time, arrival_time, total_seats, fare
            )
            
            print(f"\n{message}")
            input("\nPress Enter to continue...")
        
        elif choice == '6':  # View All Transports (Admin)
            if not system.transports:
                print("\nNo transports found")
            else:
                print("\n=== All Transports ===")
                for transport_id, transport in system.transports.items():
                    display_transport(transport)
            
            input("\nPress Enter to continue...")
        
        elif choice == '7':  # Exit
            print("\nThank you for using the Ticket Reservation System!")
            break
        
        else:
            print("\nInvalid choice! Please enter a number from 1 to 7.")

if __name__ == "__main__":
    main()
