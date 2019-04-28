import json

from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget

from jvec.framework import CountingSemaphore, Representable
from jvec.painter import PainterInterface


MODIFIERS = {
    16777248: 'shift',
    16777249: 'ctrl',
    16777251: 'alt',
    16777217: 'tab',
    16777250: 'home',
    16777220: 'enter',
    16777219: 'backspace',
    16777223: 'delete'
}


class Qt5Painter(PainterInterface):
    def __init__(self, qwidget):
        self.qwidget = qwidget

    def setBrush(self, *color):
        self.qpainter.setBrush(QColor(*color))

    def setPen(self, *color):
        self.qpainter.setPen(QColor(*color))

    def drawRect(self, x0, y0, width, height):
        self.qpainter.drawRect(x0, y0, width, height)

    def drawLine(self, *args):
        self.qpainter.drawLine(*args)

    def __enter__(self):
        self.qpainter = QPainter()
        self.qpainter.begin(self.qwidget)
        return self

    def __exit__(self, *args):
        self.qpainter.end()

class Grid(object):
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self, painter):
        grid_x = self.canvas.grid_x
        grid_y = self.canvas.grid_y
        width = self.canvas.window_width
        height = self.canvas.window_height

        for x in range(0, width, grid_x):
            painter.drawLine(x, 0, x, height)
        for y in range(0, height, grid_y):
            painter.drawLine(0, y, width, y)


class Canvas(QWidget, Representable):
    def defaults(self):
        return {
            'x0': 300,
            'y0': 300,
            'grid_x': 1,
            'grid_y': 1,
            'window_width': 450,
            'window_height': 400,
            'title': 'Editor',
            **super().defaults()
        }

    def __init__(self, **params):
        QWidget.__init__(self)
        Representable.__init__(self, **params)
        self.shapes = {}
        self.shapes_to_create = []
        self.shapes_to_delete = []
        self.mouse_pos = (0, 0)
        self.flags = {
            'mouse_claimed': CountingSemaphore(),
            'clicked': False,
            'released': False,
            **{
                key_name: False
                for key_name
                in MODIFIERS.values()
            }
        }
        self.initUI()
        self.held_keys = set()
        self.painting = False
        self.grid = Grid(self)


    def export(self):
        data = { name: shape.export() for name, shape in self.shapes.items() }
        return json.dumps(data, indent=4)


    def register(self, shape):
        if not self.painting:
            self.shapes[shape.name] = shape
        else:
            self.shapes_to_create.append(shape)

    def unregister(self, shape):
        if not self.painting:
            self.shapes.pop(shape.name, None)
        else:
            self.shapes_to_delete.append(shape)

    def after_painting(self):
        for shape in self.shapes_to_create:
            self.shapes[shape.name] = shape
        for shape in self.shapes_to_delete:
            self.shapes.pop(shape.name, None)
        self.shapes_to_create = []
        self.shapes_to_delete = []

    def initUI(self):
        self.setGeometry(self.x0, self.y0, self.window_width, self.window_height)
        self.setWindowTitle(self.title)
        self.setMouseTracking(True)
        self.show()


    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        self.mouse_pos = x - x % self.grid_x, y - y % self.grid_y
        self.update()


    def mousePressEvent(self, event):
        self.mouse_pos = event.x(), event.y()
        self.flags['clicked'] = True
        self.flags['released'] = False
        self.update()


    def mouseReleaseEvent(self, event):
        self.mouse_pos = event.x(), event.y()
        self.flags['clicked'] = False
        self.flags['released'] = True
        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        self.held_keys.add(key)
        if key in MODIFIERS:
            self.flags[MODIFIERS[key]] = True

    def keyReleaseEvent(self, event):
        key = event.key()
        self.held_keys.remove(key)
        if key in MODIFIERS:
            self.flags[MODIFIERS[key]] = False

    def paintEvent(self, event):
        with Qt5Painter(self) as painter:
            self.painting = True

            painter.setPen(0, 0, 0, 30)
            self.grid.draw(painter)

            painter.setPen(0, 0, 0)
            for shape in self.shapes.values():
                shape.draw(painter, mouse_pos=self.mouse_pos, flags=self.flags)
        self.after_painting()
