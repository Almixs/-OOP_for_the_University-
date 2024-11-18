import random
import time
from telecom_package.device import TelecomDevice

class Router(TelecomDevice):
    def __init__(self, name, device_type, ip_address, status="Off"):
        super().__init__(name, device_type, status)
        self.__ip_address = ip_address

    def restart(self):
        self.set_status("Restarting")
        print(f"Router {self.name} is restarting...")
        delay = random.uniform(1, 3)
        print(f"Restarting... (delay {delay:.2f} seconds)")
        time.sleep(delay)
        self.set_status("On")
        self.log_activity("Router restarted.")

    @property
    def ip_address(self):
        return self.__ip_address

    @ip_address.setter
    def ip_address(self, value):
        self.__ip_address = value

    def __str__(self):
        return f"{self.name} ({self.device_type}) - IP: {self.__ip_address}, Status: {self.status}"
