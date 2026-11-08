import pygame
import os

class NPC:
    def __init__(self,name,image_name,position,dialogue,zoom):
        self.name = name
        self.dialogue = dialogue

        image_path = os.path.join("game","images","npc",image_name)

        self.image = pygame.image.load(image_path).convert_alpha()

        original_width,original_height = self.image.get_size()

        self.image = pygame.transform.scale(self.image, (original_width * zoom * 1.25, original_height * zoom * 1.25))

        world_position = (position[0] * zoom,position[1] * zoom)

        self.rect = self.image.get_rect(midbottom=world_position)

        self.font = pygame.font.Font(None, 24)

    def draw(self,screen,camera_x,camera_y):
        screen.blit(self.image,(self.rect.x - camera_x, self.rect.y - camera_y))

    def draw_prompt(self,screen,camera_x,camera_y):
        text = self.font.render("E - Talk", True, "white")

        prompt_rect = text.get_rect(center=(self.rect.centerx - camera_x,self.rect.top - camera_y - 15))

        background = prompt_rect.inflate(14,8)

        pygame.draw.rect(screen,(30,30,30),background,border_radius=5)

        screen.blit(text,prompt_rect)