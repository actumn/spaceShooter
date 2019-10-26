import random
from os import path

import pygame

from spaceshooter import WIDTH, HEIGHT, WHITE, BLACK, BAR_LENGTH, BAR_HEIGHT, GREEN, FPS, font_name, sound_folder, img_dir, clock
from spaceshooter.asset import screen, background, background_rect, player_mini_img
from spaceshooter.objects import Mob, Player, Explosion, Pow
from spaceshooter.sound import expl_sounds, player_die_sound


class Game:
    pygame.display.set_caption('Space shooter')

    def __init__(self):
        self.screen = screen
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()

        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.score = 0

        self.player = Player(self)
        self.all_sprites.add(self.player)

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)

        self.screen.blit(text_surface, text_rect)

    def main_menu(self):
        pygame.mixer.music.load(path.join(sound_folder, 'menu.ogg'))
        pygame.mixer.music.play(-1)

        title = pygame.image.load(path.join(img_dir, 'main.png')).convert()
        title = pygame.transform.scale(title, (WIDTH, HEIGHT), self.screen)

        self.screen.blit(title, (0, 0))

        pygame.display.update()

        while True:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    break
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()
            else:
                self.draw_text('PRESS [ENTER] TO Begin', 30, WIDTH / 2, HEIGHT / 2)
                self.draw_text('or [Q] To Quit', 30, WIDTH / 2, (HEIGHT / 2) + 40)
                pygame.display.update()

        ready = pygame.mixer.Sound(path.join(sound_folder, 'getready.ogg'))
        ready.play()
        self.screen.fill(BLACK)
        self.draw_text('GET READY!', 40, WIDTH / 2, HEIGHT / 2)
        pygame.display.update()

    def draw_shield_bar(self, x, y, pct):
        pct = max(pct, 0)
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)

        pygame.draw.rect(self.screen, GREEN, fill_rect)
        pygame.draw.rect(self.screen, WHITE, outline_rect, 2)

    def draw_lives(self, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y
            self.screen.blit(img, img_rect)

    def new_mob(self):
        mob_element = Mob()
        self.all_sprites.add(mob_element)
        self.mobs.add(mob_element)

    def add_sprite(self, sprite):
        self.all_sprites.add(sprite)

    def add_bullet(self, bullet):
        self.bullets.add(bullet)

    def run(self):
        global death_explosion
        running = True
        menu_display = True
        while running:
            if menu_display:
                game.main_menu()
                pygame.time.wait(3000)

                pygame.mixer.music.stop()
                # Play the gameplay music
                pygame.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
                pygame.mixer.music.play(-1)     # makes the gameplay sound in an endless loop

                menu_display = False

                for _ in range(8):
                    self.new_mob()

            # step 1: process input
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # step 2: update
            self.all_sprites.update()

            # check if a bullet hit a mob
            # now we have a group of bullets and a group of mob
            hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)

            # now as we delete the mob element when we hit one with a bullet, we need to respawn them again
            # as there will be no mob_elements left out
            for hit in hits:
                self.score += 50 - hit.radius  # give different scores for hitting big and small metoers
                random.choice(expl_sounds).play()
                # m = Mob()
                # all_sprites.add(m)
                # mobs.add(m)
                expl = Explosion(hit.rect.center, 'lg')
                self.all_sprites.add(expl)
                if random.random() > 0.9:
                    pow = Pow(hit.rect.center)
                    self.all_sprites.add(pow)
                    self.powerups.add(pow)
                self.new_mob()  # spawn a new mob

            # ^^ the above loop will create the amount of mob objects which were killed spawn again
            #########################

            # check if the player collides with the mob
            hits = pygame.sprite.spritecollide(self.player, self.mobs, True,
                                               pygame.sprite.collide_circle)  # gives back a list, True makes the mob element disappear
            for hit in hits:
                self.player.shield -= hit.radius * 2
                expl = Explosion(hit.rect.center, 'sm')
                self.all_sprites.add(expl)
                self.new_mob()
                if self.player.shield <= 0:
                    player_die_sound.play()
                    death_explosion = Explosion(self.player.rect.center, 'player')
                    self.all_sprites.add(death_explosion)
                    self.player.hide()
                    self.player.lives -= 1
                    self.player.shield = 100

            # if the player hit a power up
            hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
            for hit in hits:
                if hit.type == 'shield':
                    self.player.shield += random.randrange(10, 30)
                    if self.player.shield >= 100:
                        self.player.shield = 100
                if hit.type == 'gun':
                    self.player.powerup()

            # if player died and the explosion has finished, end game
            if self.player.lives == 0 and not death_explosion.alive():
                running = False

            # 3 Draw/render
            screen.fill(BLACK)
            # draw the stargaze.png image
            screen.blit(background, background_rect)

            self.all_sprites.draw(screen)
            self.draw_text(str(self.score), 18, WIDTH / 2, 10)  # 10px down from the screen
            self.draw_shield_bar(5, 5, self.player.shield)

            # Draw lives
            self.draw_lives(WIDTH - 100, 5, self.player.lives, player_mini_img)

            # Done after drawing everything to the screen
            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
