import random
import re
#Play Game

#lets create a board obj



class Board:
    def __init__(self , dim_size , num_bombs ):
        #lets keep track of Parameters. They'll be helpful later
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # lets create the board
        self.board = self.make_new_board() # plant the bombs
        self.assign_values_to_board()


        # initialize the set to keep track of which location we've uncovered
        #we'll save (row , col) tuples into this set
        self.dug = set() # if we dig at 0,0 then self.dug = {(0,0)}
        

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r , c)


    def get_num_neighbouring_bombs(self , row , col):
        num_neighbour_bombs =0
        for r in range(max(0 , row-1) , min(self.dim_size-1 ,(row+1))+1):
            for c in range(max(0 ,col-1) , min(self.dim_size-1 , (col+1))+1):
                if(r == row and c == col):
                    # Our original location dont check
                    continue
                if self.board[r][c]  == '*':
                    num_neighbour_bombs +=1

        return num_neighbour_bombs

    def make_new_board(self):

        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0 , self.dim_size**2 -1)
            row = loc // self.dim_size # we want the number of times dim_size goes into loc to tell us
            col = loc % self.dim_size

            if board[row][col] == '*':
                # This means we've actually planted a bomb there already so keep going
                continue
            board[row][col] = '*'
            bombs_planted +=1
        
        return board    

    def dig(self , row , col):
        # dig at that location 
        # return true if sucessful dig, False if bomb dug
        # a few scenarios:
        # hit a bomb -> game over
        # dig at location with neighbour bomb -> finish dig
        # dig at location with no neighbouring bomb -> recorsively dig neighbour
        self.dug.add((row , col)) # keep track that we dug here
        if self.board[row][col] == '*':
            return False
        elif  self.board[row][col] > 0:
            return True
        # self.board[row][col] == 0 (Recursive call)

        for r in range(max(0 , row-1) , min(self.dim_size-1 ,(row+1))+1):
            for c in range(max(0 ,col-1) , min(self.dim_size-1 , (col+1))+1):
                if(r,c) in self.dug:
                    continue # don't dig where u already dug
                self.dig(r ,c)  # recusion
        #if our initial dig didn't hit a bomb , we shouldn't hit a bomb here
        return True        
    
    def __str__(self):
        # this is a magic fun where if you call print on this object
        # it'll print put what this function returns!
        # return a string that shows the board to the player

        # first let
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row , col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '   

        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep             



def play(dim_size= 10 , num_bombs=10):
    #step 1 : Create board and plant the bombs
    board = Board(dim_size , num_bombs)

    #step 2 : show the user the board and ask for where they want to dig.
    #step 3a : If location is a bomb , show game over message
    #step 3b : If location is not a bomb , Dig recursively until each Square is at least next to a bomb.
    #Step4: repeat step 2 and 3 a/b until there are no nore places to dig -> VICTORY!
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*' , input("Where would you link to dig ? Input as row , col : "))
        row , col = int(user_input[0]) , int(user_input[-1])

        if(row < 0 or row >= board.dim_size or col<0 or col >= dim_size):
            print("Invalid Location , try again. ")
            continue

        # if it's valid , we Dig
        safe = board.dig(row , col)
        if not safe:
            # Dug a bomb shit man !
            break # Game over (rip)

    if safe:
        print("CONGRATULATIONS !! You are Victorious !")
    else:
        print("SORRY GAME OVER :(")
        # LET'S REVEAL the whole board!

        board.dug = [[(r,c) for r in range(board.dim_size)] for c in range(board.dim_size)]
        print(board)


if __name__ == '__main__':
    play()

         

