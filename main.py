import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1080, 800 # make the GUI height and width 
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # WIN is short for window
pygame.display.set_caption("Avoid the Comets!") # names the top of the window with the string

BG = pygame.transform.scale(pygame.image.load("assets/bg.jpeg"), (WIDTH, HEIGHT)) # imported background image and made it scale to the GUI

PLAYER_WIDTH = 40 
PLAYER_HEIGHT = 60 #
PLAYER_VEL = 8 # width, height and speed of player box 

COMET_WIDTH = 15
COMET_HEIGHT = 30 
COMET_VEL = 5 # speed, width and height of comets coming down

FONT = pygame.font.SysFont("Timesnewroman", 40) # font and size position of the clock 


def draw(player, elapsed_time, comets): # draw function that creates GUI
    WIN.blit(BG, (0,0)) # window imports the background starting position and 

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white") 
    WIN.blit(time_text, (10, 10)) # time on the top that increments by (int) second (bc of round func it doesnt show milliseconds)


    pygame.draw.rect(WIN, "blue", player) # color of player is blue

    for comet in comets:
        pygame.draw.rect(WIN, "white", comet) # color of comets is white


    pygame.display.update() # update so that it doesnt get lost


def main():
    run = True # if false game wont even start, needs it to keep running 

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT) # x of 200, and y will be the bottom of player (bottom of screen)
    clock = pygame.time.Clock() # when using rect in pygame, it goes x,y,width,height

    start_time = time.time() # time.time = current time, which will be when game started
    elapsed_time = 0

    comet_add_increment = 1000 # every 3 seconds, comets get added onto the screen
    comet_count = 0 # variable that tells when to add the next comet
    
    comets = [] # empty string of comets
    hit = False # didnt get hit yet so initialize to false

    while run:
        comet_count += clock.tick(60) # keep track of time acurately and counts milliseconds since last tick
        elapsed_time = time.time() - start_time # storing the time we started the loop at and subtracting the start time

        if comet_count > comet_add_increment:
            for _ in range(10): # adding 10 stars at a time every 3000 ms
                comet_x = random.randint(0, WIDTH - COMET_WIDTH)
                comet = pygame.Rect(comet_x, -COMET_HEIGHT, COMET_WIDTH, COMET_HEIGHT)
                comets.append(comet)

            comet_add_increment = max(200, comet_add_increment - 50) #pick max value out of 50 and 200 so min comets is 200
            comet_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys [pygame.K_LEFT] and player.x - PLAYER_VEL >= 0: # MOVES THE LEFT ARROW KEY
            player.x -= PLAYER_VEL # clsoer to the 0 0 position on the X coordinate, 5 pixels backwards bc of VEL
        if keys [pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH: # MOVES RIGHT ARROW KEY and stops from moving off screen
            player.x += PLAYER_VEL

        for comet in comets[:]:
            comet.y += COMET_VEL
            if  comet.y > HEIGHT:
                comets.remove(comet)
            elif comet.y + comet.height >= player.y and comet.colliderect(player): #check if start collided with player at the bottom of screen
                comets.remove(comet)
                hit = True
                break
        
        if hit:
            hit_bg = pygame.image.load("assets/bg.jpeg") # loads image in from file called "bg.jpeg"
            scaled_hit_bg = pygame.transform.scale(hit_bg, (WIDTH, HEIGHT)) # Scale the image to the GUI dimensions
            WIN.blit(scaled_hit_bg, (0, 0)) 
            lost_text = FONT.render("YOU LOSE!!!!", 1, "white") # Fixed the color tuple to use RGB format instead of string
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(3000) # delays the close of the window by 3000 ms after losing 
            break

        draw(player, elapsed_time, comets) # draws the player, time and comets on the screen

    pygame.quit()


if __name__ == "__main__":
    main()
