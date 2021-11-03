class Registry:
    """A registry to map strings to classes"""

    def __init__(self, name: str) -> None:
        self._name = name
        self._obj_map = {}

    def do_register(self, name, cls):
        assert name not in self._obj_map, f'An object named {name!r} was already registered in {self._name!r} registry!'
        self._obj_map[name] = cls

    def register(self, name):
        def _register(cls):
            self.do_register(name, cls)
            return cls

        return _register

    def get(self, name):
        ret = self._obj_map.get(name)
        if ret is None:
            raise KeyError(f'No object named {name!r} found in {self._name!r} registry!')
        return ret
