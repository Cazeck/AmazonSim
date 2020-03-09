"""
Catalog just holds all of the different Items that inventory can have
"""
from Item import Item

class Catalog:

    def __init__(self):
        self.itemList = [
            Item(547840, "1-Cup Coffee and Espresso Maker"),
            Item(150644, "11lb Kitchen Scale"),
            Item(424962, "12V Power Adapter for Cars"),
            Item(490499, "26-Function Bike Tool"),
            Item(573447, "3-Step Stool"),
            Item(533512, "32 GB SD Card"),
            Item(439305, "34oz Insulated Themos"),
            Item(106510, "4-Quart Tupperware"),
            Item(628751, "4-Tier Cooling Rack"),
            Item(379920, "40 Quart Stock Pot"),
            Item(258065, "5-Bike Rack"),
            Item(372758, "5-Port Networking Switch"),
            Item(136217, "61oz Thermos"),
            Item(898073, "A-Male to Mini-B USB Cable"),
            Item(32794, "A-to-B USB Cable"),
            Item(346139, "AA Battery Charger"),
            Item(305186, "AA Rechargeable Batteries"),
            Item(236580, "Adjustable Basketball Hoop"),
            Item(707622, "Adjustable Dumbbells"),
            Item(896039, "Adjustable Gym Bench"),
            Item(973867, "Air Freshener"),
            Item(501806, "Airtight Container"),
            Item(691247, "Anti-Chafe Balm"),
            Item(538672, "Apple Peeler Contraption"),
            Item(319537, "Apron with Pockets"),
            Item(267316, "Audio Cable"),
            Item(338998, "Audio Contact Cleaner Spray"),
            Item(52279, "Audio-Technica Headphones"),
            Item(316191, "Auto Code Reader"),
            Item(152928, "Backpack"),
            Item(324674, "Backpack Full of Water"),
            Item(460868, "Baguette Pan"),
            Item(76872, "Balance Board"),
            Item(371787, "Basketball"),
            Item(84044, "Battery-Powered Lantern")

            ]

    def getItemList(self):
        return self.itemList

    def createItem(self, item_name):
        name = None
        serial = None

        # Search itemList to see if something with matching name
        for i in self.itemList:
            if i.itemName == item_name:
                name = i.itemName
                serial = i.serialNumber

        return Item(serial, name)


