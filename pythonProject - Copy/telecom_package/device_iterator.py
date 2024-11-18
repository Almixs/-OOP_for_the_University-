class DeviceIterator:
    def __init__(self, devices):
        self._devices = devices
        self._index = 0

    def __next__(self):
        if self._index < len(self._devices):
            device = self._devices[self._index]
            self._index += 1
            return device
        else:
            raise StopIteration

    def __iter__(self):
        return self
