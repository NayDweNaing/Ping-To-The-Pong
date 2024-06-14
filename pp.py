import pygame
import sys
import time

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_SPEED = 5

# Load sounds
paddle_hit_sound = pygame.mixer.Sound("paddle.wav")
wall_hit_sound = pygame.mixer.Sound("wall.wav")
game_end_sound = pygame.mixer.Sound("gameend.wav")
bg_sound = pygame.mixer.Sound("bg_sound.mp3")
# Sound Volume
bg_sound.set_volume(0.1)




# Load and scale background image
background_image = pygame.image.load("image-600x400.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping to the Pong")

ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = BALL_SPEED, BALL_SPEED

paddle_width, paddle_height = 15, 60
left_paddle_x, right_paddle_x = 10, WIDTH - 25
left_paddle_y, right_paddle_y = HEIGHT // 2 - paddle_height // 2, HEIGHT // 2 - paddle_height // 2
paddle_speed = 7
score_left, score_right = 0, 0

font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)
#loop sound
bg_sound.play(-1)

def reset_ball():
    return WIDTH // 2, HEIGHT // 2, BALL_SPEED, BALL_SPEED


game_over = False
game_started = False

def show_start_screen():
    start_text = game_over_font.render("Ping to the Pong", True, WHITE)
    instruction_text = font.render("Press Anything To Start", True, WHITE)
    screen.fill(BLACK)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + start_text.get_height()))
    pygame.display.flip()


while True:
    
    if not game_started:
        show_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                game_started = True
                score_left, score_right = 0, 0
                ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    score_left, score_right = 0, 0
                    ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()
                    game_over = False
                    

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and left_paddle_y > 0:
                left_paddle_y -= paddle_speed
            if keys[pygame.K_s] and left_paddle_y < HEIGHT - paddle_height:
                left_paddle_y += paddle_speed
            if keys[pygame.K_UP] and right_paddle_y > 0:
                right_paddle_y -= paddle_speed
            if keys[pygame.K_DOWN] and right_paddle_y < HEIGHT - paddle_height:
                right_paddle_y += paddle_speed

            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # Ball collision with paddles
            if (
                left_paddle_x < ball_x < left_paddle_x + paddle_width
                and left_paddle_y < ball_y < left_paddle_y + paddle_height
            ) or (
                right_paddle_x < ball_x < right_paddle_x + paddle_width
                and right_paddle_y < ball_y < right_paddle_y + paddle_height
            ):
                ball_speed_x = -ball_speed_x
                paddle_hit_sound.play()

            # Ball collision with top and bottom walls
            if ball_y <= 0 or ball_y >= HEIGHT:
                ball_speed_y = -ball_speed_y
                wall_hit_sound.play()

            # Scoring
            if ball_x <= 0:
                score_right += 1
                ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()
                ball_speed_x = BALL_SPEED  # Ensure the ball moves to the right after reset
                time.sleep(0.25)
            if ball_x >= WIDTH:
                score_left += 1
                ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()
                ball_speed_x = -BALL_SPEED  # Ensure the ball moves to the left after reset
                time.sleep(0.25)
            # Check if the game is over
            if score_left == 10 or score_right == 10:
                game_over = True
                game_end_sound.play()

        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, WHITE, (left_paddle_x, left_paddle_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, WHITE, (right_paddle_x, right_paddle_y, paddle_width, paddle_height))
        pygame.draw.ellipse(screen, WHITE, (ball_x - 10, ball_y - 10, 20, 20))
        score_display = font.render(f"{score_left} - {score_right}", True, WHITE)
        screen.blit(score_display, (WIDTH // 2 - 40, 10))
        
        if game_over:
            if score_left == 10:
                winner_text = "Left Side Wins!"
            else:
                winner_text = "Right Side Wins!"
            game_over_text = game_over_font.render(winner_text, True, WHITE)
            restart_text = font.render("Press Enter to Restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height()))

        pygame.display.flip()

    clock.tick(60)
