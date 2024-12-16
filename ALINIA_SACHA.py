"""
Titre : Projet programation, Donjon.

Auteur : Sacha Alinia 

Matricule : 586702

Entrées :  - 'carte.txt' : carte du donjon avec la taille et les positions des monstres
           - 'messages.txt' : contient les messages du jeu
           - difficulte : niveau de difficulté (0 pour facile, 1 pour moyen, 2 pour difficile)
           - direction : mouvements du joueur (haut, bas, gauche, droite)

Sortie :  - Affichage du jeu Donjon dans le terminal
          - Messages relatifs aux actions et événements du jeu (combat, déplacement, victoire, défaite...)

But :  - Implémenter un jeu Donjon en Python. Le joueur explore une grille contenant des monstres, des pièges, des soins et des trésors.
       - Objectif : Collecter tous les trésors sans perdre tous ses points de vie.
"""


import random 

from random import seed
seed(10)

# Dictionnaire contenant les dégâts causés par chaque type de monstre
degats = {'A': 3, 'B': 6, 'C': 9,'D': 12,'E': 15,'F': 18,'G': 21,'H': 24,'I': 27,'J': 30}


# ------------------------------------------- Fonctions ---------------------------------------------


def lire_carte(fichier: str) -> dict:
    """
    Entrée : fichier (str) : Chemin du fichier contenant la carte du donjon
    Sortie : Dictionnaire avec la taille de la carte et les positions des monstres
    But : Lire le fichier pour extraire les données nécessaires à l'initialisation du jeu
    """
    carte = {}

    with open(fichier) as file:
        carte_lst = file.readlines()

        for line in carte_lst:
            line = line.strip()

            if "Taille" in line:    # Lecture de la taille de la carte
                carte["Taille"] = int(line.split(":")[1])
            
            elif "Monstre" in line:     # Lecture des positions des monstres
                type_monstre = line.split(":")[0].split()[1]
                positions = line.split(":")[1].split(";")
                coord_final = []
                
                for pos in positions:
                    coord_tuple = tuple(map(int, pos.strip().split(',')))   # Conversion des coordonnées en tuple
                    coord_final.append(coord_tuple) 
                carte[type_monstre] = coord_final   # Ajout des coordonnées au dictionnaire
    return carte


def grille_string(grille) -> str :
    """
    Entrée : Grille du jeu sous forme de liste de listes
    Sortie : Représentation textuelle de la grille
    But : Générer un affichage visuel clair de la grille du jeu
    """
    ajout_cadre = 3
    formule_cadre = 2

    print("-" * (len(grille) * formule_cadre + ajout_cadre))

    for x in range(len(grille)):
        print('|', end="")
        for y in range(len(grille)):
            print(f" {grille[x][y]}", end="")
        print(' |')
    print("-" * (len(grille) * formule_cadre + ajout_cadre))


def afficher_grille(grille, vie: int, tresors_restants: int) -> None:
    """
    Entrée : - Grille actuelle du jeu
             - Points de vie du joueur
             - Nombre de trésors restant à collecter
    Sortie : Affiche les informations dans la console
    But : Visualiser l'état actuel du jeu, incluant la grille et les informations essentielles
    """
    grille_string(grille)    #Affichage de la grille
    print(f"Vie(s) : {vie}, Trésor(s) restant(s) : {tresors_restants}")


