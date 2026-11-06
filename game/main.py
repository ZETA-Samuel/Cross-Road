import pygame
import asyncio

pygame.init()

width,height = 800,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Cross Roads")

clock = pygame.time.Clock()

# # Player Class
# class Player(pygame.sprite.Sprite):
#     def __init__(self,pos):
#         super().__init__()
#         # up animation
#         self.player_up_1 = pygame.image.load('images/walk/Up/1.png').convert_alpha()
#         self.player_up_2 = pygame.image.load('images/walk/Up/2.png').convert_alpha()
#         self.player_up_3 = pygame.image.load('images/walk/Up/3.png').convert_alpha()
#         self.player_up_4 = pygame.image.load('images/walk/Up/4.png').convert_alpha()
#         self.player_up_5 = pygame.image.load('images/walk/Up/5.png').convert_alpha()
#         self.player_up = [self.player_up_1,self.player_up_2,self.player_up_3,self.player_up_4,self.player_up_5]
#         # down animation
#         self.player_down_1 = pygame.image.load('images/walk/Down/1.png').convert_alpha()
#         self.player_down_2 = pygame.image.load('images/walk/Down/2.png').convert_alpha()
#         self.player_down_3 = pygame.image.load('images/walk/Down/3.png').convert_alpha()
#         self.player_down_4 = pygame.image.load('images/walk/Down/4.png').convert_alpha()
#         self.player_down_5 = pygame.image.load('images/walk/Down/5.png').convert_alpha()
#         self.player_down = [self.player_down_1,self.player_down_2,self.player_down_3,self.player_down_4,self.player_down_5]
#         # left animation
#         self.player_left_1 = pygame.image.load('images/walk/Left/1.png').convert_alpha()
#         self.player_left_2 = pygame.image.load('images/walk/Left/2.png').convert_alpha()
#         self.player_left_3 = pygame.image.load('images/walk/Left/3.png').convert_alpha()
#         self.player_left_4 = pygame.image.load('images/walk/Left/4.png').convert_alpha()
#         self.player_left_5 = pygame.image.load('images/walk/Left/5.png').convert_alpha()
#         self.player_left = [self.player_left_1,self.player_left_2,self.player_left_3,self.player_left_4,self.player_left_5]

#         self.player_index = 0

#         self.player_surf = self.player_down[self.player_index]
#         self.player_rect = self.player_surf.get_rect(center=(pos))

#     def animate(self):
#         for event in pygame.event.get():
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP:
#                     self.player_rect.y -= 10
#                 elif event.key == pygame.K_DOWN:
#                     self.player_rect.y += 10
#                 if event.key == pygame.K_LEFT:
#                     self.player_rect.x -= 10
#                 elif event.key == pygame.K_RIGHT:
#                     self.player_rect.x += 10



# # loading images and making rect
# animation = {
#     'up':[],
#     'down':[],
#     'left':[]
# }
# animation_index = 0

# player = pygame.aprite.GroupSingle()
# player.add(Player())

player_surf = pygame.image.load('game/images/walk/Down/1.png')
player_surf = pygame.transform.scale(player_surf,(100,100))
player_rect = player_surf.get_rect(center=(400,300))



async def main():
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_rect.y -= 10
        elif keys[pygame.K_DOWN]:
            player_rect.y += 10
        if keys[pygame.K_LEFT]:
            player_rect.x -= 10
        elif keys[pygame.K_RIGHT]:
            player_rect.x += 10

        screen.fill('green')

        screen.blit(player_surf,player_rect)

        clock.tick(60)

        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())

