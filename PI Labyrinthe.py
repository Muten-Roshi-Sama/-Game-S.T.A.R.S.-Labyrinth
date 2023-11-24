"""
Author : F. Vassily
Date : 15.03.2022

Goal :


Input : The four arrows to move around the Maze and all answers to questions typed from a keyboard.
Output : The Interactive Maze itself.


INFO :
The .txt containing the plan : 'plan_chateau.txt'
    value 0 for an empty box,
    value 1 for a wall,
    value 2 for the exit,
    value 3 for a door which will open after answering a question,
    value 4 for a box containing an object to collect, becomes an empty case after.

The game space is (x, y) ;

The .txt containing the clues : 'dico_objets'
    (x, y), "clue"
    example : (12, 3), "un oreiller magique"

The .txt containing the Questions/Answers : 'dico_portes'
    (x, y), ("question", "réponse")
    exemple : (21, 12), ("Capitale de la Belgique ?", "Bruxelles")
    start is at 0,0


Tests   Samuel-6 ; 10:45
        Mart-23 ; 9:50
        Nk-23; 5:52


Age : 6-12 -Facile
      12-17 -Intermédiare
      18+  - Difficile


Tests : maman - 3 - 3:05 mieux expliquer les règles
        nell - lvl 1 - 2:27
             _ lvl 3 - 4:12
        nassima - lvl 3 - 2:10
        vincent - 3 -
        niky - lvl 3 - 2:26


"""
# IMPORTS
import turtle as tt
from CONFIGS import *

#-----CONSTANT VARIABLES------------------------
global Hauteur, Largeur  # for readability in next levels.
Hauteur = (abs(ZONE_PLAN_MINI[1]) + abs(ZONE_PLAN_MAXI[1]))
Largeur = (abs(ZONE_PLAN_MINI[0]) + abs(ZONE_PLAN_MAXI[0]))
WRITING_COLOR = 'BLACK'  # color of turtle when writing something.
tt.bgcolor("black")
PlayerItemList = []
position = POSITION_DEPART
dic_mouv = {'up': (-1, 0), 'down': (1, 0),
            "left": (0, -1), 'right': (0, 1)}

AllCluesNeeded = False #do you need all the clues to finish the game ?


#--------ADJUSTMENTS--------------------------------------------------------
MazeX = -350  #Left is -
MazeY = 180   #Up is +
MazeSize = 13
InventoryBg = "black"
BannerBg = InventoryBg
Endscreen = False #NOTDONE prevents from moving when GameOver
COULEUR_CASES = 'black'
Textcolor = "white"
AnimationSpeed = 0 #instant. = 0


LVL = 3 #default value : 3
keysType = 1
CODE = 5548

# ----------------------------------------------------LEVEL_1------------------------------------------------------------------------#
"""The first level of the program consist of the creation of the matrix M containing the plan, and the graphic 
representation of it using the Turtle Module. 
"""


def lire_matrice(fichier):
    """Reads the text file and converts it into a matrix."""
    contents = open(fichier).read()
    matrice = [[int(string) for string in elem.split()] for elem in contents.split('\n')[:]]
    print(matrice)
    return matrice


def calculer_pas(matrice):
    """calcule la dimension à donner aux cases"""
    Hauteur_case = Hauteur // len(matrice[0])
    Largeur_case = Largeur // len(matrice)
    return min(Hauteur_case, Largeur_case) + MazeSize  # adjust to screen.


def coordonnees(case, pas):
    """ Calculate the coordinates (left lower part of each box). """
    x, y = case
    bcoord_x = (ZONE_PLAN_MINI[0] + y * pas) + MazeX
    bcoord_y = (ZONE_PLAN_MAXI[1] - x * pas) + MazeY
    #print(bcoord_x, bcoord_y)
    return bcoord_x, bcoord_y


def tracer_carre(dimension):
    """(square : move forward, turn right) *4"""
    tt.pencolor(COULEUR_CASES)  # making the pencolor white
    tt.pendown()  # putting the pen down to start working
    for i in range(4):
        tt.fd(dimension)
        tt.rt(90)


