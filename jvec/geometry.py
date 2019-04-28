from jvec.framework import Representable, Shape, point


def fill_in_the_blanks(self):
    if self.shape is None:
        if self.lower_right is None or self.upper_left is None:
            raise KeyError(
                'Must either specify both upper_left and lower_right or one shape')
        self.lower_right = point(*self.lower_right)
        self.upper_left = point(*self.upper_left)
        self.shape = self.lower_right - self.upper_left
    elif self.lower_right is None or self.upper_left is None:
        self.shape = point(*self.shape)
        if self.lower_right is None:
            if self.upper_left is None:
                raise KeyError(
                    'Either upper_left or lower_right must be specified')
            self.lower_right = point(*self.upper_left) + self.shape
        else:
            self.upper_left = point(*self.lower_right) - self.shape

MIRRORS = {
    'corner_top_left': 'corner_bottom_right',
    'corner_top_right': 'corner_bottom_left',
    'left': 'right',
    'top': 'bottom'
}
MIRRORS = {
    **MIRRORS,
    **{ value: key for key, value in MIRRORS.items() }
}


def mirror_edge(edge):
    return MIRRORS.get(edge, None)


class Rectangle(Shape):
    def defaults(self):
        return {
            'color': None,
            'shape': None,
            'lower_right': None,
            'upper_left': None,
            'hover_thickness': 5,
            'hover_size': 5,
            'corner_size': 15,
            'hover_color': (150, 200, 150),
            'drag_color': (200, 150, 150),
            'release_color': (150, 150, 200),
            **super().defaults()
        }

    def __init__(self, canvas, **params):
        super().__init__(canvas, **params)
        self.held_edge = None
        self.held_from = None
        self.held_clone = None

    @property
    def width(self):
        return self.shape.x

    @property
    def height(self):
        return self.shape.y

    def load_params(self, params: dict, defaults: dict):
        super().load_params(params, defaults)
        fill_in_the_blanks(self)

    def draw(self, painter, mouse_pos=point(0,0), flags=None):
        if flags is None:
            flags = {}

        self.handle_movement(mouse_pos, flags)
        self.draw_main(painter)
        self.draw_edges(painter, mouse_pos, flags)

    def handle_movement(self, mouse_pos, flags):
        rect_to_move = self
        if self.held_edge:
            if flags['alt']:
                if self.held_clone is None:
                    self.held_clone = self.make_clone()
                    self.held_clone.held_edge = self.held_edge
                    self.held_clone.held_from = self.held_from
                rect_to_move = self.held_clone
            else:
                if self.held_clone is not None:
                    self.eat_clone()

        if flags['shift'] and rect_to_move.held_edge:
            rect_to_move.move_if_held(mirror_edge(rect_to_move.held_edge), rect_to_move.mirror_mouse(mouse_pos))
        rect_to_move.move_if_held(rect_to_move.held_edge, mouse_pos)


    def eat_clone(self):
        self.load_params(self.held_clone._params, self.unprotected_defaults())
        self.held_edge = self.held_clone.held_edge
        self.held_from = self.held_clone.held_from
        self.canvas.unregister(self.held_clone)
        self.held_clone = None

    def mirror_mouse(self, mouse_pos):
        return self.lower_right + self.upper_left - mouse_pos

    def recalculate_height_and_width(self):
        self.shape = None
        fill_in_the_blanks(self)

    def uninvert(self):
        if self.height < 0:
            self.shape = None
            lower, upper = self.lower_right.y, self.upper_left.y
            self.upper_left = point(self.upper_left.x, lower)
            self.lower_right = point(self.lower_right.x, upper)
        if self.width < 0:
            self.shape = None
            left, right = self.lower_right.x, self.upper_left.x
            self.upper_left = point(left, self.upper_left.y)
            self.lower_right = point(right, self.lower_right.y)
        fill_in_the_blanks(self)

    def move_if_held(self, held_edge, mouse_pos):
        if not held_edge:
            return

        if held_edge == 'corner_top_left':
            self.upper_left =  mouse_pos
        elif held_edge == 'corner_top_right':
            self.upper_left = point(self.upper_left.x, mouse_pos.y)
            self.lower_right = point(mouse_pos.x, self.lower_right.y)
        elif held_edge == 'corner_bottom_left':
            self.upper_left =  point(mouse_pos.x,  self.upper_left.y)
            self.lower_right =  point(self.lower_right.x, mouse_pos.y)
        elif held_edge == 'corner_bottom_right':
            self.lower_right = mouse_pos
        elif held_edge == 'left':
            self.upper_left =  point(mouse_pos.x,  self.upper_left.y)
        elif held_edge == 'right':
            self.lower_right = point(mouse_pos.x, self.lower_right.y)
        elif held_edge == 'top':
            self.upper_left = point(self.upper_left.x, mouse_pos.y)
        elif held_edge == 'bottom':
            self.lower_right =  point(self.lower_right.x, mouse_pos.y)
        elif held_edge == 'body':
            if self.held_from is None:
                self.held_from = self.upper_left - mouse_pos
            else:
                self.upper_left = self.held_from + mouse_pos
                self.lower_right = self.upper_left + self.shape
        self.recalculate_height_and_width()

    def which_part(self, mouse_pos):
        x0, y0 = self.upper_left
        x1, y1 = self.lower_right

        if abs(x0 - mouse_pos.x) < self.corner_size and abs(y0 - mouse_pos.y) < self.corner_size:
            return 'corner_top_left'
        elif abs(x1 - mouse_pos.x) < self.corner_size and abs(y0 - mouse_pos.y) < self.corner_size:
            return 'corner_top_right'
        if abs(x0 - mouse_pos.x) < self.corner_size and abs(y1 - mouse_pos.y) < self.corner_size:
            return 'corner_bottom_left'
        elif abs(x1 - mouse_pos.x) < self.corner_size and abs(y1 - mouse_pos.y) < self.corner_size:
            return 'corner_bottom_right'
        elif abs(x0 - mouse_pos.x) < self.hover_size and y0 < mouse_pos.y < y1:
            return 'left'
        elif abs(x1 - mouse_pos.x) < self.hover_size and y0 < mouse_pos.y < y1:
            return 'right'
        elif abs(y0 - mouse_pos.y) < self.hover_size and x0 < mouse_pos.x < x1:
            return 'top'
        elif abs(y1 - mouse_pos.y) < self.hover_size and x0 < mouse_pos.x < x1:
            return 'bottom'
        elif (x0 < mouse_pos.x < x1) and (y0 < mouse_pos.y < y1):
            return 'body'

    def draw_main(self, painter):
        if self.color:
            painter.setBrush(*self.color)
        painter.drawRect(*self.upper_left, *self.shape)

    def draw_edges(self, painter, mouse_pos, flags):
        clicked = flags.get('clicked', False)
        released = flags.get('released', False)
        mouse_claimed = flags.get('mouse_claimed')

        color = self.hover_color

        if released:
            self.held_edge = None
            self.held_from = None
            mouse_claimed.dec()
            self.uninvert()

        edge = None
        if self.held_edge is not None:
            color = self.drag_color
            edge = self.held_edge
        elif not mouse_claimed:
            edge = self.which_part(mouse_pos)
            if clicked and edge is not None:
                self.held_edge = edge
                mouse_claimed.inc()

        if edge is not None:
            self.draw_edge(painter, edge, color)

    def draw_edge(self, painter, edge, color):
        x0, y0 = self.upper_left
        x1, y1 = self.lower_right

        corner = point(self.corner_size, self.corner_size)

        painter.setBrush(*color)

        if edge == 'corner_top_left':
            painter.drawRect(x0 - self.corner_size / 2, y0 - self.corner_size / 2, *corner)
        elif edge == 'corner_top_right':
            painter.drawRect(x1 - self.corner_size / 2, y0 - self.corner_size / 2, *corner)
        elif edge == 'corner_bottom_left':
            painter.drawRect(x0 - self.corner_size / 2, y1 - self.corner_size / 2, *corner)
        elif edge == 'corner_bottom_right':
            painter.drawRect(x1 - self.corner_size / 2, y1 - self.corner_size / 2, *corner)
        elif edge == 'left':
            painter.drawRect(x0 - self.hover_size / 2, y0, self.hover_size, self.height)
        elif edge == 'right':
            painter.drawRect(x1 - self.hover_size / 2, y0, self.hover_size, self.height)
        elif edge == 'top':
            painter.drawRect(x0, y0 - self.hover_size / 2, self.width, self.hover_size)
        elif edge == 'bottom':
            painter.drawRect(x0, y1 - self.hover_size / 2, self.width, self.hover_size)
        elif edge == 'body':
            painter.drawRect(*self.upper_left, *self.shape)
