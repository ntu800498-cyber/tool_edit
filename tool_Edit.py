import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import threading
import sys
import json

class VideoEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Editor")
        self.root.geometry("750x700")

        self.input_folder = ""
        self.output_folder = ""
        self.logo_path = ""
        self.overlay_video_path = ""
        self.processing_thread = None

        # --- UI Elements ---
        tk.Label(root, text="Đường dẫn vào:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.input_folder_entry = tk.Entry(root, width=50, state="readonly")
        self.input_folder_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_input_folder).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(root, text="Đường dẫn ra:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.output_folder_entry = tk.Entry(root, width=50, state="readonly")
        self.output_folder_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_output_folder).grid(row=1, column=2, padx=5, pady=5)

        tk.Frame(root, height=10).grid(row=2, column=0, columnspan=3)
        tk.Label(root, text="Operations:", font=('Arial', 12, 'bold')).grid(row=3, column=0, columnspan=3, sticky="w",
                                                                            padx=5, pady=5)

        # Mirroring
        self.mirror_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Mirror Video (Horizontal)", variable=self.mirror_var).grid(row=4, column=1,
                                                                                              sticky="w", padx=5)

        # Speed Control
        tk.Label(root, text="Speed:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.speed_var = tk.StringVar(value="1.1") # Default to 1.0
        self.speed_options = [f"{i / 10:.1f}" for i in range(5, 21)]  # 0.5 to 2.0
        self.speed_menu = ttk.Combobox(root, textvariable=self.speed_var, values=self.speed_options, state="readonly",
                                       width=10)
        self.speed_menu.grid(row=5, column=1, sticky="w", padx=5)

        # Zoom Control
        tk.Label(root, text="Zoom Factor:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.zoom_factor_var = tk.StringVar(value="1.2")
        self.zoom_factor_options = [f"{i/10:.1f}" for i in range(10, 21)] 
        self.zoom_factor_menu = ttk.Combobox(root, textvariable=self.zoom_factor_var, values=self.zoom_factor_options,
                                             state="readonly", width=10)
        self.zoom_factor_menu.grid(row=6, column=1, sticky="w", padx=5)

        # Brightness Control
        tk.Label(root, text="Brightness Reduction:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.brightness_reduction_var = tk.StringVar(value="0%") 
        self.brightness_reduction_options = [f"{i}%" for i in range(0, 100, 10)]
        self.brightness_reduction_menu = ttk.Combobox(root, textvariable=self.brightness_reduction_var,
                                                      values=self.brightness_reduction_options, state="readonly",
                                                      width=10)
        self.brightness_reduction_menu.grid(row=7, column=1, sticky="w", padx=5)

        tk.Label(root, text="Insert Logo:").grid(row=8, column=0, padx=5, pady=5, sticky="w")

        self.logo_path_entry = tk.Entry(root, width=50, state="readonly")

        self.logo_path_entry.grid(row=8, column=1, padx=5, pady=5)

        tk.Button(root, text="Browse Logo", command=self.browse_logo).grid(row=8, column=2, padx=5, pady=5)
        self.use_logo_var = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Use Logo", variable=self.use_logo_var).grid(row=9, column=0, sticky="w", padx=5)

        tk.Label(root, text="Logo Opacity:").grid(row=10, column=0, padx=5, pady=5, sticky="w")
        self.logo_opacity_var = tk.StringVar(value="1.0") # 1.0 is fully opaque, 0.5 is 50% transparent
        self.logo_opacity_options = [f"{i/10:.1f}" for i in range(0, 11)] # 0.0 to 1.0
        self.logo_opacity_menu = ttk.Combobox(root, textvariable=self.logo_opacity_var, values=self.logo_opacity_options,
                                              state="readonly", width=10)
        self.logo_opacity_menu.grid(row=10, column=1, sticky="w", padx=5)

        tk.Label(root, text="Insert Video Overlay:").grid(row=11, column=0, padx=5, pady=5, sticky="w")
        self.overlay_video_entry = tk.Entry(root, width=50, state="readonly")
        self.overlay_video_entry.grid(row=11, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse Video", command=self.browse_overlay_video).grid(row=11, column=2, padx=5, pady=5)
        self.use_overlay_video_var = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Use Video Overlay", variable=self.use_overlay_video_var).grid(row=12, column=0, sticky="w", padx=5)

        tk.Label(root, text="Overlay Video Opacity:").grid(row=13, column=0, padx=5, pady=5, sticky="w")
        self.overlay_video_opacity_var = tk.StringVar(value="0.7") # Default to 70% opaque
        self.overlay_video_opacity_options = [f"{i/10:.1f}" for i in range(0, 11)] # 0.0 to 1.0
        self.overlay_video_opacity_menu = ttk.Combobox(root, textvariable=self.overlay_video_opacity_var, values=self.overlay_video_opacity_options,
                                                       state="readonly", width=10)
        self.overlay_video_opacity_menu.grid(row=13, column=1, sticky="w", padx=5)

        tk.Label(root, text="Quality Preset:").grid(row=14, column=0, padx=5, pady=5, sticky="w")
        self.quality_var = tk.StringVar(value="ultrafast")
        self.quality_options = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower",
                                "veryslow"]
        self.quality_menu = ttk.Combobox(root, textvariable=self.quality_var, values=self.quality_options,
                                         state="readonly", width=10)
        self.quality_menu.grid(row=14, column=1, sticky="w", padx=5)

        self.aspect_ratio_label = tk.Label(root, text="Output Aspect Ratio: 9:16 (Fixed)", font=('Arial', 10, 'italic'))
        self.aspect_ratio_label.grid(row=15, column=0, columnspan=3, sticky="w", padx=5, pady=5)

        self.process_button = tk.Button(root, text="Process Videos", command=self.start_processing)
        self.process_button.grid(row=16, column=1, pady=20)

        self.status_label = tk.Label(root, text="Status: Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=17, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

    def browse_input_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.input_folder = folder_selected
            self.input_folder_entry.config(state="normal")
            self.input_folder_entry.delete(0, tk.END)
            self.input_folder_entry.insert(0, self.input_folder)
            self.input_folder_entry.config(state="readonly")

    def browse_output_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_folder = folder_selected
            self.output_folder_entry.config(state="normal")
            self.output_folder_entry.delete(0, tk.END)
            self.output_folder_entry.insert(0, self.output_folder)
            self.output_folder_entry.config(state="readonly")

    def browse_logo(self):
        file_selected = filedialog.askopenfilename(
            title="Select Logo Image",
            filetypes=(("Image Files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
        )
        if file_selected:
            self.logo_path = file_selected
            self.logo_path_entry.config(state="normal")
            self.logo_path_entry.delete(0, tk.END)
            self.logo_path_entry.insert(0, self.logo_path)  
            self.logo_path_entry.config(state="readonly")
            self.use_logo_var.set(True)

    def browse_overlay_video(self):
        file_selected = filedialog.askopenfilename(
            title="Select Overlay Video",
            filetypes=(("MP4 Files", "*.mp4"), ("All files", "*.*"))
        )
        if file_selected:
            self.overlay_video_path = file_selected
            self.overlay_video_entry.config(state="normal")
            self.overlay_video_entry.delete(0, tk.END)
            self.overlay_video_entry.insert(0, self.overlay_video_path)
            self.overlay_video_entry.config(state="readonly")
            self.use_overlay_video_var.set(True)

    def update_status(self, message):
        max_status_length = 100
        if len(message) > max_status_length:
            truncated_message = message[:max_status_length - 3] + "..."
        else:
            truncated_message = message
        self.root.after(0, lambda: self.status_label.config(text=f"Status: {truncated_message}"))

    def start_processing(self):
        if self.processing_thread and self.processing_thread.is_alive():
            messagebox.showwarning("Processing Active", "Video processing is already in progress.")
            return

        if not self.input_folder or not self.output_folder:
            messagebox.showwarning("Input Error", "Please select both input and output folders.")
            return

        if self.use_logo_var.get() and not self.logo_path:
            messagebox.showwarning("Logo Error", "Please select a logo file if 'Use Logo' is checked.")
            return

        if self.use_overlay_video_var.get() and not self.overlay_video_path:
            messagebox.showwarning("Overlay Video Error", "Please select an overlay video file if 'Use Video Overlay' is checked.")
            return

        self.process_button.config(state=tk.DISABLED)
        self.update_status("Gathering files...")

        self.processing_thread = threading.Thread(target=self.process_videos)
        self.processing_thread.start()

    def get_video_info(self, video_path):
        """Gets video dimensions using ffprobe."""
        try:
            command = [
                "ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=width,height,avg_frame_rate",
                "-of", "json", video_path
            ]
            result = subprocess.run(command, capture_output=True, encoding='utf-8', check=True)
            data = json.loads(result.stdout)
            if data and 'streams' in data and len(data['streams']) > 0:
                stream = data['streams'][0]
                width = stream.get('width')
                height = stream.get('height')
                avg_frame_rate = stream.get('avg_frame_rate', '30/1')
                return width, height, avg_frame_rate
            return None, None, None
        except FileNotFoundError:
            self.update_status("ffprobe not found. Please install FFmpeg.")
            messagebox.showerror("FFmpeg Error", "ffprobe executable not found. Please ensure FFmpeg is installed and in your system's PATH.")
            return None, None, None
        except subprocess.CalledProcessError as e:
            error_message = f"Error getting video info for {os.path.basename(video_path)}:\n{e.stderr}"
            self.update_status(f"Error getting info for {os.path.basename(video_path)}")
            messagebox.showerror("FFprobe Error", error_message)
            return None, None, None
        except Exception as e:
            error_message = f"An unexpected error occurred getting video info for {os.path.basename(video_path)}:\n{e}"
            self.update_status(f"Unexpected error getting info for {os.path.basename(video_path)}")
            messagebox.showerror("Processing Error", error_message)
            return None, None, None

    def process_videos(self):
        video_files = [f for f in os.listdir(self.input_folder) if
                       os.path.isfile(os.path.join(self.input_folder, f)) and f.lower().endswith(
                           ('.mp4', '.avi', '.mov', '.mkv'))]
        print(f"dddđ",video_files.count)

        if not video_files:
            self.update_status("No video files found in the input folder.")
            messagebox.showinfo("No Videos", "No video files found in the input folder.")
            self.root.after(0, lambda: self.process_button.config(state=tk.NORMAL))
            return

        self.update_status(f"Found {len(video_files)} videos. Starting processing...")

        for i, video_file in enumerate(video_files):
            input_path = os.path.join(self.input_folder, video_file)
            output_filename = f"processed_9x16_{video_file}"
            output_path = os.path.join(self.output_folder, output_filename)

            original_width, original_height, avg_frame_rate = self.get_video_info(input_path)

            if original_width is None or original_height is None:
                self.update_status(f"Skipping {video_file} due to info retrieval error.")
                continue
         
            filter_complex_parts = []
          
            video_stream_in = "[0:v]"
            audio_stream_in = "[0:a]"
      
            target_width = 1080
            target_height = 1440 
           
            video_filters_list = []
            zoom_factor = float(self.zoom_factor_var.get())
            speed_factor = float(self.speed_var.get())

          
            scale_w_covered = target_width * zoom_factor
            scale_h_covered = target_height * zoom_factor

          

            scale_filter_str = f"scale={scale_w_covered}:{scale_h_covered}:force_original_aspect_ratio=increase"
            video_filters_list.append(scale_filter_str)

          
            crop_x = f"iw/2 - {target_width}/2" # iw = input width, ih = input height
            crop_y = f"ih/2 - {target_height}/2"
            crop_filter_str = f"crop={target_width}:{target_height}:{crop_x}:{crop_y}"
            video_filters_list.append(crop_filter_str)


            if self.mirror_var.get():
                video_filters_list.append("hflip")

            if speed_factor != 1.0:
                pts_value = 1.0 / speed_factor
                video_filters_list.append(f"setpts={pts_value}*PTS")

            brightness_reduction_percent_str = self.brightness_reduction_var.get().replace('%', '')
            brightness_reduction_percent = int(brightness_reduction_percent_str)
            if brightness_reduction_percent > 0:
                brightness_factor = 1.0 - (brightness_reduction_percent / 100.0)
                brightness_factor = max(0.0, min(1.0, brightness_factor))
                video_filters_list.append(f"eq=brightness={brightness_factor}")

           
            if video_filters_list:
                filter_complex_parts.append(f"{video_stream_in}{','.join(video_filters_list)}[video_filtered]")
                current_video_stream = "[video_filtered]"
            else:
                current_video_stream = video_stream_in
          
            logo_input_index = 1 
            logo_stream_name = None 
            if self.use_logo_var.get() and self.logo_path:
                logo_opacity = float(self.logo_opacity_var.get())
                filter_complex_parts.append(f"[{logo_input_index}:v]format=rgba,colorchannelmixer=aa={logo_opacity}[logo_with_opacity]")
                logo_stream_name = "[logo_with_opacity]"

          
            if logo_stream_name:
                overlay_x = "main_w-overlay_w-10"
                overlay_y = "main_h-overlay_h-10"
                filter_complex_parts.append(f"{current_video_stream}{logo_stream_name}overlay={overlay_x}:{overlay_y}[video_with_logo]")
                current_video_stream = "[video_with_logo]" 

            overlay_video_input_index = 1
            if self.use_logo_var.get() and self.logo_path:
                overlay_video_input_index = 2 

            overlay_video_stream_name = None 
            if self.use_overlay_video_var.get() and self.overlay_video_path:
                overlay_video_opacity = float(self.overlay_video_opacity_var.get())
               
                filter_complex_parts.append(f"[{overlay_video_input_index}:v]format=rgba,colorchannelmixer=aa={overlay_video_opacity}[overlay_video_with_opacity]")
                overlay_video_stream_name = "[overlay_video_with_opacity]" 

          
            if overlay_video_stream_name: 
                overlay_video_x = "main_w-overlay_w-10"
                overlay_video_y = "main_h-overlay_h-10"
                filter_complex_parts.append(f"{current_video_stream}{overlay_video_stream_name}overlay={overlay_video_x}:{overlay_video_y}[video_with_overlay]")
                current_video_stream = "[video_with_overlay]"

            final_video_stream_name = current_video_stream 

          
            audio_filters_list = []
            if speed_factor != 1.0:
                if 0.5 <= speed_factor <= 2.0:
                    audio_filters_list.append(f"atempo={speed_factor}")
                else:
                    current_tempo = speed_factor
                    while current_tempo > 2.0:
                        audio_filters_list.append("atempo=2.0")
                        current_tempo /= 2.0
                    if current_tempo >= 0.5:
                        audio_filters_list.append(f"atempo={current_tempo}")

            if audio_filters_list:
                filter_complex_parts.append(f"{audio_stream_in}{','.join(audio_filters_list)}[final_audio]")
                final_audio_stream_name = "[final_audio]"
            else:
                final_audio_stream_name = audio_stream_in


            full_command = ["ffmpeg"]

           
            full_command.extend(["-i", input_path])

          
            if self.use_logo_var.get() and self.logo_path:
                full_command.extend(["-i", self.logo_path])

          
            if self.use_overlay_video_var.get() and self.overlay_video_path:
                full_command.extend(["-i", self.overlay_video_path])

           
            if filter_complex_parts:
                full_command.extend(["-filter_complex", ";".join(filter_complex_parts)])

        
            if final_video_stream_name:
                full_command.extend(["-map", final_video_stream_name])
            else:
                self.update_status(f"Error: No final video stream defined for {video_file}.")
                messagebox.showerror("Processing Error", f"Could not define final video stream for {video_file}.")
                continue

            if final_audio_stream_name:
                full_command.extend(["-map", final_audio_stream_name])

       
            full_command.extend(["-c:v", "libx264"])
            full_command.extend(["-preset", self.quality_var.get()])
            full_command.extend(["-c:a", "aac"])
            full_command.extend(["-strict", "experimental"])

            full_command.append(output_path)

            try:
                self.update_status(f"Processing {video_file} ({i + 1}/{len(video_files)})")
                print(f"Executing FFmpeg command: {' '.join(full_command)}") # Debugging

                process = subprocess.run(
                    full_command,
                    capture_output=True,
                    encoding='utf-8',
                    errors='replace',
                    check=True
                )
                print(f"Successfully processed {video_file}:\n{process.stdout}")
            except subprocess.CalledProcessError as e:
                error_message = f"Error processing {video_file}:\n\nFFmpeg stderr:\n{e.stderr}\n\nFFmpeg stdout:\n{e.stdout}"
                self.update_status(f"Error processing {video_file}")
                messagebox.showerror("Processing Error", error_message)
            except FileNotFoundError:
                self.update_status("FFmpeg not found. Please install FFmpeg.")
                messagebox.showerror("FFmpeg Error",
                                     "FFmpeg executable not found. Please ensure FFmpeg is installed and in your system's PATH.")
                break
            except Exception as e:
                error_message = f"An unexpected error occurred with {video_file}:\n{e}"
                self.update_status(f"Unexpected error with {video_file}")
                messagebox.showerror("Processing Error", error_message)

        self.root.after(0, lambda: self.process_button.config(state=tk.NORMAL))
        self.update_status("Processing complete!")
        messagebox.showinfo("Complete", "All videos have been processed.")