def tracer_case(case, couleur, pas):
    """ Call tracer_carre to draw a square from a certain size, color, position. """
    tt.pu()
    tt.goto(coordonnees(case, pas))
    tt.pd()
    tt.fillcolor(couleur)
    tt.begin_fill()
    tracer_carre(pas)
    tt.end_fill()


def afficher_plan(matrice):
    """ Draws the whole Maze. """
    for x in range(len(matrice)):
        tt.pu()
        for y in range(len(matrice[0])):
            tracer_case((x, y), COULEURS[int(matrice[x][y])], pas)
    tt.pu()
    x, y = coordonnees(POSITION_DEPART, pas)  # Starting box-coordinates of the player.
    MIDDLE = (x + pas // 2, y - pas // 2)  # Centered starting point of the player.
    tt.goto(MIDDLE)
    tt.pd()
    tt.dot(pas * RATIO_PERSONNAGE, COULEUR_PERSONNAGE)


# ----------------------------------------------------LEVEL_2------------------------------------------------------------------------#
""" The second level consist of the code containing the movements of the player.
"""


def deplacer(matrice, position, mouvement, dict_objets, dict_portes):
    """ Function to move the player up, down, left or right in the matrix """
    x, y = position
    new_pos = x + mouvement[0], y + mouvement[1]
    MIN = 0
    MAX_Y = len(matrice[0])
    MAX_X = len(matrice)
    if MIN <= new_pos[0] < MAX_X and MIN <= new_pos[1] < MAX_Y:  # checks if player goes off-limits.
        if matrice[new_pos[0]][new_pos[1]] != 1 and matrice[new_pos[0]][new_pos[1]] != 3:
            # checks for walls and closed-doors.
            position = new_pos
            if (new_pos[0], new_pos[1]) in dict_objets:  # Check if the next box contains a clue.
                ramasser_objet(dict_objets, PlayerItemList, (new_pos[0], new_pos[1]))

        elif (new_pos[0], new_pos[1]) in dict_portes and matrice[new_pos[0]][new_pos[1]] == 3:  # Check for doors.
            temp = poser_question(matrice, (new_pos[0], new_pos[1]), mouvement, dict_portes)
            if temp:
                position = new_pos

        if matrice[new_pos[0]][new_pos[1]] == 2:  # Exit of the Maze.
            if len(PlayerItemList) == len(dict_objets) or AllCluesNeeded is False:   # if the Player got all clues.
                Endscreen = True
                writeBanner('Hooray ! You won.')
                mandala()
                tt.exitonclick()
            else:
                writeBanner("You need to find all clues to escape.")

    print('Votre Position : ', position)  # Prints the position to keep track of your advancement.
    return position


def deplacer_haut():
    """ Player going up """
    global matrice, position, pas, dic_mouv  # AS GIVEN
    temp = deplacer(matrice, position, dic_mouv['up'], dict_objets, dict_portes)
    tt.onkeypress(None, "Up")  # AS GIVEN
    if temp != position:  # if equal, the move sends the player somewhere it shouldn't, so do nothing.
        tracer_case(position, COULEUR_VUE, pas)  # Show where the player already went (=map).
        position = temp
        tt.penup()
        x, y = coordonnees(position, pas)
        MIDDLE = (x + pas // 2, y - pas // 2)  # Make sure the player is centered.
        tt.goto(MIDDLE)
        tt.pendown()
        tt.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
    tt.onkeypress(deplacer_haut, "Up")  # AS GIVEN


def deplacer_bas():
    """ Player going down """
    global matrice, position, pas, dic_mouv, dict_portes
    temp = deplacer(matrice, position, dic_mouv['down'], dict_objets, dict_portes)
    tt.onkeypress(None, "Down")
    if temp != position:
        tracer_case(position, COULEUR_VUE, pas)
        position = temp
        tt.penup()
        x, y = coordonnees(position, pas)
        MIDDLE = (x + pas // 2, y - pas // 2)
        tt.goto(MIDDLE)
        tt.pendown()
        tt.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)

    tt.onkeypress(deplacer_bas, "Down")


def deplacer_gauche():
    """ Player going left """
    global matrice, position, pas, dic_mouv, dict_portes
    temp = deplacer(matrice, position, dic_mouv['left'], dict_objets, dict_portes)
    tt.onkeypress(None, "Left")
    if temp != position:
        tracer_case(position, COULEUR_VUE, pas)
        position = temp
        tt.penup()
        x, y = coordonnees(position, pas)
        MIDDLE = (x + pas // 2, y - pas // 2)
        tt.goto(MIDDLE)
        tt.pendown()
        tt.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
    tt.onkeypress(deplacer_gauche, "Left")


def deplacer_droite():
    """ Player going right """
    global matrice, position, pas, dic_mouv, dict_portes
    temp = deplacer(matrice, position, dic_mouv['right'], dict_objets, dict_portes)
    tt.onkeypress(None, "Right")
    if temp != position:
        tracer_case(position, COULEUR_VUE, pas)
        position = temp
        tt.penup()
        x, y = coordonnees(position, pas)
        MIDDLE = (x + pas // 2, y - pas // 2)
        tt.goto(MIDDLE)
        tt.pendown()
        tt.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
    tt.onkeypress(deplacer_droite, "Right")


# ----------------------------------------------------LEVEL_3------------------------------------------------------------------------#
""" This third level is to manage the clues (objects) scattered around the maze and the display 
when you pick them up.
"""


def creer_dictionnaire_des_objets(file_2):
    """Reads the text file and converts it into a dictionary."""
    Dict = {}
    with open(file_2, encoding="UTF-8") as f:
        for line in f:
            line = line.split(",")
            line[:2] = [eval(','.join(line[:2]))]
            line[1:] = [eval(','.join(line[1:]))]
            Dict[line[0]] = line[1]
    return Dict


def ramasser_objet(dict_objets, PlayerItemList, position):
    """ Delete the clue from the matrix and add it in the menu and PlayerItemList. """
    x, y = position
    if dict_objets[position] not in PlayerItemList:
        PlayerItemList.append(dict_objets[position])
        writeBanner("Nouvel objet : " + dict_objets[position])
        writeInventory(PlayerItemList)
    matrice[x][y] = 0


def writeInventory(PlayerItemList):
    """ Write the inventory of the Player, based on CONFIGS position."""
    tt.pu()
    x, y = POINT_AFFICHAGE_INVENTAIRE
    x, y = x, y
    tt.goto(x, y)
    tt.pd()
    eraseText(heading=270, color=InventoryBg, rotation=(-90), height=30, width=30)
    # eraseText : seth to 270 to start by turtle going down.
    # width and height based on CONFIGS ZONE to adjust to the window.
    for i in range(len(PlayerItemList)): # First part of the loop to write Inventory : ...
        if i == 0:
            tt.pu()
            tt.goto(x + 30, y +10 - (i + 2) * pas)
            tt.pd()
            tt.color(Textcolor)
            tt.write("Inventory : ", move=False, align='left', font=('Verdana', 20, 'normal'))
        tt.pu()
        tt.goto(x + pas +30, y - (i + 3) * pas)  # Aesthetically : to "indent" items within Inventory.
        tt.pd()
        tt.write(PlayerItemList[i], move=False, align='left', font=('Arial', 16, 'normal'))


def writeBanner(message):
    """ Write at the top of the screen information about the player's most recent actions. """
    tt.pu()
    x, y = POINT_AFFICHAGE_ANNONCES
    x, y = x, y  # to recenter the text.-10 -30
    tt.goto(x, y)
    tt.pendown()
    eraseText(heading=90, color=BannerBg, rotation=90, height=30, width=480)
    # eraseText : seth to 90 to start by turtle going up.
    # width and height based on CONFIGS ZONE to adjust to the window.
    tt.pu()
    tt.goto(x + pas, y + pas)
    tt.pd()
    tt.color(Textcolor)
    tt.write(message, move=False, align='left', font=('Verdana', 14, 'normal'))


def eraseText(heading, color, rotation, height, width):
    """ Creates a blank frame to 'erase' text by hiding it. """
    tt.seth(heading)
    tt.color(color)
    tt.begin_fill()
    for i in range(4):  # To make a rectangle.
        if i % 2 == 0:
            tt.fd(pas * width)
            tt.rt(rotation)
        else:
            tt.fd(pas * height)
            tt.rt(rotation)
    tt.end_fill()
    tt.color(WRITING_COLOR)
    tt.seth(0)  # Make sure turtle faces the right direction.


# ----------------------------------------------------LEVEL_4------------------------------------------------------------------------#
""" The fourth level is to manage doors and to generate a pop-up window when the player needs to answer an question
 in order to get trough the door. 

"""


def poser_question(matrice, case, mouvement, dict_portes):
    """ When trying to get through a door, announce it, ask a question, if answered right, opens the door and announce
    it, else announce it. """
    res = False
    answer = tt.textinput("Question", dict_portes[case][0])
    if answer == dict_portes[case][1]:
        matrice[case[0]][case[1]] = 0
        res = True
        writeBanner("Correct, la porte s'ouvre...")
        dict_portes.pop(case)
        #print(dict_portes)
    else:
        writeBanner("FAUX, la porte demeure fermée")
    tt.listen()  # Because tt.textinput() interrupts tt.listen()

    return res


# ----------------------------------------------------BONUS------------------------------------------------------------------------#
""" This personalized bonus contains the code of the end-game animation.
"""
colors = [
         # blue shades
        (0.00, 0.00, 1.00), (0.05, 0.00, 1.00), (0.10, 0.00, 1.00), (0.15, 0.00, 1.00), (0.20, 0.00, 1.00),
        (0.25, 0.00, 1.00), (0.30, 0.00, 1.00), (0.35, 0.00, 1.00), (0.40, 0.00, 1.00), (0.45, 0.00, 1.00),
        (0.50, 0.00, 1.00), (0.55, 0.00, 1.00), (0.60, 0.00, 1.00), (0.65, 0.00, 1.00), (0.70, 0.00, 1.00),
        (0.75, 0.00, 1.00), (0.80, 0.00, 1.00), (0.85, 0.00, 1.00), (0.90, 0.00, 1.00), (0.95, 0.00, 1.00),

        # red shades
        (1.00, 0.00, 0.00), (1.00, 0.03, 0.00), (1.00, 0.05, 0.00), (1.00, 0.07, 0.00), (1.00, 0.10, 0.00),
        (1.00, 0.12, 0.00), (1.00, 0.15, 0.00), (1.00, 0.17, 0.00), (1.00, 0.20, 0.00), (1.00, 0.23, 0.00),
        (1.00, 0.25, 0.00), (1.00, 0.28, 0.00), (1.00, 0.30, 0.00), (1.00, 0.33, 0.00), (1.00, 0.35, 0.00),
        (1.00, 0.38, 0.00), (1.00, 0.40, 0.00), (1.00, 0.42, 0.00), (1.00, 0.45, 0.00), (1.00, 0.47, 0.00)
        # orange shades
    #    (1.00, 0.50, 0.00), (1.00, 0.53, 0.00), (1.00, 0.55, 0.00), (1.00, 0.57, 0.00), (1.00, 0.60, 0.00),
   #     (1.00, 0.62, 0.00), (1.00, 0.65, 0.00), (1.00, 0.68, 0.00), (1.00, 0.70, 0.00), (1.00, 0.72, 0.00),
  #      (1.00, 0.75, 0.00), (1.00, 0.78, 0.00), (1.00, 0.80, 0.00), (1.00, 0.82, 0.00), (1.00, 0.85, 0.00),
 #       (1.00, 0.88, 0.00), (1.00, 0.90, 0.00), (1.00, 0.93, 0.00), (1.00, 0.95, 0.00), (1.00, 0.97, 0.00),
        # yellow shades
   #     (1.00, 1.00, 0.00), (0.95, 1.00, 0.00), (0.90, 1.00, 0.00), (0.85, 1.00, 0.00), (0.80, 1.00, 0.00),
  #      (0.75, 1.00, 0.00), (0.70, 1.00, 0.00), (0.65, 1.00, 0.00), (0.60, 1.00, 0.00), (0.55, 1.00, 0.00),
 #       (0.50, 1.00, 0.00), (0.45, 1.00, 0.00), (0.40, 1.00, 0.00), (0.35, 1.00, 0.00), (0.30, 1.00, 0.00),
#        (0.25, 1.00, 0.00), (0.20, 1.00, 0.00), (0.15, 1.00, 0.00), (0.10, 1.00, 0.00), (0.05, 1.00, 0.00),
        # green shades
#        (0.00, 1.00, 0.00), (0.00, 0.95, 0.05), (0.00, 0.90, 0.10), (0.00, 0.85, 0.15), (0.00, 0.80, 0.20),
 #       (0.00, 0.75, 0.25), (0.00, 0.70, 0.30), (0.00, 0.65, 0.35), (0.00, 0.60, 0.40), (0.00, 0.55, 0.45),
  #      (0.00, 0.50, 0.50), (0.00, 0.45, 0.55), (0.00, 0.40, 0.60), (0.00, 0.35, 0.65), (0.00, 0.30, 0.70),
   #     (0.00, 0.25, 0.75), (0.00, 0.20, 0.80), (0.00, 0.15, 0.85), (0.00, 0.10, 0.90), (0.00, 0.05, 0.95),

    ]

def mandala():
    """ Repeats a shape x-times in a row with around 1 degree rotation using shades of color as to create a mandala."""
    tt.clear()  # Clear the window.
    tt.goto(0, 0)
    tt.hideturtle()
    tt.tracer(10, None)  # Speed of animation.
    tt.bgcolor('Black')
    c = 0
    x = 0
    while x < 1600:  # number of shapes to draw.
        idx = int(c)  # Starting color.
        color = colors[idx]
        tt.color(color)
        tt.forward(x)
        tt.right(119)
        x += 1
        c += 0.02
    # Text Message
    tt.pu()
    tt.goto(-250, 200)
    tt.pd()
    eraseText(90, "black", 90, 500, 40)
    tt.pu()
    tt.goto(0, 215)
    tt.pd()
    tt.color("White")
    tt.write(f"Bravo ! Le code est {CODE}", move=False, align='center', font=('Arial', 12, 'normal'))


# ----------------------------------------------------MAIN------------------------------------------------------------------------#
# flag = 1
if __name__ == "__main__":
    # Main code
    # if flag ==1:
    #     LVL = tt.textinput("Choose your level :", "Choose your level from 1 to 3 :")
    #     keysType = tt.textinput("Keys", "Select your keys : 1 for ZQSD/WASD and 0 for Arrows :3")
    #     flag = 0
    wn = tt.Screen()
    wn.setup(width=1.0, height=1.0, startx=None, starty=None)
    wn.title("Maze")
    tt.tracer(AnimationSpeed) # Speed of animation.
    tt.hideturtle()
    wn.bgpic("galaxy_bg.png")
    # ----------------------------------
    # keysType = 1
    if keysType == 0 :
        up = 'Up'
        down = 'Down'
        left = 'Left'
        right = 'Right'

    if keysType == 1 :
        up = 'w'
        down = 's'
        left = 'a'
        right = 'd'

    if LVL == 1:
        matrice = lire_matrice(fichier_plan1)  # Matrix containing the Maze plan
    elif LVL == 2:
        matrice = lire_matrice(fichier_plan2)
    else:
        matrice = lire_matrice(fichier_plan3)
    #print(matrice)
    #print(Hauteur, Largeur)
    #print(position)
    pas = calculer_pas(matrice)
    afficher_plan(matrice)  # Draws the whole Maze.
    # window.update()   #only if tt.tracer(0) is not activated.
    #--------------------CHOOSE LVL----------------------------------------
    #LVL = tt.textinput("Maze Setup", "Choose Level 1, 2 or 3")
    if LVL == 1:
        dict_objets = creer_dictionnaire_des_objets(fichier_objets1)
        dict_portes = creer_dictionnaire_des_objets(fichier_questions1)

    elif LVL == 2:
        dict_objets = creer_dictionnaire_des_objets(fichier_objets2)
        dict_portes = creer_dictionnaire_des_objets(fichier_questions2)

    elif LVL == 3:
        dict_objets = creer_dictionnaire_des_objets(fichier_objets3)
        dict_portes = creer_dictionnaire_des_objets(fichier_questions3)
    print(LVL)

    # ------------------------------------------------------------
    tt.listen()
    #if not Endscreen:
    tt.onkeypress(deplacer_haut, up)
    tt.onkeypress(deplacer_bas, down)
    tt.onkeypress(deplacer_gauche, left)
    tt.onkeypress(deplacer_droite, right)

    # ---------------------------------
    tt.mainloop()
    # ---------------------------------
#mandala()
