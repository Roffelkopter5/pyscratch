class PyScratchEvent:
    def __init__(self, name: str, general: str = "", **kwargs):
        self._name = name
        self._kwargs = kwargs
        self._general = general
        for k, v in kwargs.items():
            self.__setattr__(k, v)