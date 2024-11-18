class NetworkSettings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NetworkSettings, cls).__new__(cls)
            cls._instance._configurations = {}
        return cls._instance

    def set_configuration(self, key, value):
        self._configurations[key] = value

    def get_configuration(self, key):
        return self._configurations.get(key, None)
