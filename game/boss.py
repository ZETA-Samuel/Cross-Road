import pygame
from pathlib import Path

class Boss:
    def __init__(self,world_position,zoom):
        self.zoom = zoom

        sheet_path = Path(__file__).resolve().parent / "images" / "boss" / "boss.png"
        self.sheet = pygame.image.load(str(sheet_path)).convert_alpha()

        self.frames = []

        for i in range(8):
            frame = self.sheet.subsurface(pygame.Rect(i * 100,0,100,100)).copy()

            frame = pygame.transform.scale(frame,(int(100 * zoom), int(100 * zoom)))

            self.frames.append(frame)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=world_position)

        self.state = "idle"
        self.idle_frames = [0,1]
        self.attack_frames = list(range(8))

        self.frame_index = 0
        self.animation_timer = 0

        self.idle_speed = 0.35
        self.attack_speed = 0.12

        self.attack_cooldown = 5
        self.attack_timer = 0

        self.blast_radius = 200 * zoom
        self.blast_radius_increase = 0 * zoom

        self.blast_triggered = False

    def update(self,dt):

        self.blast_triggered = False

        if self.state == "idle":

            self.attack_timer += dt
            self.animation_timer += dt

            if self.animation_timer >= self.idle_speed:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % 2

            if self.attack_timer >= self.attack_cooldown:
                self.state = "attack"
                self.frame_index = 0
                self.animation_timer = 0

        elif self.state == "attack":

            self.animation_timer += dt

            if self.animation_timer >= self.attack_speed:

                self.animation_timer = 0
                self.frame_index += 1

                if self.frame_index == 4:
                    self.blast_triggered = True

                    self.blast_radius += self.blast_radius_increase

                if self.frame_index >= 8:

                    self.state = "idle"
                    self.frame_index = 0
                    self.attack_timer = 0

        if self.state == "idle":
            self.image = self.frames[self.idle_frames[self.frame_index]]

        else:
            self.image = self.frames[self.attack_frames[min(self.frame_index,7)]]

        return self.blast_triggered

    def draw(self,screen,camera_x,camera_y):
        screen.blit(self.image,(self.rect.x - camera_x,self.rect.y - camera_y))

    def hits_player(self,player_rect):

        distance = pygame.Vector2(self.rect.center).distance_to(player_rect.center)

        return distance <= self.blast_radius
