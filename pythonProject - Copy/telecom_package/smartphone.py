from telecom_package.device import TelecomDevice

class SmartPhone(TelecomDevice):
    def __init__(self, name, device_type, phone_number, battery_level=100, status="Off"):
        super().__init__(name, device_type, status)
        self.__phone_number = phone_number
        self.__battery_level = battery_level

    def make_call(self, number):
        if self.__battery_level > 0:
            print(f"Calling {number} from {self.__phone_number}...")
            self.__battery_level -= 10
            self.log_activity(f"Called {number}")
        else:
            print("Battery too low to make a call.")

    def __sub__(self, usage):
        self.__battery_level -= usage
        if self.__battery_level < 0:
            self.__battery_level = 0
        return self.__battery_level

    def __str__(self):
        return f"{self.name} ({self.device_type}) - Phone: {self.__phone_number}, Battery: {self.__battery_level}%"
