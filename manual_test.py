import json
import sys

from jvec.app import App
from jvec.geometry import Rectangle

if __name__ == '__main__':
    app = App(sys.argv)

    Rectangle(app.canvas, name="main", upper_left=(10, 15+70), shape=(200-10, 200-70))
    for i in range(10):
        Rectangle(app.canvas, name=f"upper_{i}", upper_left=(10 + 20*i, 15), shape=(10, 70), color=(200, 0, 0, 100))
        Rectangle(app.canvas, name=f"lower_{i}", upper_left=(10 + 20*i, 215), shape=(10, 70), color=(200, 0, 0, 100))

    app.start()
