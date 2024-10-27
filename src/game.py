import random

import pygame

import math

def displayText(text,size,x,y,position):
    font = pygame.font.Font("fonts/black-north-font/Blacknorthdemo-mLE25.otf",size)
    text = font.render(text,False,"white")
    if position == "center":
        rect = text.get_rect(center = (x,y))
    else:
        rect = text.get_rect(topleft = (x,y))
    screen.blit(text,rect)

class Game():
    def __init__(self,owlGroup,mouseGroup,youngGroup):
        self.owlGroup = owlGroup
        self.mouseGroup = mouseGroup
        self.youngGroup = youngGroup

    def hunt(self):
        owlMouseCollisions = pygame.sprite.groupcollide(self.owlGroup,self.mouseGroup,False,False)
        if owlMouseCollisions:
            caughtMouse = pygame.sprite.spritecollideany(self.owlGroup.sprite,self.mouseGroup)
            if self.owlGroup.sprite.clawState == "empty":
                caughtMouse.state = "caught"
                self.owlGroup.sprite.clawState = "full"


        youngMouseCollisions = pygame.sprite.groupcollide(self.youngGroup,self.mouseGroup,False,False)
        if youngMouseCollisions:
            self.youngGroup.sprite.mouseCount += 1
            fedMouse = pygame.sprite.spritecollideany(self.youngGroup.sprite,self.mouseGroup)
            fedMouse.state = "dead"
            self.owlGroup.sprite.clawState = "empty"
            if fedMouse.poisoned:
                self.youngGroup.sprite.health -= 1


    def update(self):
        self.owlGroup.update()
        self.mouseGroup.update(owlGroup.sprite.rect.x,owlGroup.sprite.rect.y)
        self.youngGroup.update()
        self.hunt()

