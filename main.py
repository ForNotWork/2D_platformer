import pygame
import random
import SpreadSheet
import math
#initializing
pygame.init()
screen_width = 400
screen_height = 600
#screen/game window
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('where_ert')
#true
shoot = False
#fps
clock = pygame.time.Clock()
fps = 60
#ENVIRONMENT
bg_Gravity = 5
#platform
Max_bullet = 5
# PLATFORM_gravity = 0.01
# platform_scroll = 0
#cube
Max_CUBE = 20
# cube_gravity = 0
cube_scroll = 0
bg_scroll = 0
#bomb
# bomb_action = 0
Max_bomb = 10
bomb_scroll = 0
robo = pygame.image.load('reso/robo.png').convert_alpha()
bg_img = pygame.image.load('reso/bg_tile.png').convert_alpha()
# platform_img = pygame.image.load('reso/platform.png').convert_alpha()
cube_img = pygame.image.load('reso/cube.png').convert_alpha()
cube_w = cube_img.get_width()
cube_h = cube_img.get_height()
cube_img = pygame.transform.scale(cube_img,(int(cube_w * 1),int(cube_h * 1)))
#spring = pygame.image.load('reso/spring.png').convert_alpha()
#tele = pygame.image.load('reso/teleport.png').convert_alpha()
bomb_img = pygame.image.load('reso/bomb.png').convert_alpha()
bomb_sheet = SpreadSheet.SpriteSheet(bomb_img)
animation_list = []
for animation in range(0,4):
    animation_list.append(bomb_sheet.get_image(animation,0,16,16,3,(0,0,0)))

The_cube = pygame.image.load('res/square.png').convert_alpha()
class Base():
    def __init__(self,x,y):
        self.image = pygame.transform.scale(The_cube,(400,100))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.health = 100
    
    def draw(self):
        screen.blit(self.image,self.rect)
    
    
    # def update(self,bomb_group):
    #     for bombs in bomb_group:
    #         if bombs.rect.colliderect(base.rect.x,base.rect.y,base.width,base.height):
    #             if bombs.rect.top < base.rect.bottom:
    #                 # bombs.kill()
    #                 base.health -= 1#random.randint(1,10)
    #                 bombs.react_b = True
    #                 bombs.explode()
        
#drawing background
def draw_bg(bg_scroll):
    screen.blit(bg_img,(0,0 - bg_scroll))
    screen.blit(bg_img,(0,600 - bg_scroll))

font_large = pygame.font.SysFont('lucida Sans', 24)
def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))

