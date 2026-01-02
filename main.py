import pygame
import time
import random
from logic import get_neighbors, get_connected_bubbles, pop_bubbles


    #Logica joc si cea care conteaza defapt phase 1

#Aici fac implementarea la generarea matricei
COLLUMS_NR = 8
ROWS_NR = 10

grid = []

for r in range(ROWS_NR):
    currect_row = []
    if r % 2 == 0:
        nr_bubbles_per_dis_row = COLLUMS_NR
    else:
        nr_bubbles_per_dis_row = COLLUMS_NR - 1
    
    for c in range(nr_bubbles_per_dis_row):
        currect_row.append(random.randint(1, 4))
    
    grid.append(currect_row)


#my_neighbors = get_neighbors(0, 1, ROWS_NR, COLLUMS_NR)
#print(f"Vecinii lui 0, 1 sunt {my_neighbors}")

i = 0
for row in grid:
    if i % 2 == 0:
        print(row)
    else:
        print(f"  {row}")
    i += 1


grupul = get_connected_bubbles(grid, 5, 5)

print(f"Grupul pe care l am gasit care sa fie de tipul {grid[5][5]} este: {grupul}")

if pop_bubbles(grid, grupul) == True:
    print("Avem grup mai mare de 3. Afisam matricea")
    i = 0
    for row in grid:
        if i % 2 == 0:
            print(row)
        else:
            print(f"  {row}")
        i += 1
else:
    print("Nu avem grup mai mare de 3")

#Putina grafica cu care m am jucat sa invat
WIDTH = 1000
HEIGHT = 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Buster")

#BG = pygame.transform.scale(pygame.image.load("bkgr.jpg"), (WIDTH, HEIGHT))
BG = pygame.image.load("bkgr.jpg")

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5

def draw(player):
    WIN.blit(BG, (0, 0))
    pygame.draw.rect(WIN, "red", player)
    pygame.display.update()



def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= PLAYER_VEL
        
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_VEL

        draw(player)
    
    pygame.quit()

if __name__ == "__main__":
    main()