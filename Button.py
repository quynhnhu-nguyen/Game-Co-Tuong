import pygame

class Button():
    def __init__(self, screen, msg, left, top):
        # Initialize button property
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 150, 50
        self.button_color = (72, 61, 139)  # Object Color
        self.text_color = (255, 255, 255)  # Text Color
        pygame.font.init()
        self.font = pygame.font.SysFont('kaiti', 20)  # Set font and size

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.left = left
        self.top = top

        self.deal_msg(msg)  # Render images

    def deal_msg(self, msg):
        # Render converts the text stored in the message to an image
        self.msg_img = self.font.render(msg, True, self.text_color, self.button_color)  
        self.msg_img_rect = self.msg_img.get_rect()
        # Set the center property of the rect to the center property of the button
        self.msg_img_rect.center = self.rect.center

    def draw_button(self):
        # Draw image on the screen
        self.screen.blit(self.msg_img, (self.left,self.top))

    def is_click(self):
        point_x, point_y = pygame.mouse.get_pos()
        x = self.left
        y = self.top
        w, h = self.msg_img.get_size()

        in_x = x < point_x < x + w
        in_y = y < point_y < y + h
        return in_x and in_y