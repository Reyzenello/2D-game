# 2D-game


This code creates a 2D Geometry Dash-inspired game using Pygame.

https://github.com/user-attachments/assets/2117fccc-5ec1-4a97-b8a5-72e49c062c35


**1. Initialization and Setup:**

- Imports `pygame`, `sys`, and `random`.
- Initializes Pygame.
- Sets screen dimensions, FPS, and colors.
- Creates the game window and clock.
- Defines fonts for text display.

**2. Player Class (`Player`):**

```python
class Player(pygame.sprite.Sprite):
    # ...
```

- Represents the player character.
- `__init__`: Initializes the player's image, position, vertical velocity, ground status, and lives.
- `update`:  Applies gravity, updates the player's vertical position, handles ground collision, and sets the `on_ground` flag.
- `jump`: Makes the player jump if they are on the ground.

**3. Obstacle Class (`Obstacle`):**

```python
class Obstacle(pygame.sprite.Sprite):
    # ...
```

- Represents an obstacle (triangle).
- `__init__`: Initializes the obstacle's image, position, and creates the shaded triangle.
- `create_shaded_triangle`: Draws a triangle with shading using different gray tones.
- `update`: Moves the obstacle to the left and removes it when it goes off-screen.

**4. Coin Class (`Coin`):**

```python
class Coin(pygame.sprite.Sprite):
    # ...
```

Represents a collectible coin.  Similar structure to the `Obstacle` class.

**5. Platform Class (`Platform`):**

```python
class Platform(pygame.sprite.Sprite):
    # ...
```

Represents a platform. Similar update method to Obstacle and Coin.

**6. `show_instructions` Function:**

- Displays game instructions on the screen and waits for a key press to start the game.

**7. `game_loop` Function:**

- The main game loop.
- Creates the player, sprite groups (for managing game objects), and initializes game variables (score, timers for spawning obstacles and coins).
- Handles events (quitting, jumping).
- Spawns obstacles, coins, and platforms at intervals using timers.
- Updates sprite positions.
- Handles collisions:
    - Player-obstacle collisions reduce lives and end the game if lives reach zero.
    - Player-coin collisions increase the score.
    - Player-platform collisions handle landing on platforms.
- Checks if the player has fallen off the screen.
- Draws the game elements (background, sprites, score, lives).

**8. `show_game_over` Function:**

- Displays the game over screen with the final score and waits for a key press to restart.

**9. `main` Function:**

- The main function that runs the game.
- Shows instructions.
- Runs the game loop.
- Shows the game over screen.
- Repeats indefinitely.
