import json

from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget

from jvec.framework import CountingSemaphore, Representable, point
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

    def drawLine(self, p0, p1):
        self.qpainter.drawLine(*p0, *p1)

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

        for x in range(0, self.canvas.window_size.x, self.canvas.grid_xy.x):
            painter.drawLine(point(x, 0), point(x, self.canvas.window_size.y))
        for y in range(0, self.canvas.window_size.y, self.canvas.grid_xy.y):
            painter.drawLine(point(0, y), point(self.canvas.window_size.x, y))


class Canvas(QWidget, Representable):
    def defaults(self):
        return {
            'x0': 300,
            'y0': 300,
            'grid_xy' : point(10, 10),
            'translation': point(100, 100),
            'window_size': point(450, 400),
            'title': 'Editor',
            'line_width': 10,
            **super().defaults()
        }

    def __init__(self, app, **params):
        # Call superclasses
        QWidget.__init__(self, app.ui.centralwidget)
        Representable.__init__(self, **params)

        # Save the app
        self.app = app

        # Set geometry etc.
        self.initUI()

        # Init grid
        self.grid = Grid(self)
        self.show_grid = True

        # Init shapes
        self.shapes = {}
        self.shapes_to_create = []
        self.shapes_to_delete = []

        # Init state
        self.mouse_pos = point(0, 0)
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
        self.held_keys = set()
        self.painting = False

    def set_grid_size(self, x, y):
        self.grid_xy = point(x, y)

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
        self.setGeometry(self.x0, self.y0, *self.window_size)
        self.setWindowTitle(self.title)
        self.setMouseTracking(True)
        self.show()

    def update_mouse_pos(self, event):
        xy = point(event.x(), event.y())
        self.mouse_pos = xy - (xy % self.grid_xy)

    def mouseMoveEvent(self, event):
        self.update_mouse_pos(event)
        self.update()

    def mousePressEvent(self, event):
        self.update_mouse_pos(event)
        self.flags['clicked'] = True
        self.flags['released'] = False
        self.update()

    def mouseReleaseEvent(self, event):
        self.update_mouse_pos(event)
        self.flags['clicked'] = False
        self.flags['released'] = True
        self.update()

    def _keyPress(self, event):
        key = event.key()
        self.held_keys.add(key)
        if key in MODIFIERS:
            self.flags[MODIFIERS[key]] = True

    def _keyRelease(self, event):
        key = event.key()
        self.held_keys.remove(key)
        if key in MODIFIERS:
            self.flags[MODIFIERS[key]] = False

    def paintEvent(self, event):
        with Qt5Painter(self) as painter:
            self.painting = True

            if self.show_grid:
                painter.setPen(0, 0, 0, 30)
                self.grid.draw(painter)

            painter.setPen(0, 0, 0)
            for shape in self.shapes.values():
                shape.draw(painter, mouse_pos=self.mouse_pos, flags=self.flags)
        self.after_painting()
        self.app.paint_complete()
