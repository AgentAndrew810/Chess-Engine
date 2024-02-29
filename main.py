import pygame

from game import Game
from gui.drawnobject import DrawnObject
from gui.constants import SCREEN_WIDTH, SCREEN_HEIGHT, MIN_WIDTH, MIN_HEIGHT

# pygame setup
pygame.init()

# change the title and icon of the window
pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load("assets/black-queen.png"))


def main() -> None:
    # setup screen and game
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    DrawnObject.set_sizes(SCREEN_WIDTH, SCREEN_HEIGHT)
    game = Game()

    # main loop
    while True:
        for event in pygame.event.get():
            # if the user hits the x button quit the application
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.VIDEORESIZE:
                # choose either the current size or minimum
                width = max(event.size[0], MIN_WIDTH)
                height = max(event.size[1], MIN_HEIGHT)

                # adjust the screen and reset the sizes in each object
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                DrawnObject.set_sizes(width, height)

        # draw everything to the screen
        game.draw(screen)
        pygame.display.flip()


# run the program
if __name__ == "__main__":
    main()
