from controller import GameController
from ui import GameUI


def main():

    controller = GameController()
    
    game_ui = GameUI(controller)
    
    game_ui.setup_window()
    
    game_ui.run()


if __name__ == "__main__":
    main()
