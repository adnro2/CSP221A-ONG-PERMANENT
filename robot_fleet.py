from abc import ABC, abstractmethod


class InsufficientBatteryError(Exception):
    """Raised when a robot attempts an action without sufficient battery."""

    def __init__(self, robot_name, available_battery, required_battery):
        message = f"Robot '{robot_name}' has insufficient battery. Available: {available_battery}%, Required: {required_battery}%."
        super().__init__(message)
        self.robot_name = robot_name
        self._battery = available_battery
        self.requiredBattery = required_battery

class Robot(ABC):
    manufacturer = "Golden Dragon"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery
        Robot.population += 1

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        self._battery = value

    def use_battery(self, amount):
        if self.battery >= amount:
            self.battery -= amount
        else:
            raise InsufficientBatteryError(self.name, self.battery, amount)

    @abstractmethod
    def perform_task(self):
        pass

    def __str__(self):
        return f"{self.name} ({self.battery}% battery)"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, battery={self.battery!r})"


class CleaningRobot(Robot):
    def __init__(self, name, battery=100, dust_capacity=100):
        super().__init__(name, battery)
        self.dust_capacity = dust_capacity

    def perform_task(self):
        cost = 50
        self.use_battery(cost)
        return f"{self.name} successfully vacuumed the area (Capacity: {self.dust_capacity}L)."


class DroneRobot(Robot):
    def __init__(self, name, battery=100, max_altitude=100):
        super().__init__(name, battery)
        self.max_altitude = max_altitude

    def perform_task(self):
        cost = 70
        self.use_battery(cost)
        return f"{self.name} flew! Reached {self.max_altitude}m."