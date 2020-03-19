
import random
from Order import Order


class OrderControl:
    """
    OrderControl class tracks the progress of an order from arrival to fulfillment

    Attributes:
       clock: Reference to the SimPy simulation environment
       inventory: Reference to the Inventory subset
       all_orders: List of Order objects that are needed to be fulfilled
       current_order: Order object that we are currently working with
    """
    def __init__(self, env, inventory):
        """
        Inits OrderControl with the SimPy environment and Inventory

        Args:
            env: SimPy simulation environment
            inventory: Inventory object so we can communicate with this subset
        """
        self.clock = env
        self.inventory = inventory
        self.all_orders = []
        self.current_order = None

    def addOrder(self, new_order):
        """
        Adds an new Order to the list of Orders to be fulfilled

        Args:
            new_order: Order object requesting specific Items from the warehouse
        """
        self.all_orders.append(new_order)

    def removeOrder(self, order_to_remove):
        """
        Remove an Order from the list of Orders when completed

        Args:
            order_to_remove: A Order object that will be removed from the list
        """
        self.all_orders.remove(order_to_remove)

    def updateOrder(self, order, new_status):
        """
        Updates the status of an individual Order

        Args:
            order: Order object we are updating the status of
            new_status: String for the Order's new status
        """
        order.updateStatus(new_status)

    def orderStatus(self, order):
        """
        Returns the status of the Order object

        Args:
            order: Order object we are receiving the status for

        Returns:
            The status of the Order object
        """
        return order.getStatus()

    def getCurrentOrder(self):
        """
        Returns the status of the current Order being worked on

        Returns:
            The status of the Order object
        """
        return self.current_order

    def genRandomOrder(self):
        """
        Creates a random Order object with Items from Catalog and adds it to
        OrderControl's list of Orders to complete
        """
        order_items = []
        order_address = self.randomAddress()
        # Choose a random number between 2 - 3 (# of Items)
        order_size = random.randrange(2, 4)
        # Choose a random Item name from Catalog 2 - 3 times
        for i in range(0, order_size):
            item = random.choice(self.inventory.catalog.getItemList())
            item_name = item.getItemName()
            order_items.append(item_name)

        # Create Order instance
        new_order = Order(order_items, order_address)
        # Add Order to Queue
        new_order.status = "In Queue"
        self.addOrder(new_order)

    def randomAddress(self):
        """
        Creates a random address from a variety of popular street name and endings

        Returns:
             order_address: A string representing an address
        """
        address_number = random.randrange(1, 500)
        street_names = ['First', 'Second', 'Third', 'Park', 'Main', 'Oak', 'Pine', 'Maple', 'Cedar', 'Elm', 'Lake']
        address_name = random.choice(street_names)
        address_endings = ['Avenue', 'Court', 'Lane', 'Parkway', 'Road', 'Street', 'Trail']
        address_street = random.choice(address_endings)

        order_address = str(address_number) + ' ' + str(address_name) + ' ' + str(address_street)

        return order_address
