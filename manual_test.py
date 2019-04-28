import json
import sys

from PyQt5.QtWidgets import QApplication

from jvec.geometry import Rectangle
from jvec.canvas import Canvas


if __name__ == '__main__':
    app = QApplication(sys.argv)
    canvas = Canvas(grid_x=10, grid_y=10)

    Rectangle(canvas, name="main", upper_left=(10, 15+70), width=200-10, height=200-70)
    for i in range(10):
        Rectangle(canvas, name=f"upper_{i}", upper_left=(10 + 20*i, 15), width=10, height=70, color=(200, 0, 0, 100))
        Rectangle(canvas, name=f"lower_{i}",upper_left=(10 + 20*i, 215), width=10, height=70, color=(200, 0, 0, 100))

    res = app.exec_()

    print(canvas.export())

    sys.exit(res)
