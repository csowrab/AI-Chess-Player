import pygame
import sklearn
from sklearn.neural_network import MLPClassifier
import chess
import pickle
from pygame.locals import *

# Pieces of the board
UPPER = "RNBKQP"
LOWER = "rnbkqp"

# Sets up board and its pieces at start.
def Board_creation():
    FEN_line = board.fen()
    Arr = []
    Row = []
    for each in FEN_line:
        if each.isnumeric() == True:
            for a in range(0,int(each)):
                Row.append("0")
        elif each == "/":
            Arr.append(Row)
            Row = []
        elif each == " ":
            Arr.append(Row)
            break
        else:
            Row.append(each)

    return Arr

# Used to write characters (pieces) on the board.
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

# Works out the end-position, and translates it to py-chess game.
def Work_out(end_position):
    column_name = ['a','b','c','d','e','f','g','h']
    row = 8 - int(end_position[1])
    column = column_name.index(end_position[0])
    return row, column

# Draws the board to the current state
def Draw_board(Drag = False, Moves_to_shade = [], Helper_move = ""):# Some values are set to default, they are used only when the user needs to.
    BOARD2 = Board_creation() # BOARD2 will store the current positions of the board,

    #row and column represent indexes of  the BOARD2 array
    row = 0 # element of each row, (1,2,3,4...,7), 
    r = 0# x_coordinate of each sqaure(0,100,200,300...,700) 
    column = 0# representing each array inside it.
    c = 0# y_coordinate for each column (0,100,...,700)
    switch = white #To switch to colors in each square 

    #Both
    x_center = 50
    y_center = 50
    index1 = index2 = 0 #Indexes of BOARD2
    switch_c = white
    ###"switch_c" ensures a whole row is not shaded black ir white. Such as if the color of the last square of the row is black, then the first square of the second row...
    #..should be black too.
        
        
    while row != 8:
        column = 0
        if switch == black:
            switch = white
        else:
            switch = black

        ###"switch_c" ensures a whole row is not shaded black ir white. Such as if the color of the last square of the row is black, then the first square of the second row
        #should be black too.
        if switch_c == white:
            switch_c = black
        else:
            switch_c = white

            
        while column != 8:
            if Drag == True and (str(row) + str(column)) in Moves_to_shade: ##"row" and "column" altogether refer to 1 square
                if (str(row) + str(column)) == Helper_move:
                    pygame.draw.rect(gameDisplay, blue,(r,c,100,100))#Shades the square in blue to move represented by helper function for that piece.
                else:
                    pygame.draw.rect(gameDisplay, green,(r,c,100,100))#Shades in green the squares that the piece can move to.
            else:
                pygame.draw.rect(gameDisplay, switch,(r,c,100,100))#Shades each sqaure either black or white.
                
            largeText = pygame.font.Font('freesansbold.ttf',100)#Size of font of pieces (represented by letters)
            #print(index2, index1)
            if BOARD2[index2][index1] != "0":
                if BOARD2[index2][index1] in UPPER:
                    TextSurf, TextRect = text_objects(BOARD2[index2][index1], largeText, sandybrown) # Colour the white pieces in "sandybrown"
                elif BOARD2[index2][index1] in LOWER:
                    TextSurf, TextRect = text_objects(BOARD2[index2][index1], largeText, chocolate)# Colour the black pieces in "chocolate" brown
                if switch_c == white:
                    switch_c = black
                else:
                    switch_c = white
                TextRect.center = ((x_center),(y_center))
                gameDisplay.blit(TextSurf, TextRect)
            x_center += 100
                
            index1 += 1
                #print("1:",index1)
            if index1 > 7:
                index1 = 0
                index2 += 1
                  #  print("1",index2)
                
                ###
            if switch == black:
                switch = white
            else:
                switch = black
            r += 100
            column += 1
        row += 1
        y_center += 100
        x_center = 50
        c += 100
        r = 0
        column = 0

