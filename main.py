import pygame
import sys

### GLOBAL VARIABLES ###
# create a screen dictionary to hold all screen-related variables
screen = {}
screen['surface'] = pygame.display.set_mode((800, 500))
screen['rect'] = screen['surface'].get_rect()

# create a ship dictionary to hold all scree-related variables
ship = {}
ship['surface'] = pygame.image.load('images/ship.png')
ship['rect'] = ship['surface'].get_rect()
ship['rect'].midbottom = screen['rect'].midbottom
ship['velocity'] = 5
ship['moving_right'] = False
ship['moving_left'] = False
ship['lives'] = 3

# keep track of bullets in a list
bullets = []

# keep track of all aliens in a list
aliens = []

fleet_vel = 1

score = 0

### GAME FUNCTIONS ###
def check_events():
    """Process the user-driven events of the game"""
    # import global variables
    global ship

    # check game events
    for event in pygame.event.get():
        # click the 'X' to quit the game
        if event.type == pygame.QUIT:
            sys.exit()

        # check keypresses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: 
                ship['moving_right'] = True                
            if event.key == pygame.K_LEFT:
                ship['moving_left'] = True
            if event.key == pygame.K_SPACE:
                fire_bullet()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship['moving_right'] = False
            if event.key == pygame.K_LEFT:
                ship['moving_left'] = False
#end of event checking

def reset_level():
    """recreate fleet at same level"""
    global ship 
    global aliens
    global bullets 

    pygame.time.wait(2000)
    bullets = []
    aliens = []
    create_alien_fleet()
    ship['rect'].midbottom = screen['rect'].midbottom

def advance_level():
    """set up the fleet for next level"""
    global ship
    global bullets
    global fleet_vel 

    # new fleet of aliens 
    create_alien_fleet()
    # emptying the bullets list 
    bullets = []
    #increase fleet velocity
    fleet_vel = abs(fleet_vel) + 1

    #center the ship at mid bottom 
    ship['rect'].midbottom = screen['rect'].midbottom 

    #update screen and pause

    update_screen()
    pygame.time.wait(2000)

def fire_bullet():
    """create a bullet from the ship's position and add it to the list of bullets"""
    global bullets
    global ship

    # check max bullets hasn't been reached
    if len(bullets) < 100:
        new_bullet = {}
        # starting position is (0, 0) but we'll modify later
        new_bullet['rect'] = pygame.Rect((0, 0), (3, 15))
        new_bullet['color'] = (60, 60, 60)
        new_bullet['vel'] = 6

        # position new bullet above the current position of the ship
        new_bullet['rect'].midbottom = ship['rect'].midtop
        
        # add new bullet to list of bullets to manage
        bullets.append(new_bullet)
    
def create_alien_fleet():
    """Create the fleet of aliens to fill the screen"""
    # create three rows of aliens
    for row_num in range(1, 4):
        create_alien_row(row_num)

def create_alien_row(row_num):
    """Create a row of aliens at the row number provided"""

    for col_num in range(1, 7):
        create_alien(row_num, col_num)
    

def create_alien(row_num, col_num):
    """create an alien and add it to the list of aliens"""
    global aliens

    # alien dictionary to hold all alien-related properties
    new_alien = {}
    new_alien['surface'] = pygame.image.load('images/alien.png')
    new_alien['rect'] = new_alien['surface'].get_rect()

    
    # position the using the column and row number.
    # each alien has one alien-width between the next
    new_alien['rect'].right = 2 * new_alien['rect'].width * col_num
    new_alien['rect'].bottom = 2 * new_alien['rect'].height * row_num

    aliens.append(new_alien)


def update_ship():
    """update the ship's rect attributes"""
    global ship

    # update the ship position
    if ship['moving_right'] and \
        ship['rect'].right + ship['velocity'] < screen['rect'].right:
        # increase x coordinate of ship
        ship['rect'].x += ship['velocity']
    if ship['moving_left'] and \
        ship['rect'].left > 0 + ship['velocity']:
        # increase x coordinate of ship
        ship['rect'].x -= ship['velocity']

def update_bullets():
    """Update the positions of each bullet in bullets list"""
    global bullets

    for bullet in bullets:
        bullet['rect'].y -= bullet['vel']
    
    # loop through a copy of bullets and remove any that are offscreen
    for bullet in bullets[:]:
        if bullet['rect'].bottom < 0:
            bullets.remove(bullet)

def update_aliens():
    """Update the fleet of aliens"""
    global aliens
    global screen
    global fleet_vel
    
    # modify the x values of all aliens
    for alien in aliens:
        alien['rect'].x += fleet_vel
    
    #check all aliens to see if any hit the wall 

    for alien in aliens:
        if alien['rect'].right >= screen['rect'].right or alien['rect'].left <= screen['rect'].left:
            handle_fleet_wall_collision() 
            break 

def handle_fleet_wall_collision():
    """change direction of fleet and drop them towards the ship""" 
    global aliens
    global fleet_vel

    fleet_vel *= -1 # change direction 
    
    for alien in aliens:
        
        alien['rect'].y += 10 # drop 10 pixels 





def check_bullet_alien_collisions():
    """Check if any bullets hit any aliens"""
    global aliens
    global bullets
    global fleet_vel
    global score
    # loop through copy of bullets to check alien collision
    for bullet in bullets[:]:
        # for each bullet, check each alien
        for alien in aliens[:]:
            if bullet['rect'].colliderect(alien['rect']):
                score += abs(fleet_vel) * 100 #increase score 
                # remove bullet and alien
                bullets.remove(bullet)
                aliens.remove(alien)
    # respawn fleet if there is no more aliens on the screen 
   
       
    if len(aliens) == 0:
        advance_level()

def aliens_reached_ship():
    """return true if any aliens reach top of the ship"""
    global ship
    global aliens

    for alien in aliens:
        if alien['rect'].bottom >= ship['rect'].top:
            return True # alien has reached the ship's level 

            #if reached the end of the loop, no aliens have reached the ship 

    return False 



def update_screen():
    """update the items drawn to the screen and flip the display"""
    global screen
    global ship
    global bullets
    global aliens

    # fill screen color
    screen['surface'].fill((230, 230, 230))

    # blit ship onto the screen
    screen['surface'].blit(ship['surface'], ship['rect'])

    # draw bullets to the screen
    for bullet in bullets:
        pygame.draw.rect(screen['surface'], bullet['color'], bullet['rect'])

    for alien in aliens:
        screen['surface'].blit(alien['surface'], alien['rect'])

    for i in range(ship['lives']):
        x = i * ship['rect'].width
    
    screen['surface'].blit(ship['surface'], (x,0))

    # draw game score to the screen 
    font = pygame.font.SysFont('dejavusansmono', 24)
    score_img = font.render(str(score), True, (0,0,0))
    score_rect = score_img.get_rect()
    score_rect.topright = screen['rect'].topright
    screen['surface'].blit(score_img, score_rect)

    # flip screen to update display
    pygame.display.flip()


### MAIN FUNCTION ###
def main():
    pygame.init()
    pygame.display.set_caption("Alien Invasion!")

    create_alien_fleet()

    # game loop
    while ship['lives'] > 0:
        pygame.time.wait(17)
        
        check_events()
        update_ship()
        update_bullets()
        update_aliens()
        check_bullet_alien_collisions()

        #check if aliens recahed the ship's level 
        if aliens_reached_ship():
            ship['lives'] -=1
            reset_level()
        update_screen()
        

main()