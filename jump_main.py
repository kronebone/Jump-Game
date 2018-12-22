import pygame
from jump_player import JumpPlayer
from jump_platform import PlatformImg
from jump_box import JumpBox


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()

# Set the width and height of the game window/screen [width, height]
size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Jumper")

# main menu setup
menu = pygame.Surface((size[0] / 2, size[1] / 2))

# pygame font setup
font = pygame.font.SysFont('calibri', 42)

# controller setup, when one is present
controller = False
try:
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    controller = True
except pygame.error as ex:
    print('Jumper Warning - No controller found')

# creating player
player = JumpPlayer(surface=screen, img_path='jump_images/eye_monster.png')
move_speed = 8
max_jump_speed = 18
jump_speed = max_jump_speed
falling_speed = 0
max_fall_speed = 7
score = 0

# creating player spawn platform
spawn_plat = [pygame.Surface.get_width(screen) / 2 - 100, 80, 200, 10]

# creating moving platforms
platform_image = pygame.image.load('jump_images/platform_img.png')
plat_1 = PlatformImg(screen, platform_image, 50, 80)
plat_2 = PlatformImg(screen, platform_image, 250, 80)
plat_3 = PlatformImg(screen, platform_image, 450, 80)
plat_4 = PlatformImg(screen, platform_image, 650, 80)
plat_5 = PlatformImg(screen, platform_image, 850, 80)
platforms = [plat_1, plat_2, plat_3, plat_4, plat_5]

# creating bounce boxes
box_hit_img = pygame.image.load('jump_images/electric_box.png')
b_box1 = JumpBox(screen, 75, 6)
b_box2 = JumpBox(screen, 75, 7)
boxes = [b_box1, b_box2]
box_dmg = 4

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# -------- Main Program Loop -----------
while not done:

    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # single press of jump key 'w' is used for jumping, so holding jump doesn't waste all jumps at once
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w and player.jumps_remaining > 0:
            player.jumps_remaining -= 1
            player.jumping = True
        # jumping using 'a' button on x360 controller
        if event.type == pygame.JOYBUTTONDOWN:
            a_button = joystick.get_button(0)
            if a_button and player.jumps_remaining > 0:
                player.jumps_remaining -= 1
                player.jumping = True

    # --- Game logic should go here

    # jumping is handled here if the jump key is pressed
    if jump_speed != 0 and player.jumping:
        player.move(0, -jump_speed)
        jump_speed -= 1
    elif jump_speed == 0:
        player.jumping = False
        jump_speed = max_jump_speed

    # keys for left and right can be held to move
    pressed = pygame.key.get_pressed()

    # polls the dpad if there is a connected controller
    if controller:
        d_pad = joystick.get_hat(0)
    else:
        d_pad = (0, 0)

    # 'a' key or left on dpad
    if pressed[pygame.K_a] or d_pad[0] == -1:
        if player.x_pos - move_speed < 0:
            player.x_pos = 0
        else:
            player.move(-move_speed, 0)

    # 'd' key or right on dpad
    if pressed[pygame.K_d] or d_pad[0] == 1:
        if player.x_pos + move_speed > pygame.Surface.get_width(screen) - player.img_width:
            player.x_pos = pygame.Surface.get_width(screen) - player.img_width
        else:
            player.move(move_speed, 0)

    # when spawning, a safe platform is created that gives the player a second to get their bearings
    s_pform = pygame.Rect(tuple(spawn_plat))
    spawn_player_pos = pygame.Rect((player.x_pos, player.y_pos, player.img_width, player.img_height))
    if spawn_player_pos.colliderect(s_pform) and player.spawn_in:
        player.hold_y_pos = True
    else:
        player.hold_y_pos = False

    # once the player moves below the spawn platform it is removed
    if player.y_pos > spawn_plat[1]:
        player.spawn_in = False

    # updating pos for each platform
    for platform in platforms:
        platform.p_update()

        # handling collision between platforms and player
        # when the player lands on a platform they move with it
        # the players jumps are replenished when landing on a platform
        pform = pygame.Rect(platform.start_x_pos, platform.y_pos, platform.img_width, platform.img_height)
        player_pos = pygame.Rect((player.x_pos, player.y_pos, player.img_width, player.img_height))
        if player_pos.colliderect(pform):
            player.jumps_remaining = 2
            player.hold_y_pos = True
            if player.x_pos - platform.speed < 0:
                pass
            elif player.x_pos - platform.speed > 0:
                player.move(-platform.speed, 0)

    # updating pos for each bounce box after player drops off spawn platform
    if not player.spawn_in:
        for box in boxes:
            box.jbox_update()

            # collision between boxes and player result in health loss and eventual death
            b_box = pygame.Rect(box.x_pos, box.y_pos, box.box_size, box.box_size)
            player_pos = pygame.Rect((player.x_pos, player.y_pos, player.img_width, player.img_height))
            if b_box.colliderect(player_pos):
                player.hp -= box_dmg
                box.box_hit = True

    # resetting if the player dies
    if player.hp <= 0:
        score = 0
        player.hp = 100
        player.spawn_in = True
        player.x_pos = pygame.Surface.get_width(screen) / 2
        player.y_pos = -3

    # player location is updated here when not on a platform
    if player.jumping:
        pass
    elif not player.hold_y_pos and falling_speed != max_fall_speed:
        player.move(0, falling_speed)
        falling_speed += 1
    elif not player.hold_y_pos and falling_speed == max_fall_speed:
        player.move(0, falling_speed)

    # if the player falls through the bottom, they lose hp and drop from the top but get their jumps back
    if player.y_pos > size[1]:
        player.hp -= 20
        player.y_pos = -3
        player.jumps_remaining = 2

    # adding to score when after dropping from spawn platform
    if not player.spawn_in:
        score += 1

    # --- Screen-clearing code goes here
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)

    # --- Drawing code should go here
    # when a player first spawns or dies this platform is used
    if player.spawn_in:
        pygame.draw.rect(screen, GREEN, tuple(spawn_plat))

    # drawing platforms and boxes
    for platform in platforms:
        screen.blit(platform.img, (platform.start_x_pos, platform.y_pos))

    for box in boxes:
        surface, color, location, line_width = box.jbox_rect()
        screen.lock()
        pygame.draw.rect(surface, color, location, line_width)
        screen.unlock()
        if box.box_hit:
            screen.blit(box_hit_img, (box.x_pos, box.y_pos))
            box.box_hit = False

    # drawing health bar
    screen.lock()
    pygame.draw.rect(surface, RED, (5, 5, 205, 40), 5)
    for health in range(player.hp * 2):
        pygame.draw.line(screen, RED, (5 + health, 5), (5 + health, 45), 4)
    screen.unlock()

    # creating jumps remaining, score and health counter on-screen text
    jumps_left_text = font.render(f'Jumps: {player.jumps_remaining}', True, WHITE)
    score_text = font.render(f'Score: {score}', True, WHITE)
    hp_left_text = font.render(f'Health: {player.hp}', True, WHITE)

    # drawing the text
    screen.blit(jumps_left_text, (pygame.Surface.get_width(screen) - 151, 5))
    screen.blit(score_text, (5, pygame.Surface.get_height(screen) - 50))
    screen.blit(hp_left_text, (5, 5))

    # player image
    screen.blit(player.img, (player.x_pos, player.y_pos))

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
