import pygame
import asyncio

pygame.init()

width,height = 800,600
screen = pygame.display.set_mode((width,height))

clock = pygame.time.Clock()

async def main():
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('green')
        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())

