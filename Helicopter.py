import pygame
import sys
import os
import random


class Obstacle(object):
    def __init__(self, x, width, screensize):
        self.x = x
        self.width = width
        self.y_top = 0
        self.top_height = random.randint(150, 250)
        self.distance = 200
        self.y_bottom = self.top_height + self.distance
        self.bottom_height = screensize[1] - self.y_bottom
        self.color = (160, 140, 190)
        self.speed = 5
        self.rect_top = pygame.Rect(
            self.x, self.y_top, self.width, self.top_height)
        self.rect_bottom = pygame.Rect(
            self.x, self.y_bottom, self.width, self.bottom_height)

    def update(self):
        self.x -= self.speed
        self.rect_top = pygame.Rect(
            self.x, self.y_top, self.width, self.top_height)
        self.rect_bottom = pygame.Rect(
            self.x, self.y_bottom, self.width, self.bottom_height)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect_top, 0)
        pygame.draw.rect(screen, self.color, self.rect_bottom, 0)

    def collision(self, player):
        if self.rect_top.colliderect(player) or self.rect_bottom.colliderect(player):
            return True
        else:
            return False


class Helicopter():
    def __init__(self, x, y):
        self.height = 30
        self.width = 40
        self.x = x
        self.y = y
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.model = pygame.image.load("Model.png")

    def update(self):
        self.y += self.speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self, screen):
        screen.blit(self.model, (self.x, self.y))


def write(screen, screensize, text, text_size):
    font = pygame.font.SysFont('Arial', text_size, False, False)
    sentence = font.render(text, 0, (255, 0, 0))

    x = int((screensize[0] - sentence.get_rect().width)*0.5)
    y = int((screensize[1] - sentence.get_rect().height)*0.5)

    screen.blit(sentence, (x, y))


def start_window():
    pygame.init()
    screensize = (700, 640)
    screen = pygame.display.set_mode(screensize)
    pygame.display.set_caption("Helicopter")
    while True:
        # event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game(screensize, screen)
                    break
        # render
        print(os.getcwd())
        graphic = pygame.image.load("Helicopter.png")
        write(screen, screensize, "Press space to play", 30)
        screen.blit(graphic, (180, 100))
        pygame.display.update()


def game(screensize, screen):
    obstacles = []
    font = pygame.font.SysFont("Times New Roman", 12, False, False)
    points = 0
    for i in range(21):
        obstacles.append(
            Obstacle(i*int(screensize[0]/20), int(screensize[0]/20), screensize))
    player = Helicopter(200, 280)
    while True:
        # fps
        pygame.time.delay(100)
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.speed = -5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player.speed = 5
        for o in obstacles:
            if o.x <= -o.width:
                obstacles.remove(o)
                points += 10
                obstacles.append(
                    Obstacle(screensize[0], int(screensize[0]/20), screensize))
            if o.collision(player.rect):
                start_window()
        # update
        player.update()
        for o in obstacles:
            o.update()
        # render
        screen.fill((0, 0, 0))
        player.render(screen)
        for o in obstacles:
            o.render(screen)
        text = font.render("Score: " + str(points), 0, (250, 0, 0))
        screen.blit(text, (40, 40))
        pygame.display.update()


start_window()
