import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from filters import Vintage, AnimeGanv2GeneratorFilter
from pilgram import css, util
import datetime

# Function to process images based on different operations
def process_image(filename, operation, text=None, font=None, font_size=None, text_color=None, text_position_x=None,
                  text_position_y=None):
    upload_folder = "uploads"
    file_path = os.path.join(upload_folder, filename)

    print(f"Processing {operation} on file {file_path}")

    # Load the image
    img = cv2.imread(file_path)

    if img is None:
        raise ValueError(f"Error loading image from {file_path}. Please check the file path.")

    # Resize the image if it's too large, while maintaining aspect ratio
    max_dimension = 1024  # Maximum allowed size for width or height
    height, width = img.shape[:2]
    if max(width, height) > max_dimension:
        # Calculate the scaling factor to maintain aspect ratio
        scaling_factor = max_dimension / float(max(width, height))
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
        print(f"Image resized to {new_size} for processing.")

    # Handle different operations based on the request
    if operation == "txt":
        processed_filename = f"{os.path.splitext(filename)[0]}_txt{os.path.splitext(filename)[1]}"
        add_text(img, processed_filename, text, font, font_size, text_color, text_position_x, text_position_y)
    elif operation == "anm":
        processed_filename = f"{os.path.splitext(filename)[0]}_anm{os.path.splitext(filename)[1]}"
        AnimeGanv2GeneratorFilter().apply(img, processed_filename)
    elif operation == "mnc":
        processed_filename = f"{os.path.splitext(filename)[0]}_mnc{os.path.splitext(filename)[1]}"
        apply_monochrome(img, processed_filename)
    elif operation == "crd":
        processed_filename = f"{os.path.splitext(filename)[0]}_crd{os.path.splitext(filename)[1]}"
        apply_card_effect(img, processed_filename)
    elif operation == "rtr":
        vintage_filter = Vintage()
        vintage_img = vintage_filter.render(img)
        processed_filename = f"{os.path.splitext(filename)[0]}_rtr{os.path.splitext(filename)[1]}"
        save_image(vintage_img, processed_filename)
    elif operation == "dnt":  # Day and Date operation
        processed_filename = f"{os.path.splitext(filename)[0]}_dnt{os.path.splitext(filename)[1]}"
        add_day_with_date(img, processed_filename)
        print(f"Processing {operation} on file {file_path}")

    else:
        raise ValueError(f"Unsupported operation: {operation}")

    return processed_filename


def add_day_with_date(img, processed_filename):
    # Convert OpenCV image (BGR) to PIL image (RGB)
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)

    # Get the current day and date
    current_day = datetime.datetime.now().strftime('%A')
    current_date = datetime.datetime.now().strftime('%d')
    day_with_date = f"{current_day}, {current_date}"
    print(f"Day with Date: {day_with_date}")

    # Set the font and size for the date text
    font_path = os.path.join('fonts/', 'Arimo-Regular.ttf')  # Update the font path if needed
    font_size = 60
    if not os.path.exists(font_path):
        print(f"Font path does not exist: {font_path}")
        return
    font = ImageFont.truetype(font_path, font_size)
    print(f"Font loaded: {font_path}")

    # Calculate text size and position
    bbox = draw.textbbox((0, 0), day_with_date, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    print(f"Text Width: {text_width}, Text Height: {text_height}")

    # Create a new image for the text and rotate it 90 degrees
    text_image = Image.new('RGBA', (text_width, text_height), (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_image)
    text_draw.text((0, 0), day_with_date, font=font, fill="white")

    # Rotate the text image by 90 degrees
    text_image_rotated = text_image.rotate(90, expand=1)

    # Calculate position to paste the text image
    position_x = 20  # Adjust as needed
    position_y = pil_img.height - text_image_rotated.size[1] - 35  # Adjust as needed
    print(f"Text position: ({position_x}, {position_y})")

    # Ensure the text is within the image boundaries
    if position_x + text_image_rotated.size[0] > pil_img.width:
        position_x = pil_img.width - text_image_rotated.size[0] - 10
    if position_y + text_image_rotated.size[1] > pil_img.height:
        position_y = pil_img.height - text_image_rotated.size[1] - 10

    # Paste the rotated text on the original image
    pil_img.paste(text_image_rotated, (position_x, position_y), text_image_rotated)

    # Convert back to OpenCV image and save
    img_with_date = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    save_image(img_with_date, processed_filename)
    print(f"Image saved to {processed_filename}")


# Function to add text to an image
def add_text(img, filename, text, font, font_size, text_color, text_position_x, text_position_y):
    # Define available font paths
    FONT_PATHS = {
        "arimo": "fonts/Arimo-Regular.ttf",
        "tinos": "fonts/Tinos-Regular.ttf",
        "playwrite": "fonts/PlaywriteCU-Regular.ttf",
        "allan": "fonts/Allan-Regular.ttf",
        "anton": "fonts/Anton-Regular.ttf",
    }

    # Set font path, size, and color
    font_path = FONT_PATHS.get(font, "fonts/arial.ttf")
    font_size = int(font_size) if font_size.isdigit() else 20
    text_color = text_color if text_color else "#000000"

    # Convert to PIL for drawing
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    font = ImageFont.truetype(font_path, font_size)

    # Draw text
    position = (int(text_position_x), int(text_position_y))
    draw.text(position, text, fill=text_color, font=font)

    # Save the processed image
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    save_image(img, filename)


# Helper function to save processed image in static folder
def save_image(img, filename):
    # Save the image to the 'static/uploads' folder for display
    output_folder = os.path.join("static", "uploads")
    os.makedirs(output_folder, exist_ok=True)  # Ensure the folder exists

    output_path = os.path.join(output_folder, filename)

    print(f"Saving processed image to {output_path}")

    cv2.imwrite(output_path, img)


# Other operations like Monochrome, Card Effect, etc.
def apply_monochrome(img, filename):
    monochrome_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    save_image(monochrome_image, filename)


def apply_card_effect(img, filename):
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    cb = util.or_convert(pil_img, "RGB")
    cs = util.fill(cb.size, [127, 187, 227, 0.2])
    cr = css.blending.overlay(cb, cs)
    cr = css.contrast(cr, 1.2)
    cr = css.saturate(cr, 1.35)
    cr = np.array(cr)
    cr = cv2.cvtColor(cr, cv2.COLOR_RGB2BGR)
    save_image(cr, filename)