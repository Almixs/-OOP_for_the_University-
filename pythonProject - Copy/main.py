import atexit
from datetime import datetime
import time
import random
from telecom_package.device import TelecomDevice, CompositeDevice, LeafDevice
from telecom_package.device_factory import DeviceFactory
from telecom_package.device_collection import DeviceCollection
from telecom_package.network_settings import NetworkSettings

# Абстрактний клас для всіх пристроїв
from abc import ABC, abstractmethod

class AbstractDevice(ABC):
    @abstractmethod
    def check_status(self):
        pass

    @abstractmethod
    def log_activity(self, action):
        pass

# Функція для операції з пристроями
def operate_device(device):
    print(device.check_status())
    device.log_activity("Checked status.")

# Логування завершення сесії
def log_session_end():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("device_log.txt", "a", encoding='utf-8') as f:
        f.write(f"{current_time} - Session ended\n")

# Реєструємо функцію завершення сесії
atexit.register(log_session_end)

# Основний код програми
if __name__ == "__main__":
    try:
        # Налаштування мережі
        network_settings = NetworkSettings()
        network_settings.set_configuration("IP", "192.168.1.1")
        print(f"Network IP: {network_settings.get_configuration('IP')}")

        # Створення пристроїв
        modem = LeafDevice("Modem", "Network")
        router = LeafDevice("Router", "Network")
        phone = LeafDevice("Smartphone", "Mobile")
        watch = LeafDevice("SmartWatch", "Wearable")

        # Зміна статусів пристроїв
        modem.set_status("On")
        router.set_status("On")
        phone.set_status("Off")
        watch.set_status("Off")

        # Операція з окремими пристроями
        operate_device(modem)
        operate_device(router)
        operate_device(phone)
        operate_device(watch)

        # Створення композитного пристрою
        composite_network = CompositeDevice("Home Network")
        composite_network.add(modem)
        composite_network.add(router)

        # Операція з композитним пристроєм
        composite_network.operate()

        # Колекція пристроїв
        device_collection = DeviceCollection()
        device_collection.add_device(modem)
        device_collection.add_device(router)
        device_collection.add_device(phone)
        device_collection.add_device(watch)

        print("\nDevices in the collection:")
        for device in device_collection:
            print(device.check_status())

    except AttributeError as e:
        error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("error_log.txt", "a", encoding='utf-8') as error_file:
            error_file.write(f"{error_time} - AttributeError: {str(e)}\n")
        print(f"An error occurred: {e}. Check error_log.txt for details.")

    except Exception as e:
        error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("error_log.txt", "a", encoding='utf-8') as error_file:
            error_file.write(f"{error_time} - Exception: {str(e)}\n")
        print(f"An error occurred: {e}. Check error_log.txt for details.")

    finally:
        print("Program finished.")

def create_device_class(name, base_classes, attributes):
    return type(name, base_classes, attributes)

DeviceClass = create_device_class('NewDevice', (TelecomDevice,), {
    'new_method': lambda self: "New method in device"
})

import inspect
print(inspect.getmembers(DeviceClass, predicate=inspect.isfunction))

def new_dynamic_method(self):
    return "Dynamically added method"

setattr(DeviceClass, 'dynamic_method', new_dynamic_method)

device_instance = DeviceClass("Dynamic Device", "Telecom")
print(device_instance.check_status())
print(device_instance.new_method())
print(device_instance.dynamic_method())
