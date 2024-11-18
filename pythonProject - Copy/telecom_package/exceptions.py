class DeviceError(Exception):
    pass

class DeviceConnectionError(DeviceError):
    def __init__(self, message="Помилка з'єднання з пристроєм"):
        self.message = message
        super().__init__(self.message)
