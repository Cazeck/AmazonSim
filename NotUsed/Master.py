from queue import PriorityQueue


class Master:

    # Create an instance of all components and create the priority queue to store Events
    def __init__(self):
        self.count = 0

        self.robot = tRobot(self)
        self.floor = tFloor(self)
        self.belt = tBelt(self)
        self.inventory = tInventory(self)
        self.order = tOrder(self)
        self.visualizer = tVisualizer(self)
        self.eventqueue = PriorityQueue()

        # Going to need to make Test Classes in Master first to figure eventqueue out
        #self.floor = Floor()
        #self.robotscheduler = RobotScheduler()
        #self.inventory = Inventory()
        #self.ordercontrol = OrderControl()
        # Belt
        # Visualizer
        # Comparator
        #self.eventqueue = PriorityQueue()


    def createEvents(self):
        print("Enqueued Initial Events for for each section")
        self.robot.enqueue('Initial robot event')
        self.floor.enqueue('Initial floor event')
        self.belt.enqueue('Initial belt event')
        self.inventory.enqueue('Initial inventory event')
        self.order.enqueue('Initial order event')
        self.visualizer.enqueue('Initial visualizer event')

    def tickCount(self):
        self.robot.tick(self.count)
        self.floor.tick(self.count)
        self.belt.tick(self.count)
        self.inventory.tick(self.count)
        self.order.tick(self.count)
        self.visualizer.tick(self.count)

    # Return the current time it is
    def getCount(self):
        return self.count

    # Increase the Time by one unit
    def increaseCount(self):
        self.count += 1

    # Look at the head of the Priority Queue without removing the Event
    # this probably wont work
    def peek(self):
        q = self.eventqueue.queue
        if not q:
            return None

        return q[0]

    # Add to the PriorityQueue as (Tick, number, Event)
    def enqueue(self, event):
        # Event number is simply to prevent Priority Queue from comparing
        # Events to each other if queue events are happening on same tick
        toQueue = (event.getTime(), event.number,  event)
        self.eventqueue.put(toQueue)

    # Remove next Event in PriorityQueue
    def dequeue(self):
        return self.eventqueue.get()



# Will be used by the components to create events that need to be completed
class Event:

    totalevents = 0

    def __init__(self, tick, arg, who):
        self.count = tick       # Time that the event was called
        self.argument = arg     # Argument passed by Component
        self.caller = who       # Who (Component) created the Event
        self.number = Event.totalevents + 1    # Done to give each event a unique number
        Event.totalevents += 1

    def getTime(self):
        return self.count

    def getArgument(self):
        return self.argument

    def getWhoCalled(self):
        return self.caller

    def fire(self, argument):
        # Can be the fire method from any of the components, so argument is component?
        print("Firing:", argument)
        #master.enqueue(newEvent)
        #print("Belt event happened at:", self.master.getCount())
        # self.argument
        # self.enqueue("Belt event happened at: ")

        # Can invoke Master.enqueue(newEvent) to add another (future) event

    def __repr__(self):
        return "Event('{}', '{}', {})".format(self.count, self.argument, self.caller)

    def __str__(self):
        return 'Event | Tick: {} -  Argument: {} - Called By: {}'.format(self.count, self.argument, self.caller)


# TEST CLASSES TO BE USED FOR FIGURING OUT HOW QUEUE WILL WORK
# Everything will need tickable and task to be added to it

class tBelt:

    def __init__(self, master):
        self.master = master
        self.currentTime = None

        self.currentBins = []


    def tick(self, count):
        self.currentTime = count

    def fire(self, argument):
        print("Belt event happened at:", self.master.getCount())
        #self.argument
        #self.enqueue("Belt event happened at: ")

        # Can invoke Master.enqueue(newEvent) to add another (future) event

    def enqueue(self, argument):
        event = Event(self.currentTime + 1, argument, self)
        self.master.enqueue(event)

    def addBin(self, bin):
        self.currentBins.append(bin)

class tFloor:

    def __init__(self, master):
        self.master = master
        self.currentTime = None

    def tick(self, count):
        self.currentTime = count

    def fire(self, argument):
        print("Floor event happened at:", self.master.getCount())
        run = argument
        #self.enqueue("Floor event happened at: ")

    def enqueue(self, argument):
        event = Event(self.currentTime + 4, argument, self)
        self.master.enqueue(event)

class tInventory:

    def __init__(self, master):
        self.master = master
        self.currentTime = None

    def tick(self, count):
        self.currentTime = count

    def fire(self, argument):
        print("Inventory event happened at:", self.master.getCount())
        run = argument
        #self.enqueue("Inventory event happened at: ")

    def enqueue(self, argument):
        event = Event(self.currentTime + 6, argument, self)
        self.master.enqueue(event)

class tOrder:

    def __init__(self, master):
        self.master = master
        self.currentTime = None

    def tick(self, count):
        self.currentTime = count

    def fire(self, argument):
        print("Order event happened at:", self.master.getCount())
        run = argument
        #self.enqueue("Order event happened at: ")

    def enqueue(self, argument):
        event = Event(self.currentTime + 5, argument, self)
        self.master.enqueue(event)

class tRobot:

    def __init__(self, master):
        self.master = master
        self.currentTime = None

    def tick(self, count):
        self.currentTime = count

    def fire(self, argument):
        print("Robot event happened at:", self.master.getCount())
        run = argument
        #self.enqueue("Robot event happened at: ")

    def enqueue(self, argument):
        event = Event(self.currentTime + 5, argument, self)
        self.master.enqueue(event)

class tVisualizer:

    def __init__(self, master):
        self.master = master
        self.currentTime = None

    def tick(self, count):
        self.currentTime = count

    def fire(self, argument):
        print("Visualizer event happened at:", self.master.getCount())
        run = argument
        #self.enqueue("Visualizer event happened at: ")

    def enqueue(self, argument):
        event = Event(self.currentTime + 3, argument, self)
        self.master.enqueue(event)


# run for allotted amount of time
def Run(limit):

    master = Master()

    master.tickCount()
    master.createEvents()

    while True:

        master.increaseCount()
        master.tickCount()
        print("\n| Tick:", master.getCount())

        # Stop Running if we've hit the time limit
        if master.getCount() > limit:
            print("Hit the Time Limit")
            break

        # If nothing is in EventQueue, advance a Tick
        if master.peek() is None:
            print("Nothing in Queue")
            continue

        # If the next Event's time matches the current time, execute it)
        while master.peek()[2].getTime() == master.getCount():
            print("Next Event:", master.peek())
            event = master.dequeue()[2]
            component = event.getWhoCalled()
            task = event.getArgument()
            component.fire(task)

            if master.peek() == None:
                break



Run(10)


# Memeing for a bit
#m = Master()

#m.tickCount()
#m.createEvents()

#print("EventQueue after createEvents()")
#print(m.eventqueue.queue)
#print(m.peek())
#print(m.peek()[2])

#print(m.eventqueue.queue)
#print(m.eventqueue.get())


#print(m.peek()[2].getTime() == m.getCount())