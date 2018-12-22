from pygame import Surface
from random import randint, choice


class JumpBox:
    def __init__(self, surface, box_size, speed):
        self.surface = surface
        self.color = (randint(25, 255), randint(25, 255), randint(25, 255))
        self.box_size = box_size
        self.speed = speed
        self.max_width = Surface.get_width(self.surface)
        self.max_height = Surface.get_height(self.surface)
        self.x_pos = randint(0, self.max_width)
        self.x_rev = choice([True, False])
        self.y_pos = randint(0, self.max_height)
        self.y_rev = choice([True, False])
        self.box_hit = False
        self.color_list = []
        for c in range(14):
            self.color_list.append((randint(25, 255), randint(25, 255), randint(25, 255)))

    def jbox_update(self):
        # left and right movement
        if self.x_pos + self.box_size <= self.max_width and self.x_rev is False:
            self.x_pos += self.speed
        elif self.x_pos + self.box_size >= self.max_width and self.x_rev is False:
            self.x_rev = True
            self.color = choice(self.color_list)
            self.x_pos -= self.speed
        elif self.x_pos >= 0 and self.x_rev is True:
            self.x_pos -= self.speed
        elif self.x_pos <= 0 and self.x_rev is True:
            self.x_rev = False
            self.color = choice(self.color_list)
            self.x_pos += self.speed

        # up and down movement
        if self.y_pos + self.box_size <= self.max_height and self.y_rev is False:
            self.y_pos += self.speed
        elif self.y_pos + self.box_size >= self.max_height and self.y_rev is False:
            self.y_rev = True
            self.color = choice(self.color_list)
            self.y_pos -= self.speed
        elif self.y_pos > 0 and self.y_rev is True:
            self.y_pos -= self.speed
        elif self.y_pos <= 0 and self.y_rev is True:
            self.y_rev = False
            self.color = choice(self.color_list)
            self.y_pos += self.speed

    def jbox_rect(self):
        return self.surface, self.color, (self.x_pos, self.y_pos, self.box_size, self.box_size), 10
