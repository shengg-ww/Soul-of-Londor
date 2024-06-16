# import module
import pygame
from pygame import mixer
import random
import sys

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
magic_fx = pygame.mixer.Sound("public/sword-battle-jingle-loop-96983.mp3")
magic_fx.set_volume(1)
bomb_fx=pygame.mixer.Sound("public/hq-explosion-6288.mp3")
# load images
background_img=pygame.image.load('public/images/6yvp9ih93wv31.webp')

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

#create function for drawing text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))
     



def game_over_screen():
    game_over = True
    
    # Load the faded image
    faded_image = pygame.image.load("public\\images\\6yvp9ih93wv31.webp").convert_alpha()
    faded_image.set_alpha(150)  # Set transparency level (0-255)


    while game_over:
        # Display the faded image as the background
        screen.blit(faded_image, (0, 0))
        
        # Display game over message
        game_over_font = pygame.font.Font(None, 50)
        game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (width // 2 + 200, screen_height // 4))
        
        # Display options as interactive buttons
        options_font = pygame.font.Font(None, 36)
        
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
            if event.type == pygame.QUIT:
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
    def __init__(self, x, y, flip, name, max_hp, atk, potions,sound):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.atk = atk
        self.flip = flip
        self.start_potion = potions
        self.potions = potions
        self.alive = True
        self.action=0
        self.animation_list = []
        self.frame_index = 0
        self.attack_type = 0
        self.attacking = False
        self.attack_type = 0
         # Cooldown attributes
        self.cooldown=0

        self.cooldowns = {
            1: 0,  # Light Attack
            2: 0,  # Special Attack
            3: 0,  # Heavy Attack
            4: 0   # Ultimate Attack
        }
        self.cooldown_duration = 60  # Cooldown duration in frames

        self.cooldown_duration = 2  # Adjust as needed
        self.attack_sound = sound
        self.hit=False
        self.jump=False
        self.running=False
        self.update_time = pygame.time.get_ticks()
        for i in range(2):
            img = pygame.image.load(f'public/images/{self.name}/0/idle{i}.png')
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_y = 0
           # Load the attack effect image


    def flip_image(self):
        self.image = pygame.transform.flip(self.animation_list[self.frame_index], True, False)
    
    def update_action(self, new_action):
    # Check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation list based on the action
            if self.attack_type == 0:  # Light Attack
                self.animation_list = [pygame.image.load(f'public/images/{self.name}/{self.action}/idle{i}.png') for i in range(2)]
            elif self.action == 1:  # Special Attack
                self.animation_list = [pygame.image.load(f'public/images/{self.name}/{self.action}/idle{i}.png') for i in range(2)]
            elif self.action == 3:  # Heavy Attack
                self.animation_list = [pygame.image.load(f'public/images/{self.name}/{self.action}/idle{i}.png') for i in range(2)]
            elif self.action == 4:  # Ultimate Attack
                self.animation_list = [pygame.image.load(f'public/images/{self.name}/{self.action}/idle{i}.png') for i in range(2)]
            else:  # Default idle animation
                self.animation_list = [pygame.image.load(f'public/images/{self.name}/0/idle{i}.png') for i in range(2)]
            # Update animation settings
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
            self.jump=True
            self.image = pygame.image.load(f'public/images/{self.name}/1/idle0.png').convert_alpha()

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            if key[pygame.K_LSHIFT]:
                draw_text("ULTIMATE", custom_font, gold, 197, 180)
               
                self.attack_type = 4
            else:
                draw_text("LIGHT ATTACK", custom_font, green, 197, 180)
           
                self.attack_type =1 
            self.attack(boss1)   
        elif mouse_buttons[1]:
            self.attack(boss1)
            draw_text("SPECIAL ATTACK", custom_font, purple, 197, 180)
            self.attack_type = 2
     
        elif mouse_buttons[2]:
            self.attack(boss1)
            draw_text("HEAVY ATTACK", custom_font, red, 197, 180)
            self.attack_type = 3
        

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
            # Define movement constraints
            MAX_DX = 300  
            MAX_DY = 200  


            # Calculate the maximum x and y boundaries
            max_x = screen_width - self.rect.width
            max_y = screen_height - self.rect.height*3

            # Generate random values for movement within constraints
            dx = random.randint(-MAX_DX, MAX_DX) 
            dy = random.randint(-MAX_DY, MAX_DY)

            # Update the position
            new_x = self.rect.x + dx
            new_y = self.rect.y + dy

            # Ensure the new position stays within the screen boundaries
            new_x = max(0, min(new_x, max_x))
            new_y = max(0, min(new_y, max_y))

            # Update the position
            self.rect.x = new_x
            self.rect.y = new_y

            # Set the cooldown period
            self.cooldown = 60  # Increase cooldown for less frequent movements
        else:
            # Decrease the cooldown period
            self.cooldown -= 1


    def attack(self, target):
        # Add hitboxes
        if self.cooldowns[self.attack_type] == 0:
            # Define hitboxes for player attacks
            if self.attack_type == 1:
                # Light Attack hitbox
                attack_hitbox = pygame.Rect(self.rect.centerx - (1 * self.rect.width * self.flip), 
                                            self.rect.y, self.rect.width, self.rect.height)
                damage = self.atk
            elif self.attack_type == 2:
                # Special Attack hitbox
                attack_hitbox = self.rect.inflate(350, 0)  # Adjust the size as needed
                damage = self.atk * 1.5
            elif self.attack_type == 3:
                # Heavy Attack hitbox
                attack_hitbox = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), 
                                            self.rect.y, 2 * self.rect.width, self.rect.height)
                damage = self.atk * 2
            elif self.attack_type == 4:
                # Ultimate Attack hitbox
                attack_hitbox = pygame.Rect(self.rect.left + 40, self.rect.top - 150, 1980, self.rect.height)
                damage = self.atk * 3

                # Ultimate Attack sound
                ultimate_attack_sound = pygame.mixer.Sound('public\hq-explosion-6288.mp3')
                ultimate_attack_sound.set_volume(0.5)
                ultimate_attack_sound.play()

                # Draw ultimate attack image
                ultimate_attack_image = pygame.image.load('public\\images\\gryGwQGV1QEk1_HctbyWg4fabTwD4TW8oX3vVsSQ71s.png').convert_alpha()
                ultimate_attack_pos = (self.rect.left + 40, self.rect.top - 150, 1980, self.rect.height)
                screen.blit(ultimate_attack_image, ultimate_attack_pos)

                # Apply damage to the boss's health
                target.hp -= damage
                # Apply cooldown to the attack
                self.cooldowns[self.attack_type] = self.cooldown_duration * 45

            # Check for collision with boss
            if attack_hitbox.colliderect(target.rect):
                # Play attack sound
                self.attack_sound.play()
                # Apply damage to the boss's health
                target.hp -= damage
                # Apply cooldown to the attack
                self.cooldowns[self.attack_type] = self.cooldown_duration

    
    def ai_attack(self, target):
        # Check if the cooldown for AI attack has expired
        if self.cooldowns["ai_attack"] <= 0:
            # Generate a random attack type
            self.attack_type = random.randint(1, 3)
            # Calculate the damage based on the attack type
            damage = self.atk
            
            # Load and display the attack effect image
            ai_attack_image = pygame.image.load('public/images/78294-light-glare-free-png-hq-thumb.png').convert_alpha()
            screen.blit(ai_attack_image, (self.rect.left, self.rect.top - 150))
            
            # Define the circular hitbox
            attack_radius = 100  # Adjust the radius as needed
            attack_center = (self.rect.centerx, self.rect.centery - 150)  # Offset for position
            attack_hitbox = pygame.Rect(attack_center[0] - attack_radius, attack_center[1] - attack_radius,
                                         attack_radius * 2, attack_radius * 2)

            # Check for collision with the target
            if attack_hitbox.colliderect(target.rect):
                # Apply damage to the target
                target.hp -= damage
                print(f"{self.name} is attacking with attack type {self.attack_type}")

            # Set the cooldown for AI attack
            self.cooldowns["ai_attack"] = 300  # 5 seconds cooldown (300 frames at 60 FPS)

                
    #handle animation updates
    def update(self):
        #check what action the player is performing
      
        animation_cooldown=300

        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if the animation has finished
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
    def update_cooldowns(self):
        for attack_type in self.cooldowns:
            if self.cooldowns[attack_type] > 0:
                self.cooldowns[attack_type] -= 1
            
                    
                   
               
                   
                


  
    def draw(self,screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),self.rect)
    
    
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
knight = Fighter(327, 800, True, 'player', 500, 50, 3,(sword_fx))
boss1 = Fighter(1520, 750, False, 'boss1', 10520, 650, 0,magic_fx)

# set position of health bar
knight_health_bar = HealthBar(197, 135, knight.hp, knight.max_hp,100)
boss1_health_bar = HealthBar(1317, 125, boss1.hp, boss1.max_hp,350)

run=True
while run:
    # draw bg
    set_bg()  
    knight.move(width,screen_height)
    # Call AI move function for boss1
    boss1.ai_move(width, screen_height)

    knight.update()
    boss1.update()
    knight.update_cooldowns()  # Update cooldowns for the player
    boss1.update_cooldowns()   # Update cooldowns for the boss
  
    knight.draw(screen)
    boss1.draw(screen)
    clock.tick(fps)
    knight_health_bar.draw(knight.hp)
    boss1_health_bar.draw(boss1.hp)
    # AI behavior for boss1
    if pygame.time.get_ticks() - boss1.update_time > 3000:  # Adjust the interval between attacks (in milliseconds)
        boss1.ai_attack(knight)  # Call the AI attack method
        boss1.update_time = pygame.time.get_ticks()  # Reset the update time
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