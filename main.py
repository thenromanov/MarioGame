import pygame
import os
import sys


class Tile(pygame.sprite.Sprite):
    def __init__(self, type, x, y, *groups):
        super().__init__(groups)
        self.image = images[type]
        self.rect = self.image.get_rect().move(x * imageSize[0], y * imageSize[1])


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(groups)
        self.image = playerImage
        self.rect = self.image.get_rect().move(x * imageSize[0], y * imageSize[1])

    def transfer(self, dx, dy):
        self.rect = self.rect.move(dx, dy)
        if pygame.sprite.spritecollideany(self, walls):
            self.rect = self.rect.move(-dx, -dy)


def loadImage(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def loadLevel(name):
    filename = 'data/' + name
    with open(filename) as mapFile:
        levelMap = [line.strip() for line in mapFile]
        maxWidth = max(map(len, levelMap))
        return list(map(lambda x: x.ljust(maxWidth, '.'), levelMap))


def terminate():
    pygame.quit()
    sys.exit()


def startScreen():
    text = ["ЗАСТАВКА", "",
            "Правила игры",
            "Если в правилах несколько строк,",
            "приходится выводить их построчно"]
    bg = pygame.transform.scale(loadImage('bg.jpg'), screenSize)
    screen.blit(bg, (0, 0))
    font = pygame.font.Font(None, 30)
    textCoord = 50
    for line in text:
        string = font.render(line, 1, pygame.Color('black'))
        rect = string.get_rect()
        textCoord += 10
        rect.top = textCoord
        rect.x = 10
        textCoord += rect.height
        screen.blit(string, rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
players = pygame.sprite.Group()


def generateLevel(level):
    newPlayer, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, sprites)
            elif level[y][x] == '#':
                Tile('wall', x, y, sprites, walls)
            elif level[y][x] == '@':
                Tile('empty', x, y, sprites)
                newPlayer = Player(x, y, players)
    return newPlayer, x, y


fps = 50
screenSize = (550, 550)
imageSize = (50, 50)

pygame.init()
screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()

playerImage = loadImage('mar.png')
images = {
    'wall': loadImage('box.png'),
    'empty': loadImage('grass.png')
}

player, x, y = generateLevel(loadLevel('level1.txt'))

startScreen()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player.transfer(10, 0)
    if keys[pygame.K_UP]:
        player.transfer(0, -10)
    if keys[pygame.K_LEFT]:
        player.transfer(-10, 0)
    if keys[pygame.K_DOWN]:
        player.transfer(0, 10)
    sprites.draw(screen)
    players.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
terminate()
