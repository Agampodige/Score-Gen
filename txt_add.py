from PIL import Image, ImageDraw, ImageFont
import json

def leaderboard_txt(image_path, text_positions, value_positions, font_path="arial.ttf", font_size=40, output_path="leaderboard.png"):
    # Open the image and ensure it's in RGBA mode for transparency
    image = Image.open(image_path).convert('RGBA')

    # Initialize ImageDraw
    draw = ImageDraw.Draw(image)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Add player names (text) to the image at specified text positions
    for name, position in text_positions.items():
        text = f"{name}:"
        draw.text(position, text, fill=(0, 0, 0, 255), font=font)  # Black text with full opacity

    # Add player scores (values) to the image at specified value positions
    for name, position in value_positions.items():
        value = str(value_positions.get(name, 0))  # Ensure we get a value, defaulting to 0
        draw.text(position, value, fill=(0, 0, 0, 255), font=font)  # Black text with full opacity

    # Save the edited image with transparent background
    image.save(output_path, 'PNG')  # Save as PNG to preserve transparency

def add_text_to_image(image_path, values, font_path, font_size, positions, output_path):
    """Add the numeric values as text on the image at specific positions."""
    # Open the image and ensure it's in RGBA mode for transparency
    img = Image.open(image_path).convert('RGBA')
    draw = ImageDraw.Draw(img)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Loop through the values and add them to the image at specified positions
    for name, value in values.items():
        if value.isdigit():  # Only display integer values
            # Get the position for the current name
            position = positions.get(name, [50, 50])  # Default position if not found
            draw.text(tuple(position), f"{value}", font=font, fill=(0, 0, 0, 255))  # Black text with full opacity

    # Save the output image with transparent background
    img.save(output_path, 'PNG')


def load_positions(positions_file_path):
    """Load positions from a JSON file."""
    try:
        with open(positions_file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading positions: {e}")
        return {}  # Return an empty dictionary if there is an error

