# import module
import pygame
from pygame import mixer
import random
import sys
import button

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
soundtracks = ['public\Dark Souls III OST - Soul of Cinder.mp3',
                'public\Elden Ring OST - The Final Battle.mp3', 
                ]

# Randomly choose a soundtrack from the list
selected_soundtrack = random.choice(soundtracks)

# Load the selected soundtrack
pygame.mixer.music.load(selected_soundtrack)

# Set volume and play the music
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1, 0.0, 5000)

sword_fx = pygame.mixer.Sound("public/bloody-blade-103593.mp3")
sword_fx.set_volume(0.2)
magic_fx = pygame.mixer.Sound("public\\hq-explosion-6288.mp3")
magic_fx.set_volume(0.3)


# load images
background_img=pygame.image.load('public/images/6yvp9ih93wv31.webp')
potion_img= pygame.image.load('public/images/Elden-Ring-Flask-of-Wondrous-Physick.webp')

#define fonts
font_path = "public/Uncracked Free Trial-6d44.woff"
custom_font = pygame.font.Font(font_path, 68)
fontty='public/DragonHunter-9Ynxj.otf'
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
potion_effect = 250

#create function for drawing text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


def game_over_screen():
    game_over = True
    
    # Load the faded image
    faded_image = pygame.image.load("public\\images\\6yvp9ih93wv31.webp").convert_alpha()

    while game_over:
        # Display the faded image as the background
        screen.blit(faded_image, (0, 0))
        game_over_font =font
        # Display victory 
        if boss1.hp <= 0:
            
            game_over_text = game_over_font.render("LEGEND FELLED", True, (255, 255, 255))
            
        
        # Display defeat
        if knight.hp<=0:
            game_over_text = game_over_font.render("YOU DIED", True, (255, 255, 255))
        
        screen.blit(game_over_text, (width // 2 + 200, screen_height // 4))
        # Display options as interactive buttons
        options_font = pygame.font.Font(font_path, 36)
        
        # Play Again Button
        play_again_text = options_font.render("Play Again", True, (255, 255, 255))
        play_again_rect = pygame.Rect(width // 2 + 200, screen_height // 4 + 50, 200, 50)
        pygame.draw.rect(screen, (0, 255, 0), play_again_rect)
        screen.blit(play_again_text, (width // 2 + 210, screen_height // 4 + 55))
        
        # Exit Button
        exit_text = options_font.render("Exit", True, (255, 255, 255))
        exit_rect = pygame.Rect(width // 2 + 200, screen_height // 4 + 120, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), exit_rect)
        screen.blit(exit_text, (width // 2 + 210, screen_height // 4 + 125))
        
        pygame.display.update()
        
        # Handle events
        for event in pygame.event.get(): 
            key = pygame.key.get_pressed()
            if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or key[pygame.K_RETURN]:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(mouse_pos):
                    # Reset game state
                    knight.hp = knight.max_hp
                    boss1.hp = boss1.max_hp
                    knight.potions=knight.start_potion
                    knight.rect.center = (327, 800)
                    boss1.rect.center = (1520, 750)
                    game_over = False
                elif exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        
        # Handle events
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(mouse_pos):
                    # Reset game state
                    knight.hp = knight.max_hp
                    boss1.hp = boss1.max_hp
                    knight.rect.center = (327, 800)
                    boss1.rect.center = (1520, 750)
                    game_over = False
                elif exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()



class Fighter():
    def __init__(self, x, y, flip, name, max_hp, atk, potions, sound):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.atk = atk
        self.flip = flip
        self.start_potion = potions
        self.potions = potions
        self.alive = True
        self.action = 0
        self.animation_list = []
        self.frame_index = 0
        self.attack_type = 0
        self.attacking = False
        self.cooldown=0
        self.cooldowns = {
            1: 0,  # Light Attack
            2: 0,  # Heavy Attack
            3: 0,  # ULtimate Attack
            "ai_attack": 0
        }
        self.cooldown_durations = {
            1: 500,  # Light Attack cooldown duration
            2: 50,  # Heavy Attack cooldown duration
            3: 500  # Ultimate Attack cooldown duration
        }
        self.attack_sound = sound
        self.hit = False
        self.jump = False
        self.running = False
        self.update_time = pygame.time.get_ticks()
        for i in range(2):
            img = pygame.image.load(f'public/images/{self.name}/0/idle{i}.png')
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_y = 0

        # Initialize font
        self.font = pygame.font.Font(None, 36)

    def flip_image(self):
        self.image = pygame.transform.flip(self.animation_list[self.frame_index], True, False)
    
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    def move(self, screen_width, screen_height):
        SPEED = 10
        GRAVITY = 10
        JUMP_VELOCITY = -20

        dx = 0
        dy = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_a]:
            dx = -SPEED
        if key[pygame.K_d]:
            dx = SPEED
        if key[pygame.K_w] or key[pygame.K_SPACE]:
            dy = JUMP_VELOCITY
            self.jump = True
            self.image = pygame.image.load(f'public/images/{self.name}/1/idle0.png').convert_alpha()

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.cooldowns[1] <= 0:
            if key[pygame.K_LSHIFT]:
                draw_text("ULTIMATE", self.font, (255, 215, 0), 537, 100)
                self.attack_type = 3
            else:
                draw_text("LIGHT ATTACK", self.font, (0, 255, 0), 537, 100)
                self.attack_type = 1
            self.attack(boss1)

        elif mouse_buttons[2] and self.cooldowns[2] <= 0:
            self.attack(boss1)
            draw_text("HEAVY ATTACK", self.font, (255, 0, 0), 537, 100)
            self.attack_type = 2
        
        # Update the action based on key release
        if not any(key):
            self.jump=True
            self.image = pygame.image.load(f'public/images/{self.name}/0/idle1.png').convert_alpha()

        dy += GRAVITY

        if self.rect.left + dx < 0:
            dx -= self.rect.left
        if self.rect.right + dx > 2 * screen_width - 370:
            dx = 2 * screen_width - self.rect.right - 370

        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.y - 250))
        self.rect.x += dx
        self.rect.y += dy

        if boss1.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

    def ai_move(self, screen_width, screen_height):
        if self.cooldown <= 0:
            MAX_DX = 400  
            MAX_DY = 200  

            max_x = screen_width 
            max_y = screen_height - self.rect.height * 3

            dx = random.randint(-MAX_DX, MAX_DX) 
            dy = random.randint(-MAX_DY, MAX_DY)

            new_x = self.rect.x + dx
            new_y = self.rect.y + dy

            new_x = max(0, min(new_x, max_x))
            new_y = max(0, min(new_y, max_y))

            self.rect.x = new_x
            self.rect.y = new_y

            self.cooldown = 60
        else:
            self.cooldown -= 1

    def attack(self, target):
        if self.cooldowns[self.attack_type] <= 0:
            if self.attack_type == 1:
                attack_hitbox = pygame.Rect(self.rect.centerx - (1 * self.rect.width * self.flip),
                                            self.rect.y, self.rect.width, self.rect.height)
                damage = self.atk - 25
                self.attack_sound = pygame.mixer.Sound('public\\bloody-blade-103593.mp3')
                self.attack_sound.set_volume(0.5)
                self.attack_sound.play()
                self.attack_image = pygame.image.load('public\\images\\42-425182_sword-slash-effect-png.png').convert_alpha()
                self.attack_pos = (self.rect.centerx - (1 * self.rect.width * self.flip),
                                            self.rect.y, self.rect.width, self.rect.height)
            elif self.attack_type == 2:
                attack_hitbox = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip),
                                            self.rect.y, 2 * self.rect.width, self.rect.height)
                damage = self.atk * 3
                self.attack_sound = pygame.mixer.Sound('public\\9mm-pistol-shoot-short-reverb-7152.mp3')
                self.attack_sound.set_volume(0.5)
                self.attack_sound.play()
                self.attack_image = pygame.image.load('public\\images\\slash-effect-png-picture-in-full-hd-download-high-quality-image-now.png').convert_alpha()
                self.attack_pos = (self.rect.centerx - (2 * self.rect.width * self.flip),
                                            self.rect.y, 2 * self.rect.width, self.rect.height)
            elif self.attack_type == 3:
                attack_hitbox = pygame.Rect(self.rect.centerx - (12*self.rect.width * self.flip),
                                            self.rect.y, 12* self.rect.width, self.rect.height)
                damage = self.atk * 5

                self.attack_sound = pygame.mixer.Sound('public\\cannon-fire-161072.mp3')
                self.attack_sound.set_volume(0.5)
                self.attack_sound.play()

                self.attack_image = pygame.image.load('public/images/gryGwQGV1QEk1_HctbyWg4fabTwD4TW8oX3vVsSQ71s.png').convert_alpha()
                self.attack_pos = (self.rect.centerx - ( 7*self.rect.width * self.flip),
                                            self.rect.y, 12* self.rect.width, self.rect.height)

            if attack_hitbox.colliderect(target.rect):
                self.attack_sound.play()
                target.hp -= damage

            self.cooldowns[self.attack_type] = self.cooldown_durations[self.attack_type]
            self.attack_start_time = pygame.time.get_ticks()
            screen.blit(self.attack_image, self.attack_pos)




    def ai_attack(self, target):
        if self.cooldowns["ai_attack"] <= 0:
            self.attack_type = random.randint(1, 3)
            damage = self.atk

            self.attack_start_time = pygame.time.get_ticks()
            self.show_attack_image = True
            
            attack_radius = 300
            attack_center = (self.rect.centerx, self.rect.centery)
            attack_hitbox = pygame.Rect(attack_center[0] - attack_radius, attack_center[1] - attack_radius, 2 * attack_radius, 2 * attack_radius)

            if attack_hitbox.colliderect(target.rect):
                target.hp -= damage

            self.cooldowns["ai_attack"] = random.randint(300, 1000)

        elif self.show_attack_image and pygame.time.get_ticks() - self.attack_start_time < 2000:
            ai_attack_image = pygame.image.load('public\\images\\Glowing-Golden-Light-PNG-Download-Image (1).png').convert_alpha()
            ai_attack_sound = pygame.mixer.Sound('public\\hq-explosion-6288.mp3')
            ai_attack_sound.set_volume(0.5)
            screen.blit(ai_attack_image, (self.rect.left - 320, self.rect.top - 300))
            ai_attack_sound.play()
        else:
            self.show_attack_image = False

    def update(self):
        animation_cooldown = 300
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            if not self.alive:
                self.frame_index = len(self.animation_list[self.action]) - 1

    def update_cooldowns(self):
        for attack_type in self.cooldowns:
            if self.cooldowns[attack_type] > 0:
                self.cooldowns[attack_type] -= 1

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

        timer_font = pygame.font.Font(fontty, 22)
        
        # Determine colors based on cooldowns
        light_attack_color = (0, 255, 0) if self.cooldowns[1] <= 0 else (255, 0, 0)
        heavy_attack_color = (0, 255, 0) if self.cooldowns[2] <= 0 else (255, 0, 0)
        ultimate_attack_color = (0, 255, 0) if self.cooldowns[3] <= 0 else (255, 0, 0)

        light_attack_text = timer_font.render(f"Light Attack: {self.cooldowns[1] // 100:.1f}s", True, light_attack_color)
        heavy_attack_text = timer_font.render(f"Heavy Attack: {self.cooldowns[2] // 100:.1f}s", True, heavy_attack_color)
        ultimate_attack_text = timer_font.render(f"Ultimate Attack: {self.cooldowns[3] // 100:.1f}s", True, ultimate_attack_color)

        y_start = 170
        y_gap = 30

    

        self.update_cooldowns()    
        screen.blit(light_attack_text, (170, y_start))
        screen.blit(heavy_attack_text, (170, y_start + 2 * y_gap))
        screen.blit(ultimate_attack_text, (170, y_start + 3 * y_gap))



        

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


    
class HealthBar():
    def __init__(self, x, y, hp, max_hp, width):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        self.width = width

    def draw(self, hp):
        # Update with new health
        self.hp = hp
        # Ensure health doesn't go below 0
        if self.hp < 0:
            self.hp = 0
        # Calculate health ratio
        ratio = self.hp / self.max_hp
        # Calculate width of health bar
        current_width = int(self.width * ratio)
        # Draw the health bar
        pygame.draw.rect(screen, red, (self.x, self.y, self.width, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, current_width, 20))
        # Draw the health number
        health_font = pygame.font.SysFont(None, 24)
        health_text = health_font.render(str(self.hp) + '/' + str(self.max_hp), True, white)
        screen.blit(health_text, (self.x + self.width + 10, self.y))
   



#set position of characters   
knight = Fighter(327, 800, True, 'player', 1500, 150, 5,sword_fx)
boss1 = Fighter(1520, 750, False, 'boss1', 10520, 650, 0,magic_fx)

# set position of health bar
knight_health_bar = HealthBar(197, 135, knight.hp, knight.max_hp,100)
boss1_health_bar = HealthBar(1317, 125, boss1.hp, boss1.max_hp,350)

# creating buttons
potion_button=button.Button(screen,457,125,potion_img,64,64)

run = True
while run:
    # draw bg
    set_bg()  
    knight.move(width, screen_height)
    # Call AI move function for boss1
    boss1.ai_move(width, screen_height)
    boss1.ai_attack(knight)

    knight.update()
    boss1.update()
    knight.update_cooldowns()  # Update cooldowns for the player
    boss1.update_cooldowns()   # Update cooldowns for the boss
  
    knight.draw(screen)
    boss1.draw(screen)
    clock.tick(fps)
    knight_health_bar.draw(knight.hp)
    boss1_health_bar.draw(boss1.hp)
    # control player actions
    # reset action variables
    attack = False
    potion = False
    target = None

    if potion_button.draw():
        potion = True
        # show number of potions remaining
    draw_text(str(knight.potions), font, white, 427, 137)
    if potion == True:
        if knight.potions > 0:
            # check if the potion would heal the player beyond max health
            if knight.max_hp - knight.hp > potion_effect:
                heal_amount = potion_effect
            else:
                heal_amount = knight.max_hp - knight.hp
            knight.hp += heal_amount
            knight.potions -= 1

    if boss1.hp <= 0 or knight.hp <= 0:
        game_over_screen()


    for event in pygame.event.get():
        # quit if user presses X button
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            run=False
        if event.type==pygame.QUIT:
            run=False
    pygame.display.update()
pygame.quit()