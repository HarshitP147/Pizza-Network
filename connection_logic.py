import time
import socket

def check_connection(p2p_port,suppliers_list):
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
