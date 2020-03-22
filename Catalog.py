
from Item import Item


class Catalog:
    """
    Catalog is simply a collection of all of the possible Item objects we can use in this sumulation

    Can also generate new instances of Items that are within the Catalog

    Attributes:
        item_list: A list of Item Objects
    """
    def __init__(self):
        """
        Inits Catalog with a list of all possible Items
        """
        self.item_list = [
            Item(547840, "1-Cup Coffee and Espresso Maker"),
            Item(150644, "11lb Kitchen Scale"),
            Item(424962, "12V Power Adapter for Cars"),
            Item(573447, "3-Step Stool"),
            Item(533512, "32 GB SD Card"),
            Item(439305, "34oz Insulated Themos"),
            Item(106510, "4-Quart Tupperware"),
            Item(258065, "5-Bike Rack"),
            Item(372758, "5-Port Networking Switch"),
            Item(136217, "61oz Thermos"),
            Item(898073, "A-Male to Mini-B USB Cable"),
            Item(32794, "A-to-B USB Cable"),
            Item(346139, "AA Battery Charger"),
            Item(305186, "AA Rechargeable Batteries"),
            Item(973867, "Air Freshener"),
            Item(319537, "Apron with Pockets"),
            Item(267316, "Audio Cable"),
            Item(316191, "Auto Code Reader"),
            Item(152928, "Backpack"),
            Item(324674, "Backpack Full of Water"),
            Item(460868, "Baguette Pan"),
            Item(76872, "Balance Board"),
            Item(371787, "Basketball"),
            Item(84044, "Battery-Powered Lantern"),
            Item(385102, "Beer Mug Set"),
            Item(823226, "Bidet"),
            Item(229467, "Bike Mirror"),
            Item(970854, "Bike Tail Light"),
            Item(130748, "Blender Bottle"),
            Item(170103, "Bookshelf Speakers"),
            Item(139797, "Bottle Opener"),
            Item(951434, "Bread Knife"),
            Item(527503, "Brownie Pan"),
            Item(29846, "Butter Crock"),
            Item(931995, "Can Opener"),
            Item(815265, "Car Battery Monitor"),
            Item(954547, "Cleaning Pads"),
            Item(84513, "Cutting Board"),
            Item(595145, "Cycling Helmet Mirror"),
            Item(878795, "Cycling Shorts"),
            Item(192719, "DVD+R Discs (8.5 GB)"),
            Item(520544, "Danish Dough Whisk"),
            Item(578771, "Digital Bathroom Scale"),
            Item(748763, "Digital Kitchen Scale"),
            Item(796905, "Drinking Glasses"),
            Item(91687, "Dry Bag"),
            Item(259450, "Dryer vent cleaning system"),
            Item(745712, "Drying Rack"),
            Item(891433, "Dumbbell Rack"),
            Item(374709, "Egg / Bacon Microwave Cooker"),
            Item(452859, "Egg Beater"),
            Item(148733, "Electric Duster Vacuum"),
            Item(590089, "Electric Meat Grinder"),
            Item(582932, "Electric Scooter"),
            Item(241881, "Electric Smoker"),
            Item(828697, "Electric Wok"),
            Item(920858, "Elevation Training Gear"),
            Item(621860, "Ethernet Cable"),
            Item(916785, "Fake TV Burglar Deterrent"),
            Item(978234, "Fire Starter"),
            Item(876529, "First Aid Kit"),
            Item(155989, "Foam Roller"),
            Item(977238, "Foldable Laundry Bin"),
            Item(144728, "Folding Laundry Basket"),
            Item(385373, "Food Coloring Set"),
            Item(374235, "Food Dehydrator and Jerky Maker"),
            Item(465271, "Fruit Corer"),
            Item(827768, "Fruit and Vegetable Wash"),
            Item(222585, "Frying Pan Set"),
            Item(703866, "Garage Door Remote"),
            Item(615817, "Golf Bag"),
            Item(230105, "Golf Balls"),
            Item(224678, "Grocery Bag Holder"),
            Item(582055, "HD 3D Plasma TV"),
            Item(33198, "Handheld Blender"),
            Item(147914, "Home Theater Speakers"),
            Item(370123, "Huge Portable Hammock"),
            Item(173986, "Ice Cream Scooper"),
            Item(650713, "Inflatable Boat"),
            Item(89562, "Inflatable Kayak"),
            Item(281078, "Knife Sharpener"),
            Item(216490, "LED Flashlight"),
            Item(714837, "LED Keychain Light"),
            Item(167426, "Ladybug Night Light"),
            Item(726532, "Laminating Machine Combo Pack"),
            Item(578053, "Lapdesk Laptop Speaker"),
            Item(394760, "Laptop Stand"),
            Item(487950, "Lasagna Trio Pan"),
            Item(896533, "Legit Dartboard"),
            Item(927254, "Letter Opener"),
            Item(781913, "Lithium Batteries"),
            Item(958833, "Machete Knife"),
            Item(723504, "Magnifying Glass"),
            Item(20032, "Massage Stick"),
            Item(856643, "Measuring Cups"),
            Item(168516, "Meat Tenderizer"),
            Item(854597, "Mega Plunger"),
            Item(357981, "Mortar and Pestle"),
            Item(574051, "Mouse Trap"),
            Item(339573, "Nonstick Frying Pan"),
            Item(273023, "Outdoor Party Game"),
            Item(921231, "Pasta Machine"),
            Item(31379, "Pedal-less Bike"),
            Item(339604, "Pedometer"),
            Item(626330, "Peeler"),
            Item(515355, "Pepper Grinder"),
            Item(822949, "Personal Fan"),
            Item(706215, "Pet Food Container"),
            Item(418759, "Pie Crust Maker"),
            Item(740014, "Pineapple Slicer and De-Corer"),
            Item(268979, "Ping Pong Paddle"),
            Item(957109, "Pitching Machine"),
            Item(206518, "Pizza Cutter"),
            Item(885876, "Pizza Oven Thing"),
            Item(26911, "Pizza Pan"),
            Item(758460, "Pizza and Baking Stone"),
            Item(615120, "Pocket Rescusitator"),
            Item(277208, "Portable Folding Chair"),
            Item(405209, "Portable Gas Grill"),
            Item(448222, "Portable Stove"),
            Item(193253, "Potato Ricer"),
            Item(26347, "Power Strip"),
            Item(714476, "Pressure Cooker"),
            Item(516855, "Programmable Lego Robot"),
            Item(228091, "Programmable Switch"),
            Item(666364, "Propulsion Scooter"),
            Item(902919, "Punching Bag"),
            Item(311059, "Reusable Grocery Bags"),
            Item(605467, "Rice Cooker"),
            Item(607004, "Rolling Pin"),
            Item(336572, "Rowing Machine"),
            Item(261924, "Rust Stain Remover"),
            Item(688945, "Sausage Stuffer"),
            Item(197417, "Scissors"),
            Item(792364, "Scooter"),
            Item(325426, "Scotch Tape"),
            Item(378676, "Shoe Rack"),
            Item(227133, "Silverware Tray"),
            Item(398144, "Simple Projector"),
            Item(735053, "Skateboard"),
            Item(64336, "Skateboard Ramp Kit"),
            Item(654136, "Sleeping Bag"),
            Item(4950, "Smoke Detector"),
            Item(214329, "Snorkel Equipment"),
            Item(768860, "Snow Cone Maker"),
            Item(127837, "Solo Raft"),
            Item(190304, "Soup and Drink Thermos"),
            Item(28523, "Spice Rack"),
            Item(601964, "Spinning Organizer"),
            Item(401558, "Steak Knives"),
            Item(112791, "Storage Bin"),
            Item(240526, "Strawberry Stem Remover"),
            Item(722925, "Super-Soft, Absorbant Towel"),
            Item(165777, "Sushi Maker"),
            Item(919455, "TV Stand"),
            Item(209826, "TV mount"),
            Item(845979, "Table Tennis Set"),
            Item(981927, "Tactile Keyboard"),
            Item(253874, "Thermos Travel Mug"),
            Item(80819, "Tiny Portable Speakers"),
            Item(364472, "Tongs"),
            Item(874425, "Toothbrush Holder"),
            Item(255937, "Trash Can"),
            Item(411422, "USB Wi-Fi Adapter"),
            Item(48067, "Utensil Holder"),
            Item(139219, "Velcro Cable Ties"),
            Item(692184, "Volleyball"),
            Item(613341, "Waffle Maker"),
            Item(841499, "Whiskey Glass"),
            Item(243691, "Wine Aerator"),
            Item(879597, "Wine Saver"),
            Item(522223, "Wireless Camera"),
            Item(400368, "Wireless Mouse"),
            Item(758769, "Wok"),
            Item(175094, "Yoga Mat")]

    def getItemList(self):
        """
        Returns the list of Item Objects

        Returns:
            List of Item Objects
        """
        return self.item_list

    def createItem(self, item_name):
        """
        Creates a new instance of an Item object that is within the Catalog

        Args:
            item_name: A string that is an item name

        Returns:
            Item object matching the name of item_name
        """
        name = None
        serial = None

        # Search item_list to see if something with matching name
        for i in self.item_list:
            if i.getItemName() == item_name:
                name = i.getItemName()
                serial = i.getSerialNumber()

        return Item(serial, name)
