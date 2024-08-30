import socket
from tabulate import tabulate

def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# For sending messages to specific IP address on specific port
def send_response(message, ip, port):
    response_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        response_socket.sendto(message.encode(), (ip, port))
    except:
        print("\nThere was an error sending response")
    finally:
        response_socket.close()

# Prints table of ALIVE suppliers
def order_supplies(suppliers_list):
    data = []
    headers = ["Name", "IP Address", "Ingredient", "Quality", "Quantity"]
    for supplier in suppliers_list:
            data.append([supplier.name, supplier.ip_address, supplier.ingredient, supplier.quality, supplier.quantity])

    print(tabulate(data, headers=headers, tablefmt="grid"))


# Searches for suppliers with specific ingredient
def search_suppliers_by_ingredient(target_ingredient,suppliers_list):
    matching_suppliers_list = []
    for supplier in suppliers_list:
        if supplier.ingredient == target_ingredient:
            matching_suppliers_list.append(supplier)
    data = []
    print("\nSuppliers with " + target_ingredient + "'s")
    headers = ["Name", "IP Address", "Ingredient", "Quality", "Quantity"]
    for supplier in matching_suppliers_list:
            data.append([supplier.name, supplier.ip_address, supplier.ingredient, supplier.quality, supplier.quantity])

    print(tabulate(data, headers=headers, tablefmt="grid"))
