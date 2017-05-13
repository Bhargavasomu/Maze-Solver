# These are the imports
import pygame,sys,string
import random
from pygame.locals import *
from Queue import PriorityQueue
pygame.init()

# These are the global variables
frontier = PriorityQueue()
r_s = -1; c_s = -1; r_g = -1; c_g = -1
r = -1; c = -1
vis = [[0]*1 for i in range(1)]
board = [['-']*1 for i in range(1)]
rect = [['-']*1 for i in range(1)]
parent = [['-']*1 for i in range(1)]
g_val = [['-']*1 for i in range(1)]
path = []

# These are the colors
BLACK = [0,0,0]
WHITE = [255,255,255]
RED = [255,0,0]
GREEN = [0,255,0]
DARK_GREEN = [0,180,0]
BLUE = [0,0,255]
YELLOW = [255,255,0]
PINK = [255,0,255]
ORANGE = [255,165,0]
GREY = [128,128,128]

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
        return event.key
    elif event.type == pygame.QUIT:
        pygame.quit()
        quit()
    else:
        pass

def display_box(screen,message1,message2,disp1,disp2):
    fontobject = pygame.font.Font('freesansbold.ttf',20)

    pygame.draw.rect(screen,WHITE,((screen.get_width() / 2) - 100,(screen.get_height() / 2) - 10+disp1,200,20), 0)
    pygame.draw.rect(screen,BLACK,((screen.get_width() / 2) - 102,(screen.get_height() / 2) - 12+disp1,204,24), 2)

    pygame.draw.rect(screen,WHITE,((screen.get_width() / 2) - 100,(screen.get_height() / 2) - 10+disp2,200,20), 0)
    pygame.draw.rect(screen,BLACK,((screen.get_width() / 2) - 102,(screen.get_height() / 2) - 12+disp2,204,24), 2)

    if len(message1) != 0:
        screen.blit(fontobject.render(message1, 1, BLACK),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10+disp1))
    if len(message2) != 0:
        screen.blit(fontobject.render(message2, 1, BLACK),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10+disp2))
    pygame.display.flip()

def InputBox():
    INIT_WIDTH = 1080
    INIT_HEIGHT = 720
    WINDOW = pygame.display.set_mode([INIT_WIDTH,INIT_HEIGHT])    # Drawing the main window
    SCREEN = pygame.display.get_surface()
    SCREEN.fill(WHITE)
    screen = SCREEN
    pygame.font.init()
    current_string1 = []        # This is the first input string
    current_string2 = []        # This is the second input string
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = text_objects("Grid Details", largeText)
    TextRect.center = ((INIT_WIDTH/2),100)
    SCREEN.blit(TextSurf, TextRect)

    display_box(screen,"Rows" + ": " + string.join(current_string1,""),"Cols" + ": " + string.join(current_string2,""),0,100)
    while 1:
        inkey = get_key()
        if inkey == K_BACKSPACE:
            current_string1 = current_string1[0:-1]
        elif inkey == K_RETURN:
            break
        elif 48<=inkey<= 57:
            current_string1.append(chr(inkey))
        display_box(screen,"Rows" + ": " + string.join(current_string1,""),"Cols" + ": " + string.join(current_string2,""),0,100)
    while 1:
        inkey = get_key()
        if inkey == K_BACKSPACE:
            current_string2 = current_string2[0:-1]
        elif inkey == K_RETURN:
            break
        elif 48<=inkey<= 57:
            current_string2.append(chr(inkey))
        display_box(screen,"Rows" + ": " + string.join(current_string1,""),"Cols" + ": " + string.join(current_string2,""),0,100)

    return [string.join(current_string1,""),string.join(current_string2,"")]

def text_objects(text,font):
    textSurface = font.render(text,True,BLACK)
    return textSurface,textSurface.get_rect()

def game_intro():
    INIT_WIDTH = 1080
    INIT_HEIGHT = 720
    WINDOW1 = pygame.display.set_mode([INIT_WIDTH,INIT_HEIGHT])    # Drawing the main window
    SCREEN1 = pygame.display.get_surface()
    button = pygame.draw.rect(SCREEN1,GREEN,(500,450,100,50))
    intro = True
    while intro:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                if button.collidepoint(mouse):
                    return
        SCREEN1.fill(WHITE)
        largeText = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = text_objects("Maze Solver", largeText)
        TextRect.center = ((INIT_WIDTH/2),(INIT_HEIGHT/2))
        SCREEN1.blit(TextSurf, TextRect)

        if button.collidepoint(mouse):
            button = pygame.draw.rect(SCREEN1,DARK_GREEN,(500,450,100,50))
        else:
            button = pygame.draw.rect(SCREEN1,GREEN,(500,450,100,50))

        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("START", smallText)
        textRect.center = ( (500+(100/2)), (450+(50/2)) )
        SCREEN1.blit(textSurf, textRect)

        pygame.display.update()

