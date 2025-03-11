class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop() if self.stack else None

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


class Node:
    def __init__(self, passenger, flight):
        self.passenger = passenger
        self.flight = flight
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def book_ticket(self, passenger, flight):
        new_node = Node(passenger, flight)
        new_node.next = self.head
        self.head = new_node

    def remove_ticket(self, passenger, flight):
        current = self.head
        prev = None
        while current:
            if current.passenger == passenger and current.flight == flight:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False

    def view_tickets(self):
        current = self.head
        tickets = []
        while current:
            tickets.append(f"{current.passenger} - {current.flight}")
            current = current.next
        return tickets


class Array:
    def __init__(self):
        self.flights = []

    def add_flight(self, flight):
        self.flights.append(flight)
        self.flights.sort()

    def remove_flight(self, flight):
        if flight in self.flights:
            self.flights.remove(flight)

    def get_flights(self):
        return self.flights


# Initialize data structures
undo_stack = Stack()
booking_queue = Queue()
ticket_list = LinkedList()
available_flights = Array()

while True:
    print("\n1. Admin Login\n2. Customer Login\n3. Exit")
    user_type = input("Enter your choice: ")

    if user_type == '1':  # Admin Panel
        while True:
            print("\n--- Admin Panel ---")
            print("1. Add Flight\n2. Remove Flight\n3. View Available Flights\n4. Logout")
            admin_choice = input("Enter your choice: ")

            if admin_choice == '1':
                flight = input("Enter flight details: ")
                available_flights.add_flight(flight)
                print("Flight added successfully!")
            elif admin_choice == '2':
                flight = input("Enter flight details to remove: ")
                available_flights.remove_flight(flight)
                print("Flight removed successfully!")
            elif admin_choice == '3':
                print("Available Flights:", available_flights.get_flights())
            elif admin_choice == '4':
                break
            else:
                print("Invalid choice. Try again.")

    elif user_type == '2':  # Customer Panel
        while True:
            print("\n--- Customer Panel ---")
            print("1. Book Ticket\n2. Process Booking\n3. Undo Last Booking\n4. View Booked Tickets\n5. View Available Flights\n6. Logout")
            customer_choice = input("Enter your choice: ")

            if customer_choice == '1':
                passenger = input("Enter passenger name: ")
                flight = input("Enter flight details: ")
                if flight in available_flights.get_flights():
                    undo_stack.push((passenger, flight))
                    ticket_list.book_ticket(passenger, flight)
                    booking_queue.enqueue((passenger, flight))
                    print("Ticket booked successfully!")
                else:
                    print("Flight not available.")
            elif customer_choice == '2':
                processed_booking = booking_queue.dequeue()
                if processed_booking:
                    print("Processed Booking:", processed_booking)
                else:
                    print("No bookings to process.")
            elif customer_choice == '3':
                last_booking = undo_stack.pop()
                if last_booking:
                    passenger, flight = last_booking
                    if ticket_list.remove_ticket(passenger, flight):
                        print(f"Undo Last Booking: {passenger} - {flight}")
                    else:
                        print("No previous booking found.")
                else:
                    print("No booking to undo.")
            elif customer_choice == '4':
                print("Booked Tickets:", ticket_list.view_tickets())
            elif customer_choice == '5':
                print("Available Flights:", available_flights.get_flights())
            elif customer_choice == '6':
                break
            else:
                print("Invalid choice. Try again.")

    elif user_type == '3':  # Exit
        break
    else:
        print("Invalid choice. Try again.")