# Main function where the chess-board is displayed, along with allowing the user to click on squares  
def main(AI_is_white, BOARD2):

    intro = True
    gameDisplay.fill(white)
    largeText = pygame.font.Font('freesansbold.ttf',150)
    pygame.display.update()

    BOARD2 = Board_creation()
    Draw_board()
    pygame.display.update()

    drag = False # This is used to initiate effects when the user makes the first click to move.
    shown = False # To prevent the program to show moves available again on IDLE 
    Helper_on = False# Shades a square in blue when is set to (True)
    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                Game_over_screen("Q") #Displays screen "You have decided to quit!"
                pygame.quit()
                quit()
        if board.turn == AI_is_white:
            move = ""
            Make_move(board, AI_is_white, move) #Function used to make the AI its own move.  

        else:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if drag == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h and Helper_on == False:# Helper_on is true when the user presses the key "h", pressing it again will turn "Helper_on" to false
                        Helper_on = True
                        clock.tick(50)
                    elif event.key == pygame.K_h and Helper_on == True:
                        Helper_on = False
                        clock.tick(50)

                        
                if Helper_on == True:
                    Helper_move = Helper(registered,  AI_is_white)# Function will use the model loaded by the user to check for the best move that piece can do.
                    if Helper_move != None:
                        Helper_row, Helper_column = Work_out(str(Helper_move)[2:])
                        Helper_move = str(Helper_row) + str(Helper_column)
                        Draw_board(True, Moves_from_selected, Helper_move)
                else:
                    Draw_board(True, Moves_from_selected)
                            
            if shown == False:
                c = 0
                for each in board.legal_moves:
                    c += 1
                if c == 0:
                    print("NONE")
                    Game_over_screen("AI_wins")# If the list of moves from AI is empty, the screen will display text stating "You lost!"
                shown = True

            #From here onwards, we will explain how mouse clicks are processed by the program.
            if click[0] == 1:
                clock.tick(15)
                if len(str(mouse[0])) < 3:
                    cent_x = 0
                else:
                    cent_x = int(str(mouse[0])[0])# As explained before, "cent_x" records which column is selected by using the first digit of the x-coordinate greater than, or equal to 100 
                    #If x-coordinate is less than 100, we will take it as 0 instead.
                    
                if len(str(mouse[1])) < 3:
                    cent_y = 0
                else:
                    cent_y = int(str(mouse[1])[0])# This records row selected by using the first coordinate of the y-coordinate that is greater than or equal to 100.
                     #If y-coordinate is less than 100, we will take it as 0 instead.
                    
                if drag == False:
                    if BOARD2[cent_y][cent_x] != "0":# Checks if the first square clicked in not empty
                        starting_x = cent_x
                        starting_y = cent_y
                        drag = True 
                        registered = Alpha[starting_y][starting_x] #Taking cent_x and cent_y as indexes, we can map this to a square in the array "Alpha". 
                        
                        Moves_from_selected = [] #This will contain moves from the selected piece, which will be represented as squares shaded in green.
                        for each in board.legal_moves:
                            if str(each)[0:2] == registered:
                                Num_row, Num_column = Work_out(str(each)[2:])
                                Moves_from_selected.append(str(Num_row) + str(Num_column))
                                
                else: #If drag is True, then program waits for the user to click on the second square.
                    finish_x = cent_x 
                    finish_y = cent_y

                    BOARD2 = Board_creation()
                    Draw_board()
                    move = Alpha[starting_y][starting_x] + Alpha[finish_y][finish_x] # A move is generated by combining
                    print("Move:", move)
                    Fifth = Make_move(board, AI_is_white, move)# When a pawn reaches the end of the board, the player will press a key from "q","r","b","n" and the pawn will transform
                    if Fifth == False:#Checks whether transforming is needed.
                        move = ""
                        drag = False
                        print("Select again")
                    else:
                        if Fifth != False:
                            if Fifth != "":
                                pass

                            BOARD2 = Board_creation()
                            pygame.display.update()
                            shown = False
                        
                            drag = False
                            Helper_on = False
                            pygame.display.update()


            pygame.display.update()
            

        clock.tick(15)

# Distinguishes between a move made by the AI or move made by the user.
def Make_move(board, AI_is_white, move): 
    if board.turn == AI_is_white:
        Best_move = Trials(board, AI_is_white, clf)
        board.push(Best_move)

        BOARD2 = Board_creation()
        Draw_board()
        pygame.display.update()

    else:

        Done = False
        choice = move
        while Done == False:
            Fifth = False
            for each in board.legal_moves:
                if str(each) == choice:
                    Done = True
                elif str(each)[0:4] == choice and Fifth == False:
                    add = Transform(move)
                    choice = move + add
                    Fifth = True
                    print("New move:", choice)
                    if str(each) == choice:
                        Done = True
            if Done == False:
                print("The move you entered is not valid")
                return False
                    


        selected = chess.Move.from_uci(choice)
        board.push(selected)
        BOARD2 = Board_creation()
        Draw_board()
        if Fifth == True:
            return add
        else:
            return ""

