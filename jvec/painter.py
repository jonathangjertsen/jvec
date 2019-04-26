class PainterInterface(object):
    def setBrush(self, color):
        pass

    def drawRect(self, x0, y0, width, height):
        pass

    def setPen(self, *color):
        pass

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass

