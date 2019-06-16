"""
Julien
Verdun
12/06/2019
"""
# -*- coding: utf-8 -*-

"""
Le jeu se déroule sur une grille à deux dimensions.
À chaque étape, l’évolution d’une cellule est entièrement déterminée par l’état de ses huit voisines de la façon suivante :

Une chute de « bombes » non périodique.
Une cellule morte 0 possédant exactement trois voisines vivantes devient vivante (elle naît).
Une cellule vivante 1 possédant deux ou trois voisines vivantes le reste, sinon elle meurt.
"""

from tkinter import *
from tkinter.messagebox import *
import numpy as np
import random
import time

global width_grid, length_grid, length_square, Lx, Ly,entire_time,period_time
width_grid = 810
length_grid = 810
length_square = 20
Lx = width_grid//length_square
Ly = length_grid//length_square
entire_time=100
period_time=1



class ZoneAffichage(Canvas):
    def __init__(self, parent, w=width_grid, l=length_grid, _bg='white'):
        self.__w = w
        self.__l = l
        self.__fen_parent=parent
        Canvas.__init__(self, parent, width=w, height=l, bg=_bg, relief=RAISED, bd=5)
        self.create_rectangle(10,10,w,l,outline="black",width=2)
        for i in range(Ly):
            self.create_line(10,length_square*i+10,w,length_square*i+10,fill="black",width = 2)
        for j in range(Lx):
            self.create_line(length_square*j+10,10,length_square*j+10,l,fill="black",width = 2)





class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.__grid = np.random.randint(0, 2, (Lx, Ly))

        self.__liste_squares = []

        self.__generation = 1
        self.__text_generation = Label(self)
        self.__text_generation.pack(side = TOP)
        self.__text_generation.config(text = "Generation : {}".format(self.__generation))

        self.__text_rules = Label(self)
        self.__text_rules.pack(side=TOP)
        self.__text_rules.config(text="Use the key up to play !!")

        self.title('JEU DE LA VIE')
        self.__zoneAffichage = ZoneAffichage(self)
        self.__zoneAffichage.pack(padx = 5,pady=5)

        # Création d'un widget Button (bouton Effacer)
        self.__boutonEffacer = Button(self, text='Effacer', command=self.effacer).pack(side=LEFT, padx=5, pady=5)
        # Création d'un widget Button (bouton Quitter)
        self.__boutonQuitter = Button(self, text='Quitter', command=self.destroy).pack(side=LEFT, padx=5, pady=5)

        self.display_round()

        self.focus_set()

        self.bind("<Key>", self.jeu_de_la_vie)

    def effacer(self):
        self.__zoneAffichage.delete(ALL)

    def get_generation(self):
        return self.__generation

    def set_generation(self,gene):
        self.__generation = gene

    def sum_living_cell(self,x, y, current_round):

        if 1 <= x <= Lx - 2 and 1 <= y <= Ly - 2:
            sum_living_cell = sum(sum(current_round[x - 1:x + 2, y - 1:y + 2]))

        elif x == 0:
            if 1 <= y <= Ly - 2:
                sum_living_cell = sum(sum(current_round[x:x + 2, y - 1:y + 2]))
            elif y == 0:
                sum_living_cell = sum(sum(current_round[x:x + 2, y:y + 2]))
            elif y == Ly - 1:
                sum_living_cell = sum(sum(current_round[x:x + 2, y - 1:y+1]))

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
        sum_living_cell -= current_round[x][y]
        return sum_living_cell

    def next_round(self, old_round):
        new_round = np.copy(old_round)
        for i in range(Lx):
            for j in range(Ly):
                if old_round[i][j] == 0 :
                    if self.sum_living_cell(i, j, old_round) == 3:
                        new_round[i][j] = 1
                    else:
                        new_round[i][j] = 0
                if old_round[i][j] == 1 :
                    square_score = self.sum_living_cell(i, j, old_round)
                    if square_score != 2 and square_score != 3 :
                        new_round[i][j] = 0
                    else:
                        new_round[i][j] = 1
        return new_round

    def display_round(self):
        for elt in self.__liste_squares:
            self.__zoneAffichage.delete(elt)
        self.__liste_squares = []
        for i in range(Lx):
            for j in range(Ly):
                if self.__grid[i][j] == 1:
                    self.__liste_squares.append(self.__zoneAffichage.create_rectangle(10 + length_square * i,10 + length_square * j,10 + length_square * (i+1) ,10 + length_square * (j+1),fill="black",outline="black"))
        print("Generation ploted")

    def is_changing(self,grid1, grid2):
        if np.size(grid1) != np.size(grid2):
            return True
        for i in range(np.size(grid1, 0)):
            for j in range(np.size(grid1, 1)):
                if grid1[i][j] != grid2[i][j]:
                    return True
        return False

    def jeu_de_la_vie(self,event):
        touche = event.keysym
        if touche == "Up":
            self.jeu_de_la_vie_one_round()
        elif touche == "Down":
            self.jeu_de_la_vie_n_rounds()
        else:
            print("Key not recognized, please use key up or down !")

    def jeu_de_la_vie_n_rounds(self):
        for i in range(entire_time):
            grid1 = np.copy(self.__grid)
            self.__grid = self.next_round(grid1)
            if self.is_changing(grid1, self.__grid):
                self.display_round()
            else:
                break
            self.__generation += 1
            self.__text_generation.config(text = "Generation :" + str(self.__generation))
            time.sleep(period_time)


    def jeu_de_la_vie_one_round(self):
        self.__grid = self.next_round(self.__grid)
        self.__generation += 1
        self.__text_generation.config(text = "Generation :" + str(self.__generation))
        self.display_round()







if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
