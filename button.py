import pygame

class Button():
    def __init__(self, ai_settings, screen, msg) -> None:
        ''' Initializes button attributes '''
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Button dimensions and config
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build button's rect obj and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Preparing button message - only once 
        self.prep_msg(msg)
        
    def prep_msg(self, msg):
        ''' Turn msg into a rendered image and center text on the button '''
        self.msg_img = self.font.render(msg, True, self.text_color, 
                                        self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def draw_button(self):
        ''' Draw blank button and then draw message '''
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_img, self.msg_img_rect)