def deplacer_personnage(direction, position_personnage, grille, vie) -> tuple:
    """
    Entrée : - Direction choisie par le joueur ('h', 'b', 'g', 'd')
             - Position actuelle du joueur
             - Grille de jeu
             - Points de vie du joueur
    Sortie : Nouvelle position du joueur, grille mise à jour, et points de vie restants
    But : Gérer le déplacement du joueur, les interactions avec les cases, et les conséquences (perte de vie, gain)
    """
    (x, y) = position_personnage

    # Calcul de la nouvelle position en fonction de la direction choisie
    if direction == 'h':
        nouvelle_position = (x - 1, y)
    elif direction == 'b':
        nouvelle_position = (x + 1, y)
    elif direction == 'g':
        nouvelle_position = (x, y - 1)
    elif direction == 'd':
        nouvelle_position = (x, y + 1)

    # Vérification si le déplacement reste dans les limites de la grille    
    if 0 <= nouvelle_position[0] < len(grille) and 0 <= nouvelle_position[1] < len(grille[0]):
        element = grille[nouvelle_position[0]][nouvelle_position[1]]

        # Interagir avec le contenu de la case avant de déplacer le joueur
        if element in degats.keys():    # Rencontre un monstre
            print(f"Vous rencontrez un monstre {element} ! Vous perdez {degats[element]} points de vie.")
            vie -= degats[element]
            # La case devient vide après l'interaction
            grille[nouvelle_position[0]][nouvelle_position[1]] = '*'
        elif element == 'T':    # Rencontre un trésor
            pass
        elif element == '+':    # Rencontre une trousse de secours
            vie += 5 

        # Mettre à jour la grille : on efface d'abord la position actuelle du joueur
        grille[x][y] = '*'  # Remplacer l'ancienne position par une case vide
        # Ensuite, on place le joueur à la nouvelle position
        grille[nouvelle_position[0]][nouvelle_position[1]] = "P"  # Le joueur prend sa nouvelle position

        # Retourner la nouvelle position et la grille mise à jour
        return nouvelle_position, grille, vie
    else:
        # Si le déplacement est hors limites, on ne fait rien
        return position_personnage, grille, vie    # Position inchangée si le déplacement est invalide


def deplacer_monstres(grille, carte, degats):
    """
    Entrée : Grille actuelle, dictionnaire de la carte et dégats des monstres
    Sortie : Dégâts infligés au joueur
    But : Déplacer les monstres de manière aléatoire et gérer les interactions avec le joueur
    """
    damage = 0
    for elem in carte:
        if elem != "Taille":    # Ignorer la clé "Taille" dans la carte
            for i, coord in enumerate(carte[elem]):
                x, y = coord[0], coord[1]
                monstre = grille[x][y]
                direction = random.choice(['h', 'b', 'g', 'd'])    # Choix aléatoire de la direction
                nouvelle_position = (x, y)
                
                # Calcul de la nouvelle position
                if direction == 'h':
                    nouvelle_position = (x - 1, y)  
                elif direction == 'b':
                    nouvelle_position = (x + 1, y)
                elif direction == 'g':
                    nouvelle_position = (x, y - 1)  
                elif direction == 'd':
                    nouvelle_position = (x, y + 1)
                
                # Si la nouvelle position est valide et disponible
                if (0 <= nouvelle_position[0] < len(grille) and 0 <= nouvelle_position[1] < len(grille) 
                    and (grille[nouvelle_position[0]][nouvelle_position[1]] == '*' 
                    or grille[nouvelle_position[0]][nouvelle_position[1]] == 'P')):

                    carte[elem][i] = nouvelle_position     # Mise à jour de la position dans la carte
                    grille[x][y] = '*'     # L'ancienne position est maintenant vide
    
                    if grille[nouvelle_position[0]][nouvelle_position[1]] == '*':
                        grille[nouvelle_position[0]][nouvelle_position[1]] = monstre    # Déplacement réussi
                    else:
                        grille[nouvelle_position[0]][nouvelle_position[1]] = 'P'    # Le joueur est attaqué
                        damage += degats[monstre]     # Dégâts infligés au joueur
    return damage


def tresors(grille, nombre_tresors):
    """
    Entrée : - Grille initiale vide
             - Nombre de trésors à ajouter
    Sortie : Grille avec les trésors ajoutés
    But : Placer les trésors sur des cases aléatoires de la grille
    """
    taille = len(grille)

    for i in range(nombre_tresors):
        end = False
        while not end:
            x = random.randint(0, taille - 1)   # Génération de coordonnées aléatoires
            y = random.randint(0, taille -1)

            if grille[x][y] == '*':    # Vérification si la case est vide
                grille[x][y] = 'T'    # Placement d'un trésor
                end = True    # Sortir de la boucle
    return grille


