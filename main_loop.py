import pygame
import config
from shape import dynamic_shape_object
from world import world_object

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode(config.SURFACE_SIZE)
surface = pygame.Surface(config.SURFACE_SIZE)
world = world_object()

main_shape:dynamic_shape_object = world.add_shape([100, 100], [[0, -40], [-40, 0], [0, 120], [40, 0]], "dynamic")
world.add_shape([300, 500], [[0, -40], [-40, 0], [0, 120], [40, 0]])
world.add_shape([500, 650], [[0, -80], [-50, -20], [-50, 90], [200, 90]])
world.add_shape([500, 300], [[-200, -100], [-100, 20], [20, -50]])
world.add_shape([0, 0], [[0, 0], [0, 20], [config.SURFACE_SIZE[0], 20], [config.SURFACE_SIZE[0], 0]])
world.add_shape([0, config.SURFACE_SIZE[1]-20], [[0, 0], [0, 20], [config.SURFACE_SIZE[0], 20], [config.SURFACE_SIZE[0], 0]])
world.add_shape([0, 0], [[20, 0], [0, 0], [0, config.SURFACE_SIZE[1]], [20, config.SURFACE_SIZE[1]]])
world.add_shape([config.SURFACE_SIZE[0]-20, 0], [[20, 0], [0, 0], [0, config.SURFACE_SIZE[1]], [20, config.SURFACE_SIZE[1]]])


flag = True
pressed = {'left':False, 'right':False, 'up':False, 'down':False}

while flag:
    clock.tick(config.FPS)
    surface.fill(config.FILL_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pressed['left'] = True
            elif event.key == pygame.K_RIGHT:
                pressed['right'] = True
            elif event.key == pygame.K_UP:
                pressed['up'] = True
            elif event.key == pygame.K_DOWN:
                pressed['down'] = True


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                pressed['left'] = False
            elif event.key == pygame.K_RIGHT:
                pressed['right'] = False
            elif event.key == pygame.K_UP:
                pressed['up'] = False
            elif event.key == pygame.K_DOWN:
                pressed['down'] = False

    if pressed['left']:
        main_shape.rotate(config.ROTATION_MULTIER)
    if pressed['right']:
        main_shape.rotate(-config.ROTATION_MULTIER)
    if pressed['up']:
        main_shape.move_forwards()
    if pressed['down']:
        main_shape.move_backwards()

    main_shape.update_variables(world.shapes)
    world.draw(surface)
    window.blit(surface, (0,0))
    pygame.display.update()

