import pygame
import random
import math
import os
import time
import json
import neat
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

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    Winner = p.run(main, 50)

def main(genomes, config):

    nets = []
    ge =[]
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    run = True
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappia !")
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

        if len(birds) > 0:
            if (len(pipes) > 1) and (birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()):
                    pipe_ind = 1
            else:
                run = False
                break
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness = ge[x].fitness + 0.1
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()


        bird.move()
        add_pipe = False
        rem = []

        for x,bird in enumerate(birds):
            if(bird.y + bird.img.get_height() >= 700) or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
                if int(score) > int(high_score):
                    high_score = score
                main(genomes, config)

        for pipe in pipes:
            for x,bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    if int(score) > int(high_score):
                        high_score = score
                    main(genomes, config)
                if (not (pipe.passed) and (pipe.x < bird.x)):
                    pipe.passed = True
                    add_pipe = True

            if (pipe.x + pipe.PIPE_TOP.get_width() < 0):
                rem.append(pipe)
            pipe.move()

        if (add_pipe):
            score = score + 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        base.move()
        draw_window(win,bird,base,pipes,score,high_score)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feed_forward.txt")
    run(config_path)
    main(genomes, config)