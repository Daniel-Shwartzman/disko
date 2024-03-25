from src.mvc.controller import ImageController
from src.mvc.view import ImageRegistryManager

# main function
def main():
    # Database file path
    db_file = 'image_data.db'

    # Initialize controller and GUI objects
    controller = ImageController(db_file)
    gui = ImageRegistryManager(db_file, controller)

    # Run GUI
    gui.run()

# Entry point of the application
if __name__ == '__main__':
    main()
