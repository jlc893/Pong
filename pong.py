import pygame, sys
import time


#General Setup
pygame.init()
pygame.mixer.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH, HEIGHT = (1000, 700)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN.fill(BLACK)
pygame.display.set_caption('Pong')
playerwin = pygame.USEREVENT + 1
opponentwin = pygame.USEREVENT + 2
WINNERFONT = pygame.font.SysFont('comicsans', 30)
BEASTFONT = pygame.font.SysFont('comicsans', 70)

#Variables
clock = pygame.time.Clock()
FPS = 160
player = pygame.Rect(WIDTH - 20, HEIGHT/2 - 70, 10, 140)
opponent = pygame.Rect(10, HEIGHT/2 - 70, 10, 140)



#Sounds
bounce_sound = pygame.mixer.Sound("sounds_ping_pong_8bit/ping_pong_8bit_beeep.ogg")
top_bottom_bounce = pygame.mixer.Sound("sounds_ping_pong_8bit/ping_pong_8bit_peeeeeep.ogg")

class pongball():
    def __init__(self):
        self.ball = pygame.Rect(490, 340, 20, 20)
        self.xdirection = 1
        self.movey = 0.0
        self.x = 490.0
        self.y = 340.0

    def checky(self):
        if self.ball.y <= 0 or self.ball.y >= 680:
            self.movey *= -1
            bounce_sound.play()


    # Handles Collisions
    def move(self, dist):
        self.y += self.movey
        self.x += self.xdirection * abs(dist**2 - self.movey**2)**.5

    def is_collision(self):
        if player.colliderect(self.ball) or opponent.colliderect(self.ball):
            return True
        else:
            return False

    def collision(self, dist):
        if player.colliderect(self.ball):
            bounce_sound.play()
            self.xdirection *= -1
            paddley = self.ball.y + 10 - player.y - 70
            self.movey = paddley / 140 * dist

        elif opponent.colliderect(self.ball):
            bounce_sound.play()
            self.xdirection *= -1
            paddley = self.ball.y + 10 - opponent.y - 70
            self.movey = paddley / 140 * dist


def move_players(keys_pressed, opponent, player):
    if keys_pressed[pygame.K_w] and opponent.y > 15:
        opponent.y -= 3
    if keys_pressed[pygame.K_s] and opponent.y < 545:
        opponent.y += 3
    if keys_pressed[pygame.K_i] and player.y > 15:
        player.y -= 3
    if keys_pressed[pygame.K_k] and player.y < 545:
        player.y += 3


def draw(playerlives, opponentlives):
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, player)
    pygame.draw.rect(WIN, WHITE, opponent)
    pygame.draw.ellipse(WIN, WHITE, ball.ball)
    pygame.draw.aaline(WIN, WHITE, (500, 0), (500, 700))
    player_lives_text = WINNERFONT.render('Player Lives: ' + str(playerlives), 1, WHITE)
    opponent_lives_text = WINNERFONT.render('Opponent Lives: ' + str(opponentlives), 1, WHITE)
    WIN.blit(player_lives_text, (800, 15))
    WIN.blit(opponent_lives_text, (25, 15))

    pygame.display.update()
ball = pongball()


def intro():
    WIN.fill((112, 128, 144))
    space_bar_image = pygame.transform.scale(pygame.image.load('Assets/space_to_start.png'), (800, 250))
    WIN.blit(space_bar_image, (100, 200))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("clicked")
                main()





# FUNCTION
def main():
    clock = pygame.time.Clock()
    dist = 1.6
    playerlives = 3
    opponentlives = 3
    game_active = True
    over_image = pygame.image.load('Assets/gameover.png')
    over_rect = over_image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    restart_image = pygame.image.load('Assets/restart.png')
    restart_rect = restart_image.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 250))

    while True:
        #state_manager()
        if game_active == False:
            WIN.blit(over_image, over_rect)
            WIN.blit(restart_image, restart_rect)
            winnertext = WINNERFONT.render(f'{winner} WINS!', 1, WHITE)
            WIN.blit(winnertext, (430, 500))
            pygame.display.update()
            player.y = 280
            opponent.y =280

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if restart_rect.collidepoint(x, y):
                        print("clicked")
                        main()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys_pressed = pygame.key.get_pressed()
            move_players(keys_pressed, opponent, player)
            clock.tick(FPS)
            ball.checky()
            if ball.x >= 980:
                playerlives -= 1
                ball.xdirection *= -1
                ball.x = 490.0
                ball.y = 340.0
                ball.ball.x = 490
                ball.ball.y = 340
                dist = 1.6
                ball.movey = 0

            if ball.x <= 0:
                opponentlives -= 1
                ball.xdirection *= -1
                ball.x = 490
                ball.y = 340
                ball.ball.x = 490
                ball.ball.y = 340
                dist = 1.6
                ball.movey = 0

            if ball.is_collision():
                ball.collision(dist)
                if dist < 8:
                    dist += .4
            ball.move(dist)
            ball.ball.x = round(ball.x)
            ball.ball.y = round(ball.y)
            draw(playerlives, opponentlives)
            if playerlives == 0:
                game_active = False
                winner = "opponent"
            if opponentlives == 0:
                game_active = False
                winner = "player"

while True:
    intro()
if __name__ == "__main__":
    main()
