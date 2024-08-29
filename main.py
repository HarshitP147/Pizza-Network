from threading import Thread

from supplier_class import Supplier
from negotation_logic import negotiating

# These are changed according to the requirements
broadcast_port = 21000
p2p_port = 20000
negotiation_port = 22000  # Assuming a different port for negotiation
broadcast_address = '255.255.255.255'   # this means broadcast to all that connects

# Initializes system asking user to enter details
# Starts threads for broadcasting presence, listening for discovery and responses, handling negotiation requests, 
# checking connections, and confirming connections.
# Provides command line interface to list connected peers, negotiate for ingredients, search for suppliers, or quit the program.

def main():
    thread1 = threading.Thread(target=broadcast_presence, args=(broadcast_address, broadcast_port))
    thread2 = threading.Thread(target=listen_for_discovery, args=(broadcast_port, p2p_port, my_details))
    thread3 = threading.Thread(target=listen_for_discovery_response, args=(p2p_port,))
    thread4 = threading.Thread(target=listen_for_negotiation_requests, args=(negotiation_port,))
    thread5 = threading.Thread(target=check_connection, args=(p2p_port,))
    thread6 = threading.Thread(target=confirm_connection, args=(p2p_port, me))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()

    running = True

    my_details = {
        'name': input("Enter supplier name: "),
        'ip': '172.20.10.4',    # add this for dynamic IP allocation
        'ingredient': input("Enter ingredient: "),
        'quantity': int(input("Enter quantity available: ")),
        'quality': input("Enter quality of ingredient\nA - Very high Quality\nB - High Quality\nC - Good Quality\nD - Acceptable Quality\nE - Bad quality\nF - Very bad quality\n")
    }

   
    while my_details['quality'] not in ['A','B','C','D','E','F']:
        print("Invalid ingredient quality")
        my_details['quality'] = input("Enter quality again:")

    me = Supplier(my_details['name'], my_details['ip'], my_details['ingredient'], my_details['quality'], my_details['quantity'], 1)
    suppliers_list.append(me)

    while running:
        print("List of commands:")
        print("1. list = list all the peers connected")
        print("2. negotiate = negotiate for an ingredient")
        print("3. search = search for a person or an ingredient")
        print("4. quit = quit the menu and exit the program")

        command = input("Enter a command:")
        if command == "list":
            order_supplies()

        if command == "negotiate":
            negotiating(negotiation_port)

        if command == "search":
            header = input("Enter what you are searching for:")
            search_suppliers_by_ingredient(header)

        if command == "quit":
            running = False



 if __name__ == "__main__":
     main()
