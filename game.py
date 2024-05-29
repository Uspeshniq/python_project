import pygame
pygame.init()

size = pygame.display.set_mode((500,480))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('C:/git/python_project/pictures/R1.png'), pygame.image.load('C:/git/python_project/pictures/R2.png'), pygame.image.load('C:/git/python_project/pictures/R3.png'), pygame.image.load('C:/git/python_project/pictures/R4.png'), pygame.image.load('C:/git/python_project/pictures/R5.png'), pygame.image.load('C:/git/python_project/pictures/R6.png'), pygame.image.load('C:/git/python_project/pictures/R7.png'), pygame.image.load('C:/git/python_project/pictures/R8.png'), pygame.image.load('C:/git/python_project/pictures/R9.png')]
walkLeft = [pygame.image.load('C:/git/python_project/pictures/L1.png'), pygame.image.load('C:/git/python_project/pictures/L2.png'), pygame.image.load('C:/git/python_project/pictures/L3.png'), pygame.image.load('C:/git/python_project/pictures/L4.png'), pygame.image.load('C:/git/python_project/pictures/L5.png'), pygame.image.load('C:/git/python_project/pictures/L6.png'), pygame.image.load('C:/git/python_project/pictures/L7.png'), pygame.image.load('C:/git/python_project/pictures/L8.png'), pygame.image.load('C:/git/python_project/pictures/L9.png')]
bg = pygame.image.load('C:/git/python_project/pictures/bg.jpg')
char = pygame.image.load('C:/git/python_project/pictures/standing.png')

clock = pygame.time.Clock()


class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
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
                size.blit(walkLeft[0], (self.x, self.y))
                


class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.speed = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

class enemy(object):
    walkRight = [pygame.image.load('C:/git/python_project/pictures/R1E.png'), pygame.image.load('C:/git/python_project/pictures/R2E.png'), pygame.image.load('C:/git/python_project/pictures/R3E.png'), pygame.image.load('C:/git/python_project/pictures/R4E.png'), pygame.image.load('C:/git/python_project/pictures/R5E.png'), pygame.image.load('C:/git/python_project/pictures/R6E.png'), pygame.image.load('C:/git/python_project/pictures/R7E.png'), pygame.image.load('C:/git/python_project/pictures/R8E.png'), pygame.image.load('C:/git/python_project/pictures/R9E.png'), pygame.image.load('C:/git/python_project/pictures/R10E.png'), pygame.image.load('C:/git/python_project/pictures/R11E.png')]
    walkLeft = [pygame.image.load('C:/git/python_project/pictures/L1E.png'), pygame.image.load('C:/git/python_project/pictures/L2E.png'), pygame.image.load('C:/git/python_project/pictures/L3E.png'), pygame.image.load('C:/git/python_project/pictures/L4E.png'), pygame.image.load('C:/git/python_project/pictures/L5E.png'), pygame.image.load('C:/git/python_project/pictures/L6E.png'), pygame.image.load('C:/git/python_project/pictures/L7E.png'), pygame.image.load('C:/git/python_project/pictures/L8E.png'), pygame.image.load('C:/git/python_project/pictures/L9E.png'), pygame.image.load('C:/git/python_project/pictures/L10E.png'), pygame.image.load('C:/git/python_project/pictures/L11E.png')]
    
    def __init__(self, x, y, widht, height, end):
        self.x = x
        self.y = y
        self.height = height
        self.widht = widht
        self.end = end
        self.WalkCount = 0
        self.speed = 3

    def draw(self, size):
        self.move()
        if self.WalkCount + 1 >= 33:
            self.WalkCount = 0

        if self.speed > 0:
            size.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
        else:
            size.blit(self.walkLeft[self.WalkCount//3], (self.x, self.y))
            self.walkCount += 1
    
    def move(self):
        if self.speed > 0:
            if self.x < self.path[1] + self.speed:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.x += self.speed
                self.WalkCount = 0


def redrawGameWindow():
    size.blit(bg, (0,0))
    manlike.draw(size)
    for bullet in bullets:
        bullet.draw(size)
    
    pygame.display.update()


#mainloop
manlike = player(200, 410, 64,64)
goblin = enemy(100, 410, 64, 64, 300)
bullets = []
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.speed
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if manlike.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 5:
            bullets.append(projectile(round(manlike.x + manlike.width //2), round(manlike.y + manlike.height//2), 6, (0,0,0), facing))

    if keys[pygame.K_LEFT] and manlike.x > manlike.speed:
        manlike.x -= manlike.speed
        manlike.left = True
        manlike.right = False
        manlike.standing = False
    elif keys[pygame.K_RIGHT] and manlike.x < 500 - manlike.width - manlike.speed:
        manlike.x += manlike.speed
        manlike.right = True
        manlike.left = False
        manlike.standing = False
    else:
        manlike.standing = True
        manlike.walkCount = 0
        
    if not(manlike.isJump):
        if keys[pygame.K_UP]:
            manlike.isJump = True
            manlike.right = False
            manlike.left = False
            manlike.walkCount = 0
    else:
        if manlike.jumpCount >= -10:
            var = 1
            if manlike.jumpCount < 0:
                var = -1
            manlike.y -= (manlike.jumpCount ** 2) * 0.5 * var
            manlike.jumpCount -= 1
        else:
            manlike.isJump = False
            manlike.jumpCount = 10
            
    redrawGameWindow()

pygame.quit()