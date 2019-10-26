from os import path

import pygame

from spaceshooter import BLACK, WIDTH, HEIGHT, img_dir

screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
missile_img = pygame.image.load(path.join(img_dir, 'missile.png')).convert_alpha()

meteor_images = [
    pygame.image.load(path.join(img_dir, image)) for image in [
        'meteorBrown_big1.png',
        'meteorBrown_big2.png',
        'meteorBrown_med1.png',
        'meteorBrown_med3.png',
        'meteorBrown_small1.png',
        'meteorBrown_small2.png',
        'meteorBrown_tiny1.png',
    ]
]

explosion_anime = {
    'lg': [],
    'sm': [],
    'player': [],
}
for i in range(9):
    img = pygame.image.load(path.join(img_dir, f'regularExplosion0{i}.png')).convert()
    img.set_colorkey(BLACK)

    # resize explosion
    explosion_anime['lg'].append(pygame.transform.scale(img, (75, 75)))
    explosion_anime['sm'].append(pygame.transform.scale(img, (32, 32)))

    # player explosion
    img = pygame.image.load(path.join(img_dir, f'sonicExplosion0{i}.png')).convert()
    img.set_colorkey(BLACK)
    explosion_anime['player'].append(img)

# load power ups
powerup_images = {
    'shield': pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert(),
    'gun': pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert(),
}

