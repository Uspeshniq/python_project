# copyright 2024
import pygame

pygame.init()

win = pygame.display.set_mode((500,480))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()


class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True

    def draw(self, size):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                size.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                size.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
            else:
                if self.right:
                    size.blit(walkRight[0], (self.x, self.y))
                else:
                    win.blit(walkLeft[0], (self.x, self.y))

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.speed = 8 * facing
    def draw(self,size):
        pygame.draw.circle(size, self.color, (self.x, self.y), self.radius)


def redrawGameWindow():
    win.blit(bg, (0,0))
    manlike.draw(win)
    
    pygame.display.update()


manlike = player(200, 410, 64,64)
execute = True
while execute:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            execute = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and manlike.x > manlike.vel:
        manlike.x -= manlike.vel
        manlike.left = True
        manlike.right = False
    elif keys[pygame.K_RIGHT] and manlike.x < 500 - manlike.width - manlike.vel:
        manlike.x += manlike.vel
        manlike.right = True
        manlike.left = False
    else:
        manlike.right = False
        manlike.left = False
        manlike.walkCount = 0
        
    if not(manlike.isJump):
        if keys[pygame.K_SPACE]:
            manlike.isJump = True
            manlike.right = False
            manlike.left = False
            manlike.walkCount = 0
    else:
        if manlike.jumpCount >= -10:
            neg = 1
            if manlike.jumpCount < 0:
                neg = -1
            manlike.y -= (manlike.jumpCount ** 2) * 0.5 * neg
            manlike.jumpCount -= 1
        else:
            manlike.isJump = False
            manlike.jumpCount = 10
            
    redrawGameWindow()

pygame.quit()
