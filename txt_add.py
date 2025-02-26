from PIL import Image, ImageDraw, ImageFont

def add_text_to_image(image_path, texts, font_path="arial.ttf", font_size=40, output_path="overlay.png"):
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
