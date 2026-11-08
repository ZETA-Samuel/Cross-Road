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

    def start(self,npc):
        self.npc = npc
        self.line_index = 0
        self.active = True

    def advance(self):

        if self.line_index < len(self.npc.dialogue) - 1:
            self.line_index += 1
        else:
            self.close()

    def close(self):

        self.active = False
        self.npc = None
        self.line_index = 0

    def draw(self):

        if not self.active:
            return

        pygame.draw.rect(self.screen,(25,25,35),self.panel,border_radius=12)

        pygame.draw.rect(self.screen,(220,220,220),self.panel,3,border_radius=12)

        # NPC name
        name_text = self.name_font.render(self.npc.name,True,(255,220,100))

        self.screen.blit(name_text,(self.panel.x + 20,self.panel.y + 15))

        message = self.npc.dialogue[self.line_index]

        words = message.split()
        lines = []
        current_line = ""

        max_width = self.panel.width - 40

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

            self.screen.blit(text,(self.panel.x + 20, self.panel.y + 65 + i * 27))

        hint = self.font.render("SPACE:Continue   ESC:Exit",True,(180,180,180))

        self.screen.blit(hint,(self.panel.right - hint.get_width() - 20,self.panel.bottom - 30))

