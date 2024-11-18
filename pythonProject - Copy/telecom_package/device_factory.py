class DeviceMeta(type):
    registry = {}

    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        if name != "ComponentDevice":
            DeviceMeta.registry[name] = new_class
        return new_class

class DeviceFactory:
    @staticmethod
    def create_device(device_type, *args, **kwargs):
        device_class = DeviceMeta.registry.get(device_type)
        if device_class:
            return device_class(*args, **kwargs)
        else:
            raise ValueError(f"Unknown device type: {device_type}")
