import os
import json
import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import filedialog
from txt_add import add_text_to_image

def get_font_paths(font_dirs):
    font_paths = {}
    for font_dir in font_dirs:
        if os.path.exists(font_dir):  # Check if the directory exists
            for font_file in os.listdir(font_dir):
                if font_file.lower().endswith(('.ttf', '.otf', '.ttc')):
                    font_name = os.path.splitext(font_file)[0]
                    font_paths[font_name.lower()] = os.path.join(font_dir, font_file)  # Store keys in lowercase
    return font_paths

def get_installed_fonts(font_dirs):
    return sorted(get_font_paths(font_dirs).keys())

def apply_selected_font():
    """Apply the selected font to textboxes and keep the UI unchanged."""
    selected_font = font_var.get()
    size_str = font_size_entry.get().strip()
    
    # Set default font size if input is invalid
    try:
        size = int(size_str) if size_str.isdigit() else 14
    except ValueError:
        size = 14

    if selected_font:
        # Apply font style to textboxes and preview label
        textbox1.configure(font=(selected_font, size))
        textbox2.configure(font=(selected_font, size))
        textbox3.configure(font=(selected_font, size))
        textbox4.configure(font=(selected_font, size))
        preview_label.configure(font=(selected_font, 16))

def create_labeled_entry(parent, label_text):
    label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 14, "bold"))
    label.pack(pady=(5, 2))
    entry = ctk.CTkEntry(parent, width=300)
    entry.pack(pady=5)
    return entry

def load_positions(json_file_path):
    """Load text positions from a JSON file."""
    try:
        with open(json_file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading positions: {e}")
        return {
            "Luwes": [50, 50],
            "Anthony": [50, 150],
            "Julien": [50, 250],
            "Joseph": [50, 350]
        }

def filter_fonts(*args):
    """Filter font dropdown based on search term."""
    search_term = search_entry.get().lower()
    filtered_fonts = [font for font in get_installed_fonts(font_dirs) if search_term in font]
    font_dropdown.configure(values=filtered_fonts)
    if filtered_fonts:
        font_var.set(filtered_fonts[0])
    else:
        font_var.set("")

def select_overlay_image():
    """Allow the user to select the overlay image file."""
    overlay_image_path = filedialog.askopenfilename(title="Select Overlay Image", filetypes=[("PNG Files", "*.png")])
    if overlay_image_path:
        overlay_image_entry.delete(0, tk.END)
        overlay_image_entry.insert(0, overlay_image_path)

def select_positions_file():
    """Allow the user to select the positions JSON file."""
    positions_file_path = filedialog.askopenfilename(title="Select Positions JSON", filetypes=[("JSON Files", "*.json")])
    if positions_file_path:
        positions_file_entry.delete(0, tk.END)
        positions_file_entry.insert(0, positions_file_path)

def select_output_folder():
    """Allow the user to select the output folder."""
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if output_folder:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, output_folder)

def select_additional_font_folders():
    """Allow the user to select additional font directories."""
    selected_dirs = filedialog.askdirectory(title="Select Additional Font Folders", mustexist=True)
    if selected_dirs:
        font_dirs.append(selected_dirs)  # Append the selected folder to the font directories list
        update_font_dropdown()  # Update the font dropdown with the new fonts

def update_font_dropdown():
    """Update the font dropdown list with the fonts from the selected directories."""
    installed_fonts = get_installed_fonts(font_dirs)
    font_dropdown.configure(values=installed_fonts)
    if installed_fonts:
        font_var.set(installed_fonts[0])

def on_submit():
    """Handle the submit button action."""
    values = {
        "Luwes": textbox1.get(),
        "Anthony": textbox2.get(),
        "Julien": textbox3.get(),
        "Joseph": textbox4.get(),
        "Selected Font": font_var.get(),
        "Font Size": font_size_entry.get()
    }

    selected_font = values["Selected Font"].lower()
    selected_font_path = get_font_paths(font_dirs).get(selected_font)

    if not selected_font_path:
        messagebox.showerror("Error", "Selected font not found.")
        return

    overlay_image_path = overlay_image_entry.get().strip()
    positions_file_path = positions_file_entry.get().strip()
    output_folder = output_folder_entry.get().strip()

    if not overlay_image_path or not positions_file_path or not output_folder:
        messagebox.showerror("Error", "Please select the overlay image, positions file, and output folder.")
        return

    positions = load_positions(positions_file_path)
    
    texts = [(values[key], tuple(positions.get(key, [50, 50]))) for key in ["Luwes", "Anthony", "Julien", "Joseph"]]

    try:
        font_size = int(values["Font Size"])
    except ValueError:
        font_size = 14  # Default font size

    output_file_path = os.path.join(output_folder, "overlay.png")

    try:
        add_text_to_image(overlay_image_path, texts, font_path=selected_font_path, font_size=font_size, output_path=output_file_path)
        messagebox.showinfo("Success", f"Image saved successfully to {output_file_path}.")
    except Exception as e:
        messagebox.showerror("Error", f"Error generating image: {e}")

