
class Order:
    """
    Order class represent the order that a customer would make on a website

    These orders consist of a list of Item names from the Catalog's lists of items.
    It will also have an address that all of these Items be shipped to

    Class Variables:
        num_of_orders: A integer used to count the total number of orders

    Attributes:
        order_items: A list of Item names, these are the Items needed to be grabbed
        collected: A list of Items from order_items that has been satisfied
        ship_address: A string representing and address to send the Items to
        status: A string telling the Order's current status (Not Used)
        order_id: A integer used to name each unique order
    """
    num_of_orders = 0

    def __init__(self, items, address):
        """
        Inits Order with a list of Items and an address to ship to

        Args:
            items: A list of strings that are the names of items the customer wants
            address: A a string of the location to send the items when the order is fulfilled
        """
        self.order_items = items
        self.collected = []
        self.ship_address = address
        self.status = "None"
        self.fulfilled = False

        self.order_id = Order.num_of_orders + 1
        Order.num_of_orders += 1

    def updateStatus(self, new_status):
        """
        Updates the status string of the Order

        Args:
            new_status: A string of the Order's current status
        """
        self.status = new_status

    def getStatus(self):
        """
        Returns the status of the Order

        Returns:
            String of the Order's status
        """
        return self.status

    def isFilled(self):
        """
        Checks to see if all of the Items needed for the Order have been collected

        If so, change the Order to fulfilled

        Returns:
            A boolean whether or not the Order has been satisfied
        """
        # Check if these are the same size
        # We already checked if the Items are correct when adding
        if len(self.order_items) == len(self.collected):
            self.setFilled()
            print("We have all items for the order!")
            return self.fulfilled

        print("Order not complete, not full")
        return self.fulfilled

    def setFilled(self):
        """
        Changes the order status to 'Filled' and sets fulfilled to be True
        """
        self.status = 'Filled'
        self.fulfilled = True

    def getItems(self):
        """
        Returns the list of Items wanted in the Order

        Returns:
            A list of strings containing each Item
        """
        return self.order_items

    def getShipAddr(self):
        """
        Returns the address of the Order

        Returns:
            A string representing the address
        """
        return self.ship_address

    def collectedItems(self):
        """
        Returns the Shelf that the Item is on

        Returns:
            The Shelf object that this Item is located at
        """
        return self.collected

    # Adds item to collected if it matched the name of the current item in the order list
    def addItem(self, new_item):
        """
        Adds an Item to the collected attribute. That means that item has been collected
        and we can move on to the next one

        Args:
            new_item: A Item object that has been successfully grabbed

        Raises:
            Exception: Wrong item is trying to be added
        """
        grabbed_items = len(self.collected)
        if new_item.getItemName() == self.order_items[grabbed_items]:
            self.collected.append(new_item)

        else:
            raise Exception(f'Item {new_item} is not the correct item for this order')

    def __repr__(self):
        """
        Unambiguous representation of Order object

        Used for debugging and logging

        Returns:
            In the format: Order(address, status, order_items, collected)
            Ex: Shelf('101 North Ave', 'Grabbing Items', ['Handbag', 'T-Shirt'], [None])
        """
        return "Order('{}', {}, {}, {})".format(self.ship_address, self.status, self.order_items, self.collected)

    def __str__(self):
        """
        Readable representation of Order object

        Used for display

        Returns:
            In the format:
            Order Id: 2 - Ship Address: '101 North Ave' - Status 'Grabbing Items'
            Order: ['Handbag', 'T-Shirt']
            Collected: [Handbag]
        """
        return 'Order Id: {} - Ship Address: {} - Status: {} \nOrder: {} \nCollected: {}'.format(self.order_id,
                                                                                                     self.ship_address,
                                                                                                     self.status,
                                                                                                     self.order_items,
                                                                                                     self.collected)
