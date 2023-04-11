import pygame
import time
from pygame.locals import *
import os
import random

print(os.getcwd())

"""
En résumé, cette ligne de code sert à vérifier si le script est exécuté en tant que
programme principal et à initialiser le module pygame dans ce cas. Cela permet d'assurer que le 
code fonctionne correctement en exécutant toutes les étapes nécessaires avant l'exécution du reste 
du code.
"""

SIZE = 40
BACKGROUND_COLOR = (255, 192, 203)


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("C:/Users/guela/Documents/ProjetPythonSnake/ProjetSnakeHakim/Jeu_Serpent/ressources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = [SIZE] * 3
        self.y = [SIZE] * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x[0], self.y[0]))
        pygame.display.flip()
        
    def move(self):
        self.x[0] = random.randint(0,24)*SIZE #attention a ne poas mettre de valeur trop grande faire moin 
        self.y[0] = random.randint(0,19)*SIZE #1 indexe pour pas qu il place la pomme hors de l ecran


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.image = pygame.image.load("C:/Users/guela/Documents/ProjetPythonSnake/ProjetSnakeHakim/Jeu_Serpent/ressources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = "down"
        
    def increase_length(self):
        self.length+=1
        self.x.append(-1) #permet d ajouter un element a la fin de la liste d ou le (-1)
        self.y.append(-1)
        
    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            """
            cette boucle permet pour chaque deplacement de la tete du serpent quelque soit le nombre de bloc
            suivant, de combler les trous c est a dire qu a chaque mouvement de la tete chaque bloc recupere
            la position-1 de son succeseur en parcourant toute la taille des blocs additionner
            """
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE

        self.draw()

    def draw(self):
        self.parent_screen.fill((BACKGROUND_COLOR))

        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game for HAKIM")
        
        pygame.mixer.init()
        self.play_background_music()
        
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 15)  # c est ici avec le 3eme parametre qu on change le nombre de bloc
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
 
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False  
    
    def play_background_music(self):
        pygame.mixer.music.load("C:/Users/guela/Documents/ProjetPythonSnake/ProjetSnakeHakim/Jeu_Serpent/ressources/bg_music_1.mp3") 
        pygame.mixer.music.play()

    def play_sound(self, sound_name):
        if sound_name == "ding":
            sound = pygame.mixer.Sound("C:/Users/guela/Documents/ProjetPythonSnake/ProjetSnakeHakim/Jeu_Serpent/ressources/1_snake_game_resources_ding.mp3")
        elif sound_name == "crash":
            sound = pygame.mixer.Sound("C:/Users/guela/Documents/ProjetPythonSnake/ProjetSnakeHakim/Jeu_Serpent/ressources/1_snake_game_resources_crash (1).mp3")
            
        pygame.mixer.Sound.play(sound) 
        
    def render_background(self):
        
        bg = pygame.image.load("C:/Users/guela/Documents/ProjetPythonSnake/ProjetSnakeHakim/Jeu_Serpent/ressources/background.jpg")
        self.surface.blit(bg, (0,0))
    
    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        
        #colision du serpent avec la pomme
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x[0], self.apple.y[0]):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()
            
        #collision du serpent avec lui meme 
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                print("game over")
                raise "game over" 

    
    def display_score(self):
        font = pygame.font.SysFont("arial",30)
        score = font.render(f"Score: {self.snake.length}" , True, (255, 255, 255)) #le f de format permet de changer dynamiquement les valeur des attribut
        self.surface.blit(score, (800,10))
    
    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont("arial",30)
        line1 = font.render(f"Game is over ! Your score is  {self.snake.length}" , True, (255, 255, 255))
        self.surface.blit(line1, (200,300)) #c est le milieu de l ecran
        line2 = font.render("To play ask you teacher HAKIM and press Enter.To exit press Return ", True, (255, 255, 255))
        self.surface.blit(line2, (10,350))
        
        pygame.display.flip()
        
        pygame.mixer.music.pause()
     
    def reset(self):
        self.snake = Snake(self.surface, 5)  # c est ici avec le 3eme parametre qu on change le nombre de bloc
        self.apple = Apple(self.surface)
               
    def run(self):
        running = True
        pause = False

        """
        faire tres attention meme les commentaire doivent etre indexe avec la bonne indentation si il est dans une
        condition j'ai pas passe 15 minutes a debugger la !!! pour ce commentaire
        on declare une variable booleene a running
        on creer une boucle infinie dans laquel on va utilise des conditions de 
        sortie pour le joueur avec des action KEYDOWN    
        """

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:  # bien faire attention ici KEYDOWN n est pas la fleche du bas mais plutot un attribut qui permet de verifier si l action est de nature "pression de touche clavier"
                    if event.key == K_ESCAPE:
                        running = False
                        
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                        
                    if not pause:    
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False
            
            try:
                if not pause:    
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)


if __name__ == '__main__':
    game = Game()
    game.run()
    
    
    
"""
Probleme recurent:
dans ce code j ai rencontre enormement de probleme du a la compatibilite du type de data exemple:beaucoup
d erreur ou on attendez un type de donne genre list mais qu on avait un entier et cela casse le code etc 
"""