def main():
    """Initialize and run the application."""
    global textbox1, textbox2, textbox3, textbox4, font_var, font_dropdown
    global search_entry, preview_label, font_size_entry, overlay_image_entry
    global positions_file_entry, output_folder_entry, font_dirs

    # Default font directories
    font_dirs = [r"C:\Windows\Fonts", r"Fonts"]

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = ctk.CTk()
    app.geometry("500x700")
    app.title("OverGen")
    app.resizable(False, False)

    # Scrollable Frame
    scrollable_frame = ctk.CTkScrollableFrame(app)
    scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # Title Label
    title_label = ctk.CTkLabel(scrollable_frame, text="Enter Details", font=("Arial", 18, "bold"))
    title_label.pack(pady=10)
    # Submit Button
    submit_button = ctk.CTkButton(scrollable_frame, text="Gen", command=on_submit)
    submit_button.pack(pady=20)
    # Search Entry for Font Filtering
    search_entry = ctk.CTkEntry(scrollable_frame, width=300, placeholder_text="Search font...")
    search_entry.pack(pady=(10, 5))
    search_entry.bind("<KeyRelease>", filter_fonts)

    # Font Dropdown for Selection
    font_var = tk.StringVar(value="Arial")
    installed_fonts = get_installed_fonts(font_dirs)
    font_dropdown = ctk.CTkComboBox(scrollable_frame, values=installed_fonts, variable=font_var,
                                   width=300, command=lambda x: apply_selected_font())
    font_dropdown.pack(pady=5)


    # Preview Label to show font
    preview_label = ctk.CTkLabel(scrollable_frame, text="Sample Text Preview", font=(font_var.get(), 16))
    preview_label.pack(pady=5)

    # Font Size Entry
    font_size_label = ctk.CTkLabel(scrollable_frame, text="Font Size:", font=("Arial", 14, "bold"))
    font_size_label.pack(pady=(10, 2))
    font_size_entry = ctk.CTkEntry(scrollable_frame, width=300)
    font_size_entry.insert(0, "14")  # Default value
    font_size_entry.pack(pady=5)

    # Textboxes for user input
    textbox1 = create_labeled_entry(scrollable_frame, "Luwes")
    textbox2 = create_labeled_entry(scrollable_frame, "Anthony")
    textbox3 = create_labeled_entry(scrollable_frame, "Julien")
    textbox4 = create_labeled_entry(scrollable_frame, "Joseph")

    # Select Overlay Image
    overlay_image_label = ctk.CTkLabel(scrollable_frame, text="Select Overlay Image", font=("Arial", 14))
    overlay_image_label.pack(pady=10)
    overlay_image_entry = ctk.CTkEntry(scrollable_frame, width=300)
    overlay_image_entry.pack(pady=5)
    overlay_image_button = ctk.CTkButton(scrollable_frame, text="Browse", command=select_overlay_image)
    overlay_image_button.pack(pady=5)

    # Select Positions JSON
    positions_file_label = ctk.CTkLabel(scrollable_frame, text="Select Positions File", font=("Arial", 14))
    positions_file_label.pack(pady=10)
    positions_file_entry = ctk.CTkEntry(scrollable_frame, width=300)
    positions_file_entry.pack(pady=5)
    positions_file_button = ctk.CTkButton(scrollable_frame, text="Browse", command=select_positions_file)
    positions_file_button.pack(pady=5)

    # Select Output Folder
    output_folder_label = ctk.CTkLabel(scrollable_frame, text="Select Output Folder", font=("Arial", 14))
    output_folder_label.pack(pady=10)
    output_folder_entry = ctk.CTkEntry(scrollable_frame, width=300)
    output_folder_entry.pack(pady=5)
    output_folder_button = ctk.CTkButton(scrollable_frame, text="Browse", command=select_output_folder)
    output_folder_button.pack(pady=5)

    # Select Additional Font Folders
    add_font_folder_button = ctk.CTkButton(scrollable_frame, text="Add Font Folder", command=select_additional_font_folders)
    add_font_folder_button.pack(pady=10)

    

    app.mainloop()

if __name__ == "__main__":
    main()
