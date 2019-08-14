"""
Julien
Verdun
12/06/2019
"""
# -*- coding: utf-8 -*-


"""
Le jeu se déroule sur une grille à deux dimensions.
À chaque étape, l’évolution d’une cellule est entièrement déterminée par l’état de ses huit voisines de la façon suivante :
- une cellule morte 0 (blanche) possédant exactement trois voisines vivantes devient vivante (elle naît).
- une cellule vivante 1 (noire) possédant deux ou trois voisines vivantes le reste, sinon elle meurt.


-----------------------


The game takes place on a 2D grid. 
Each step, the state of a square depends on the state of the 8 squares around it as follows :
- a dead square 0 (white) who has exactly 3 living neighbors becomes alive (it burns)
- a living square 1 (black) who have exactly 2 or 3 living neighors stays alive, otherwise it deads.
"""

from tkinter import *
from tkinter.messagebox import *
import numpy as np
import random
import time

global width_grid, length_grid, length_square, Lx, Ly
"""
You can here change the parameters of the grid (width and length) and the length of a square.
"""
width_grid = 410 #width of the grid (10 + width)
length_grid = 410 #length of the grid (10 + length)
length_square = 10 #length of a square
Lx = width_grid//length_square #number of square across the width
Ly = length_grid//length_square #number of square across the length

def generate_symbole(figure_name = "canon"):
    """
    Return an array including the figure.
    """
    if figure_name == "planeur": #PLANNEUR
        planneur = np.zeros((3, 3))
        planneur[1, 0] = 1
        planneur[0, 1] = 1
        planneur[0, 2] = 1
        planneur[1, 2] = 1
        planneur[2, 2] = 1
        return planneur
    elif figure_name == "canon": #CANON
        canon = np.zeros((36,9))
        canon[0:2,5:7] = 1
        canon[11,4:7] = 1
        canon[15:17,4:7] = 1
        canon[12,3] = 1
        canon[14,3] = 1
        canon[13,2] = 1
        canon[12,7] = 1
        canon[14,7] = 1
        canon[13,8] = 1
        canon[25,0:2] = 1
        canon[22:25,1:3] = 1
        canon[21,2:5] = 1
        canon[24,3] = 1
        canon[22:25,4:6] = 1
        canon[25,5:7] = 1
        canon[30,1:3] = 1
        canon[34:36,3:5] = 1
        return canon
    else:
        return 0




class ZoneAffichage(Canvas):
    """
    This class defines the displayed zone (its dimensions) and draws the grid.
    """
    def __init__(self, parent, w=width_grid, l=length_grid, _bg='white'):
        self.__w = w
        self.__l = l
        self.__fen_parent=parent
        Canvas.__init__(self, parent, width=w, height=l, bg=_bg, relief=RAISED, bd=5)
        self.create_rectangle(10,10,w,l,outline="black",width=2)
        for i in range(Ly): #drawing of the horizontal lines
            self.create_line(10,length_square*i+10,w,length_square*i+10,fill="black",width = 1)
        for j in range(Lx): #drawing of the vertical lines
            self.create_line(length_square*j+10,10,length_square*j+10,l,fill="black",width = 1)





