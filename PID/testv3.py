import pygame
import numpy as np

# ---------- Basic setup ----------
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎮 PID Simulation Game (pygame Edition)")
clock = pygame.time.Clock()

# ---------- Colors ----------
WHITE = (240, 240, 240)
BLACK = (10, 10, 10)
RED = (255, 80, 80)
BLUE = (80, 150, 255)
GREEN = (80, 255, 100)
GRAY = (180, 180, 180)

# ---------- Target ----------
TARGET = 90  # target angle
angle = 0.0
error_sum = 0
last_error = 0

# ---------- PID initial values ----------
Kp, Ki, Kd = 1.0, 0.0, 0.1

# ---------- Slider UI ----------
slider_rects = {
    "Kp": pygame.Rect(100, 450, 200, 10),
    "Ki": pygame.Rect(350, 450, 200, 10),
    "Kd": pygame.Rect(600, 450, 200, 10)
}
slider_values = {"Kp": Kp, "Ki": Ki, "Kd": Kd}
dragging = None

def draw_slider(name, value):
    rect = slider_rects[name]
    # Draw track
    pygame.draw.rect(screen, GRAY, rect)
    # Handle
    handle_x = rect.x + (value / (3 if name == "Kp" else (0.5 if name == "Ki" else 0.3))) * rect.width
    pygame.draw.circle(screen, BLUE, (int(handle_x), rect.centery), 8)
    # Label
    font = pygame.font.SysFont(None, 24)
    label = font.render(f"{name}: {value:.2f}", True, BLACK)
    screen.blit(label, (rect.x, rect.y - 25))

# ---------- Simulation function ----------
def pid_update(Kp, Ki, Kd, angle, error_sum, last_error, dt):
    error = TARGET - angle
    error_sum += error * dt
    derivative = (error - last_error) / dt
    output = Kp * error + Ki * error_sum + Kd * derivative
    angle += (output - 0.05 * angle) * dt  # simulate inertia
    return angle, error_sum, error

# ---------- Draw robot arm ----------
def draw_robot(angle):
    center = (WIDTH//2, HEIGHT//2 - 100)
    length = 150
    rad = np.radians(angle)
    end = (center[0] + length * np.cos(rad), center[1] - length * np.sin(rad))
    pygame.draw.line(screen, RED, center, end, 6)
    pygame.draw.circle(screen, BLACK, center, 8)
    font = pygame.font.SysFont(None, 32)
    screen.blit(font.render(f"Angle: {angle:.1f}°", True, BLACK), (WIDTH//2 - 80, 100))

# ---------- Main Loop ----------
running = True
dt = 0.02

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Drag sliders
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for name, rect in slider_rects.items():
                if rect.collidepoint(event.pos):
                    dragging = name
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # reset simulation
                angle, error_sum, last_error = 0.0, 0.0, 0.0

    # Handle dragging
    if dragging:
        x, y = pygame.mouse.get_pos()
        rect = slider_rects[dragging]
        rel_x = max(0, min(rect.width, x - rect.x))
        if dragging == "Kp":
            slider_values["Kp"] = (rel_x / rect.width) * 3
        elif dragging == "Ki":
            slider_values["Ki"] = (rel_x / rect.width) * 0.5
        elif dragging == "Kd":
            slider_values["Kd"] = (rel_x / rect.width) * 0.3

    # Update PID
    Kp, Ki, Kd = slider_values["Kp"], slider_values["Ki"], slider_values["Kd"]
    angle, error_sum, last_error = pid_update(Kp, Ki, Kd, angle, error_sum, last_error, dt)

    # Draw everything
    draw_robot(angle)
    for name, val in slider_values.items():
        draw_slider(name, val)

    # Target line
    pygame.draw.line(screen, GREEN, (WIDTH//2 + 150*np.cos(np.radians(TARGET)),
                                     HEIGHT//2 - 100 - 150*np.sin(np.radians(TARGET))),
                                     (WIDTH//2, HEIGHT//2 - 100), 2)

    font = pygame.font.SysFont(None, 24)
    screen.blit(font.render("Press SPACE to reset", True, BLACK), (WIDTH//2 - 80, HEIGHT - 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