def nbr_tresors(grille):
    """
    Entrée : Grille actuelle du jeu 
    Sortie : Nombre de trésors restants sur la grille
    But : Compter le nombre de trésors non encore collectés
    """
    count = 0   # Initialisation du compteur
    for i in grille:
        count += i.count('T')   # Comptage des cases contenant un trésor
    return count


def ajouter_monstre(grille):
    """
    Entrée : Grille actuelle du jeu sous forme de liste de listes
    Sortie : La grille est modifiée en place, avec un nouveau monstre ajouté sur une case vide
    But : Ajouter un monstre aléatoire à une position disponible dans la grille
          en choisissant aléatoirement le type de monstre et sa position
    """
    x, y = random.randint(0, len(grille)-1), random.randint(0, len(grille)- 1)     # Génération de coordonnées aléatoires
    while grille[x][y] != '*':     # Vérification si la case est vide
        x, y = random.randint(0, len(grille)- 1), random.randint(0, len(grille)- 1)

    monstre = random.choice(list(degats.keys()))    # Choix aléatoire d'un type de monstre
    grille[x][y] = monstre     # Placement du monstre sur la grille
    print(f"Nouveau monstre {monstre} ajouté à ({x}, {y}) avec {degats[monstre]} dégâts.")


def ajouter_trousse_secours(grille):
    """
    Entrée : Grille actuelle du jeu sous forme de liste de listes
    Sortie : La grille est modifiée en place, avec une trousse de secours ajoutée sur une case vide
    But : Ajouter une trousse de secours à une position aléatoire disponible dans la grille
    """
    x, y = random.randint(0, len(grille)- 1), random.randint(0, len(grille)-1)   # Génération de coordonnées aléatoires
    while grille[x][y] != '*':     # Vérification si la case est vide
        x, y = random.randint(0, len(grille)- 1), random.randint(0, len(grille)- 1)

    grille[x][y] = '+'    # Placement de la trousse de secours


# ----------------------- Main ------------------------  


