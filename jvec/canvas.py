import json

from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget

from jvec.framework import CountingSemaphore, Representable
from jvec.painter import PainterInterface


class Qt5Painter(PainterInterface):
    def __init__(self, qwidget):
        self.qwidget = qwidget

    def setBrush(self, *color):
        self.qpainter.setBrush(QColor(*color))

    def setPen(self, *color):
        self.qpainter.setPen(QColor(*color))

    def drawRect(self, x0, y0, width, height):
        self.qpainter.drawRect(x0, y0, width, height)

    def __enter__(self):
        self.qpainter = QPainter()
        self.qpainter.begin(self.qwidget)
        return self

    def __exit__(self, *args):
        self.qpainter.end()


class Canvas(QWidget, Representable):
    def __init__(self, **params):
        super().__init__()
        self.shapes = {}
        self.mouse_pos = (0, 0)
        self.flags = {
            'mouse_claimed': CountingSemaphore()
        }
        self.load_params(params, {
            'x0': 300,
            'y0': 300,
            'grid_x': 1,
            'grid_y': 1,
            'window_width': 450,
            'window_height': 400,
            'title': 'Editor',
        })
        self.initUI()


    def export(self):
        data = { name: shape.export() for name, shape in self.shapes.items() }
        return json.dumps(data, indent=4)


    def register(self, shape):
        self.shapes[shape.name] = shape


    def initUI(self):
        self.setGeometry(self.x0, self.y0, self.window_width, self.window_height)
        self.setWindowTitle(self.title)
        self.setMouseTracking(True)
        self.show()


    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        if not (x % self.grid_x) or not (y % self.grid_y):
            self.mouse_pos = x, y
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


    def paintEvent(self, event):
        with Qt5Painter(self) as painter:
            painter.setPen(0, 0, 0)
            for shape in self.shapes.values():
                shape.draw(painter, mouse_pos=self.mouse_pos, flags=self.flags)