# This is where the AI chooses the best move from the list.
def Trials(board, turn, clf): 
    Cboard = board # A copy of the current board is made.
    highest = 0
    index = None
    for move in board.legal_moves: # board.legal_moves contains the list of moves that are available
        Cboard.push(move)
        recorded = Numbered_pieces(Cboard.fen()) #This finite loop will test every move in the list
        if turn == True:
            prob = clf.predict_proba([recorded])[0][2]# "predict_proba(...)" outputs an array containing probabilities, this will be in form [black,draw,white]
        else:
            prob = clf.predict_proba([recorded])[0][0]
        if prob > highest or index == None:
            highest = prob
            index = move
        Cboard.pop()# Move executed is undone to allow the next move in the list to occur.
    print("")
    if index == None:# If the list of moves is empty, screen will display text written "You won!"
        Game_over_screen("Player_win")
    print("AI: " +str(index))
    #print(highest)
    #print(index)
    return index

# Takes care of transforming pawns, when they reach end of the board.
def Transform(move):
    print("Select a letter to transform by (press either 'q' for queen, 'r' for rook,'n' for knight or 'b' bishop on the keyboard):")
    Button = pygame.key.get_pressed()
    Finished = False
    while not Finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    Finished = True
                    return "q"
                if event.key == pygame.K_n:
                    Finished = True
                    return "n"
                if event.key == pygame.K_b:
                    Finished = True
                    return "b"
                if event.key == pygame.K_r:
                    Finished = True
                    return "r"

# Activates Helper function.
def Helper(string, AI_is_white):
    turn = not AI_is_white

    for each in board.legal_moves:
        Cboard = board
        highest = 0
        index = None
        for move in board.legal_moves:
            if str(move)[0:2] == string:
                Cboard.push(move)
                recorded = Numbered_pieces(Cboard.fen())
                if turn == False:
                    prob = clf.predict_proba([recorded])[0][2]
                else:
                    prob = clf.predict_proba([recorded])[0][0]
                if prob > highest or index == None:
                    highest = prob
                    index = move
                Cboard.pop()
    return index

# Maps pieces from letters to numbers, to allow Algorithm to compare against dataset trained.
def Numbered_pieces(string):
    Numbers = ["1","2","3","4","5","6","7","8","9","0"]
    dictionary = { "p" : 1, "r" : 2, "n" : 3, "b" : 4, "q" : 5, "k" : 6, "P" : -1, "R" : -2, "N" : -3, "B" : -4, "Q" : -5, "K" : -6 }
    Num_grid = []
    for piece in string:
        if piece == "/":
            pass
        elif piece == " ":
            break
        elif piece in Numbers:
            for number in range (0,int(piece)):
                Num_grid.append(int(0))
        elif piece == " ":
            break
        else:
            Num_grid.append(dictionary[piece])
    return Num_grid

# Produces game ppver screen.
def Game_over_screen(Reason):
    gameDisplay.fill(white)
    
    if Reason == "Q":
        Create_Text("You have quit!", 400, 400, 115, black)
        pygame.display.update()
        quit()

    elif Reason == "Player_win":
         Create_Text("You Won!", 400, 400, 115, black)
         pygame.display.update()
         quit()

    else:
        Create_Text("You lost!", 400, 400, 115, black)
        pygame.display.update()
        quit()


