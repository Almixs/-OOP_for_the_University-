from abc import ABC, abstractmethod
from datetime import datetime
import time
import random
from telecom_package.device_factory import DeviceMeta

class AbstractDevice(ABC):
    @abstractmethod
    def check_status(self):
        pass

    @abstractmethod
    def log_activity(self, action):
        pass

class TelecomDevice(AbstractDevice):
    def __init__(self, name, device_type, status="Off"):
        self.__name = name
        self.__device_type = device_type
        self.__status = status

    def __del__(self):
        print(f"Device {self.__name} ({self.__device_type}) has been destroyed.")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def device_type(self):
        return self.__device_type

    @device_type.setter
    def device_type(self, value):
        self.__device_type = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    def __eq__(self, other):
        return self.device_type == other.device_type and self.status == other.status

    def __add__(self, other):
        return f"{self.name} ({self.device_type}) and {other.name} ({other.device_type}) are combined."

    def check_status(self):
        return f"Device status: {self.__name} ({self.__device_type}) is {self.__status}"

    def log_activity(self, action):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("device_log.txt", "a", encoding='utf-8') as f:
            f.write(f"{current_time} - {self.__name} ({self.__device_type}): {action}\n")

    def set_status(self, status=None, name=None, device_type=None):
        if status:
            delay = random.uniform(1, 3)
            print(f"Setting status... (delay {delay:.2f} seconds)")
            time.sleep(delay)
            self.__status = status
        if name:
            self.__name = name
        if device_type:
            self.__device_type = device_type
        self.log_activity(f"Updated status or attributes. New status: {self.__status}")

class ComponentDevice(ABC):
    @abstractmethod
    def operate(self):
        pass

class LeafDevice(ComponentDevice):
    def __init__(self, name, device_type):
        self.name = name
        self.device_type = device_type
        self.status = "Off"

    def operate(self):
        print(f"{self.name} ({self.device_type}) is operating")
        self.log_activity("Operating")  # Логуємо дію

    def check_status(self):
        return f"{self.name} is {self.status}"

    def set_status(self, status):
        self.status = status

    def log_activity(self, action):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("device_log.txt", "a", encoding='utf-8') as f:
            f.write(f"{current_time} - {self.name} ({self.device_type}): {action}\n")

class CompositeDevice(ComponentDevice):
    def __init__(self, name):
        self.name = name
        self.devices = []

    def add(self, device: ComponentDevice):
        self.devices.append(device)

    def remove(self, device: ComponentDevice):
        self.devices.remove(device)

    def operate(self):
        print(f"Composite group {self.name} operation:")
        for device in self.devices:
            device.operate()

def log_operation(func):
    def wrapper(*args, **kwargs):
        print(f"Викликається {func.__name__} для {args[0].__class__.__name__}")
        result = func(*args, **kwargs)
        print(f"Завершення {func.__name__} для {args[0].__class__.__name__}")
        return result
    return wrapper

def create_device_class(name, base_classes, attributes):
    return type(name, base_classes, attributes)

DeviceClass = create_device_class('NewDevice', (TelecomDevice,), {
    'new_method': lambda self: "New method in device"
})
