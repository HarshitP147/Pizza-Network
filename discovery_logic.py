import socket
import threading

from discovery_logic import send_

# Listens for "PIZZA" on broadcast port (UDP)
# When receives "PIZZA" responds on p2p port with details
def listen_for_discovery(discovery_port, p2p_port, my_details):
    discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_socket.bind(('0.0.0.0', discovery_port))
    while True:
        data, sender_address = discovery_socket.recvfrom(1024)
        message = data.decode()
        if message.startswith("PIZZA"):
            response_message = f"DETAILS {my_details['name']} {my_details['ip']} {my_details['ingredient']} {my_details['quality']} {my_details['quantity']}"
            send_response(response_message, sender_address[0], p2p_port)

# Listens for p2p response to "PIZZA" with details
# If supplier not already in list, adds them in
def listen_for_discovery_response(p2p_port):
    discovery_received_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_received_socket.bind(('0.0.0.0', p2p_port))
    while True:
        data, sender_address = discovery_received_socket.recvfrom(1024)
        message = data.decode()
        if message.startswith("DETAILS"):
            _, name, ip_address, ingredient, quality, quantity = message.split()
            if not any(supplier.name == name for supplier in suppliers_list):
                new_supplier = Supplier(name, ip_address, ingredient, quality, quantity, 1)
                suppliers_list.append(new_supplier)
                print(f"\nNew memebr {name} has joined the network")



