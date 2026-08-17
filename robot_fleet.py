import functools
import logging
from abc import ABC, abstractmethod


class InsufficientBatteryError(Exception):
    """Raised when a robot attempts an action without sufficient battery."""

    def __init__(self, robot_name, available_battery, required_battery):
        message = f"Robot '{robot_name}' has insufficient battery. Available: {available_battery}%, Required: {required_battery}%."
        super().__init__(message)
        self.robot_name = robot_name
        self.available_battery = available_battery
        self.required_battery = required_battery

logging.basicConfig(level=logging.INFO)

def log_action(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Starting {func.__name__} execution.")
        result = func(*args, **kwargs)
        logging.info(f"Finished {func.__name__} execution.")
        return result
    return wrapper

def run_task_safely(robot, **kwargs):

    try:
        result = robot.perform_task(**kwargs)
    except InsufficientBatteryError as error:
        logging.error(f"Task failed: {error}")
    else:
        print(result)
    finally:
        print(f"Current battery level for {robot.name}: {robot.battery}%")
        
class Robot(ABC):
    manufacturer = "Golden Dragon"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery
        Robot.population += 1

    @classmethod
    def from_config(cls, config):
        """Constructs an instance of cls from a dictionary."""
        name = config["name"]
        battery = config.get("battery", 100)
        # Capture any subclass-specific attributes passed in config
        extra_kwargs = {k: v for k, v in config.items() if k not in ("name", "battery")}
        return cls(name=name, battery=battery, **extra_kwargs)

    @property
    def battery(self):
        return self.available_battery

    @battery.setter
    def battery(self, value):
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        self.available_battery = value

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

    @log_action
    def perform_task(self, **kwargs):
        cost = 50
        self.use_battery(cost)
        return f"{self.name} successfully vacuumed the area (Capacity: {self.dust_capacity}L)."

class DroneRobot(Robot):

    def __init__(self, name, battery=100, max_altitude=100):
        super().__init__(name, battery)
        self.max_altitude = max_altitude
        self.current_altitude = 0

    def perform_task(self):
        cost = 70
        self.use_battery(cost)
        self.current_altitude = min(50, self.max_altitude)
        return (
            f"{self.name} flew! reached {self.current_altitude}m "
            f"(Max: {self.max_altitude}m). Battery remaining: {self.battery}%"
        )

def fleet_report(robots):

    print("Fleet Status Report")
    for robot in robots:
        print(str(robot))
    print(f"Total Active Fleet Population: {Robot.population}")

class BrokenFleetTracker:

    log_entries = []  

    def add_entry(self, entry):
        self.log_entries.append(entry)


class CorrectedFleetTracker:

    def __init__(self):
        self.log_entries = []  

    def add_entry(self, entry):
        self.log_entries.append(entry)


def demonstrate_mutable_trap():

    print("=== Broken Fleet Tracker (Mutable Class Attribute) ===")
    tracker_a = BrokenFleetTracker()
    tracker_b = BrokenFleetTracker()

    tracker_a.add_entry("Unit Alpha online")
    print(f"Tracker A logs: {tracker_a.log_entries}")
    print(f"Tracker B logs: {tracker_b.log_entries}  <- Bug: Tracker B shares Tracker A's list!")

    print("\n=== Corrected Fleet Tracker (Instance Attribute) ===")
    fixed_a = CorrectedFleetTracker()
    fixed_b = CorrectedFleetTracker()

    fixed_a.add_entry("Unit Beta online")
    print(f"Fixed A logs: {fixed_a.log_entries}")
    print(f"Fixed B logs: {fixed_b.log_entries}  <- Correct: Fixed B remains empty and isolated.")

# Temporary experimental helper
def emergency_battery_drain(robots):
    """Drain all robots to 0% battery immediately (experimental)."""
    for robot in robots:
        robot.battery = 0