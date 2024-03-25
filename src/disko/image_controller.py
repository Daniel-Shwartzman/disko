# controller.py
from kubernetes import config
from model import ImageDataModel
import docker


class ImageController:
    def __init__(self, db_file):
        self.model = ImageDataModel(db_file)
        self.docker_client = docker.from_env()
        
    def get_kubernetes_clusters(self):

    def is_from_dockerhub(self, image):

    def calculate_amount_per_registry(self, images):

    def calculate_percentages(self, table_name):

    def transfer_image(self, image, new_registry, tag, username, password):

    def copy_images(self, images, new_registry, tag, username, password):

    def export_sha256(self, image_name, image_tag):
