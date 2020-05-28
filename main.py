import pygame
import random
import math
import os
import time
import json
from bird import Bird
from base import Base
from pipe import Pipe
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

fond = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bg.png")))

STAT_FONT = pygame.font.Font("assets/PixelGosub-ZaRz.ttf", 20)

def draw_window(win,bird,base,pipes,score,high_score):
    win.blit(fond,(0,0))
    for pipe in pipes:
        pipe.draw(win)
    text = STAT_FONT.render("Score: "+str(score),1,(255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    best_score = STAT_FONT.render("Best Score: "+high_score,1,(255,255,255))
    win.blit(best_score, (10,10))
    bird.draw(win)
    base.draw(win)
    pygame.display.update()

def main():
    run = True
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    bird = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(600)]
    score = 0
    with open("best_score.json") as out_file:
        data = json.load(out_file)
        high_score = str(data["bestscore"])


    while (run):
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                myData = {}
                myData["bestscore"] = int(high_score)
                with open("best_score.json", "w") as json_file:
                    json.dump(myData, json_file)
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        pipe_ind = 0


        bird.move()
        add_pipe = False
        rem = []

        if bird.y >= 700 or bird.y < 0:
            if int(score) > int(high_score):
                high_score = score
            main()

        for pipe in pipes:
            if (pipe.collide(bird)):
                if int(score) > int(high_score):
                    high_score = score
                main()
            if (not (pipe.passed) and (pipe.x < bird.x)):
                pipe.passed = True
                add_pipe = True

            if (pipe.x + pipe.PIPE_TOP.get_width() < 0):
                rem.append(pipe)
            pipe.move()

        if (add_pipe):
            pipes.append(Pipe(600))
            score = score + 1

        for r in rem:
            pipes.remove(r)

        base.move()
        draw_window(win,bird,base,pipes,score,high_score)

if __name__ == "__main__":
    main()