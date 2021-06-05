import pygame
import os


class Settings():
    width = 1280
    height = 720
    fps = 60
    title = "Resources"
    file_path = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(file_path, "resources")

    @staticmethod
    def get_dim():
        return (Settings.width, Settings.height)

BOMB_IMAGE = []
BOMB_IMAGE.append(pygame.image.load(os.path.join(Settings.images_path, "mine2.png")))