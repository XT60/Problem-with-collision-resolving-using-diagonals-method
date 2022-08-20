import pygame
import config
from world import world_object

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode(config.SURFACE_SIZE)
surface = pygame.Surface(config.SURFACE_SIZE)
world = world_object()

main_shape = world.add_shape([[100, 100], [100, 140], [120, 140], [150, 130], [110, 90]])
world.add_shape([[500, 700], [460, 720], [510, 770]])
world.add_shape([[400, 500], [360, 520], [410, 570]])
world.add_shape([[100, 200], [30, 220], [110, 240], [140, 210]])
world.add_shape([[100, 350], [20, 560], [300, 300]])
world.add_shape([[600, 600], [600, 690], [690, 690], [690, 600]])
world.add_shape([[600, 0], [600, 400], [800, 400], [800, 0]])
world.add_shape([[410, 0], [200, 200], [300, 250], [500, 70]])
world.add_shape([[100, 600], [20, 650], [50, 780], [550, 250]])


flag = True
movement = [0,0]

while flag:
    clock.tick(config.FPS)
    surface.fill(config.FILL_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                movement[0] -= 1
            elif event.key == pygame.K_RIGHT:
                movement[0] += 1
            elif event.key == pygame.K_UP:
                movement[1] -= 1
            elif event.key == pygame.K_DOWN:
                movement[1] += 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                movement[0] += 1
            elif event.key == pygame.K_RIGHT:
                movement[0] -= 1
            elif event.key == pygame.K_UP:
                movement[1] += 1
            elif event.key == pygame.K_DOWN:
                movement[1] -= 1

    main_shape.move(movement)   
    world.update_variables()
    world.draw(surface)
    window.blit(surface, (0,0))
    pygame.display.update()

