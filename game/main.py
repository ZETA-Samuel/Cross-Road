import pygame
import asyncio
from pytmx.util_pygame import load_pygame
from npc import NPC
from dialogue import DialogueBox
from boss import Boss

pygame.init()
pygame.mixer.init()

width,height = 800,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Cross Roads")

clock = pygame.time.Clock()

pygame.mixer.music.load("game/music/background.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

cat_sound = pygame.mixer.Sound("game/music/meow.mp3")
cat_sound.set_volume(1)

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

COIN_POSITION = (300,300)
PORTAL_POSITION = (700,300)

PORTAL_DESTINATION = (100,100)

coin_collected = False

coin_rect = pygame.Rect(COIN_POSITION[0] * zoom,COIN_POSITION[1] * zoom,20 * zoom,20 * zoom)

portal_rect = pygame.Rect(PORTAL_POSITION[0] * zoom,PORTAL_POSITION[1] * zoom, 40 * zoom, 60 * zoom)

BOSS_POSITION = (600,300)

boss = None
game_timer = 0

BOSS_SPAWN_TIME = 120

red_flash_timer = 0
RED_FLASH_DURATION = 0.2

PLAYER_START = (300,300)

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
        portrait_name="cat.png",
        position=(330,300),
        dialogue=[
            "...",
            "Hi my name is Squirk",
            "I am also lost",
            "This place has been turned into ruins by monsters",
            "We must fight them to retain our peace",
        ],
        zoom=zoom
        ),

    NPC(
        name="Wanderer",
        image_name="npc_1.png",
        portrait_name="npc_1.png",
        position=(330,350),
        dialogue=[
            "...",
            "This is a placeholder",
        ],
        zoom = zoom,
    ),

    NPC(
        name="Manjushree",
        image_name="npc_2.png",
        portrait_name="npc_2.png",
        position=(300,400),
        dialogue=[
            "...",
            "Hi, How are you?",
        ],
        zoom = zoom,
    )
]

dialogue_box = DialogueBox(screen)
INTERACTION_DISTANCE = 50 * zoom

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

def draw_coin():
    if coin_collected:
        return
    center = (coin_rect.centerx - camera_x,coin_rect.centery - camera_y)

    pygame.draw.circle(screen,(255,190,0),center,15 * zoom)
    pygame.draw.circle(screen, (255,235,80), center, 10 * zoom)
    pygame.draw.circle(screen, (180,110,0), center,5 * zoom)

def draw_portal():
    center = portal_rect.center

    pygame.draw.ellipse(screen,(100,30,200),(center[0] - 25 * zoom - camera_x,center[1] - 35 * zoom - camera_y, 50* zoom, 70 * zoom))

    pygame.draw.ellipse(screen,(30,150,255),(center[0] - 17 * zoom - camera_x, center[1] - 27 * zoom - camera_y, 34 * zoom, 54 * zoom))

    pygame.draw.ellipse(screen,(180,220,255),(center[0] - 8 * zoom - camera_x,center[1] - 18 * zoom - camera_y, 16 * zoom, 36 * zoom))

def draw_coin_status():
    font = pygame.font.Font(None,28)

    if coin_collected:
        message = "Portal key: COLLECTED"
        color = (100,255,100)
    else:
        message = "Find the golden coin!!!"
        color = (255,220,80)

    text = font.render(message,True,color)
    screen.blit(text, (15,15))


async def main():
    global camera_x,camera_y
    global player_x,player_y
    global current_direction
    global player_rect
    global coin_collected
    global boss, game_timer, red_flash_timer

    animation_index = 0
    animation_timer = 0

    running = True
    while running:

        dt = clock.tick(60) / 1000
        nearby_npc = get_nearest_npc()

        game_timer += dt

        if boss is None and game_timer >= BOSS_SPAWN_TIME:
            boss = Boss(BOSS_POSITION, zoom)

        portal_distance = pygame.Vector2(player_rect.center).distance_to(portal_rect.center)

        near_portal = portal_distance < 60 * zoom

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if dialogue_box.active:
                    pygame.mixer.music.stop()
                    if event.key == pygame.K_SPACE:
                        dialogue_box.advance()
                        cat_sound.play()
                    elif event.key == pygame.K_ESCAPE:
                        dialogue_box.close()
                        pygame.mixer.music.play(-1)
                else:
                    if event.key == pygame.K_e:
                        if near_portal:
                            if coin_collected:
                                player_x = PORTAL_DESTINATION[0] * zoom
                                player_y = PORTAL_DESTINATION[1] * zoom

                                player_rect.topleft = (round(player_x),round(player_y))

                                camera_x = 0
                                camera_y = 0

                                print("Portal entered!")

                            else:
                                print("You need the golden coin!")

                        elif nearby_npc:
                            dialogue_box.start(nearby_npc)

        if boss:

            blast = boss.update(dt)

            if blast:

                red_flash_timer = RED_FLASH_DURATION

                if boss.hits_player(player_rect):

                    print("PLAYER HIT! RESPAWNING...")

                    player_x = PLAYER_START[0] * zoom
                    player_y = PLAYER_START[1] * zoom

                    player_rect.topleft = (round(player_x),round(player_y))

                    camera_x = 0
                    camera_y = 0

        if red_flash_timer > 0:
            red_flash_timer = max(0, red_flash_timer - dt)

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

        if not coin_collected and player_rect.colliderect(coin_rect):
            coin_collected = True


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

        if not coin_collected:
            draw_coin()

        draw_portal()

        if boss:
            boss.draw(screen,camera_x,camera_y)

        draw_coin_status()

        for npc in npcs:
            npc.draw(screen,camera_x,camera_y)

        screen.blit(player_surf,(player_rect.x - camera_x,player_rect.y - camera_y))

        nearby_npc = get_nearest_npc()

        if nearby_npc and not dialogue_box.active:
            nearby_npc.draw_prompt(screen,camera_x,camera_y)

        dialogue_box.update(dt)
        
        dialogue_box.draw()

        if red_flash_timer > 0:

            red_overlay = pygame.Surface((width,height))
            red_overlay.fill((255,0,0))
            red_overlay.set_alpha(110)

            screen.blit(red_overlay, (0,0))

        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())

