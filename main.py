import numpy as np
import pygame
import sys

# initialization variable

# element identifiers
identifier_bomb = -1
# game setup
boardSize = 10
totalBombs = 10
initialUncovered = 20
# initialization
gameBoard = np.zeros([boardSize,boardSize],dtype=np.int8)

# function definitions
def prev(i):
    if i-1<0:
        return 0
    else:
        return i-1

def nex(i):
    if i+2>boardSize:
        return boardSize
    else:
        return i+2

def total_bombs_around(r, c):
    return np.sum(gameBoard[prev(r):nex(r),prev(c):nex(c)]==identifier_bomb)

def check_move(r,c,displayBoard):
    displayBoard[r,c]=gameBoard[r,c]
    if gameBoard[r,c]==identifier_bomb:
        return 0 # game end
    else:
        return 1 # game continues
    
def create_game_board():
    # generating random indexes for bombs placement
    bombLocations = np.random.choice(np.arange(boardSize*boardSize),size=totalBombs,replace=False)
    # placing the bombs
    for x in bombLocations:
        gameBoard.flat[x] = identifier_bomb
    # placing hints for bomb locations
    for r in range(totalBombs):
        for c in range(totalBombs):
            if gameBoard[r,c]!=identifier_bomb:
                gameBoard[r,c]=total_bombs_around(r,c)
    # view the populated game board
    #print(gameBoard)
    # Hide all the cells and only show some hints and empty cells (at random)
    displayBoard = np.full((boardSize,boardSize),' ')
    uncoveredLocations = np.random.choice(np.setdiff1d(np.arange(boardSize*boardSize),bombLocations),size=initialUncovered,replace=False)
    for x in uncoveredLocations:
        displayBoard.flat[x] = str(gameBoard.flat[x])
    # view the populated display board
    # print(displayBoard)
    return displayBoard

def show_game_board(gameScreen,displayBoard):
    # fill the screen with white
    gameScreen.fill((255,255,255))
    # draw the grid
    for i in range(boardSize):
        pygame.draw.line(gameScreen,(0,0,0),(0,i*50),(500,i*50))
        pygame.draw.line(gameScreen,(0,0,0),(i*50,0),(i*50,500))
    # draw all the numbers in blue, 0s in green, and F in red     
    for i in range(boardSize):
        for j in range(boardSize):
            font = pygame.font.Font('freesansbold.ttf', 32)
            if displayBoard[i,j]=='F':
                text = font.render(str(displayBoard[i,j]), True, (255,0,0))
            elif displayBoard[i,j]=='0':
                text = font.render(str(displayBoard[i,j]), True, (0,255,0))
            else:
                text = font.render(str(displayBoard[i,j]), True, (0,0,255))
            textRect = text.get_rect()
            textRect.center = (i*50+25,j*50+25)
            gameScreen.blit(text,textRect)
    # update the screen
    pygame.display.update()

def show_instructions(gameScreen):
    # fill the screen with white
    gameScreen.fill((255,255,255))
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("Left click: uncover", True, (0,0,0))
    textRect = text.get_rect()
    textRect.center = (250,150)
    gameScreen.blit(text,textRect)
    text = font.render("Right click: place flag", True, (0,0,0))
    textRect = text.get_rect()
    textRect.center = (250,200)
    gameScreen.blit(text,textRect)
    text = font.render("Middle click: show hint", True, (0,0,0))
    textRect = text.get_rect()
    textRect.center = (250,250)
    gameScreen.blit(text,textRect)
    # ask the user to click on the screen to start the game
    text = font.render("Click to start", True, (0,0,0))
    textRect = text.get_rect()
    textRect.center = (250,350)
    gameScreen.blit(text,textRect)
    # update the screen
    pygame.display.update()
    # hold the screen until the user clicks on it
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
            if event.type == pygame.QUIT:
                # quit pygame
                pygame.quit()
                return False
                #sys.exit(0)
    return True

def main():
    # create the game board
    displayBoard = create_game_board()
    # initialize pygame
    pygame.init()
    # create the screen
    screen = pygame.display.set_mode((500,500))
    # set the title
    pygame.display.set_caption("Minesweeper")
    # show instructions
    running = show_instructions(screen)
    # game loop
    while running:
        # get user input to quit the game (by clicking the close button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # check if left mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                r = int(x/50)
                c = int(y/50)
                if event.button == 1:
                    # left click: send the click location to the check_move function
                    running = check_move(r,c,displayBoard)
                elif event.button == 3:
                    # right click: place a flag on the cell
                    displayBoard[r,c]='F'
                elif event.button == 2:
                    # middle click: show hint for the cell
                    displayBoard[r,c]=str(gameBoard[r,c])
        # show the game board
        show_game_board(screen,displayBoard)
        # check if the game is over and show the game over message
        if not running:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render("Game Over", True, (255,0,0))
            textRect = text.get_rect()
            textRect.center = (250,250)
            screen.blit(text,textRect)
            # show the location of all bombs
            for i in range(boardSize):
                for j in range(boardSize):
                    if gameBoard[i,j]==identifier_bomb:
                        text = font.render('B', True, (255,0,0))
                        textRect = text.get_rect()
                        textRect.center = (i*50+25,j*50+25)
                        screen.blit(text,textRect)
            pygame.display.update()
            # hold the screen until the user closes it by clicking the close button
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # quit pygame
                        pygame.quit()
                        sys.exit(0)
    # quit pygame
    pygame.quit()
    

if __name__ == "__main__":
    main()
