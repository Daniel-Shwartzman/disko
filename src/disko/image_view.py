# view.py
import tkinter as tk
from tkinter import ttk, messagebox
import time
from src.mvc.controller import ImageController

class ImageRegistryManager:
    def __init__(self, db_file):
        self.controller = ImageController(db_file)
        self.root = tk.Tk()
        self.root.title("Image Registry Manager")
        self.root.style = ttk.Style()
        self.root.style.theme_use('clam')
        self.columns = ['Registry Name', 'Number of Images', 'Percentage']
        self.treeview = None
        self.checkboxes = {col: tk.BooleanVar(value=True) for col in self.columns}
        self.selected_cluster = None
        self.pull_username = None
        self.pull_password = None
        self.push_username = None
        self.push_password = None
        self.listbox = None
        self.push_tag = None
        self.selected_images = []
        

    def display_image_data(self, table_name):

    def cluster_selection(self, clusters):

    def confirm_cluster_selection(self, selected_cluster, cluster_selection_window):

    def create_images_table_screen(self):

    def update_columns(self):
    
    def select_docker_images(self):

    def confirm_image_selection(self, selected_indices, select_images_window):
    
    def registry_input_screen(self, selected_images):

    def submit_registry_details(self, pull_username, pull_password, push_username, push_password, push_url, push_tag, selected_images, window):

    def run(self):
