import pygame
import asyncio
from pytmx.util_pygame import load_pygame

pygame.init()

width,height = 800,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Cross Roads")

clock = pygame.time.Clock()

# loading maps
tmx_data = load_pygame("game/map.tmx")

map_width = tmx_data.width * tmx_data.tilewidth
map_height = tmx_data.height * tmx_data.tileheight

map_surface = pygame.Surface((map_width,map_height), pygame.SRCALPHA)

# Draw map layers
for layer in tmx_data.visible_layers:
    if hasattr(layer, "tiles"):
        for x,y,image in layer.tiles():

            map_surface.blit(image,(x*tmx_data.tilewidth,y*tmx_data.tileheight))


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
#                     self.player_rect.centery -= 10
#                 elif event.key == pygame.K_DOWN:
#                     self.player_rect.centery += 10
#                 if event.key == pygame.K_LEFT:
#                     self.player_rect.centerx -= 10
#                 elif event.key == pygame.K_RIGHT:
#                     self.player_rect.centerx += 10



# # loading images and making rect
# animation = {
#     'up':[],
#     'down':[],
#     'left':[]
# }
# animation_index = 0

# player = pygame.aprite.GroupSingle()
# player.add(Player())

# camera settings
camera_x = 0
camera_y = 0

CAMERA_MARGIN_X = 300
CAMERA_MARGIN_Y = 200


player_surf = pygame.image.load('game/images/walk/Down/1.png')
player_surf = pygame.transform.scale(player_surf,(100,100))
player_rect = player_surf.get_rect(center=(400,300))
player_speed = 100


async def main():
    global camera_x,camera_y
    
    running = True
    while running:

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_rect.centery -= player_speed * dt
        if keys[pygame.K_DOWN]:
            player_rect.centery += player_speed * dt
        if keys[pygame.K_LEFT]:
            player_rect.centerx -= player_speed * dt
        if keys[pygame.K_RIGHT]:
            player_rect.centerx += player_speed * dt

        screen_player_x = player_rect.centerx - camera_x
        screen_player_y = player_rect.centery - camera_y

        # Horizontal camera movement

        if screen_player_x > width - CAMERA_MARGIN_X:
            camera_x = player_rect.centerx - (width - CAMERA_MARGIN_X)

        elif screen_player_x < CAMERA_MARGIN_X:
            camera_x = player_rect.centerx - CAMERA_MARGIN_X

        # Vertical camera movement

        if screen_player_y > height - CAMERA_MARGIN_Y:
            camera_y = player_rect.centery - (height - CAMERA_MARGIN_Y)

        elif screen_player_y < CAMERA_MARGIN_Y:
            camera_y = player_rect.centery - CAMERA_MARGIN_Y


        screen.fill('green')

        screen.blit(map_surface, (-camera_x,-camera_y))

        screen.blit(player_surf,(player_rect.centerx - camera_x,player_rect.centery - camera_y))

        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())

