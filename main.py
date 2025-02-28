import os
import json
import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont

from txt_add import add_text_to_image

class App:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("500x750")
        self.app.title("ScoreGen")
        self.app.resizable(False, False)

        self.font_dirs = [r"C:\\Windows\\Fonts", r"Fonts"]
        self.font_var = tk.StringVar(value="Arial")
        self.font_size_entry = None
        self.textbox1 = None
        self.textbox2 = None
        self.textbox3 = None
        self.textbox4 = None
        self.config_file_entry = None

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_widgets()
        self.app.mainloop()

    def create_widgets(self):
        scrollable_frame = ctk.CTkScrollableFrame(self.app)
        scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

        ctk.CTkLabel(scrollable_frame, text="Enter Details", font=("Arial", 18, "bold")).pack(pady=10)

        font_dropdown = ctk.CTkComboBox(scrollable_frame, values=list(self.get_font_paths(self.font_dirs).keys()), variable=self.font_var, width=300)
        font_dropdown.pack(pady=5)

        self.font_size_entry = ctk.CTkEntry(scrollable_frame, width=300)
        self.font_size_entry.insert(0, "14")
        self.font_size_entry.pack(pady=5)

        self.textbox1 = self.create_labeled_entry(scrollable_frame, "Luwes")
        self.textbox2 = self.create_labeled_entry(scrollable_frame, "Anthony")
        self.textbox3 = self.create_labeled_entry(scrollable_frame, "Julien")
        self.textbox4 = self.create_labeled_entry(scrollable_frame, "Joseph")

        self.config_file_entry = self.create_labeled_entry(scrollable_frame, "Config File Path")
        ctk.CTkButton(scrollable_frame, text="Browse", command=lambda: self.select_file(self.config_file_entry, [("JSON Files", "*.json")], "Select Config File")).pack(pady=5)

        ctk.CTkButton(scrollable_frame, text="Generate", command=self.on_submit).pack(pady=20)

    def create_labeled_entry(self, parent, label_text):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12))
        label.pack(pady=5)
        entry = ctk.CTkEntry(parent, width=300)
        entry.pack(pady=5)
        return entry

    def select_file(self, entry, file_types, title):
        file_path = filedialog.askopenfilename(title=title, filetypes=file_types)
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    def on_submit(self):
        values = {
            "Luwes": self.textbox1.get().strip(),
            "Anthony": self.textbox2.get().strip(),
            "Julien": self.textbox3.get().strip(),
            "Joseph": self.textbox4.get().strip(),
            "Selected Font": self.font_var.get(),
            "Font Size": self.font_size_entry.get().strip()
        }

        selected_font = values["Selected Font"].lower()
        selected_font_path = self.get_font_paths(self.font_dirs).get(selected_font)
        if not selected_font_path:
            messagebox.showerror("Error", "Selected font not found.")
            return

        config_file_path = self.config_file_entry.get().strip()
        if not config_file_path:
            messagebox.showerror("Error", "Please select the config JSON file.")
            return

        config = self.load_json(config_file_path)
        overlay_image_path = config.get("overlay_image_path", "path/to/overlay.png")
        leaderboard_image_path = config.get("leaderboard_image_path", "path/to/leaderboard.png")
        overlay_positions_file_path = config.get("overlay_positions_file_path", "path/to/overlay_positions.json")
        leaderboard_positions_file_path = config.get("leaderboard_positions_file_path", "path/to/leaderboard_positions.json")
        output_folder = config.get("output_folder", "path/to/output/folder")

        overlay_positions = self.load_json(overlay_positions_file_path)
        leaderboard_positions = self.load_json(leaderboard_positions_file_path)

        text_positions = leaderboard_positions.get("text_positions", {})
        value_positions = leaderboard_positions.get("value_positions", {})

        scores = {}
        for name in ["Luwes", "Anthony", "Julien", "Joseph"]:
            try:
                scores[name] = int(values[name])
            except ValueError:
                scores[name] = 0

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        new_text_positions = {}
        new_value_positions = {}
        x_name, x_score, y_start, line_spacing = 550, 1400, 490, 110

        for i, (name, score) in enumerate(sorted_scores):
            new_text_positions[name] = [x_name, y_start + i * line_spacing]
            new_value_positions[name] = [x_score, y_start + i * line_spacing]

        try:
            font_size = int(values["Font Size"])
        except ValueError:
            font_size = 14

        overlay_output_path = os.path.join(output_folder, "overlay.png")
        leaderboard_output_path = os.path.join(output_folder, "leaderboard.png")

        try:
            add_text_to_image(
                overlay_image_path, 
                values, 
                font_path=selected_font_path, 
                font_size=font_size, 
                positions=overlay_positions, 
                output_path=overlay_output_path
            )
            messagebox.showinfo("Success", f"Overlay image saved successfully to {overlay_output_path}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating overlay image: {e}")
            print(e)

        try:
            self.leaderboard_txt(
                leaderboard_image_path, 
                new_text_positions, 
                new_value_positions, 
                scores, 
                font_path=r"Fonts\Genflox.ttf", 
                font_size=70, 
                output_path=leaderboard_output_path
            )
            messagebox.showinfo("Success", f"Leaderboard image saved successfully to {leaderboard_output_path}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating leaderboard image: {e}")
            print(e)

    def leaderboard_txt(self, image_path, text_positions, value_positions, scores, font_path, font_size=70, output_path="leaderboard.png"):
        color_mapping = {
            "Luwes": (255, 165, 0, 255),   # orange
            "Anthony": (255, 255, 0, 255),  # yellow
            "Julien": (0, 255, 0, 255),     # green
            "Joseph": (0, 0, 255, 255)      # blue
        }
        
        image = Image.open(image_path).convert('RGBA')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, font_size)

        for name, pos in text_positions.items():
            color = color_mapping.get(name, (0, 0, 0, 255))
            draw.text(tuple(pos), f"{name}:", fill=color, font=font)

        for name, pos in value_positions.items():
            color = color_mapping.get(name, (0, 0, 0, 255))
            draw.text(tuple(pos), str(scores.get(name, "0")), fill=color, font=font)

        image.save(output_path, 'PNG')

    def load_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON from {file_path}: {e}")
            return {}

    def get_font_paths(self, font_dirs):
        font_paths = {}
        for font_dir in font_dirs:
            if os.path.exists(font_dir):
                for font_file in os.listdir(font_dir):
                    if font_file.lower().endswith((".ttf", ".otf")):
                        font_name = os.path.splitext(font_file)[0].lower()
                        font_paths[font_name] = os.path.join(font_dir, font_file)
        return font_paths

if __name__ == "__main__":
    App()