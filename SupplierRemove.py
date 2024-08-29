import socket
import threading
import time
from tabulate import tabulate

from supplier_class import Supplier
from negotation_logic import negotiating
from helpers import order_supplies, search_suppliers_by_ingredient

suppliers_list = []             # List of suppliers of type supplier
print_lock = threading.Lock()   # Lock for thread-safe printing

# Periodically broadcasts "PIZZA" over broadcast port (UDP) to specific broadcast address
def broadcast_presence(broadcast_address, broadcast_port):
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        try:
            message = "PIZZA"
            broadcast_socket.sendto(message.encode(), (broadcast_address, broadcast_port))
            time.sleep(5)
        except KeyboardInterrupt:
            break
    broadcast_socket.close()
def check_connection(p2p_port):
    retry_connection = False

    while True:
        for supplier in suppliers_list:
            try:
                tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_socket.settimeout(10)
                tcp_socket.connect((supplier.ip_address, p2p_port))
                tcp_socket.send(b"ALIVE?")
                response = tcp_socket.recv(1024).decode()
                if response.startswith("YES"):
                    #print(f"Connection with {supplier.name} is alive.")
                    _, name, ip_address, ingredient, quality, quantity = response.split()
                    supplier.name = name
                    supplier.ip_address = ip_address
                    supplier.ingredient = ingredient
                    supplier.quality = quality
                    supplier.quantity = int(quantity)
                    supplier.connection = 1

                    retry_connection = False
            except socket.timeout:
                print(f"\nConnection with {supplier.name} is no longer alive.")
                supplier.connection = 0
                suppliers_list.remove(supplier)
            except ConnectionError:
                print(f"\nThere is an error on connecting with {supplier.name}")
                retry_connection = True
                suppliers_list.remove(supplier)
            finally:
                tcp_socket.close()

        time.sleep(10)  # Adjust the interval as needed


def confirm_connection(p2p_port, me):
    tcp_response_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_response_socket.bind(('0.0.0.0', p2p_port))
    tcp_response_socket.listen(1)

    while True:
        conn, addr = tcp_response_socket.accept()
        #with print_lock:
            #print(f"Received TCP connection from {addr}")
        data = conn.recv(1024).decode()
        if data == "ALIVE?":
            #message = f"YES {myname} {myIP} {myingredient} {myquality} {myquantity}"
            message = f"YES {me.name} {me.ip_address} {me.ingredient} {me.quality} {me.quantity}"
            conn.send(message.encode())
        conn.close()

# Initializes system asking user to enter details
# Starts threads for broadcasting presence, listening for discovery and responses, handling negotiation requests, 
# checking connections, and confirming connections.
# Provides command line interface to list connected peers, negotiate for ingredients, search for suppliers, or quit the program.
def main():
    # my_hostname = socket.gethostname()
    # myIP = socket.gethostbyname(my_hostname)

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
            search_suppliers_by_ingredient(header,suppliers_list)

        if command == "quit":
            running = False


if __name__ == "__main__":
    main()
