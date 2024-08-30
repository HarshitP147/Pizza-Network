# Supplier class which represents a supplier with all of its details (name, ip_address, ingredient, quality, quantity, connection)
# Contains a method for negotiating based on quantity and quality
class Supplier:
    def __init__(self, name, ip_address, ingredient, quality, quantity, connection):
        self.name = name
        self.ip_address = ip_address
        self.ingredient = ingredient
        self.quality = quality
        self.quantity = int(quantity)  # Quantity of the ingredient available
        self.connection = connection

    def negotiate(self, requested_ingredient, requested_quantity, requested_quality):
        requested_quantity = int(requested_quantity)
        self.quantity = int(self.quantity)
        # Simple negotiation logic: accept if quantity is sufficient and quality matches
        if self.ingredient == requested_ingredient and self.quantity >= requested_quantity and self.quality == requested_quality:
            self.quantity -= requested_quantity  # Deduct the quantity
            print(f"\nNEGOTIATION REQUEST ACCEPTED")
            return "ACCEPTED"
        print(f"\nNEGOTIATION REQUEST REJECTED")
        return "REJECTED"
