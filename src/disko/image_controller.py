# controller.py
from kubernetes import config
from model import ImageDataModel
import docker


class ImageController:
    def __init__(self, db_file):
        self.model = ImageDataModel(db_file)
        self.docker_client = docker.from_env()

    def get_kubernetes_clusters(self):
        try:
            config.load_kube_config()
            contexts, _ = config.list_kube_config_contexts()
            cluster_names = [context["context"]["cluster"] for context in contexts]
            return cluster_names
        except Exception as e:
            print("Error:", e)
            return []

    def is_from_dockerhub(self, image):
        parts = image.split('/')
        if len(parts) == 1:
            return True
        if '.' not in parts[0] and ':' not in parts[0]:
            return True
        if 'docker.io' in parts[0]:
            return True
        return False

    def calculate_amount_per_registry(self, images):

    def calculate_percentages(self, table_name):

    def transfer_image(self, image, new_registry, tag, username, password):

    def copy_images(self, images, new_registry, tag, username, password):

    def export_sha256(self, image_name, image_tag):
