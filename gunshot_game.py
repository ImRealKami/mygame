import pygame
import os
import random

#General Setup
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GunShot Game")

#Loading Images
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "space.jpg")), (WIDTH, HEIGHT))
GUNMAN = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "spaceboy.png")), (130, 130)).convert_alpha()
PLANET = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "planet.png")), (160, HEIGHT))
BULLET = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "bullet.png")), (80, 80))
ENEMY1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "enemy1.png")), (80, 80))
ENEMY2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "enemy2.png")), (80, 80))
ENEMY3 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "enemy3.png")), (80, 80))

#Loading Sounds
SHOOT_SOUND = pygame.mixer.Sound(os.path.join("assets", "music", "shoot.wav"))
HIT_SOUND = pygame.mixer.Sound(os.path.join("assets", "music", "minus-health.mp3"))
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join("assets", "music", "game-over.mp3"))

#Speeds and cooldowns
BULLET_SPEED = 6
PLAYER_SPEED = 5
BULLET_COOLDOWN = 400
ENEMY_SPEED = 6
ENEMY_SPAWN_COOLDOWN = 2000

#Rects
planet_rect = PLANET.get_rect(topleft=(0, 0))
gunman_rect = GUNMAN.get_rect(center=(planet_rect.right + 100, HEIGHT // 2))

#Masks
gunman_mask = pygame.mask.from_surface(GUNMAN)
bullet_mask = pygame.mask.from_surface(BULLET)
planet_mask = pygame.mask.from_surface(PLANET)
enemy1_mask = pygame.mask.from_surface(ENEMY1)
enemy2_mask = pygame.mask.from_surface(ENEMY2)
enemy3_mask = pygame.mask.from_surface(ENEMY3)

#Game Variables
health = 100
score = 0
high_score = 0

#Font
font = pygame.font.SysFont('bauhaus', 30, bold=True)
lost_font = pygame.font.SysFont('consolas', 70)

def read_high_score():
    if not os.path.exists('high_score.txt'):
        with open('high_score.txt', 'w') as file:
            file.write('0')
    with open('high_score.txt', 'r') as file:
        high_scores = file.readlines()
        high_scores = [int(score.strip()) for score in high_scores]
        high_score = max(high_scores)
        return high_score

def write_high_score(score):
    with open('high_score.txt', 'a') as file:
        file.write(str(score) + '\n')

def handle_move():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and gunman_rect.top > 0:
        gunman_rect.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and gunman_rect.bottom < HEIGHT:
        gunman_rect.y += PLAYER_SPEED
    if keys[pygame.K_LEFT] and gunman_rect.left > planet_rect.right - 15:
        gunman_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and gunman_rect.right < WIDTH // 2 + 50:
        gunman_rect.x += PLAYER_SPEED

def draw(bullet_rect, enemies, health, score):
    window.blit(BG, (0, 0))
    window.blit(PLANET, planet_rect.topleft)
    window.blit(GUNMAN, gunman_rect.topleft)
    if bullet_rect:
        window.blit(BULLET, bullet_rect)
    for enemy in enemies:
        window.blit(enemy['image'], enemy['rect'].topleft)
    
    pygame.draw.rect(window, (255, 0, 0), (10, 40, 200, 20))
    pygame.draw.rect(window, (0, 255, 0), (10, 40, health * 2, 20))

    health_text = font.render("Health", True, (173, 216, 230))  # Light blue color
    window.blit(health_text, (10, 10))

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    pygame.display.update()

def main_menu():
    title_font = pygame.font.SysFont('comicsans', 60)
    instruction_font = pygame.font.SysFont('comicsans', 40)
    high_score = read_high_score()

    run = True
    while run:
        window.fill((0, 0, 0))
        title_text = title_font.render("GunShot Game", True, (255, 255, 255))
        instruction_text = instruction_font.render("Press any key to start", True, (255, 255, 255))
        high_score_text = instruction_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        
        window.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - title_text.get_height() - 20))
        window.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT//2 + 20))
        window.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 + 60))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                run = False

def main():
    global health, score, high_score
    main_menu()

    run = True
    clock = pygame.time.Clock()
    last_bullet_time = 0
    last_enemy_spawn_time = 0
    bullet_rect = None
    enemies = []
    enemies_off_screen = 0

    while run:
        clock.tick(60)
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not bullet_rect or (current_time - last_bullet_time > BULLET_COOLDOWN):
                        SHOOT_SOUND.play()
                        bullet_rect = BULLET.get_rect()
                        bullet_rect.centerx = gunman_rect.right
                        bullet_rect.centery = gunman_rect.centery
                        last_bullet_time = current_time

        if bullet_rect:
            bullet_rect.x += BULLET_SPEED
            if bullet_rect.x > WIDTH:
                bullet_rect = None

        if current_time - last_enemy_spawn_time > ENEMY_SPAWN_COOLDOWN:
            enemy_type = random.choice([ENEMY1, ENEMY2, ENEMY3])
            enemy_rect = enemy_type.get_rect(right=WIDTH, centery=random.randint(0, HEIGHT))
            enemies.append({'image': enemy_type, 'rect': enemy_rect, 'mask': pygame.mask.from_surface(enemy_type)})
            last_enemy_spawn_time = current_time

        for enemy in enemies:
            enemy['rect'].x -= ENEMY_SPEED
            if enemy['rect'].right < 0:
                enemies_off_screen += 1
                enemies.remove(enemy)

                if enemies_off_screen >= 3:
                    health -= 5
                    enemies_off_screen = 0

                if health <= 0:
                    draw(bullet_rect, enemies, health, score)
                    game_over_text = lost_font.render("GAME OVER", True, (255, 0, 0))
                    window.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - game_over_text.get_height()//2))
                    pygame.display.update()
                    pygame.time.delay(5000)

                    if score > high_score:
                        write_high_score(score)
                    run = False
                    pygame.quit()
                    return

        if bullet_rect:
            for enemy in enemies:
                offset_x = bullet_rect.x - enemy['rect'].x
                offset_y = bullet_rect.y - enemy['rect'].y

                if enemy['mask'].overlap(bullet_mask, (offset_x, offset_y)):
                    enemies.remove(enemy)
                    bullet_rect = None
                    score += 1
                    break

        for enemy in enemies:
            offset_x = enemy['rect'].x - gunman_rect.x
            offset_y = enemy['rect'].y - gunman_rect.y

            if gunman_mask.overlap(enemy['mask'], (offset_x, offset_y)):
                HIT_SOUND.play()
                health -= 7
                enemies.remove(enemy)

                if health <= 0:
                    draw(bullet_rect, enemies, health, score)
                    GAME_OVER_SOUND.play()
                    game_over_text = lost_font.render("GAME OVER", True, (255, 0, 0))
                    window.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - game_over_text.get_height()//2))
                    pygame.display.update()
                    pygame.time.delay(5000)

                    if score > high_score:
                        write_high_score(score)
                    run = False
                    pygame.quit()
                    return

        handle_move()
        draw(bullet_rect, enemies, health, score)

if __name__ == '__main__':
    main()
