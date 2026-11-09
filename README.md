# Cross-Road
A spooky game made using pygame.

# Why I made it
It kind of followed the theme of Week-3 of Terra which was Spooky. So I made a dungeon game. The movement is simple with Arrow Keys and you interact with the surrounding with 'E'. The game is dungeon explorer along with escape theme. Use the progress bar to determine how close you are to the objective. Avoid getting near to the Enemy.(It explodes violently). The screen turns red indicating the boss has exploded but it doesn't die (never). Escape without getting killed.

Some assets are made by me but the player and surrounding asset were downloaded. See the credits in LICENSE.

## Run in a browser

You can go to: https://zeta-samuel.github.io/Cross-Road/

![Game screenshot](gameplay.png)

Install the requirements and start Pygbag from the repository root:

```shell
python -m pip install -r requirements.txt
python -m pygbag game
```

Open the localhost URL printed by Pygbag (usually `http://localhost:8000`) and
click the page once the game has loaded.

Hint: It is hard to beat the game in first try so try to memorize the map-layout :)

## UPDATE
I let my brother play the game and realized few things:
- The objective was unclear
- The boss was broken and boring
I have fixed a few things from last time:
Now, there is a progress bar at the top indicating the closeness of player and coin and portal and the boss spawns after 20 seconds and teleports every 10 seconds  near the player.

