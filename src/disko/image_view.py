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
        image_names = self.controller.model.db.select_all(self.selected_cluster)

        window_width = 700
        window_height = 300

        select_images_window = tk.Toplevel(self.root)
        select_images_window.title("Select Docker Images")
        select_images_window.geometry(f"{window_width}x{window_height}")

        label = ttk.Label(select_images_window, text="Please select Docker images:")
        label.pack()

        max_text_width = max(len(name) for name in image_names)
        listbox_width = min(max_text_width * 10, 300)

        self.listbox = tk.Listbox(select_images_window, selectmode=tk.MULTIPLE, width=listbox_width)
        for name in image_names:
            self.listbox.insert(tk.END, name)
        self.listbox.pack(expand=True, fill='both')

        confirm_button = ttk.Button(select_images_window, text="Confirm", command=lambda: self.confirm_image_selection(self.listbox.curselection(), select_images_window))
        confirm_button.pack()

    def confirm_image_selection(self, selected_indices, select_images_window):
        if selected_indices:
            selected_images = [self.listbox.get(index) for index in selected_indices]
            self.registry_input_screen(selected_images)
            select_images_window.destroy()
        else:
            messagebox.showerror("Error", "Please select Docker images.")
    
    def registry_input_screen(self, selected_images):
        registry_input_window = tk.Toplevel(self.root)
        registry_input_window.title("Registry Input")
        
        pull_label = ttk.Label(registry_input_window, text="Pulling Registry:")
        pull_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        pull_username_label = ttk.Label(registry_input_window, text="Username:")
        pull_username_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        pull_username_entry = ttk.Entry(registry_input_window)
        pull_username_entry.grid(row=1, column=1, padx=5, pady=5)
        pull_password_label = ttk.Label(registry_input_window, text="Password:")
        pull_password_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        pull_password_entry = ttk.Entry(registry_input_window, show="*")
        pull_password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        push_url_label = ttk.Label(registry_input_window, text="Pushing Registry URL:")
        push_url_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        push_url_entry = ttk.Entry(registry_input_window)
        push_url_entry.grid(row=3, column=1, padx=5, pady=5)
        
        push_username_label = ttk.Label(registry_input_window, text="Username:")
        push_username_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        push_username_entry = ttk.Entry(registry_input_window)
        push_username_entry.grid(row=4, column=1, padx=5, pady=5)
        
        push_password_label = ttk.Label(registry_input_window, text="Password:")
        push_password_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        push_password_entry = ttk.Entry(registry_input_window, show="*")
        push_password_entry.grid(row=5, column=1, padx=5, pady=5)

        push_tag_label = ttk.Label(registry_input_window, text="tag:")
        push_tag_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        push_tag_entry = ttk.Entry(registry_input_window)
        push_tag_entry.grid(row=6, column=1, padx=5, pady=5)
        
        submit_button = ttk.Button(registry_input_window, text="Submit", command=lambda: self.submit_registry_details(
            pull_username_entry.get(), pull_password_entry.get(), push_username_entry.get(), push_password_entry.get(),
            push_url_entry.get(), push_tag_entry.get(), selected_images, registry_input_window))
        submit_button.grid(row=7, column=0, columnspan=2, pady=10)

    def submit_registry_details(self, pull_username, pull_password, push_username, push_password, push_url, push_tag, selected_images, window):
        self.pull_username = pull_username
        self.pull_password = pull_password
        self.push_username = push_username
        self.push_password = push_password
        self.push_url = push_url
        self.push_tag = push_tag
        self.selected_images = selected_images
        self.controller.copy_images(self.selected_images, self.push_url, self.push_tag, self.push_username, self.push_password)
        
        window.destroy()

        time.sleep(20)
        self.root.destroy()

    def run(self):
        frame = ttk.Frame(self.root, style='DarkFrame.TFrame')
        frame.pack(padx=100, pady=100)

        self.treeview = ttk.Treeview(frame, columns=self.columns, show='headings', style='Custom.Treeview')
        for col in self.columns:
            self.treeview.heading(col, text=col)

        self.treeview.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.treeview.yview)
        scrollbar.pack(side='right', fill='y')
        self.treeview.configure(yscrollcommand=scrollbar.set)

        cluster_names = self.controller.get_kubernetes_clusters()

        button_select_cluster = ttk.Button(self.root, text="Select Cluster", command=lambda: self.cluster_selection(cluster_names), style='Custom.TButton')
        button_select_cluster.pack(pady=10)
        
        button_change_registry = ttk.Button(self.root, text="Change Registry", command=self.select_docker_images, style='Custom.TButton')
        button_change_registry.pack(pady=10)

        button_export = ttk.Button(self.root, text="Export", command=self.select_docker_images, style='Custom.TButton')
        button_export.pack(pady=10)

        button_show_images_table = ttk.Button(self.root, text="Show Images Table", command=self.create_images_table_screen, style='Custom.TButton')
        button_show_images_table.pack(pady=10)
        self.root.mainloop()
        
