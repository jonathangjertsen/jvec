import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from jvec.canvas import Canvas
from jvec.gui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.canvas = Canvas(self, grid_x=10, grid_y=10)
        self.canvas.setGeometry(0, 0, self.canvas.width(), self.canvas.height())
        self.ui.centralwidget.setGeometry(0, 0, self.canvas.width()*2, self.canvas.height()*2)
        self.ui.showGridCheckBox.clicked.connect(self.show_grid_clicked)
        self.ui.gridSizeSpinBox.valueChanged.connect(self.value_changed)
        self.frames = 0

    def show_grid_clicked(self, state):
        self.canvas.show_grid = state
        self.canvas.update()

    def value_changed(self, value):
        self.canvas.set_grid_size(value, value)
        self.canvas.update()

    def paint_complete(self):
        self.frames += 1
        if not self.frames % 10:
            data = self.canvas.export()
            self.ui.text_current_json.setPlainText(data)

    def mouseMoveEvent(self, event):
        self.canvas._mouseMove(event)

    def mousePressEvent(self, event):
        self.canvas._mousePress(event)

    def mouseReleaseEvent(self, event):
        self.canvas._mouseRelease(event)

    def keyPressEvent(self, event):
        self.canvas._keyPress(event)

    def keyReleaseEvent(self, event):
        self.canvas._keyRelease(event)

class App(QApplication):
    def __init__(self, args):
        QApplication.__init__(self,args)
        self.main = MainWindow()

    def start(self):
        self.main.show()
        sys.exit(self.exec_())

    @property
    def canvas(self):
        return self.main.canvas