#class player
class Player():
    def __init__(self,x,y):
        self.image = pygame.transform.scale(robo,(35,35))
        self.image.set_colorkey((0,0,0))
        self.width = 35
        self.height = 35
        self.rect =  pygame.Rect(0,0,self.width,self.height)
        # self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speed = 0.3
        self.fired = False
        self.score = 0
        self.count = 0

    def draw(self):
        #screen.blit(self.image,self.rect.x - 12,self.rect.y - 15)
        screen.blit(self.image,self.rect)
    
    def shoot(self):
        # pos = pygame.mouse.get_pos()
        # x_dist = pos[0] - self.rect.midleft[0]
        # y_dist = -(pos[1] - self.rect.midleft[1])
        # self.angle = math.degrees(math.atan2(y_dist, x_dist))
        # pos = pygame.mouse.get_pos()
        for bombs in bomb_group:
            x_dist = bombs.rect.x - self.rect.midleft[0]
            y_dist = -(bombs.rect.y - self.rect.midleft[1])
            self.angle = math.degrees(math.atan2(y_dist, x_dist))
		#get mouseclick
            # if pygame.mouse.get_pressed()[0] and self.fired == False:
            if self.fired == True:
                self.fired = False
            if (math.sqrt((x_dist)**2 + (y_dist)**2) < 150) and self.fired == False:
                self.fired = True
                if len(cube_group) < Max_bullet and self.count == 0:
                    bullet = Cube(cube_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
                    cube_group.add(bullet)
                # self.count += 0.1
                # if self.count > 2:
                #     self.count = 0
		#reset mouseclick
            # if pygame.mouse.get_pressed()[0] == False:
            # if self.fired == True:
            #     self.fired = False
        
    def move(self):
        dx = 0
        dy = 0
        
        #key presses
        # key = pygame.key.get_pressed()
        # if key[pygame.K_a]:
        #     dx -= 5
        # if key[pygame.K_d]:
        #     dx += 5
        # if key[pygame.K_w]:
        #     dy -= 5
        # if key[pygame.K_s]:
        #     dy += 5
        for bombs in bomb_group:
            x_Dist = bombs.rect.x - self.rect.midleft[0]
            y_Dist = -(bombs.rect.y - self.rect.midleft[1])
            if(math.sqrt((x_Dist)**2 + (y_Dist)**2) < 300):
                if self.rect.x < bombs.rect.x:
                    dx += 1
                else:
                    dx -= 1
                if self.rect.y < bombs.rect.y:
                    dy += 1
                else:
                    dy -= 1
        #collision
        if self.rect.right + dx < 0:
            dx = screen_width
        if self.rect.left + dx >screen_width:
            dx = -self.rect.left
        if self.rect.top +dy >300:#screen_height:
            dy = -self.rect.top
        if self.rect.bottom + dy < 35:
            dy = 300#screen_height
        #update
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

#cubes
class Cube(pygame.sprite.Sprite):
    def __init__(self,image,x,y,angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle)
        self.speed = 5
        self.vel_y = -(math.sin(self.angle) * self.speed)
        self.vel_x = math.cos(self.angle) * self.speed
    
    def update(self):
        if self.rect.right < 0 or self.rect.left > screen_width or self.rect.bottom < 0 or self.rect.top > screen_height:
            self.kill()
            
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
#exsplosion
class Bomb(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.bomb_action = 0
        self.cool = 0
        self.image = animation_list[self.bomb_action]
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 1
        self.react_B = False
        self.react_b = False
        
    def explode(self):
        # for bombs in bomb_group:
            if self.react_b == True :#or bombs.react_B:
                # base.health -= random.randint(1,3)
                self.cool += 0.1
                if self.cool >2:
                    self.cool = 0.1
                    self.bomb_action += 1
                if self.bomb_action >3:
                    self.bomb_action = 0
                    self.kill()
                    robo.score += random.randint(1,5)
                self.image = animation_list[self.bomb_action]
            if self.react_B == True:#or bombs.react_B:
                # base.health -= random.randint(1,3)
                self.cool += 0.1
                if self.cool >1:
                    self.cool = 0.1
                    self.bomb_action += 1
                if self.bomb_action >3:
                    self.bomb_action = 0
                    self.kill()
                    base.health -= 3#random.randint(1,10)
                self.image = animation_list[self.bomb_action]
            # if bombs.react_b :#or bombs.react_B:
            #     # base.health -= random.randint(1,3)
            #     bombs.cool += 0.1
            #     if bombs.cool >2:
            #         bombs.cool = 0.1
            #         bombs.bomb_action += 1
            #     if bombs.bomb_action >3:
            #         bombs.bomb_action = 0
            #         bombs.kill()
            #         robo.score += random.randint(1,5)
            #     bombs.image = animation_list[bombs.bomb_action]
            # elif bombs.react_B :#or bombs.react_B:
            #     # base.health -= random.randint(1,3)
            #     bombs.cool += 0.1
            #     if bombs.cool >1:
            #         bombs.cool = 0.1
            #         bombs.bomb_action += 1
            #     if bombs.bomb_action >3:
            #         bombs.bomb_action = 0
            #         bombs.kill()
            #         base.health -= 3#random.randint(1,10)
            #     bombs.image = animation_list[bombs.bomb_action]
    
    def update(self,bomb_scroll):
        self.rect.y -= bomb_scroll * self.vel_y
        if self.rect.top <= 0:
            self.kill()

def check_collison():
    for bombs in bomb_group:
        for cubes in cube_group:
            if bombs.rect.colliderect(cubes.rect.x,cubes.rect.y,cubes.width,cubes.height):
                if cubes.rect.bottom > bombs.rect.top:
                    # robo.score += 1
                    cubes.kill()
                    bombs.react_b = True
                    # bombs.explode()
    # for bombs in bomb_group:
            if bombs.rect.colliderect(base.rect.x,base.rect.y,base.width,base.height):
                if base.rect.bottom > bombs.rect.top:
                    # base.health -= 1#random.randint(1,10)
                    bombs.react_B = True
                    # bombs.explode()
#player
robo = Player(screen_width//2,200)
#brain
base = Base(0,0)
# #bomb
bomb_group = pygame.sprite.Group()
bomb = Bomb(300,400)
bomb_group.add(bomb)
#cube
cube_group = pygame.sprite.Group()

#game loop
spawn_point = False
run = True
while run:
    clock.tick(fps)
    
    #draw back
    bg_scroll += bg_Gravity
    if bg_scroll > 600:
        bg_scroll = 0
    draw_bg(bg_scroll)
    
    #brain
    base.draw()
    
    #robo
    robo.move()
    robo.shoot()
    robo.draw()
    
    #cube
    
    #cube gravity
    cube_group.update()
    cube_group.draw(screen)
    pos = pygame.mouse.get_pos()
    #bombs
    if pygame.mouse.get_pressed()[0] == True and spawn_point == False:
        spawn_point = True
    #     pos = pygame.mouse.get_pos()
    # if pygame.mouse.get_pressed()[0] == True:
    if pygame.mouse.get_pressed()[0] == False and spawn_point == True:
        if len(bomb_group) < Max_bomb:
            p_w = random.randint(40, 60)
            # p_x = random.randint(0,screen_width - p_w)
            p_x = pos[0]#random.randint(0,screen_width - p_w)
            # p_y = bomb.rect.y + random.randint(80, 100)
            p_y = pos[1]#bomb.rect.y + random.randint(80, 100)
            # bomb = Bomb(p_x,p_y,p_w)
            bomb = Bomb(p_x,p_y)
            bomb_group.add(bomb)
            spawn_point = False
            # pos = [0,0]
    
    #bomb gravity
    bomb_scroll = random.randint(1,3)
    bomb_group.update(bomb_scroll)
    for bombs in bomb_group:
        bombs.explode()
    bomb_group.draw(screen)
    
    #dead
    check_collison()
    #base.update(bomb_group)

    draw_text('SCORE : ' + str(robo.score),font_large,(255,255,255),250,0)
    draw_text('HEALTH : ' + str(base.health),font_large,(255,255,255),0,0)
    
    #game over
    if base.health < 0 :
        run = False
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()
pygame.quit()
