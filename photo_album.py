import os
import tkinter
from tkinter import filedialog

import pygame


def main():
    pygame.init()
    directory = './images/'
    files = os.listdir(directory)
    for file in files:
        if os.path.splitext(file)[1] != '.jpg':
            files.remove(file)


    window = pygame.display.set_mode((1000, 1000), pygame.RESIZABLE)
    i = 0
    image = pygame.image.load(directory + files[0])
    new_image = pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2))
    is_alive = True

    while is_alive:
        window.fill((255, 255, 255))
        window.blit(new_image, (10, 100))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                window = pygame.display.set_mode((event.w, event.w), pygame.RESIZABLE)
            elif event.type == pygame.QUIT:
                is_alive = False
                continue
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    i = (i + 1) % len(files)
                    image = pygame.image.load(directory + files[i])
                    new_image = pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2))
                elif event.key == pygame.K_LEFT:
                    i = (i - 1) % len(files)
                    image = pygame.image.load(directory + files[i])
                    new_image = pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2))
                elif event.key == pygame.K_c:
                    root = tkinter.Tk()
                    root.withdraw()
                    directory = filedialog.askdirectory() + '/'
                    print(directory)
                    files = os.listdir(directory)
                    for file in files:
                        if os.path.splitext(file)[1] != '.jpg':
                            files.remove(file)
                    image = pygame.image.load(directory + files[0])
                    new_image = pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2))
                    i = 0

    pygame.quit()


if __name__ == '__main__':
    main()