def main():
    print("### Nouvelle partie initiée ! ###\nBienvenue dans l'exploration de donjon !\n")

    # Demande à l'utilisateur de choisir la difficulté
    difficulte = input("Choisissez la difficulté (0: Facile, 1: Moyen, 2: Difficile) : ").strip()
    
    # Validation de l'entrée de l'utilisateur pour la difficulté
    while difficulte not in ['0', '1', '2']:
        print("Erreur : Choisissez une difficulté valide.")
        difficulte = input("Choisissez la difficulté (0: Facile, 1: Moyen, 2: Difficile) : ").strip()

    fichier_carte = 'carte.txt'     # Chemin vers le fichier contenant la carte du donjon
    carte = lire_carte(fichier_carte)    # Lecture du fichier pour obtenir la carte
    taille = carte["Taille"]    # Récupération de la taille de la grille
    print(carte)    # Affichage du contenu de la carte lue (optionnel)

    # Initialisation des points de vie et du nombre de trésors en fonction de la difficulté
    if difficulte == '0':   # Facile
        vie = 100
        tresors_restants = 3    # Moyen
    elif difficulte == '1':
        vie = 20
        tresors_restants = 6    # Difficile
    elif difficulte == '2':
        vie = 10
        tresors_restants = 10

    # Création de la grille vide de taille 'taille x taille'
    grille = []
    
    for i in range(taille):    # Initialisation des lignes de la grille
        ligne = []
        for j in range(taille):    # Initialisation des colonnes de la grille
            ligne.append('*')
        grille.append(ligne)
    
    # Placement des trésors sur la grille
    grille = tresors(grille, tresors_restants)

    # Placement des monstres sur la grille en fonction des positions dans le fichier 'carte.txt'
    for monstre, positions in carte.items():
        if monstre != "Taille":
            nb_monstres = len(positions)

            # Affichage du nombre de monstres et de leur emplacement
            if nb_monstres == 1:
                print(f"{nb_monstres} monstre {monstre} avec {degats[monstre]} est ajouté à l'emplacement {positions}")
            else:
                print(f"{nb_monstres} monstres {monstre} avec {degats[monstre]} sont ajoutés à l'emplacement {positions}")

            for (x, y) in positions:    # Placement des monstres sur la grille
                grille[x][y] = monstre

    # Initialisation de la position du personnage à (0, 0) et marquage de cette position dans la grille
    position_personnage = (0, 0)
    grille[0][0] = 'P'  

    # Si la difficulté est difficile (niveau 2), ajout de pièges
    if difficulte == '2':
        tour = 0
        piege = []

        # Placement de 3 pièges aléatoires sur la grille
        for i in range(3):
            x = random.randint(0, taille - 1)   # Génération de coordonnées aléatoires
            y = random.randint(0, taille - 1)
            piege.append((x, y))    # Ajout des pièges à la liste


    # Boucle principale du jeu qui continue tant que le joueur a des vies et qu'il reste des trésors
    while vie > 0 and tresors_restants > 0:
        afficher_grille(grille, vie, tresors_restants)  # Affichage de l'état actuel du jeu
        direction = input("Déplacez-vous (h: haut, b: bas, g: gauche, d: droite) : ")
        
        # Validation de la direction entrée
        while direction not in ['h', 'b', 'g', 'd']:
            print("Seulement 4 déplacements possibles (h: haut, b: bas, g: gauche, d: droite) : ")
            direction = input("Entrez une direction (h: haut, b: bas, g: gauche, d: droite) : ")
        
        # Mise à jour de la position du personnage après le déplacement
        position_personnage, grille, vie = deplacer_personnage(direction, position_personnage, grille, vie)
        
        # Mise à jour du nombre de trésors restants
        tresors_restants = nbr_tresors(grille)     

        # Si la difficulté est moyenne (niveau 1), les monstres se déplacent et attaquent
        if difficulte == '1':
            monstre_attaquant = deplacer_monstres(grille, carte, degats)
            if monstre_attaquant != None:   # Si un monstre attaque, réduire les points de vie
                vie -= monstre_attaquant 

        # Si la difficulté est difficile (niveau 2), les monstres se déplacent et attaquent,
        # et des monstres ou trousses de secours peuvent être ajoutés à chaque tour
        if difficulte == '2':
            monstre_attaquant = deplacer_monstres(grille, carte, degats)
            tour += 1
            
            # Ajout d'un monstre tous les 5 tours
            if tour % 5 == 0:   
                ajouter_monstre(grille)
            # Ajout d'une trousse de secours tous les 3 tours
            elif tour % 3 == 0:
                ajouter_trousse_secours(grille)
            # Si un monstre attaque, réduire les points de vie
            elif monstre_attaquant != None:
                vie -= monstre_attaquant 

            # Vérification de la proximité des pièges
            pos_piege = False
            for x, y in piege:
                if abs(position_personnage[0] - x) <= 1 and abs(position_personnage[1] - y) <= 1:
                    pos_piege = True
                    break
            
            # Avertissement si un piège est proche
            if pos_piege:
                print("Avertissement : un piège est à proximité !")

            # Si le personnage se trouve sur un piège, il meurt
            if position_personnage in piege:
                vie = 0
                break
    # Si le joueur meurt, afficher un message de fin de jeu
    if vie <= 0:
        print("Vous êtes mort... Game over !")
    # Si tous les trésors sont collectés, afficher un message de victoire
    elif tresors_restants == 0:
        print("Félicitations, vous avez collecté tous les trésors !")


# ------------------------------------------------- Corps du code -------------------------------------------------

if __name__ == "__main__":
    main()