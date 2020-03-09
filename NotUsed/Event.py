# Probably goes within Master, but working on it here for now
# These Events will we looped in a Queue within Master
# Every class will create an event when they do something

class Event:

    def __init__(self, tick, arg, who):
        self.count = tick       # Time that the event was called
        self.argument = arg     # Argument passed by Component
        self.caller = who       # Who (Component) created the Event

    def getTime(self):
        return self.count

    def getArgument(self):
        return self.argument

    def getWhoCalled(self):
        return self.caller

    # When called, do whatever the argument is
    def fire(self, argument):
        # Can invoke Master.enqueue(newEvent) to at another future Event to Master's Queue
        print("Meme")
