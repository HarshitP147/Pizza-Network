import socket

from helper_func import send_response

# Listens for negotiation requests and responses on negotiation port
# Negotiates based on inventory
# Sends response to requester
def listen_for_negotiation_requests(port,suppliers_list):
    negotiation_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    negotiation_socket.bind(('0.0.0.0', port))
    while True:
        data, sender_address = negotiation_socket.recvfrom(1024)
        message = data.decode()
        print(message)
        if message.startswith("NEGOTIATE"):
            _, ingredient, quantity, quality = message.split()
            for supplier in suppliers_list:
                if supplier.ip_address == sender_address[0]:  # Avoid self-negotiation
                    continue
                response = supplier.negotiate(ingredient, int(quantity), quality)
                response_message = f"NEGOTIATION RESPONSE: {response}"
                send_response(response_message, sender_address[0], port)
                break  # Assuming one supplier per IP for simplicity


# Sends a negotiation request to a specific IP address on p2p port
def send_negotiation_request(target_ip, port, ingredient, quantity, quality):
    """
    Sends a negotiation request to the specified IP address and port.
    """
    message = f"NEGOTIATE {ingredient} {quantity} {quality}"
    send_response(message, target_ip, port)     # helper function

# For entering negotiation request
# Sends this request
def negotiating(negotiation_port):
        try:
            target_ip = input("Enter target IP: ").strip()
            ingredient = input("Enter ingredient: ").strip()
            quantity = int(input("Enter quantity: ").strip())
            quality = input("Enter quality: ").strip()
        except KeyboardInterrupt:
            return

        # Assuming the negotiation port is known and fixed for simplicity
        send_negotiation_request(target_ip, negotiation_port, ingredient, quantity, quality)
