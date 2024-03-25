from src.disko.sqlite import SQLiteCRUD

class ImageDataModel:
    def __init__(self, image_controller, db_file):
        self.db = SQLiteCRUD(db_file)
        self.controller = image_controller

    def insert_images_with_amount(self, table_name):
        images = self.db.select_column(table_name, 'image_name')
        amount = self.controller.calculate_amount_per_registry(images)
        for registry, count in amount.items():
            self.db.insert_data(table_name, (registry, count))

    def insert_cluster_names_to_db(self):
        cluster_names = self.controller.get_kubernetes_clusters()
        for cluster_name in cluster_names:
            self.db.insert_data('clusters', (cluster_name,))
