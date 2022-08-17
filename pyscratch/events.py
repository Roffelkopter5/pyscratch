class PyScratchEvent:
    def __init__(self, name: str, **kwargs):
        self._name = name
        self._kwargs = kwargs
        for k, v in kwargs.items():
            self.__setattr__(k, v)