def print_until_quit(SCREEN):
    while(1):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                return
            else:
                print_board(SCREEN)

def print_board(SCREEN):
    MARGIN = 5
    BLOCK_WIDTH = 40
    BLOCK_HEIGHT = 40
    for i in range(r):
        for j in range(c):
            if board[i][j] == 'S':
                color = GREEN
            elif board[i][j] == 'W':
                color = BLUE
            elif board[i][j] == 'V':
                color = WHITE
            elif board[i][j] == 'F':
                color = YELLOW
            elif board[i][j] == 'G':
                color = RED
            elif board[i][j] == 'P':
                color = PINK
            else:
                color = BLACK
            rect[i][j] = pygame.draw.rect(SCREEN,color,(((MARGIN*(j+1)) + (j*BLOCK_WIDTH)),((MARGIN*(i+1)) + (i*BLOCK_WIDTH)),BLOCK_WIDTH,BLOCK_HEIGHT))
            pygame.display.flip()

def replace(r,c,val):
    for item in frontier.queue:
        if item[3][0]==r and item[3][1]==c:
            item = list(item)
            item[0] = val       # converting to list so as to change values
            item = tuple(item)
            return

def evalfn(row,col,parent_row,parent_col):                   # f(n) for each state (row,col)
    g = g_val[parent_row][parent_col] + 1
    h = abs(row-r_g) + abs(col-c_g)     # here h is the second priority function
    f = g+h
    prior3 = min(abs(row-r_g),abs(col-c_g))
    return [f,h,prior3]

def find_child(row,col):
    # finds accessible children of state (row,col) out of r rows and c columns
    # The children which are to be added into the frontier should not be visited and should not be a wall
    children = []
    if (0<=row+1<r) and (vis[row+1][col]==0) and (board[row+1][col]!='W'):
        val = evalfn(row+1,col,row,col)
        temp = [row+1,col,val]
        children.append(temp)
    if (0<=row-1<r) and (vis[row-1][col]==0) and (board[row-1][col]!='W'):
        val = evalfn(row-1,col,row,col)
        temp = [row-1,col,val]
        children.append(temp)
    if (0<=col+1<c) and (vis[row][col+1]==0) and (board[row][col+1]!='W'):
        val = evalfn(row,col+1,row,col)
        temp = [row,col+1,val]
        children.append(temp)
    if (0<=col-1<c) and (vis[row][col-1]==0) and (board[row][col-1]!='W'):
        val = evalfn(row,col-1,row,col)
        temp = [row,col-1,val]
        children.append(temp)
    random.shuffle(children)
    return children

def solver(SCREEN):
    child_count = 0
    while(1):
        if frontier.empty():
            print "Cannot Reach The Goal"
            break
        temp = frontier.get()
        ele = temp[3]
        vis[ele[0]][ele[1]] = 1             # into the closed set
        board[ele[0]][ele[1]] = 'V'
        if (ele[0]==r_g) and (ele[1]==c_g):
            print "Reached Goal"
            path.append([r_g,c_g])
            for i in range(0,r):
                for j in range(0,c):
                    if board[i][j] != 'W':
                        board[i][j] = '-'
            i = ele[0]; j = ele[1]
            board[i][j] = 'G'
            while parent[i][j] != '-':
                path.append(parent[i][j])
                i1 = parent[i][j][0]
                j1 = parent[i][j][1]
                i = i1
                j = j1
                if i == r_s and j == c_s:
                    board[i][j] = 'S'
                elif i == r_g and j == c_g:
                    board[i][j] = 'G'
                else:
                    board[i][j] = 'P'
            print_until_quit(SCREEN)
            break
        children = find_child(ele[0],ele[1])
        for child in children:
            val = child[2]
            row1 = child[0]
            col1 = child[1]
            if board[row1][col1]=='F':      # F,G ( V,S,W cannot occur here )
                if ((g_val[ele[0]][ele[1]] + 1) < g_val[row1][col1]):
                    g_val[row1][col1] = g_val[ele[0]][ele[1]] + 1
                    replace(row1,col1,g_val[row1][col1]+val[1])
                    parent[row1][col1] = [ele[0],ele[1]]
            else:   # add to the frontier and set parent and set g_val
                board[row1][col1] = 'F'
                frontier.put((val[0],val[1],child_count,[row1,col1]))
                parent[row1][col1] = [ele[0],ele[1]]
                g_val[row1][col1] = g_val[ele[0]][ele[1]]+1
                child_count = child_count+1

        print_board(SCREEN)

