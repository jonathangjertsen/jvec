REQUIRED = "__REQUIRED__"


class CountingSemaphore(object):
    def __init__(self):
        self.value = 0

    def inc(self):
        self.value += 1

    def dec(self):
        if self.value > 0:
            self.value -= 1

    def __bool__(self):
        return self.value > 0


class Representable(object):
    def __init__(self, *args, **params):
        self._params = params

    def load_params(self, params: dict, defaults: dict):
        names = defaults.keys()

        if len(set(names)) < len(names):
            raise KeyError("Duplicate names encountered")

        for name in names:
            if defaults[name] is REQUIRED:
                setattr(self, name, params.pop(name))
            else:
                setattr(self, name, params.pop(name, defaults[name]))


    def export(self):
        data = self.data()
        data['__repr__'] = repr(self)
        return data


    def data(self):
        return { name: getattr(self, name) for name in self._params }


    def __repr__(self):
        typename = type(self).__name__
        args = ", ".join(f"{k}={repr(v)}" for k, v in self.data().items())
        return f"{typename}(canvas, {args})"
