from telecom_package.device import TelecomDevice
from telecom_package.device_iterator import DeviceIterator

class DeviceCollection:
    def __init__(self):
        self._devices = []

    def add_device(self, device: TelecomDevice):
        self._devices.append(device)

    def __iter__(self):
        return DeviceIterator(self._devices)
