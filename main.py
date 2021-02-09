import pygame
from models import Game
from constants import DIMENSIONS

game = Game(pygame,DIMENSIONS["WIDTH"],DIMENSIONS["HEIGHT"],DIMENSIONS["ROWS"])
game.run()


