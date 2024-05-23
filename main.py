import pygame

from controller import GameController
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
    game_controller = GameController()

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

            if not game_controller.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game_controller.grab_piece(*event.pos)

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    game_controller.drop_piece(*event.pos)

            # if not game_controller.game_over:
            #     if game_controller.player_turn:
            #         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #             game_controller.grab_piece(*event.pos)

            #         if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            #             game_controller.drop_piece(*event.pos)

            #     else:
            #         game_controller.make_computer_move()

        # draw everything to the screen
        game_controller.update_clocks()
        game_controller.draw(screen)
        pygame.display.flip()


# run the program
if __name__ == "__main__":
    main()
