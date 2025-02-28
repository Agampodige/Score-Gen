from PIL import Image, ImageDraw, ImageFont
import os


def leaderboard_txt(image_path, texts, font_path="arial.ttf", font_size=40, output_path="overlay.png"):
    # Open the image and ensure it's in RGB mode
    image = Image.open(image_path).convert('RGB')
    
    # Initialize ImageDraw
    draw = ImageDraw.Draw(image)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Add each text to the image
    for text, position in texts:
        draw.text(position, text, fill=(0, 0, 0), font=font)  # White text

    # Save the edited image
    image.save(output_path, 'JPEG')

    # Optionally, display the image
def add_text_to_image(image_path, values, font_path, font_size, positions, output_path):
    """Add the numeric values as text on the image at specific positions."""
    from PIL import Image, ImageDraw, ImageFont
    
    # Open the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Loop through the values and add them to the image at specified positions
    for value, (name, pos) in zip(values.values(), positions.items()):
        if value.isdigit():  # Only display integer values
            # Get the position for the current name
            position = tuple(positions.get(name, [50, 50]))  # Default position if not found
            draw.text(position, value, font=font, fill="black")

    # Save the output image
    img.save(output_path)
