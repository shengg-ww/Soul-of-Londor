# import module
import pygame
from pygame import mixer
import random

# initialise module
mixer.init()
pygame.init()
clock= pygame.time.Clock()
fps=120

# set screen dimensions
bottom_panel = 150
width=1080
screen_height=1920

# load music
# List of soundtrack filenames
soundtracks = ['Soul of Londor/public/Dark Souls III OST - Soul of Cinder.mp3',
                'Soul of Londor/public/Elden Ring OST - The Final Battle.mp3', 
                ]

# Randomly choose a soundtrack from the list
selected_soundtrack = random.choice(soundtracks)

# Load the selected soundtrack
pygame.mixer.music.load(selected_soundtrack)

# Set volume and play the music
pygame.mixer.music.set_volume(0.50)
pygame.mixer.music.play(-1, 0.0, 15000)

# load images
background_img=pygame.image.load('Soul of Londor/public/images/6yvp9ih93wv31.webp')

#define fonts
font_path = "Soul of Londor/public/Uncracked Free Trial-6d44.woff"
custom_font = pygame.font.Font(font_path, 68)
fontty='Soul of Londor/public/DragonHunter-9Ynxj.otf'
font = pygame.font.Font(fontty, 40)

# drawing background
def set_bg():
    screen.blit(background_img,(0,0))
    # sets text position
    draw_text(f'Hollow Knight', font, white, 197, 90)
    draw_text(f'Voidborne Harbinger', font, white, 1317, 80)

# create window
screen= pygame.display.set_mode((screen_height,width))
pygame.display.set_caption('Souls of Londor')




#define colours
red = (117, 24, 24)
white = (255,255,255)
black=(0,0,0)
purple=(193,50,255)
gold=(198,194,81)
green=(69,159,66)

#create function for drawing text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))
     


class Fighter():
    def __init__(self,x,y,name, max_hp,atk,potions):
        self.name=name
        self.max_hp=max_hp
        self.hp=max_hp
        self.atk=atk
        self.start_potion=potions
        self.potions=potions
        self.alive=True
        self.animation_list=[]
        self.frame_index=0
        self.attack_type=0
        self.update_time= pygame.time.get_ticks()
        for i in range(2):
           img= pygame.image.load(f'Soul of Londor/public/images/{self.name}/Idle/idle{i}.png')
           self.animation_list.append(img)
        self.image=self.animation_list[self.frame_index]
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.vel_y=0
    def move(self, screen_width, screen_height):
        SPEED = 10
        GRAVITY = 15  # Adjust the gravity value as needed
        JUMP_VELOCITY = -30  # Adjust the jump velocity as needed

        dx = 0
        dy = 0

        key = pygame.key.get_pressed()

        # movement buttons
        if key[pygame.K_a]:
            dx = -SPEED
        if key[pygame.K_d]:
            dx = SPEED
        if key[pygame.K_w] or key[pygame.K_SPACE]:
            dy = JUMP_VELOCITY

        #attack buttons 
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Left mouse button
            if key[pygame.K_LSHIFT]:  # Right mouse button
                draw_text("ULTIMATE",custom_font, gold, 197, 180)
                self.attack_type=4
            else:
                draw_text("LIGHT ATTACK",custom_font, green,197, 180)
                self.attack_type=1
        elif mouse_buttons[1]:  # middle mouse button
            draw_text("SPECIAL ATTACK",custom_font, purple,197, 180)
            self.attack_type=2
        elif mouse_buttons[2]:  # Right mouse button
            draw_text("HEAVY ATTACK",custom_font, red, 197, 180)
            self.attack_type=3
       
        # Apply gravity
        dy += GRAVITY

        if self.rect.left+ dx<0: 
            dx-=self.rect.left
        if self.rect.right+ dx>2*screen_width-370:
            dx=2*screen_width - self.rect.right-370
        # Prevent the character from moving off the screen vertically
        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.y-250))
        self.rect.x += dx  
        self.rect.y += dy 

    # method for attacking
    def attack(self):
        pass

    def update(self):
        animation_cooldown=100
        # handle animation
        self.image=self.animation_list[self.frame_index]
        if pygame.time.get_ticks()-self.update_time> animation_cooldown:
            self.update_time=pygame.time.get_ticks()
            self.frame_index+=1
        if self.frame_index>=len(self.animation_list):
            self.frame_index=0

    def draw(self):
        screen.blit(self.image,self.rect)

class HealthBar():
    def __init__(self, x, y, hp, max_hp, width):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        self.width = width
       

    def draw(self, hp):
		#update with new health
        self.hp = hp
		#calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, red, (self.x, self.y, 150 * ratio, 20))

#set position of characters   
knight= Fighter(327,800,'player',500,50,3)        
boss1= Fighter(1520,750,'boss1',10520,650,0)

# set position of health bar
knight_health_bar = HealthBar(197, 135, knight.hp, knight.max_hp,100)
boss1_health_bar = HealthBar(1317, 125, boss1.hp, boss1.max_hp,500)

run=True
while run:
    # draw bg
    set_bg()  
    knight.move(width,screen_height)

    knight.update()
    boss1.update()
  
    knight.draw()
    boss1.draw()
    clock.tick(fps)
    knight_health_bar.draw(knight.hp)
    boss1_health_bar.draw(boss1.hp)


    for event in pygame.event.get():
        # quit if user presses X button
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            run=False
        if event.type==pygame.QUIT:
            run=False
    pygame.display.update()
pygame.quit()