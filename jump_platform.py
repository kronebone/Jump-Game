from pygame import Surface
from random import randint


# for use as a built-in shape
class Platform:
    def __init__(self, surface, color, offset, y_range, length=100, height=10, speed=10):
        self.surface = surface
        self.color = color
        self.offset = offset
        self.y_range = y_range
        self.length = length
        self.height = height
        self.speed = speed
        self.start_x_pos = Surface.get_width(self.surface) + self.offset
        self.y_pos = randint(Surface.get_height(self.surface) / 2 - self.y_range,
                             Surface.get_height(self.surface) / 2 + self.y_range)

    def p_update(self):
        self.start_x_pos -= self.speed
        if self.start_x_pos + self.length <= 0:
            self.start_x_pos = Surface.get_width(self.surface)
            self.y_pos = randint(Surface.get_height(self.surface) / 2 - self.y_range,
                                 Surface.get_height(self.surface) / 2 + self.y_range)

    def p_rect(self):
        return self.surface, self.color, (self.start_x_pos, self.y_pos, self.length, self.height)


# for use as a sprite
class PlatformImg:
    def __init__(self, surface, img, offset, y_range, speed=10):
        self.surface = surface
        self.img = img
        self.offset = offset
        self.y_range = y_range
        self.speed = speed
        self.start_x_pos = Surface.get_width(self.surface) + self.offset
        self.y_pos = randint(Surface.get_height(self.surface) / 2 - self.y_range,
                             Surface.get_height(self.surface) / 2 + self.y_range)

        self.img_bounds = list(Surface.get_bounding_rect(self.img))
        self.img_width = self.img_bounds[2]
        self.img_height = self.img_bounds[3]

    def p_update(self):
        self.start_x_pos -= self.speed
        if self.start_x_pos + self.img_width <= 0:
            self.start_x_pos = Surface.get_width(self.surface)
            self.y_pos = randint(Surface.get_height(self.surface) / 2 - self.y_range,
                                 Surface.get_height(self.surface) / 2 + self.y_range)
