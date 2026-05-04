from bike_for_your_life.cli import main
from bike_for_your_life.terminal import clear_screen


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("Game exited.")
