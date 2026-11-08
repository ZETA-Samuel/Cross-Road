import pygame

class DialogueBox:

    def __init__(self,screen):

        self.screen = screen

        self.font = pygame.font.Font(None,28)
        self.name_font = pygame.font.Font(None,34)

        self.active = False
        self.npc = None
        self.line_index = 0

        self.panel = pygame.Rect(25,420,750,155)

        self.visible_chars = 0
        self.typing_speed = 35
        self.typing_timer = 0

        self.portraits = {
            "cat.png":   pygame.image.load("game/images/Portraits/cat.png").convert_alpha(),
            "npc_1.png":   pygame.image.load("game/images/Portraits/npc_1.png").convert_alpha(),
            "npc_2.png": pygame.image.load("game/images/Portraits/npc_2.png").convert_alpha()

        }

        for name in self.portraits:
            self.portraits[name] = pygame.transform.scale(self.portraits[name],(100,85))


    def start(self,npc):
        self.npc = npc
        self.line_index = 0
        self.active = True

        self.visible_chars = 0
        self.typing_timer = 0

    def advance(self):
        message = self.npc.dialogue[self.line_index]

        if self.visible_chars < len(message):
            self.visible_chars = len(message)
            return

        if self.line_index < len(self.npc.dialogue) - 1:
            self.line_index += 1
            self.visible_chars = 0
            self.typing_timer = 0
        else:
            self.close()

    def update(self,dt):

        if not self.active:
            return

        message = self.npc.dialogue[self.line_index]

        if self.visible_chars < len(message):
            self.typing_timer += dt

            if self.typing_timer >= 1 / self.typing_speed:
                self.visible_chars += 1
                self.typing_timer = 0

    def close(self):

        self.active = False
        self.npc = None
        self.line_index = 0

    def draw(self):

        if not self.active:
            return

        pygame.draw.rect(self.screen,(25,25,35),self.panel,border_radius=12)

        portrait = self.portraits.get(self.npc.portrait_name)

        if portrait:
            self.screen.blit(portrait,(self.panel.x + 20, self.panel.y + 35))

        # NPC name
        name_text = self.name_font.render(self.npc.name,True,(255,255,100))

        self.screen.blit(name_text,(self.panel.x + 140,self.panel.y + 15))

        message = self.npc.dialogue[self.line_index][:self.visible_chars]

        words = message.split()
        lines = []
        current_line = ""

        max_width = self.panel.width - 160

        for word in words:

            test = current_line + word + " "

            if self.font.size(test)[0] <= max_width:
                current_line = test

            else:
                lines.append(current_line)
                current_line = word + " "

        if current_line:
            lines.append(current_line)

        for i,line in enumerate(lines):

            text = self.font.render(line,True,"white")

            self.screen.blit(text,(self.panel.x + 140, self.panel.y + 65 + i * 27))
            

        hint = self.font.render("SPACE:Continue   ESC:Exit",True,(180,180,180))

        self.screen.blit(hint,(self.panel.right - hint.get_width() - 20,self.panel.bottom - 30))

