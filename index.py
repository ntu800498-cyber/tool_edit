import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tool_Edit import VideoEditorApp

class indexpy:
    def __init__(root,self):
            super().__init__()
            self.title("Chọn Các chức năng")
            self.geometry("400x300")

            # Container chứa tất cả các màn hình
            container = tk.Frame(self)
            container.pack(fill="both", expand=True)

            self.frames = {}

