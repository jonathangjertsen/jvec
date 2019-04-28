import re

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
    def defaults(self):
        return {}

    def protected(self):
        return {}

    def __init__(self, *args, **params):
        self._params = params
        self.load_params(params.copy(), self.defaults())

    def load_params(self, params: dict, defaults: dict):
        names = defaults.keys()

        if len(set(names)) < len(names):
            raise KeyError("Duplicate names encountered")

        for name in names:
            if defaults[name] is REQUIRED:
                setattr(self, name, params.pop(name))
            else:
                setattr(self, name, params.pop(name, defaults[name]))

    def unprotected_defaults(self):
        return { key: val for key, val in self.defaults().items() if key not in self.protected() }

    def export(self):
        data = self.data()
        data['__repr__'] = repr(self)
        return data


    def data(self):
        return { name: getattr(self, name) for name in self._params }

    def make_clone(self):
        return type(self)(**self.data())

    def paste_params(self, other):
        self.load_params(other._params, self.DEFAULTS)

    def __repr__(self):
        typename = type(self).__name__
        args = ", ".join(f"{k}={repr(v)}" for k, v in self.data().items())
        return f"{typename}(canvas, {args})"


class Shape(Representable):
    def defaults(self):
        return {
            'name': REQUIRED,
            **super().defaults()
        }

    def protected(self):
        return {
            'name',
            *super().protected()
        }

    def __init__(self, canvas: 'Canvas', **params):
        super().__init__(canvas, **params)
        self.canvas = canvas
        self.canvas.register(self)

    def make_clone(self):
        clone_token = "__clone__"
        rex = re.compile("(.*{})(\d+)".format(clone_token))
        data = self.data()
        match = rex.match(data['name'])
        if match:
            nonnum, num = match.groups()
            num = int(num) + 1
            data['name'] = f"{nonnum}{num}"
        else:
            data['name'] = f"{data['name']}{clone_token}0"
        return type(self)(self.canvas, **data)
