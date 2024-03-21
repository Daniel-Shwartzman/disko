# model.py
from src.disko.sqlite import SQLiteCRUD

class ImageDataModel:
    def __init__(self, db_file):
        self.db = SQLiteCRUD(db_file)

    def insert_images_with_amount(self, table_name, images):
        

    def insert_cluster_names_to_db(self, cluster_names):
        
