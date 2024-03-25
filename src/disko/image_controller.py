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
        amount = {}
        for image_tuple in images:
            registry = image_tuple[2]
            amount[registry] = amount.get(registry, 0) + 1
        return amount

    def calculate_percentages(self, table_name):
        image_data = self.model.db.select_all(table_name)
        amounts = self.calculate_amount_per_registry(image_data)
        total_images = sum(amounts.values())
        percentages = [(registry, amount, (amount / total_images) * 100) for registry, amount in amounts.items()]
        return percentages


    def transfer_image(self, image, new_registry, tag, username, password):
        self.docker_client.login(username=username, password=password)
        pulled_image = self.docker_client.images.pull(image)
        if pulled_image:
            print(f"Image {image} pulled successfully")
        new_image_tag = f"{new_registry}:{tag}"
        pulled_image.tag(new_image_tag)
        push = self.docker_client.images.push(new_image_tag)
        if push:
            print(f"Image {image} pushed to {new_registry}")
        else:
            print(f"Failed to push image {image} to {new_registry}")

    def copy_images(self, images, new_registry, tag, username, password):
        for image_tuple in images:
            image = image_tuple[0]
            image_name, image_tag = image.split(":")
            self.transfer_image(image_name, new_registry, tag, username, password)
            self.export_sha256(image_name, image_tag)

    def export_sha256(self, image_name, image_tag):
        sha256_hash = hashlib.sha256(f"{image_name}:{image_tag}".encode()).hexdigest()
        with open("sha256_hashes.txt", "a") as file:
            file.write(f"{image_name}:{image_tag} - SHA256: {sha256_hash}\n")
