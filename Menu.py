from operator import index
import tkinter as tk

from index import indexpy
from tool_Edit import VideoEditorApp

# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Chọn Các chức năng")
#         self.geometry("400x300")

#         # Container chứa tất cả các màn hình
#         container = tk.Frame(self)
#         container.pack(fill="both", expand=True)

#         self.frames = {}

#         # Khởi tạo các màn hình
#         for F in (StartPage, SettingsPage):
#             page_name = F.__name__
#             frame = F(parent=container, controller=self)
#             self.frames[page_name] = frame
#             frame.grid(row=0, column=0, sticky="nsew")

#         self.show_frame("StartPage")

#     def show_frame(self, page_name):
#         '''Hiển thị màn hình theo tên'''
#         frame = self.frames[page_name]
#         frame.tkraise() # Đưa màn hình này lên trên cùng

# class StartPage(tk.Frame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         label = tk.Label(self, text="Đây là màn hình chính")
#         label.pack(pady=10)
        
#         button = tk.Button(self, text="Đi đến Cài đặt",
#                            command=lambda: controller.show_frame("SettingsPage"))
#         button.pack()

# class SettingsPage(tk.Frame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         label = tk.Label(self, text="Đây là màn hình cài đặt")
#         label.pack(pady=10)
        
#         button = tk.Button(self, text="Quay lại",
#                            command=lambda: controller.show_frame("StartPage"))
#         button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    # app = indexpy(root)
    app = VideoEditorApp(root)
    root.mainloop()