import pygame
import os
import random

WIDTH = 576
HEIGHT = 800
FPS = 30

pygame.init()
pygame.font.init()
font_score = pygame.font.SysFont("comicsans", 30)
font_giua = pygame.font.SysFont("conmicsans", 70)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

img_dir = os.getcwd()

background = pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "imgs", "bg.png")), (WIDTH, 395))
base_image = pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "imgs", "base.png")), (WIDTH * 2, 35))

pipe_image_bottom = pygame.image.load(os.path.join(img_dir, "imgs", "pipe-green.png"))
pipe_image_red = pygame.image.load(os.path.join(img_dir, "imgs", "pipe-red.png"))

bird1_list = ["bird1.png", "bird2.png", "bird3.png"]
bird1_imgs = []
for img in bird1_list:
    bird1_imgs.append(pygame.image.load(os.path.join(img_dir, "imgs", img)))

bird2_list = ["redbird-upflap.png", "redbird-midflap.png", "redbird-downflap.png"]
bird2_imgs = []
for img in bird2_list:
    bird2_imgs.append(pygame.image.load(os.path.join(img_dir, "imgs", img)))

def tim_nguoi_thang(score1, score2):
    if score1 > score2:
        render_text(font_giua,"You win", (288, 197), (255,0,0))
        render_text(font_giua, "You lose", (288, 197 + 405), (255, 255, 255))
    elif score1 < score2:
        render_text(font_giua,"You lose", (288,197), (255,255,255))
        render_text(font_giua,"You win", (288, 197 + 405), (255, 0, 0))
    else:
        render_text(font_giua,"DRAWN", (288,197), (0,255,0))
        render_text(font_giua,"DRAWN", (288, 197+405), (0, 255, 0))

def render_text(font, s, pos, color):
    text = font.render(s, True, color)
    text_rect = text.get_rect(center=pos)
    screen.blit(text, text_rect)

def add_pipe(pos):
    if pos == 1:
        height = random.randrange(30, 200)
        rd = random.randrange(0, 5)
        if rd == 1:
            pipe_t = Pipe(pipe_image_red, 700, height, 1, "tren")
            pipe_d = Pipe(pipe_image_red, 700, height, 1, "duoi")
        else:
            pipe_t = Pipe(pipe_image_bottom, 700, height, 1, "tren")
            pipe_d = Pipe(pipe_image_bottom, 700, height, 1, "duoi")
        pipe_list_1.append(pipe_t)
        pipe_list_1.append(pipe_d)
        pipes_1.add(pipe_t)
        pipes_1.add(pipe_d)

    elif pos == 2:
        height = random.randrange(30, 200)
        rd = random.randrange(0, 5)
        if rd == 1:
            pipe_t = Pipe(pipe_image_red, 700, height, 2, "tren")
            pipe_d = Pipe(pipe_image_red, 700, height, 2, "duoi")
        else:
            pipe_t = Pipe(pipe_image_bottom, 700, height, 2, "tren")
            pipe_d = Pipe(pipe_image_bottom, 700, height, 2, "duoi")
        pipe_list_2.append(pipe_t)
        pipe_list_2.append(pipe_d)
        pipes_2.add(pipe_t)
        pipes_2.add(pipe_d)

