from Queue import PriorityQueue
import random

# defining global variables here
frontier = PriorityQueue()
r_s = -1; c_s = -1; r_g = -1; c_g = -1
r = -1; c = -1
vis = [[0]*1 for i in range(1)]
path = []
board = [['-']*1 for i in range(1)]
parent = [['-']*1 for i in range(1)]
g_val = [['-']*1 for i in range(1)]
# end of defining global variables

def print_board():
    for i in range(0,r):
        for j in range(0,c):
            print board[i][j],
        print
    print

def print_path():
    for i in range(0,r):
        for j in range(0,c):
            if board[i][j] != 'W':
                board[i][j] = '-'
    for node in path:
        row = node[0]
        col = node[1]
        if row == r_s and col == c_s:
            board[row][col] = 'S'
        elif row == r_g and col == c_g:
            board[row][col] = 'G'
        else:
            board[row][col] = 'P'
    print_board()


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

def solver():
    child_count = 0
    while(1):
        print_board()
        if frontier.empty():
            print "Cannot Reach The Goal"
            break
        temp = frontier.get()
        ele = temp[3]
        print ele
        vis[ele[0]][ele[1]] = 1             # into the closed set
        board[ele[0]][ele[1]] = 'V'
        if (ele[0]==r_g) and (ele[1]==c_g):
            print "Reached Goal"
            path.append([r_g,c_g])
            i = ele[0]; j = ele[1]
            while parent[i][j] != '-':
                path.append(parent[i][j])
                i1 = parent[i][j][0]
                j1 = parent[i][j][1]
                i = i1
                j = j1
            break
        children = find_child(ele[0],ele[1])
        print children
        for child in children:
            val = child[2]
            row1 = child[0]
            col1 = child[1]
            if board[row1][col1]=='F':      # F,G ( V,S,W cannot occur here )
                # if (g_val[row1][col1]=='-'):    # means that this node has been added to frontier for the first time
                #     p = parent[row1][col1]
                #     g_val[row1][col1] = g_val[p[0]][p[1]] + 1  # definitely if board[row1][col1]=f then g_val != '-'
                #     frontier.put((val[0],val[1],val[2],[row1,col1]))
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

def main():
    global r,c,r_s,c_s,r_g,c_g,vis,board,parent,g_val      # used global keyword for modifying the global variables
    r,c = raw_input("Enter number of Rows and Columns: ").split()
    r = int(r); c = int(c)

    r_s,c_s = raw_input("Enter Start row and column: ").split()     # Start State
    r_s = int(r_s); c_s = int(c_s)
    if (r_s<0) or (c_s<0) or (r_s>=r) or (c_s>=c) :
        raise ValueError('Rows are from 0 to R-1 and columns are from 0 to C-1')

    r_g,c_g = raw_input("Enter Goal row and column: ").split()      # Goal State
    r_g = int(r_g); c_g = int(c_g)
    if (r_g<0) or (c_g<0) or (r_g>=r) or (c_g>=c) :
        raise ValueError('Rows are from 0 to R-1 and columns are from 0 to C-1')

    vis = [[0]*c for i in range(r)]
    board = [['-']*c for i in range(r)]
    parent = [['-']*c for i in range(r)]
    g_val = [['-']*c for i in range(r)]
    vis[r_s][c_s] = 1
    board[r_s][c_s] = 'S'
    board[r_g][c_g] = 'G'

    k = int(raw_input("Enter number of walls: "))                   # adding walls
    for i in range(k):
        r_w,c_w = raw_input("Enter Wall row and column: ").split()
        r_w = int(r_w); c_w = int(c_w)
        board[r_w][c_w] = 'W'

    print
    frontier.put((-1,-1,-1,[r_s,c_s]))      # the 3rd value is the child number
    g_val[r_s][c_s] = 0
    solver()
    print_path()

if __name__ == '__main__':
    main()
