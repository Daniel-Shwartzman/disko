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
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        image_data = self.controller.model.db.select_all(table_name)

        registry_amount = self.controller.calculate_amount_per_registry(image_data)
        percentages = self.controller.calculate_percentages(table_name)

        for registry, num_images in registry_amount.items():
            percentage = next((p[2] for p in percentages if p[0] == registry), 0)
            self.treeview.insert('', 'end', values=(registry, num_images, f"{percentage:.0f}%"))

    def cluster_selection(self, clusters):
        cluster_selection_window = tk.Toplevel(self.root)
        cluster_selection_window.title("Cluster Selection")
        cluster_selection_window.lift()
        cluster_selection_window.focus_force()

        label = ttk.Label(cluster_selection_window, text="Please select a cluster:")
        label.pack()
        cluster_var = tk.StringVar()
        cluster_combobox = ttk.Combobox(cluster_selection_window, textvariable=cluster_var, values=clusters)
        cluster_combobox.pack()

        confirm_button = ttk.Button(cluster_selection_window, text="Confirm", command=lambda: self.confirm_cluster_selection(cluster_var.get(), cluster_selection_window))
        confirm_button.pack()

    def confirm_cluster_selection(self, selected_cluster, cluster_selection_window):
        if selected_cluster:
            cluster_selection_window.destroy()
            self.controller.model.db.create_table(selected_cluster)
            self.display_image_data(selected_cluster)
            self.selected_cluster = selected_cluster
        else:
            messagebox.showerror("Error", "Please select a cluster.")

    def create_images_table_screen(self):
        images_table_window = tk.Toplevel(self.root)
        images_table_window.title("Images Table")

        frame = ttk.Frame(images_table_window, style='DarkFrame.TFrame')
        frame.pack(padx=20, pady=20)

        self.treeview = ttk.Treeview(frame, columns=['Image', 'TimeStamp'], show='headings', style='Custom.Treeview')
        self.treeview.heading('Image', text='Image')
        self.treeview.heading('TimeStamp', text='TimeStamp')
        self.treeview.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.treeview.yview)
        scrollbar.pack(side='right', fill='y')
        self.treeview.configure(yscrollcommand=scrollbar.set)

        if self.selected_cluster:
            image_data = self.controller.model.db.select_all(self.selected_cluster)

            for image in image_data:
                self.treeview.insert('', 'end', values=(image[0], image[1]))
        else:
            messagebox.showerror("Error", "No cluster selected.")

    def update_columns(self):
        selected_columns = [column.get() for column in self.checkboxes.values()]
        for col in self.columns:
            if col in selected_columns:
                self.treeview.column(col, display=True)
            else:
                self.treeview.column(col, display=False)
        
    
    def select_docker_images(self):

    def confirm_image_selection(self, selected_indices, select_images_window):
    
    def registry_input_screen(self, selected_images):

    def submit_registry_details(self, pull_username, pull_password, push_username, push_password, push_url, push_tag, selected_images, window):

    def run(self):
