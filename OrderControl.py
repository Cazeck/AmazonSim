import random
from Order import Order


# Going to function similarly to RobotScheduler but handling orders instead

class OrderControl:

    def __init__(self, env, inv):
        self.clock = env
        self.inventory = inv
        self.allOrders = []     # a List of orders, dictionary might be necessary
        self.currentOrder = None

        #self.populate()

    def addOrder(self, order):
        # a check to see if there is a duplicate order?
        self.allOrders.append(order)

    def removeOrder(self, order):
        # check to see if an order has been shipped?
        # set order status to cancelled?
        self.allOrders.remove(order)

    # Update the status of an individual order
    def updateOrder(self, order, newStatus):
        order.updateStatus(newStatus)

    # Receive status of an indiviual order
    def orderStatus(self, order):
        return order.getStatus()

    # Current order being worked on
    def getCurrentOrder(self):
        return self.currentOrder

    # Creates a Random Order objects with Items from Catalog
    def genRandomOrder(self):
        order_items = []
        order_address = self.randomAddress()
        # Choose a random number between 2 - 3 (# of Items)
        order_size = random.randrange(2, 4)
        # Choose a random Item from Catalog 2 - 3 times
        for i in range(0, order_size):
            item = random.choice(self.inventory.catalog.getItemList())
            order_items.append(item)

        # Create Order instance
        new_order = Order(order_items, order_address)
        # Add Order to Queue
        self.addOrder(new_order)
        #return new_order

    # Generate random address for an Order
    def randomAddress(self):
        address_number = random.randrange(1, 500)
        street_names = ['First', 'Second', 'Third', 'Park', 'Main', 'Oak', 'Pine', 'Maple', 'Cedar', 'Elm', 'Lake']
        address_name = random.choice(street_names)
        address_endings = ['Avenue', 'Court', 'Lane', 'Parkway', 'Road', 'Street', 'Trail']
        address_street = random.choice(address_endings)

        order_address = str(address_number) + ' ' + str(address_name) + ' ' + str(address_street)

        return order_address

    def populate(self):
        # Create some order instances   #Add Bagpipe bad to order1
        testorders = [Order(['Socks', 'Puck'], "99 Grove Street"),
                    Order(['Tic-Tac', 'Singular Orange'], "290 Whipple Street"),
                    Order(['Hydras Lament', 'Shifters Shield', "Tic-Tac"], "432 Archer Avenue")]


        for i in testorders:
            i.updateStatus('In Queue')
            self.addOrder(i)
