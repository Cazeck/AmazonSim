from Order import Order

# Going to function similarly to RobotScheduler but handling orders instead


class OrderControl:

    # Should order status' be listed here or within Orders class?

    def __init__(self):
        self.allOrders = []     # a List of orders, dictionary might be necessary
        self.currentOrder = None

        self.populate()

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

    #
    #def complete

    def populate(self):
        # Create some order instances   #Add Bagpipe bad to order1
        testorders = [Order(['Socks', 'Puck'], "99 Grove Street"),
                    Order(['Tic-Tac', 'Singular Orange'], "290 Whipple Street"),
                    Order(['Hydras Lament', 'Shifters Shield', "Tic-Tac"], "432 Archer Avenue")]


        for i in testorders:
            i.updateStatus('In Queue')
            self.addOrder(i)