class Owl(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.l1 = pygame.image.load("images/owlL1.png")
        self.l2 = pygame.image.load("images/owlL2.png")
        self.r1 = pygame.image.load("images/owlR1.png")
        self.r2 = pygame.image.load("images/owlR2.png")

        self.LSurfs = [self.l1,self.l2]
        self.RSurfs = [self.r1,self.r2]
        self.index = 0

        self.image = self.l1
        self.rect = self.image.get_rect(center = (screenX/2,screenY/2))

        self.speed = 3
        self.direction = "L"

        self.timer = 0


        self.clawState = "empty"



    def move(self):
        moveX = 0
        moveY = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            moveX = -self.speed
            self.direction = "L"
        elif keys[pygame.K_RIGHT]:
            moveX = self.speed
            self.direction = "R"
        elif keys[pygame.K_DOWN]:
            moveY = self.speed
        elif keys[pygame.K_UP]:
            moveY = -self.speed


        # MOVE
        self.rect.x += moveX
        self.rect.y += moveY

        if self.rect.y > screenY-200:
            self.rect.y = screenY-200
        elif self.rect.y < 0:
            self.rect.y = 0

        if self.rect.x > screenX:
            self.rect.x = 0
        elif self.rect.x < 0:
            self.rect.x = screenX

    def animate(self):
        if self.timer % 50 == 0:
            if self.index == 0:
                self.index = 1
            elif self.index == 1:
                self.index = 0

        if self.direction == "L":
            self.image = self.LSurfs[self.index]
        else:
            self.image = self.RSurfs[self.index]

    def update(self):
        self.move()
        self.animate()

        self.timer += 1

class Young(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/3owlets.png")
        self.rect = self.image.get_rect(center = (1100,345))
        self.health = 3
        self.mouseCount = 0

        self.oneOwlet = pygame.image.load("images/oneOwlet.png")
        self.twoOwlets = pygame.image.load("images/2owlets.png")
        self.threeOwlets = pygame.image.load("images/3owlets.png")

        self.oneJuv = pygame.image.load("images/1juv.png")
        self.twoJuv = pygame.image.load("images/2juv.png")
        self.threeJuv = pygame.image.load("images/3juv.png")

        self.owlets = [self.oneOwlet,self.twoOwlets,self.threeOwlets]
        self.juvs = [self.oneJuv,self.twoJuv,self.threeJuv]


    def displayStats(self):
        displayText("Mice caught: " + str(self.mouseCount),50,0,100,"left")

    def update(self):
        if self.mouseCount <= 2:
            self.image = self.owlets[self.health-1]
        else:
            self.image = self.juvs[self.health-1]

        self.displayStats()



class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/mouseL.png")
        self.rect = self.image.get_rect(center = (random.randrange(0,screenX),screenY-100))
        self.timer = 0

        self.state = "free"

        #decide poisoned or not
        num = random.randrange(0,10)
        if num < 2:
            self.poisoned = True
            self.speed = 1
        else:
            self.poisoned = False
            self.speed = 5

        self.xChange = random.randrange(-self.speed,self.speed)


    def moveFree(self,owlX,owlY):
        # avoid owl
        distance = math.sqrt((self.rect.x - owlX)**2 + (self.rect.y - owlY)**2)

        l = pygame.image.load("images/mouseL.png")
        r = pygame.image.load("images/mouseR.png")

        if distance < 200 and not self.poisoned:
            if self.rect.x < owlX:
                self.xChange = -random.randrange(2,4)

            else:
                self.xChange = random.randrange(2,4)
        # random movement
        else:
            if self.timer % 20 == 0:
                self.xChange = random.randrange(-self.speed,self.speed)


        # MOVE
        self.rect.x += self.xChange

        if self.xChange < 0:
            self.image = l
        else:
            self.image = r

        # bounce off edge of screen
        if self.rect.x > screenX:
            self.rect.x = 0
        elif self.rect.x < 0:
            self.rect.x = screenX

    def checkState(self):
        if self.state == "dead":
            self.kill()

    def update(self,owlX,owlY):
        if self.state == "free":
            self.moveFree(owlX,owlY)
        elif self.state == "caught":
            self.rect.x = owlX
            self.rect.y = owlY + 50
        elif self.state == "falling":
            self.rect.y += 5
        self.checkState()
        self.timer += 1


pygame.init()

screenX = 1400
screenY = 800
screen = pygame.display.set_mode((screenX,screenY))
clock = pygame.time.Clock()
pygame.display.set_caption("Mousehunter")

#backgrounds

background = pygame.image.load("images/background.png")
ground = pygame.Surface((screenX,100))
ground.fill("darkgreen")
black = pygame.Surface((screenX,screenY))
black.fill("black")

#sprite groups
owlGroup = pygame.sprite.GroupSingle()
owlGroup.add(Owl())
mouseGroup = pygame.sprite.Group()
for i in range(20):
    mouseGroup.add(Mouse())
youngGroup = pygame.sprite.GroupSingle()
youngGroup.add(Young())
print(str(youngGroup.sprite.health))

game = Game(owlGroup,mouseGroup,youngGroup)

gameState = "start"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if gameState == "start":
        screen.blit(black,(0,0))
        displayText("Mousehunter",100,screenX/2,screenY/2,"center")
        displayText("Hunt mice, feed them to your young",20,screenX/2,screenY/2+100,"center")
        displayText("Poisoned mice move slow and will not flee, AVOID AT ALL COSTS",20,screenX/2,screenY/2+200,"center")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            gameState = "playing"
    elif gameState == "playing":
        screen.blit(background,(0,0))
        screen.blit(ground,(0,screenY-100))
        if youngGroup.sprite.health <= 0 or youngGroup.sprite.mouseCount >= 5:
            gameState = "end"

        owlGroup.draw(screen)
        mouseGroup.draw(screen)
        youngGroup.draw(screen)
        game.update()

    elif gameState == "end":
        screen.blit(black,(0,0))

        displayText("You raised " + str(youngGroup.sprite.health) + " chicks!",50,screenX/2,screenY/2,"center")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            gameState = "playing"

    pygame.display.update()
    clock.tick(60)