# Displays first 2 screes (difficulty and turn choice).
def Menu_Display(): # The function displays the first 2 screens of the game.
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    pygame.display.set_mode((800,600))
    gameDisplay.fill(black)
    largeText = pygame.font.Font('freesansbold.ttf',80)
    
    Create_Text("Select a Difficulty", 400, 200, 80, white)
    Create_Text("Note: In the game, press 'h' to turn the helper function on and off", 400, 500, 20, white)
    Difficulty = 0
    Turn = ""
    
    Loop = True
    while Loop:
        for event in pygame.event.get():
            #These 2 lines will be appearing again the code, it tracks the coordinates of the mouse.
            mouse = pygame.mouse.get_pos() 
            click = pygame.mouse.get_pressed()
            
            if 150< mouse[0] < 250 and 300 < mouse[1] < 400: # Button effect when mouse is in "Easy".
                pygame.draw.rect(gameDisplay, bright_green,(150,300,100,100))
                Create_Text("Easy",200,350,30,white)
                pygame.display.update()
                if click[0] == True:
                    Difficulty = 1
                    Loop = False
                    break
            else:
                pygame.draw.rect(gameDisplay, green,(150,300,100,100))
                Create_Text("Easy",200,350,30,white)
                pygame.display.update()
                

            if 350 < mouse[0] < 450 and 300 < mouse[1] < 400:# Button effect when mouse is in "Medium".
                pygame.draw.rect(gameDisplay, bright_yellow,(350,300,100,100))
                Create_Text("Medium",400,350,30,white)  
                pygame.display.update()
                if click[0] == True:
                    Difficulty = 2
                    Loop = False
                    break
            else:
                pygame.draw.rect(gameDisplay, yellow,(350,300,100,100))
                Create_Text("Medium",400,350,30,white)
                pygame.display.update()

            if 550 < mouse[0] < 650 and 300 < mouse[1] < 400:# Button effect when mouse is in "Hard".
                pygame.draw.rect(gameDisplay, bright_red,(550,300,100,100))
                Create_Text("Hard",600,350,30,white)  
                pygame.display.update()
                if click[0] == True:
                    Difficulty = 3
                    Loop = False
                    break
            else:
                pygame.draw.rect(gameDisplay, red,(550,300,100,100))
                Create_Text("Hard",600,350,30,white)
                pygame.display.update()

    #From here onwards, the code will ask whether to play as black or white
    gameDisplay.fill(black)    
    Create_Text("Color to play as?", 400, 200, 80, white)
    pygame.display.update()

    Loop = True
    while Loop:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if 200< mouse[0] < 300 and 300 < mouse[1] < 400:#Effect when user goes on "White"
                pygame.draw.rect(gameDisplay, bright_green,(200,300,100,100))
                Create_Text("White",250,350,30,white)
                pygame.display.update()
                if click[0] == True:
                    AI_is_white = False
                    Loop = False
                    break
            else:
                pygame.draw.rect(gameDisplay, green,(200,300,100,100))
                Create_Text("White",250,350,30,white)
                pygame.display.update()

            if 400< mouse[0] < 500 and 300 < mouse[1] < 400:#Effect when the user goes on "Black"
                pygame.draw.rect(gameDisplay, bright_green,(400,300,100,100))
                Create_Text("Black",450,350,30,white)
                pygame.display.update()
                if click[0] == True:
                    AI_is_white = True
                    Loop = False
                    break
            else:
                pygame.draw.rect(gameDisplay, green,(400,300,100,100))
                Create_Text("Black",450,350,30,white)
                pygame.display.update()


    return Difficulty, AI_is_white # The 2 parameters selected by the user are returned to the main program.
                

#Used to create letters on the boards.     
def Create_Text(Text,x,y,size,color):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect = text_objects(Text, largeText, color)
    TextRect.center = ((x),(y))
    gameDisplay.blit(TextSurf, TextRect)   
    

pygame.init()
 
display_width = 800
display_height = 800
 
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
blue = (0,0,255)
yellow = (204,204,0)
red = (255,0,0)

bright_green = (40,100,0)
bright_red = (170, 1, 20)
bright_yellow = (255,255,102)
chocolate = (210,105,30)
sandybrown = (244,164,96)
 
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Chess')
clock = pygame.time.Clock()

#How the squares are represented in the chess board.
Alpha = [["a8","b8","c8","d8","e8","f8","g8","h8"],   
             ["a7","b7","c7","d7","e7","f7","g7","h7"],
             ["a6","b6","c6","d6","e6","f6","g6","h6"],
             ["a5","b5","c5","d5","e5","f5","g5","h5"],
             ["a4","b4","c4","d4","e4","f4","g4","h4"],
             ["a3","b3","c3","d3","e3","f3","g3","h3"],
             ["a2","b2","c2","d2","e2","f2","g2","h2"],
             ["a1","b1","c1","d1","e1","f1","g1","h1"]]



Difficulty, AI_is_white = Menu_Display()
if Difficulty == 1:
    f = open("MLP_net", "rb")
    clf = pickle.load(f)
    f.close()
elif Difficulty == 2:
    f = open("MLP_net(25,25)", "rb")
    clf = pickle.load(f)
    f.close()
else:
    f = open("MLP_net_5000000 (25,25)", "rb")
    clf = pickle.load(f)
    f.close()    
    
board = chess.Board() #Chess game is created.
BOARD2 = Board_creation() # Chess_board is drawn.
gameDisplay = pygame.display.set_mode((display_width,display_height)) # display is at size 800x800.
main(AI_is_white, BOARD2)# Main function runs.
                    
