from telecom_package.device import TelecomDevice

class SmartWatch(TelecomDevice):
    def __init__(self, name, device_type, battery_level=100, status="Off"):
        super().__init__(name, device_type, status)
        self.__battery_level = battery_level

    @property
    def battery_level(self):
        return self.__battery_level

    def check_battery(self):
        return f"Battery level: {self.__battery_level}%"

    def __lt__(self, other):
        return self.battery_level < other.battery_level

    def __str__(self):
        return f"{self.name} ({self.device_type}) - Battery: {self.__battery_level}%"