class Player(pygame.sprite.Sprite):
    def __init__(self, anh, y):
        super().__init__()
        self.image_imgs = anh
        self.image = self.image_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = 10
        self.speedx = 0
        self.current_img = 0
        self.vel = 0
        self.tick_count = 0
        self.height = self.rect.y
        self.tilt = 0
        self.img_count = 0
        self.MAX_ROTATION = 25
        self.ROT_VEL = 20
        self.ANIMATION_TIME = 5

    def jump(self):
        self.vel = -8
        self.tick_count = 0
        self.height = self.rect.y

    def move(self):
        self.tick_count += 1

        # for downward acceleration
        displacement = self.vel * (self.tick_count) + 0.5 * (3) * (self.tick_count) ** 2  # calculate displacement

        # terminal velocity
        if displacement >= 6:
            displacement = (displacement / abs(displacement)) * 6

        if displacement < 0:
            displacement -= 6

        self.rect.y = self.rect.y + displacement

        if displacement < 0 or self.rect.y < self.height + 8:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def update(self):
        self.move()
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            img = self.image_imgs[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            img = self.image_imgs[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            img = self.image_imgs[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            img = self.image_imgs[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            img = self.image_imgs[0]
            self.img_count = 0
        if self.tilt <= -80:
            img = self.image_imgs[1]
            self.img_count = self.ANIMATION_TIME * 2

        self.image = pygame.transform.rotate(img, self.tilt)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, pipe_img, x, height, manhinh, pos):
        super().__init__()
        self.height = height
        self.pipe_spec = False
        if pipe_img == pipe_image_red:
            self.pipe_spec = True
            self.GAP = 110
        else:
            self.GAP = 150

        if manhinh == 1:
            if pos == "duoi":
                self.image = pygame.transform.scale(pipe_img, (52, 395 - base_image.get_height() - self.GAP - self.height))
                self.rect = self.image.get_rect()
                self.rect.top = self.height + self.GAP
            elif pos == "tren":
                img = pygame.transform.scale(pipe_img, (52, self.height))
                self.image = pygame.transform.flip(img, False, True)
                self.rect = self.image.get_rect()
                self.rect.top = 0
        elif manhinh == 2:
            if pos == "duoi":
                self.image = pygame.transform.scale(pipe_img, (52, 395 - base_image.get_height() - self.GAP - self.height))
                self.rect = self.image.get_rect()
                self.rect.top = self.height + self.GAP + 405
            elif pos == "tren":
                img = pygame.transform.scale(pipe_img, (52, self.height))
                self.image = pygame.transform.flip(img, False, True)
                self.rect = self.image.get_rect()
                self.rect.top = 0 + 405

        self.rect.x = x
        self.speedx = 7
        self.passed = False

    def update(self):
        self.rect.x -= self.speedx

class Base(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = base_image
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.x = 0
        self.speedx = 5

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right < WIDTH:
            self.rect.x = 0

all_sprite_1 = pygame.sprite.Group()
all_sprite_2 = pygame.sprite.Group()
pipes_1 = pygame.sprite.Group()
pipes_2 = pygame.sprite.Group()

base_1 = Base(395)
base_2 = Base(800)
all_sprite_1.add(base_1)
all_sprite_2.add(base_2)

pipe_list_1 = []
rem_1 = []
score_1 = 0
pipe_list_2 = []
rem_2 = []
score_2 = 0

run = True
start_game = False
end_game = False
start_game_2 = False
end_game_2 = False
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and start_game:
                player_1.jump()
            # if event.key == pygame.K_w and start_game == False:
            #     pipe_list_1 = []
            #     rem_1 = []
            #     score_1 = 0
            #     start_game = True
            #     player_1 = Player(bird1_imgs, int(395/2))
            #     all_sprite_1.add(player_1)
            #     add_pipe(1)

            if event.key == pygame.K_p and start_game_2:
                player_2.jump()

            if event.key == pygame.K_SPACE and start_game_2 == False and start_game == False:

                pipe_list_1 = []
                rem_1 = []
                score_1 = 0
                start_game = True
                end_game = False
                player_1 = Player(bird1_imgs, int(395 / 2))
                all_sprite_1.add(player_1)
                add_pipe(1)

                start_game_2 = True
                end_game_2 = False
                pipe_list_2 = []
                rem_2 = []
                score_2 = 0
                add_pipe(2)
                player_2 = Player(bird2_imgs, int(395 / 2 + 405))
                all_sprite_2.add(player_2)

    if start_game:
        all_sprite_1.update()
        pipes_1.update()

        # them ong
        if pipe_list_1[0].rect.x < 400:
            add_pipe(1)
            rem_1.append(pipe_list_1.pop(0))
            rem_1.append(pipe_list_1.pop(0))

        # kiem tra ong di het man hinh va xoa, cong diem
        if len(rem_1) != 0:
            if rem_1[0].passed == False and rem_1[0].rect.right < player_1.rect.left:
                if rem_1[0].pipe_spec:
                    score_1 += 2
                    rem_1[0].passed = True
                else:
                    score_1 += 1
                    rem_1[0].passed = True

            if rem_1[0].rect.right < 0:
                rem_1[0].kill()
                rem_1[1].kill()
                rem_1.pop(0)
                rem_1.pop(0)

        # kiem tra tren duoi
        if player_1.rect.y < 0:
            player_1.rect.y = 0
        if player_1.rect.bottom > 360:
            start_game = False
            end_game = True
            pipes_1.empty()
            player_1.kill()

        #kiem tra va vao ong
        hits = pygame.sprite.spritecollide(player_1, pipes_1, False)
        if hits:
            player_1.kill()
            pipes_1.empty()
            start_game = False
            end_game = True

        screen.blit(background,(0,0))
        all_sprite_1.draw(screen)
        pipes_1.draw(screen)
        render_text(font_score, "Player1: " + str(score_1), (500,15), (255,255,255))

        # pygame.display.update([0, 0, WIDTH, 395])
    else:
        screen.blit(background, (0, 0))
        render_text(font_score, "Player1: " + str(score_1), (500,15), (255,255,255))
        screen.blit(bird1_imgs[0], (10, int(395/2)))
        screen.blit(base_image, (0,360))
        # if end_game and end_game_2:
        #     tim_nguoi_thang(score_1, score_2)

        # pygame.display.update([0, 0, WIDTH, 395])

    if start_game_2:
        all_sprite_2.update()
        pipes_2.update()

        # them ong
        if pipe_list_2[0].rect.x < 400:
            add_pipe(2)
            rem_2.append(pipe_list_2.pop(0))
            rem_2.append(pipe_list_2.pop(0))

        # kiem tra ong di het man hinh va xoa, cong diem
        if len(rem_2) != 0:
            if rem_2[0].passed == False and rem_2[0].rect.right < player_2.rect.left:
                if rem_2[0].pipe_spec:
                    score_2 += 2
                    rem_2[0].passed = True
                else:
                    score_2 += 1
                    rem_2[0].passed = True

            if rem_2[0].rect.right < 0:
                rem_2[0].kill()
                rem_2[1].kill()
                rem_2.pop(0)
                rem_2.pop(0)

        # kiem tra tren duoi
        if player_2.rect.y < 405:
            player_2.rect.y = 405
        if player_2.rect.bottom > 765:
            start_game_2 = False
            end_game_2 = True
            pipes_2.empty()
            player_2.kill()

        # kiem tra va vao ong
        hits = pygame.sprite.spritecollide(player_2, pipes_2, False)
        if hits:
            player_2.kill()
            pipes_2.empty()
            start_game_2 = False
            end_game_2 = True

        screen.blit(background, (0, 405))
        all_sprite_2.draw(screen)
        pipes_2.draw(screen)
        render_text(font_score, "Player2: " + str(score_2), (500,15+405), (255,255,255))

        # pygame.display.update([0, 405, WIDTH, 395])
    else:
        screen.blit(background, (0, 405))
        render_text(font_score, "Player2: " + str(score_2), (500,15+405), (255,255,255))
        screen.blit(bird2_imgs[0], (10, int(395 / 2) + 405))
        screen.blit(base_image, (0, 765))

        # pygame.display.update([0, 405, WIDTH, 395])

    if end_game and end_game_2:
        tim_nguoi_thang(score_1, score_2)

    pygame.display.update()


pygame.quit()