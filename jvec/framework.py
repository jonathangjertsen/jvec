import re

REQUIRED = "__REQUIRED__"


class point(tuple):
    __slots__ = []

    def __new__(cls, *args):
        if len(args) == 2:
            return tuple.__new__(cls, args)
        elif len(args) == 1:
            return args
        raise ValueError(f"len(args) must be 1 or 2, not {len(args)}")

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def __add__(self, other):
        return point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return point(self.x - other.x, self.y - other.y)

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return self - other

    def __len__(self):
        return 2

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __str__(self):
        return repr(self)

    def __mod__(self, other):
        return point(self.x % other.x, self.y % other.y)


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