class FenPrincipale(Tk):
    """
    This class defines the game and the links between the game and the graphical interface.
    """
    def __init__(self):
        Tk.__init__(self)
        # random initialization of the grid
        self.__grid = np.random.randint(0, 2, (Lx, Ly))
        # initialization of the displayed squares
        self.__liste_squares = []
        # initialization of the generation (number of move) and the displayed text showing this variable
        self.__generation = 1
        self.__text_generation = Label(self)
        self.__text_generation.pack(side = TOP)
        self.__text_generation.config(text = "Generation : {}".format(self.__generation))
        # text showing the rules
        self.__text_rules = Label(self)
        self.__text_rules.pack(side=TOP)
        self.__text_rules.config(text="Press a key to play !!")
        # initialization of the graphical interface contents
        self.title('Life game')
        self.__zoneAffichage = ZoneAffichage(self)
        self.__zoneAffichage.pack(padx = 5,pady=5)

        # figures Button : allow you to choose the figure you want to plot, restart the game
        self.__boutonCanon = Button(self, text='Cannon', command=self.canon).pack(side=LEFT, padx=5, pady=5)
        self.__boutonPlanneur = Button(self, text='Planeur', command=self.planeur).pack(side=LEFT, padx=5, pady=5)
        self.__boutonRandom = Button(self, text='Random', command=self.random).pack(side=LEFT, padx=5, pady=5)

        # delete Button : allows you to exit the game
        self.__boutonQuitter = Button(self, text='Exit', command=self.destroy).pack(side=LEFT, padx=5, pady=5)
        # display the grid
        self.display_round()
        # connect the keyboard to the graphical interface and keep ready to run the method jeu_de_la_vie
        self.focus_set()
        self.bind("<Key>", self.jeu_de_la_vie)

        self.__figure = "random"

    def canon(self):
        self.__figure = "canon"
        self.restart("canon")

    def planeur(self):
        self.__figure = "planeur"
        self.restart("planeur")

    def random(self):
        self.__figure = "random"
        self.restart("random")

    def get_generation(self):
        """
        Give the number of the generation
        """
        return self.__generation

    def set_generation(self,gene):
        """
        Modified the variable generation
        """
        self.__generation = gene

    def restart(self,figure = "random"):
        """
        Initialize the different variables in order to start a new game.
        """
        if figure == "canon" or figure == "planeur":
            self.__grid = np.zeros((Lx,Ly))
            if figure == "canon" :
                if Lx < 40 or Ly < 12:
                    return self.restart("random")
                figure_grid = generate_symbole(figure)#3x3
                self.__grid[Lx//2-18:Lx//2+18,Ly//2-4:Ly//2+5] = figure_grid
            elif  figure == "planeur" :
                if Lx < 5 or Ly < 5:
                    return self.restart("random")
                figure_grid = generate_symbole(figure)#36x9
                self.__grid[Lx//2-1:Lx//2+2,Ly//2-1:Ly//2+2] = figure_grid
        else:
            # random initialization of the grid
            self.__grid = np.random.randint(0, 2, (Lx, Ly))
        # initialization of the generation (number of move) and the displayed text showing this variable
        self.__generation = 1
        self.__text_generation.config(text="Generation : {}".format(self.__generation))
        self.display_round()

    def sum_living_cell(self,x, y, current_round):
        """
        Comput the sum of the squares around a given square of coordinates x and y.
        The value of the squares contained in the grid current_round are 1 for a living square (black) and 0 for a dead square (white).
        The computation is done depending on the position of the square (on a side or somewhere else).
        """
        if 1 <= x <= Lx - 2 and 1 <= y <= Ly - 2:#if the square is not on a side of the grid
            sum_living_cell = sum(sum(current_round[x - 1:x + 2, y - 1:y + 2])) #we take the 8 squares around it to comput the sum

        elif x == 0: #if the square is on the left side of the grid
            if 1 <= y <= Ly - 2: #if the square isn't on the top or bottom squares of the grid
                sum_living_cell = sum(sum(current_round[x:x + 2, y - 1:y + 2])) #we take the 5 squares around it to comput the sum
            elif y == 0: #if the square is on the top side
                sum_living_cell = sum(sum(current_round[x:x + 2, y:y + 2])) #we take the 3 squares around it to comput the sum
            elif y == Ly - 1: #if the square is on the bottom side
                sum_living_cell = sum(sum(current_round[x:x + 2, y - 1:y+1])) #we take the 3 squares around it to comput the sum
        #and so on for the other side
        elif x == Lx - 1:
            if 1 <= y <= Ly - 2:
                sum_living_cell = sum(sum(current_round[x - 1:x+1, y - 1:y + 2]))
            elif y == 0:
                sum_living_cell = sum(sum(current_round[x - 1:x+1, y:y + 2]))
            elif y == Ly - 1:
                sum_living_cell = sum(sum(current_round[x - 1:x+1, y - 1:y+1]))

        elif y == 0:
            if 1 <= x <= Lx - 2:
                sum_living_cell = sum(sum(current_round[x - 1:x + 2, y:y + 2]))
            elif x == 0:
                sum_living_cell = sum(sum(current_round[x:x + 2, y:y + 2]))
            elif x == Lx - 1:
                sum_living_cell = sum(sum(current_round[x - 1:x+1, y:y + 2]))

        elif y == Ly - 1:
            if 1 <= x <= Lx - 2:
                sum_living_cell = sum(sum(current_round[x:x + 2, y - 1:y+1]))
            elif x == 0:
                sum_living_cell = sum(sum(current_round[x:x + 2, y - 1:y+1]))
            elif x == Lx - 1:
                sum_living_cell = sum(sum(current_round[x - 1:x+1, y - 1:y+1]))
        else:
            print("Square situation not found !")
        sum_living_cell -= current_round[x][y] #we delete the square that we add on the sum
        return sum_living_cell

    def next_round(self, old_round):
        """
        Depending on the last grid (old_round), compute the the new one with the life game rules
        """
        new_round = np.copy(old_round) #copy of the old grid
        # for each square
        for i in range(Lx):
            for j in range(Ly):
                if old_round[i][j] == 0 : #if the cell is dead, it will live if it has 3 living neighbors.
                    if self.sum_living_cell(i, j, old_round) == 3:
                        new_round[i][j] = 1
                    else:
                        new_round[i][j] = 0
                if old_round[i][j] == 1 : #if the cell is alive, it won't dead if it has 2 or 3 living neighors.
                    square_score = self.sum_living_cell(i, j, old_round)
                    if square_score != 2 and square_score != 3 :
                        new_round[i][j] = 0
                    else:
                        new_round[i][j] = 1
        return new_round

    def display_round(self):
        """
        Display the grid on the graphical interface : colour the squares in white for a dead cell (0) and in black for a living one (1)
        """
        # for each squares of the grid
        for elt in self.__liste_squares:
            self.__zoneAffichage.delete(elt) #we delete the old square
        self.__liste_squares = []
        # for each squares of the grid
        for i in range(Lx):
            for j in range(Ly):
                # if the cell is living
                if self.__grid[i][j] == 1:
                    #we colour it in black, else it stays in white.
                    self.__liste_squares.append(self.__zoneAffichage.create_rectangle(10 + length_square * i,10 + length_square * j,10 + length_square * (i+1) ,10 + length_square * (j+1),fill="black",outline="black"))
        print("Generation {} ploted".format(self.__generation))

    def jeu_de_la_vie(self,event):
        """
        Whenever a key is touched by the user, this function is ran.
        It computes the new grid, displays it and updates the variables and displayed text related to the generation number.
        """
        self.__grid = self.next_round(self.__grid)
        self.__generation += 1
        self.__text_generation.config(text = "Generation :" + str(self.__generation))
        self.display_round()



# lauching of the windows
if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
