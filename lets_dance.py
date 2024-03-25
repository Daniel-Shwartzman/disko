from src.disko.image_controller import ImageController
from src.disko.image_view import ImageRegistryManager
from src.disko.image_model import ImageDataModel

# main function
def main():
    # Database file path
    db_file = 'image_data.db'

    # Initialize model, controller, and GUI objects
    model = ImageDataModel(ImageController, db_file)
    controller = model.controller
    gui = ImageRegistryManager(db_file, controller)

    # Run GUI
    gui.run()

# Entry point of the application
if __name__ == '__main__':
    main()
