"""
Snake — a simple Pygame game built for the browser via pygbag.

DESIGN FOR CUSTOMIZATION
-------------------------
Everything a kid might want to tweak lives in the CONSTANTS block below:
change the grid size, speed, colors, or what happens when you eat food.
Try changing SNAKE_COLOR to a random color each time you eat, or making
FOOD_COLOR flash!

HOW THE BROWSER VERSION WORKS
-------------------------------
Normal Pygame games use a `while True:` loop. Browser (WASM) games can't
block the browser tab like that, so pygbag requires an ASYNC main loop:
every pass through the loop we `await asyncio.sleep(0)` to hand control
back to the browser for a moment. That's the only real difference from
a normal desktop Pygame script.
"""

import asyncio
import random
import sys

import pygame

# ---------------------------------------------------------------------------
# CONSTANTS — tweak these to customize the game!
# ---------------------------------------------------------------------------
GRID_SIZE = 20                  # size of one cell, in pixels
GRID_WIDTH = 24                 # board width, in cells
GRID_HEIGHT = 18                # board height, in cells
SCREEN_WIDTH = GRID_SIZE * GRID_WIDTH
SCREEN_HEIGHT = GRID_SIZE * GRID_HEIGHT + 60  # extra space for the score bar

STARTING_LENGTH = 3
STARTING_SPEED = 8              # moves per second — higher = faster/harder
SPEED_INCREASE_PER_FOOD = 0.25  # game gets a little faster each time you eat

BG_COLOR = (18, 18, 28)
GRID_LINE_COLOR = (30, 30, 42)
SNAKE_COLOR = (80, 220, 120)
SNAKE_HEAD_COLOR = (140, 255, 170)
FOOD_COLOR = (240, 90, 90)
TEXT_COLOR = (235, 235, 245)
GAME_OVER_COLOR = (240, 90, 90)

FONT_NAME = None  # None = pygame's default font


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_NAME, 28)
        self.big_font = pygame.font.Font(FONT_NAME, 48)
        self.reset()

    def reset(self):
        mid_x, mid_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.snake = [(mid_x - i, mid_y) for i in range(STARTING_LENGTH)]
        self.direction = (1, 0)
        self.pending_direction = (1, 0)
        self.speed = STARTING_SPEED
        self.score = 0
        self.game_over = False
        self.food = self.spawn_food()

    def spawn_food(self):
        occupied = set(self.snake)
        while True:
            pos = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
            if pos not in occupied:
                return pos

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.game_over:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.reset()
            return

        key_to_dir = {
            pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
            pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
            pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
            pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
        }
        new_dir = key_to_dir.get(event.key)
        if new_dir is None:
            return

        # Prevent reversing directly into yourself.
        opposite = (-self.direction[0], -self.direction[1])
        if new_dir != opposite:
            self.pending_direction = new_dir

    def update(self):
        if self.game_over:
            return

        self.direction = self.pending_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Wall collision
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            self.game_over = True
            return

        # Self collision
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.speed += SPEED_INCREASE_PER_FOOD
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill(BG_COLOR)

        # Subtle grid lines
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_LINE_COLOR, (x, 60), (x, SCREEN_HEIGHT))
        for y in range(60, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_LINE_COLOR, (0, y), (SCREEN_WIDTH, y))

        # Food
        food_rect = pygame.Rect(
            self.food[0] * GRID_SIZE, 60 + self.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(self.screen, FOOD_COLOR, food_rect, border_radius=6)

        # Snake
        for i, (sx, sy) in enumerate(self.snake):
            rect = pygame.Rect(sx * GRID_SIZE, 60 + sy * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
            pygame.draw.rect(self.screen, color, rect, border_radius=4)

        # Score bar
        pygame.draw.rect(self.screen, BG_COLOR, (0, 0, SCREEN_WIDTH, 60))
        score_surf = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_surf, (16, 16))

        if self.game_over:
            over_surf = self.big_font.render("Game Over", True, GAME_OVER_COLOR)
            hint_surf = self.font.render(
                "Press Enter / Space to play again", True, TEXT_COLOR
            )
            self.screen.blit(
                over_surf,
                over_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)),
            )
            self.screen.blit(
                hint_surf,
                hint_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)),
            )

        pygame.display.flip()

    async def run(self):
        move_timer = 0.0
        while True:
            dt = self.clock.tick(60) / 1000.0  # seconds since last frame

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_input(event)

            move_timer += dt
            step = 1.0 / self.speed
            if move_timer >= step:
                move_timer = 0.0
                self.update()

            self.draw()

            # Required for pygbag: yield control back to the browser each frame.
            await asyncio.sleep(0)


async def main():
    game = SnakeGame()
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())
