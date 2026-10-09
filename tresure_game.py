import pygame as py
import random

py.init()
screen = py.display.set_mode((800, 600))
py.display.set_caption("TREASURE HUNT")
clock = py.time.Clock()

colour1 = (255, 125, 255)
colour2 = (125, 100, 200)
colour3 = (0, 0, 0)
colour4 = (165, 88, 99)

font = py.font.Font(None, 40)
bigfont = py.font.Font(None, 70)

player = py.Rect(380, 280, 40, 40)
coin = py.Rect(200, 200, 25, 15)

enemies = [
    py.Rect(100, 100, 35, 35),
    py.Rect(299, 200, 35, 35),
    py.Rect(300, 340, 35, 35)
]
enemies_speed = [[3, 2], [4, 2], [-2, 4]]

score = 0
live = 2
game_over = False
hit_timer = 0
running = True

while running:
    clock.tick(60)

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                running = False
            if event.key == py.K_r and game_over:
                player.x = 380
                player.y = 280
                score = 0
                live = 2
                hit_timer = 0
                game_over = False

    key = py.key.get_pressed()

    if not game_over:
       
        if key[py.K_LEFT] or key[py.K_a]:
            player.x -= 4
        if key[py.K_RIGHT] or key[py.K_d]:
            player.x += 4
        if key[py.K_UP] or key[py.K_w]:
            player.y -= 4
        if key[py.K_DOWN] or key[py.K_s]:
            player.y += 4

        player.clamp_ip(screen.get_rect())

        
        for i in range(len(enemies)):
            enemies[i].x += enemies_speed[i][0]
            enemies[i].y += enemies_speed[i][1]

            if enemies[i].left <= 0 or enemies[i].right >= 800:
                enemies_speed[i][0] *= -1
            if enemies[i].top <= 0 or enemies[i].bottom >= 600:
                enemies_speed[i][1] *= -1

        
        if player.colliderect(coin):
            score += 10
            coin.x = random.randint(20, 750)
            coin.y = random.randint(20, 550)

       
        if hit_timer > 0:
            hit_timer -= 1

       
        for enemy in enemies:
            if player.colliderect(enemy) and hit_timer == 0:
                live -= 1
                hit_timer = 60
                player.x = 370
                player.y = 390
                if live <= 0:
                    game_over = True

    
    screen.fill(colour1)
    py.draw.rect(screen, colour2, coin, border_radius=8)

    for enemy in enemies:
        py.draw.rect(screen, colour3, enemy, border_radius=8)

    if hit_timer == 0 or (hit_timer // 5) % 2 == 0:
        py.draw.rect(screen, colour4, player, border_radius=8)

    screen.blit(font.render(f"SCORE : {score}", True, colour4), (20, 20))
    screen.blit(font.render(f"LIVES : {live}", True, colour1), (450, 20))

    if game_over:
        message = bigfont.render("GAME OVER !", True, colour3)
        restart = font.render("Press R to RESTART / PLAY AGAIN", True, colour2)
        screen.blit(message, message.get_rect(center=(400, 260)))
        screen.blit(restart, restart.get_rect(center=(400, 360)))

    py.display.flip()

py.quit()