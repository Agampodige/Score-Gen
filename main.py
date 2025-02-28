import os
import json
import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import filedialog
from txt_add import add_text_to_image, leaderboard_txt  # Ensure this module exists

def load_config(json_file_path):
    """Load configuration from a JSON file."""
    try:
        with open(json_file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {
            "overlay_image_path": "path/to/overlay.png",
            "leaderboard_image_path": "path/to/leaderboard.png",
            "overlay_positions_file_path": "path/to/overlay_positions.json",
            "leaderboard_positions_file_path": "path/to/leaderboard_positions.json",
            "output_folder": "path/to/output/folder"
        }

def load_positions(positions_file_path):
    """Load positions from a JSON file."""
    try:
        with open(positions_file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading positions: {e}")
        return {}  # Return an empty dictionary if there is an error

def get_font_paths(font_dirs):
    """Retrieve available font paths from given directories."""
    font_paths = {}
    for font_dir in font_dirs:
        if os.path.exists(font_dir):
            for font_file in os.listdir(font_dir):
                if font_file.lower().endswith((".ttf", ".otf")):
                    font_name = os.path.splitext(font_file)[0].lower()
                    font_paths[font_name] = os.path.join(font_dir, font_file)
    return font_paths

def get_installed_fonts(font_dirs):
    """Retrieve a list of available font names."""
    return list(get_font_paths(font_dirs).keys())

def create_labeled_entry(parent, label_text):
    """Create a labeled text entry widget."""
    label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12))
    label.pack(pady=5)
    entry = ctk.CTkEntry(parent, width=300)
    entry.pack(pady=5)
    return entry

def select_file(entry, file_types, title):
    """Allow the user to select a file and update entry widget."""
    file_path = filedialog.askopenfilename(title=title, filetypes=file_types)
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def on_submit():
    """Handle the submit button action."""
    global font_size_entry  # Ensure font_size_entry is defined globally

    # Get user input
    values = {
        "Luwes": textbox1.get().strip(),
        "Anthony": textbox2.get().strip(),
        "Julien": textbox3.get().strip(),
        "Joseph": textbox4.get().strip(),
        "Selected Font": font_var.get(),
        "Font Size": font_size_entry.get().strip()
    }

    selected_font = values["Selected Font"].lower()
    selected_font_path = get_font_paths(font_dirs).get(selected_font)

    if not selected_font_path:
        messagebox.showerror("Error", "Selected font not found.")
        return

    config_file_path = config_file_entry.get().strip()

    if not config_file_path:
        messagebox.showerror("Error", "Please select the config JSON file.")
        return

    # Load config from JSON
    config = load_config(config_file_path)

    overlay_image_path = config["overlay_image_path"]
    leaderboard_image_path = config["leaderboard_image_path"]
    overlay_positions_file_path = config["overlay_positions_file_path"]
    leaderboard_positions_file_path = config["leaderboard_positions_file_path"]
    output_folder = config["output_folder"]

    # Load positions from respective JSON files
    overlay_positions = load_positions(overlay_positions_file_path)
    leaderboard_positions = load_positions(leaderboard_positions_file_path)

    # Validate and convert scores to integers
    try:
        scores = {name: int(score) for name, score in values.items() if name in overlay_positions and score.isdigit()}
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for scores.")
        return

    # Sort scores in ascending order
    sorted_texts = [(f"{name}: {score}", tuple(leaderboard_positions.get(name, [50, 50]))) for name, score in sorted(scores.items(), key=lambda x: x[1])]

    # Convert font size
    try:
        font_size = int(values["Font Size"])
    except ValueError:
        font_size = 14  # Default font size

    # Define output paths
    overlay_output_path = os.path.join(output_folder, "overlay.png")
    leaderboard_output_path = os.path.join(output_folder, "leaderboard.png")

    # Generate overlay image
    try:
        add_text_to_image(overlay_image_path, values, font_path=selected_font_path, font_size=font_size, positions=overlay_positions, output_path=overlay_output_path)
        messagebox.showinfo("Success", f"Overlay image saved successfully to {overlay_output_path}.")
    except Exception as e:
        messagebox.showerror("Error", f"Error generating overlay image: {e}")
        print(e)

    # Generate leaderboard image
    try:
        leaderboard_txt(leaderboard_image_path, sorted_texts, font_path=selected_font_path, font_size=font_size, output_path=leaderboard_output_path)
        messagebox.showinfo("Success", f"Leaderboard image saved successfully to {leaderboard_output_path}.")
    except Exception as e:
        messagebox.showerror("Error", f"Error generating leaderboard image: {e}")
        print(e)

def main():
    """Initialize and run the application."""
    global textbox1, textbox2, textbox3, textbox4, font_var
    global config_file_entry, font_dirs, font_size_entry

    font_dirs = [r"C:\\Windows\\Fonts", r"Fonts"]
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.geometry("500x750")
    app.title("ScoreGen")
    app.resizable(False, False)

    scrollable_frame = ctk.CTkScrollableFrame(app)
    scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

    ctk.CTkLabel(scrollable_frame, text="Enter Details", font=("Arial", 18, "bold")).pack(pady=10)

    font_var = tk.StringVar(value="Arial")
    font_dropdown = ctk.CTkComboBox(scrollable_frame, values=get_installed_fonts(font_dirs), variable=font_var, width=300)
    font_dropdown.pack(pady=5)

    font_size_entry = ctk.CTkEntry(scrollable_frame, width=300)
    font_size_entry.insert(0, "14")
    font_size_entry.pack(pady=5)

    textbox1 = create_labeled_entry(scrollable_frame, "Luwes")
    textbox2 = create_labeled_entry(scrollable_frame, "Anthony")
    textbox3 = create_labeled_entry(scrollable_frame, "Julien")
    textbox4 = create_labeled_entry(scrollable_frame, "Joseph")

    config_file_entry = create_labeled_entry(scrollable_frame, "Config File Path")
    ctk.CTkButton(scrollable_frame, text="Browse", command=lambda: select_file(config_file_entry, [("JSON Files", "*.json")], "Select Config File")).pack(pady=5)

    ctk.CTkButton(scrollable_frame, text="Generate", command=on_submit).pack(pady=20)
    app.mainloop()

if __name__ == "__main__":
    main()
