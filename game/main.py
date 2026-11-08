import pygame
import asyncio
from pytmx.util_pygame import load_pygame
from npc import NPC
from dialogue import DialogueBox

pygame.init()

width,height = 800,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Cross Roads")

clock = pygame.time.Clock()

# loading maps
zoom = 2
player_size = (25 * zoom, 25 * zoom)

animations = {
    "Up": [],
    "Down": [],
    "Left": [],
    "Right": []
}

for direction in animations:
    for frame in range(1,6):
        image = pygame.image.load(f"game/images/walk/{direction}/{frame}.png").convert_alpha()
        image = pygame.transform.scale(image,player_size)
        animations[direction].append(image)

current_direction = "Down"
player_surf = animations["Down"][0]
player_rect = player_surf.get_rect(topleft=(300,300))
player_speed = 100 * zoom

# animation variables
animation_index = 0
animation_timer = 0
animation_speed = 0.12


tmx_data = load_pygame("game/map.tmx")

map_width = tmx_data.width * tmx_data.tilewidth * zoom
map_height = tmx_data.height * tmx_data.tileheight * zoom

map_surface = pygame.Surface((map_width,map_height), pygame.SRCALPHA)
# Draw map layers
for layer in tmx_data.visible_layers:
    if hasattr(layer, "tiles"):
        for x,y,image in layer.tiles():
            print(x,y,image)
            scaled_image = pygame.transform.scale(image,(image.get_width() * zoom,image.get_height() * zoom))
            map_surface.blit(scaled_image,(x * tmx_data.tilewidth * zoom,y * tmx_data.tileheight * zoom))

collision_rects = []
collision_layer = tmx_data.get_layer_by_name("collision")

for x,y,image in collision_layer.tiles():

    rect = pygame.Rect(x * tmx_data.tilewidth * zoom, y * tmx_data.tileheight * zoom, tmx_data.tilewidth * zoom, tmx_data.tileheight * zoom)

    collision_rects.append(rect)

npcs = [

    NPC(
        name="Lost traveller",
        image_name="1.png",
        position=(330,300),
        dialogue=[
            "Hi my name is Squirk",
            "I am also lost",
            "This place has been turned into ruins by monsters",
            "We must fight them to retain our peace",
        ],
        zoom=zoom
        )

]

dialogue_box = DialogueBox(screen)
INTERACTION_DISTANCE = 100 * zoom

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

player_x = float(player_rect.x)
player_y = float(player_rect.y)

def get_nearest_npc():

    nearest = None
    closest_distance = INTERACTION_DISTANCE

    for npc in npcs:

        distance = pygame.Vector2(player_rect.center).distance_to(npc.rect.center)

        if distance < closest_distance:
            closest_distance = distance
            nearest = npc

        return nearest

async def main():
    global camera_x,camera_y
    global player_x,player_y
    global current_direction
    global player_rect

    animation_index = 0
    animation_timer = 0

    running = True
    while running:

        dt = clock.tick(60) / 1000
        nearby_npc = get_nearest_npc()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if dialogue_box.active:
                    if event.key == pygame.K_SPACE:
                        dialogue_box.advance()
                    elif event.key == pygame.K_ESCAPE:
                        dialogue_box.close()
                else:
                    if event.key == pygame.K_e and nearby_npc:
                        dialogue_box.start(nearby_npc)

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if not dialogue_box.active:

            if keys[pygame.K_UP]:
                dy = -1
            if keys[pygame.K_DOWN]:
                dy = 1
            if keys[pygame.K_LEFT]:
                dx = -1
            if keys[pygame.K_RIGHT]:
                dx = 1

        direction = pygame.Vector2(dx,dy)

        if direction.length() > 0:
            direction = direction.normalize()

        player_x += direction.x * player_speed * dt
        player_rect.x = round(player_x)

        for collision in collision_rects:
            if player_rect.colliderect(collision):
                if direction.x > 0:
                    player_rect.right = collision.left 
                elif direction.x < 0:
                    player_rect.left = collision.right
                player_x = player_rect.x

        player_y += direction.y * player_speed * dt
        player_rect.y = round(player_y)

        for collision in collision_rects:
            if player_rect.colliderect(collision):
                if direction.y > 0:
                    player_rect.bottom = collision.top 
                elif direction.y < 0:
                    player_rect.top = collision.bottom 
                player_y = player_rect.y

        if dx != 0 or dy != 0:
            if abs(dx) > abs(dy):
                if dx > 0:
                    current_direction = "Right"
                else:
                    current_direction = "Left"
            else:
                if dy > 0:
                    current_direction = "Down"
                else:
                    current_direction = "Up"

            animation_timer += dt

            if animation_timer >= animation_speed:
                animation_timer = 0
                animation_index = (animation_index + 1) % len(animations[current_direction])

        else:
            animation_index = 0
            animation_timer = 0

        player_surf = animations[current_direction][animation_index]

        old_center = player_rect.center
        player_rect = player_surf.get_rect(center=old_center)

        player_rect.topleft = (round(player_x), round(player_y))

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

        camera_x = max(0, min(camera_x, map_width - width))
        camera_y = max(0, min(camera_y,map_height - height))

        screen.fill('green')

        screen.blit(map_surface, (-camera_x,-camera_y))

        for npc in npcs:
            npc.draw(screen,camera_x,camera_y)

        screen.blit(player_surf,(player_rect.x - camera_x,player_rect.y - camera_y))

        nearby_npc = get_nearest_npc()

        if nearby_npc and not dialogue_box.active:
            nearby_npc.draw_prompt(screen,camera_x,camera_y)

        dialogue_box.update(dt)
        
        dialogue_box.draw()

        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())

