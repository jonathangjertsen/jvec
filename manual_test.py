import json
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from jvec.geometry import Rectangle
from jvec.canvas import Canvas
from jvec.gui import Ui_MainWindow


class App(QApplication):
    def __init__(self, args):
        QApplication.__init__(self,args)
        self.main_window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
        self.canvas = Canvas(self, grid_x=10, grid_y=10)
        self.ui.centralwidget.setGeometry(0, 0, self.canvas.width()*2, self.canvas.height()*2)
        self.canvas.setGeometry(0, 0, self.canvas.width(), self.canvas.height())

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

    def show(self):
        self.main_window.show()
        sys.exit(self.exec_())

if __name__ == '__main__':
    app = App(sys.argv)

    Rectangle(app.canvas, name="main", upper_left=(10, 15+70), width=200-10, height=200-70)
    for i in range(10):
        Rectangle(app.canvas, name=f"upper_{i}", upper_left=(10 + 20*i, 15), width=10, height=70, color=(200, 0, 0, 100))
        Rectangle(app.canvas, name=f"lower_{i}",upper_left=(10 + 20*i, 215), width=10, height=70, color=(200, 0, 0, 100))

    app.show()

    print(app.canvas.export())

    sys.exit(res)
