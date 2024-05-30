import pygame
import random

pygame.init()

win_width, win_height = 800, 600
win = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption("First Game")


walkRight = [pygame.image.load(f'C:/MOJE DA PIPAME/coding/PROJECT!!!/python_project/pictures/R{i}.png') for i in range(1, 10)]
walkLeft = [pygame.image.load(f'C:/MOJE DA PIPAME/coding/PROJECT!!!/python_project/pictures/L{i}.png') for i in range(1, 10)]
bg = pygame.image.load('C:/MOJE DA PIPAME/coding/PROJECT!!!/python_project/pictures/bg.jpg') 
bg = pygame.transform.scale(bg, (win_width, win_height))  # Resize the background to fit the window
char = pygame.image.load('C:/MOJE DA PIPAME/coding/PROJECT!!!/python_project/pictures/standing.png')


bulletSound = pygame.mixer.Sound('C:/MOJE DA PIPAME/coding/PROJECT!!!/python_project/sound effects/bullet.mp3')
hitSound = pygame.mixer.Sound('C:/MOJE DA PIPAME/coding/PROJECT!!!/python_project/sound effects/hit.mp3')
music = pygame.mixer.music.load('C:/MOJE DA PIPAME/coding/PROJECT!!!/python_project/sound effects/music.mp3')
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
score = 0
jump_height = 10  

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = jump_height
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
       

    def hit(self):
        self.isJump = False
        self.jumpCount = jump_height
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (win_width // 2 - text.get_width() // 2, win_height // 2 - text.get_height() // 2))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Enemy(object):
    walkRight = [pygame.image.load(f'C:/MOJE DA PIPAME/coding/PROJECT!!!/python_project/pictures/R{i}E.png') for i in range(1, 12)]
    walkLeft = [pygame.image.load(f'C:/MOJE DA PIPAME/coding/PROJECT!!!/python_project/pictures/L{i}E.png') for i in range(1, 12)]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True
        self.isJump = False
        self.jumpCount = jump_height
        self.jumpVel = 8  

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

    def move(self):
        if self.visible:
            if self.x < man.x:
                self.x += self.vel
                self.right = True
                self.left = False
            elif self.x > man.x:
                self.x -= self.vel
                self.right = False
                self.left = True

            if not self.isJump:
                if self.y + self.hitbox[3] < man.y + man.hitbox[3]:
                    self.isJump = True
            else:
                if self.jumpCount >= -jump_height:
                    neg = 1        
                    if self.jumpCount < 0:
                        neg = -1
                    self.y -= (self.jumpCount ** 2) * 0.5 * neg
                    self.jumpCount -= 1
                else:
                    self.isJump = False
                    self.jumpCount = jump_height

            for plat in platforms:
                if self.hitbox[1] + self.hitbox[3] >= plat.y and self.hitbox[1] + self.hitbox[3] <= plat.y + 5:
                    if self.hitbox[0] + self.hitbox[2] > plat.x and self.hitbox[0] < plat.x + plat.width:
                        self.y = plat.y - self.hitbox[3]
                        self.isJump = False
                        self.jumpCount = jump_height

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
            self.x = random.randint(0, win_width - self.width)
            self.y = 410
            self.health = 10
            self.visible = True
        print('hit')

class Platform(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, win):
        pygame.draw.rect(win, (139, 69, 19), self.rect)

def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (win_width - text.get_width() - 10, 10))
    man.draw(win)
    for goblin in goblins:
        goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    for plat in platforms:
        plat.draw(win)
    pygame.display.update()


font = pygame.font.SysFont('comicsans', 30, True)
man = Player(300, 410, 64, 64)
bullets = []
goblins = [Enemy(random.randint(0, win_width - 64), 410, 64, 64, 450) for _ in range(3)]  # Multiple monsters
platforms = [
    Platform(100, 500, 200, 10),
    Platform(400, 400, 200, 10),
    Platform(600, 300, 200, 10)
]

run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    for bullet in bullets:
        for goblin in goblins:
            if goblin.visible:
                if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                    if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                        hitSound.play()
                        goblin.hit()
                        score += 1
                        bullets.pop(bullets.index(bullet))

        if 0 < bullet.x < win_width:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:
            bulletSound.play()
            facing = -1 if man.left else 1
            bullets.append(Projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < win_width - man.width - man.vel:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -jump_height:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = jump_height

    redrawGameWindow()

pygame.quit()

