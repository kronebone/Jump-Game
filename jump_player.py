from pygame import Surface, image


class JumpPlayer:
    def __init__(self, surface, img_path):
        self.surface = surface
        self.x_pos = Surface.get_width(self.surface) / 2
        self.y_pos = 0
        self.img = image.load(img_path)

        self.hold_y_pos = False
        self.spawn_in = True

        self.player_rect = [self.x_pos, self.y_pos, 10, 10]  # x_pos, y_pos, rect_width, rect_height

        self.img_bounds = list(Surface.get_bounding_rect(self.img))
        self.img_width = self.img_bounds[2]
        self.img_height = self.img_bounds[3]

        self.jumps_remaining = 2
        self.jumping = False

        self.hp = 100

    def move(self, x_change, y_change):
        self.x_pos += x_change
        self.y_pos += y_change

