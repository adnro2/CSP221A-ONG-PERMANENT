from abc import ABC
from abc import abstractmethod

class Robot(ABC):
    manufacturer = "Golden Dragon"
    population = 0

    @abstractmethod
    def perform_task(self): pass

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery
        RobotFleet.population += 1

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        if value < 0:
            value = 0
        if value > 100:
            value = 100
        self._battery = value

    def __str__(self):
        return f"{self.name} ({self.battery}% battery)"

    def __repr__(self):
        return f"RobotFleet(name={self.name!r}, battery={self.battery!r})"