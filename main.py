import pygame

from controller import Controller
from game import MIN_HEIGHT, MIN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, DrawnObject

# pygame setup
pygame.init()

# change the title and icon of the window
pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load("assets/black-queen.png"))


def main() -> None:
    # setup screen and game
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    DrawnObject.set_sizes(SCREEN_WIDTH, SCREEN_HEIGHT)
    controller = Controller()

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

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                controller.mouse_click(*event.pos)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                controller.mouse_release(*event.pos)

            if controller.game_active and not controller.player_turn:
                controller.make_computer_move()

        # draw everything to the screen
        controller.update_clocks()
        controller.draw(screen)
        pygame.display.flip()


# run the program
if __name__ == "__main__":
    main()
