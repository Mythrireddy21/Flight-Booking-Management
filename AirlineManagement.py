class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop() if self.stack else None

    def peek(self):
        return self.stack[-1] if self.stack else None

    def is_empty(self):
        return len(self.stack) == 0


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        return self.queue.pop(0) if self.queue else None

    def is_empty(self):
        return len(self.queue) == 0


class Flight:
    def __init__(self, flight_id, origin, destination, time, available_seats):
        self.flight_id = flight_id
        self.origin = origin
        self.destination = destination
        self.time = time
        self.available_seats = available_seats

    def __str__(self):
        return f"Flight {self.flight_id}: {self.origin} -> {self.destination}, Time: {self.time}, Available Seats: {self.available_seats}"


class Ticket:
    def __init__(self, passenger_name, flight):
        self.passenger_name = passenger_name
        self.flight = flight
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add_ticket(self, passenger_name, flight):
        new_ticket = Ticket(passenger_name, flight)
        new_ticket.next = self.head
        self.head = new_ticket

    def cancel_ticket(self, passenger_name, flight_id):
        current = self.head
        prev = None

        while current:
            if current.passenger_name == passenger_name and current.flight.flight_id == flight_id:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next

                current.flight.available_seats += 1  # Restore seat availability
                return True  # Ticket canceled
            prev = current
            current = current.next

        return False  # Ticket not found

    def view_tickets(self):
        current = self.head
        tickets = []
        while current:
            tickets.append(f"{current.passenger_name} - {current.flight}")
            current = current.next
        return tickets


class Array:
    def __init__(self):
        self.flights = []

    def add_flight(self, flight):
        self.flights.append(flight)

    def remove_flight(self, flight_id):
        for flight in self.flights:
            if flight.flight_id == flight_id:
                self.flights.remove(flight)
                return True
        return False

    def get_flights(self):
        return self.flights

    def find_flight(self, flight_id):
        for flight in self.flights:
            if flight.flight_id == flight_id:
                return flight
        return None


# Initialize data structures
ticket_queue = Queue()  # For processing booking requests
ticket_list = LinkedList()  # To store booked tickets
available_flights = Array()  # Store available flights (starts empty)
canceled_tickets_stack = Stack()  # Stack to store canceled tickets for undo functionality

while True:
    print("\n--- Airline Management System ---")
    print("1. Admin Login")
    print("2. Customer Login")
    print("3. Exit")
    user_type = input("Enter your choice: ")

    if user_type == '1':  # Admin panel
        while True:
            print("\n--- Admin Panel ---")
            print("1. Add Flight")
            print("2. Remove Flight")
            print("3. View Available Flights")
            print("4. Logout")
            admin_choice = input("Enter your choice: ")

            if admin_choice == '1':  # Add Flight
                flight_id = int(input("Enter flight ID: "))
                origin = input("Enter origin: ")
                destination = input("Enter destination: ")
                time = input("Enter flight time: ")
                available_seats = int(input("Enter available seats: "))
                flight = Flight(flight_id, origin, destination, time, available_seats)
                available_flights.add_flight(flight)
                print("Flight added successfully!")
            elif admin_choice == '2':  # Remove Flight
                flight_id = int(input("Enter flight ID to remove: "))
                if available_flights.remove_flight(flight_id):
                    print("Flight removed successfully!")
                else:
                    print("Flight not found!")
            elif admin_choice == '3':  # View Available Flights
                print("\nAvailable Flights:")
                flights = available_flights.get_flights()
                if flights:
                    for flight in flights:
                        print(flight)
                else:
                    print("No flights available.")
            elif admin_choice == '4':  # Logout
                break
            else:
                print("Invalid choice. Try again.")

    elif user_type == '2':  # Customer panel
        while True:
            print("\n--- Customer Panel ---")
            print("1. Book Ticket")
            print("2. Process Booking")
            print("3. Cancel Ticket")
            print("4. View Booked Tickets")
            print("5. View Available Flights")
            print("6. Undo Last Canceled Ticket")
            print("7. Logout")
            customer_choice = input("Enter your choice: ")

            if customer_choice == '1':  # Book Ticket
                passenger_name = input("Enter passenger name: ")
                print("\nAvailable Flights:")
                flights = available_flights.get_flights()
                if flights:
                    for flight in flights:
                        print(flight)
                    flight_id = int(input("Enter flight ID to book: "))
                    flight = available_flights.find_flight(flight_id)

                    if flight and flight.available_seats > 0:
                        flight.available_seats -= 1  # Decrease available seats
                        ticket_list.add_ticket(passenger_name, flight)  # Add the booking to the ticket list
                        ticket_queue.enqueue((passenger_name, flight))  # Add the booking to the queue
                        print(f"Ticket booked successfully for {passenger_name} on {flight}")
                    else:
                        print("Flight not available or no seats left.")
                else:
                    print("No flights available to book.")

            elif customer_choice == '2':  # Process Booking
                processed_booking = ticket_queue.dequeue()
                if processed_booking:
                    print(f"Processed Booking: {processed_booking[0]} - {processed_booking[1]}")
                else:
                    print("No bookings to process.")

            elif customer_choice == '3':  # Cancel Ticket
                passenger_name = input("Enter your name: ")
                flight_id = int(input("Enter flight ID to cancel: "))

                if ticket_list.cancel_ticket(passenger_name, flight_id):
                    print(f"Ticket for {passenger_name} on Flight {flight_id} has been canceled.")
                    canceled_tickets_stack.push((passenger_name, flight_id))  # Push canceled ticket to stack
                else:
                    print("Ticket not found. Make sure you entered the correct flight ID.")

            elif customer_choice == '4':  # View Booked Tickets
                print("\nBooked Tickets:")
                tickets = ticket_list.view_tickets()
                if tickets:
                    for ticket in tickets:
                        print(ticket)
                else:
                    print("No tickets booked.")

            elif customer_choice == '5':  # View Available Flights
                print("\nAvailable Flights:")
                flights = available_flights.get_flights()
                if flights:
                    for flight in flights:
                        print(flight)
                else:
                    print("No flights available.")

            elif customer_choice == '6':  # Undo Last Canceled Ticket
                last_canceled = canceled_tickets_stack.pop()
                if last_canceled:
                    passenger_name, flight_id = last_canceled
                    flight = available_flights.find_flight(flight_id)
                    if flight:
                        flight.available_seats -= 1  # Restore seat
                        ticket_list.add_ticket(passenger_name, flight)  # Re-add ticket to booked list
                        print(f"Undid cancellation for {passenger_name} on Flight {flight_id}. Ticket restored.")
                    else:
                        print("Flight not found. Cannot undo cancellation.")
                else:
                    print("No canceled tickets to undo.")

            elif customer_choice == '7':  # Logout
                break

            else:
                print("Invalid choice. Try again.")

    elif user_type == '3':  # Exit
        break
    else:
        print("Invalid choice. Try again.")
