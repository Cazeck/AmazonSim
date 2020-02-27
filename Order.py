from Item import Item

class Order:

    numoforders = 0

    def __init__(self, items, address):
        self.orderitems =  items    # items will be a list of item names needed
        self.collected = []         # collected will be a list of items that have already been grabbed (in Bin)
        self.shipaddr = address
        self.status = "None"
        self.numoforders += 1
        self.orderid = self.numoforders
        self.fulfilled = False      # are all of the needed items in the bin / packaged?
        self.shipped = False        # has this order been fully completed

    def updateStatus(self, newstatus):
        self.status = newstatus

    def getStatus(self):
        return self.status

    def isFilled(self):
        #ind = 0

        if len(self.orderitems) == len(self.collected):   # if same size, we already checked if the item is okay in add
            self.setFilled()
            print("Order Complete")
            return self.fulfilled

            #for i in self.orderitems:
            #    if i == self.collected[ind]:
            #        ind += 1

            #    else:
            #        print("Order not complete: Item doesnt match")
            #        return self.fulfilled


        print("Order not complete, not full")
        return self.fulfilled

    def setFilled(self):
        self.status = 'Filled'
        self.fulfilled = True

    def getItems(self):
        return self.orderitems

    def collectedItems(self):
        return self.collected

    def ship(self):
        self.shipped = True     # Order fully completed, can be deleted / removed now

    # Adds item to collected if it matched the name of the current item in the order list
    def addItem(self, newitem):
        grabbeditems = len(self.collected)
        if newitem.getItemName() == self.orderitems[grabbeditems]:
            self.collected.append(newitem)

        else:
            print('Thats not the correct item')

    # remove from collected items, not from order list  (is this even needed?)
    # probably better off assuming that orders cannot be changed once made
    def removeItem(self, item):
        self.collected.remove(item)

    # Umambiguous reperestation of object, used for debugging / loggin - seen for developers
    # Item('Bong', 67090, 4)

    def __repr__(self):
        return "Order('{}', {}, {}, {})".format(self.shipaddr, self.status, self.orderitems, self.collected)

    # readable representation of an object, used for display to end users
    # Item: Hydras Lament - Serial No: 11008 - Shelf: None

    def __str__(self):
        return '|Address: {} - Status: {}  \n| Order:     {} \n| Collected: {}'.format(self.orderid, self.shipaddr, self.status, self.orderitems, self.collected)


#item1 = Item('Bagpipe', 51009)
#item2 = Item('Tic-Tac', 57678)
#item3 = Item('Hydras Lament', 11008)
#item4 = Item('Socks', 13009)
#item5 = Item('Puck', 34678)
#item6 = Item('Shifters Shield', 81035)
#item7 = Item('Tic-Tac', 57678)
#item8 = Item('Singular Orange', 34231)

#orderList1 = [item1, item3, item5]
#orderList2 = [item2, item4, item6]

#order = Order(orderList1, '104 Meme Avenue')

#print('orderitems')
#print(order.orderitems)

#print('collected')
#print(order.collected)

#order.addItem(item1)

#print('collected')
#print(order.collected)

#order.addItem(item2)
#order.addItem(item3)

#print(order.collected)
#print(order.isFilled())


#order.addItem(item5)

#print(order.isFilled())

#print(order)