def main(r,c):
    global r_s,c_s,r_g,c_g,board,rect,vis,parent,g_val
    board = [['-']*c for i in range(r)]
    rect = [[0]*c for i in range(r)]
    vis = [[0]*c for i in range(r)]
    parent = [['-']*c for i in range(r)]
    g_val = [['-']*c for i in range(r)]

    # These are the settings
    FPS = 60
    BLOCK_WIDTH = 40
    BLOCK_HEIGHT = 40
    MARGIN = 5          # Distance b/w each block
    WIDTH = (MARGIN*(c+1)) + (c*BLOCK_WIDTH) + 100       # This is for the screen, 300 is to accomodate GO button
    HEIGHT = (MARGIN*(r+1)) + (r*BLOCK_HEIGHT)

    # This is the screen setup
    WINDOW = pygame.display.set_mode([WIDTH,HEIGHT])    # Drawing the main window
    CAPTION = pygame.display.set_caption('Maze')        # Naming the window
    SCREEN = pygame.display.get_surface()               # This function gives reference to the screen
    clock = pygame.time.Clock()

    SCREEN.fill(WHITE)                                   # Background color for
    temp1 = (MARGIN*(c+1)) + (c*BLOCK_WIDTH) + 5
    temp2 = (MARGIN*(r/2-1)) + ((r/2-1)*BLOCK_HEIGHT)
    # Drawing Rectangles
    button = pygame.draw.rect(SCREEN,GREEN,(temp1,temp2,90,50))
    for i in range(r):
        for j in range(c):
            rect[i][j] = pygame.draw.rect(SCREEN,BLACK,(((MARGIN*(j+1)) + (j*BLOCK_WIDTH)),((MARGIN*(i+1)) + (i*BLOCK_WIDTH)),BLOCK_WIDTH,BLOCK_HEIGHT))

    pygame.display.flip()                                # update display
    clicks = 0             # number of clicks till now
    running = True
    while running:
        pos = pygame.mouse.get_pos()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif i.type == MOUSEBUTTONDOWN:
                if button.collidepoint(pos) and r_s!=-1 and c_s!=-1 and r_g!=-1 and c_g!=-1:
                    return SCREEN
                for i in range(r):
                    for j in range(c):
                        if rect[i][j].collidepoint(pos):
                            clicks = clicks+1
                            if clicks == 1:
                                board[i][j] = 'S'
                                r_s = i
                                c_s = j
                                color = GREEN   # start box color
                            elif clicks == 2:
                                board[i][j] = 'G'
                                r_g = i
                                c_g = j
                                color = RED     # goal box color
                            elif clicks>2:
                                if i==r_s and j==c_s:
                                    color = GREEN
                                elif i==r_g and j==c_g:
                                    color = RED
                                elif board[i][j] == 'W':
                                    color = BLACK
                                    board[i][j] = '-'
                                else:
                                    board[i][j] = 'W'
                                    color = BLUE    # walls color
                            rect[i][j] = pygame.draw.rect(SCREEN,color,(((MARGIN*(j+1)) + (j*BLOCK_WIDTH)),((MARGIN*(i+1)) + (i*BLOCK_WIDTH)),BLOCK_WIDTH,BLOCK_HEIGHT))
        if button.collidepoint(pos):
            button = pygame.draw.rect(SCREEN,DARK_GREEN,(temp1,temp2,90,50))
        else:
            button = pygame.draw.rect(SCREEN,GREEN,(temp1,temp2,90,50))
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("GO", smallText)
        textRect.center = ( button.left + button.width/2, button.top + button.height/2 )
        SCREEN.blit(textSurf, textRect)
        pygame.display.flip()

def controller():
    global r,c
    game_intro()
    temp = InputBox()
    r = int(temp[0])
    c = int(temp[1])
    screen = main(r,c)
    frontier.put((-1,-1,-1,[r_s,c_s]))
    g_val[r_s][c_s] = 0
    solver(screen)


if __name__ == '__main__':
    controller()
