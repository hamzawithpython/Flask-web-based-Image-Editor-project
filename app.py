from flask import Flask, render_template, request, flash, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
import os
from PIL import Image, ImageDraw, ImageFont
from image_processing import process_image
from utils import allowed_file
from collage import make_collage
import datetime


# Flask app configuration
UPLOAD_FOLDER = 'uploads'
COLLAGE_FOLDER = 'collage'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COLLAGE_FOLDER'] = COLLAGE_FOLDER

# Ensure the collage folder exists
os.makedirs(COLLAGE_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Collage route
@app.route("/collage")
def collage():
    return render_template("collage.html")

# Collage creation route
@app.route("/collage/create", methods=["POST"])
def create_collage():
    if 'files' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('files')
    rows = int(request.form.get('rows', 2))
    cols = int(request.form.get('cols', 2))

    # Ensure valid files were uploaded
    images = []
    for file in files:
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            images.append(Image.open(file_path))

    if len(images) < rows * cols:
        return jsonify({'error': f'Please upload at least {rows * cols} images'}), 400

    # Create the collage
    collage = make_collage(images, rows, cols)

    # Ensure the 'static/collages/' directory exists
    collage_folder = os.path.join("static", "collages")
    os.makedirs(collage_folder, exist_ok=True)

    # Save the collage in the 'static/collages/' folder
    collage_filename = "collage.png"
    collage_path = os.path.join(collage_folder, collage_filename)

    # Log the path where collage will be saved
    print(f"Saving collage to: {collage_path}")

    # Try saving the collage and handle potential errors
    try:
        collage.save(collage_path)
        print(f"Collage successfully saved at: {collage_path}")
    except Exception as e:
        print(f"Error saving collage: {str(e)}")
        return jsonify({'error': 'Failed to save collage'}), 500

    # Return the collage URL as JSON
    collage_url = url_for('static', filename=f'collages/{collage_filename}')
    print(f"Collage URL: {collage_url}")
    return jsonify({'collage_url': collage_url}), 200


# Serve the collage
@app.route("/collages/<filename>")
def serve_collage(filename):
    return send_file(os.path.join(app.config['COLLAGE_FOLDER'], filename))

# New route to add date with day
@app.route("/add-date", methods=["POST"])
def add_date():
    # Handle file upload
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Open the image and get its dimensions
        img = Image.open(file_path)
        width, height = img.size

        # Get the current day and date
        current_day = datetime.datetime.now().strftime('%A')
        current_date = datetime.datetime.now().strftime('%d')
        day_with_date = f"{current_day}, {current_date}"

        # Set the font and size for the date text
        font_path = os.path.join('static/fonts', 'arial.ttf')  # Path to a font file
        font_size = 40
        font = ImageFont.truetype(font_path, font_size)

        # Create a draw object to add text to the image
        draw = ImageDraw.Draw(img)
        text_width, text_height = draw.textsize(day_with_date, font=font)

        # Positioning: Rotate the text 90 degrees and place it at the bottom-left corner
        text_image = Image.new('RGBA', (text_height, text_width), (255, 255, 255, 0))
        text_draw = ImageDraw.Draw(text_image)
        text_draw.text((0, 0), day_with_date, font=font, fill="white")

        # Rotate the text image by 90 degrees
        text_image_rotated = text_image.rotate(90, expand=1)

        # Paste the rotated text on the original image (bottom-left corner)
        img.paste(text_image_rotated, (0, height - text_image_rotated.size[1]), text_image_rotated)

        # Save the modified image with the date and day
        processed_filename = f"dated_{filename}"
        processed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
        img.save(processed_file_path)

        processed_image_url = url_for('static', filename=f'uploads/{processed_filename}')
        return jsonify({'processed_image_url': processed_image_url}), 200

    return jsonify({'error': 'Invalid file type'}), 400

# Image editing route
@app.route("/edit", methods=["POST"])
def edit_image():
    # Get the operation from the form data
    operation = request.form.get("operation")

    # Handle file upload
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Get other form fields (if applicable)
        text = request.form.get("inputText")
        font = request.form.get("font")
        fontSize = request.form.get("fontSize")
        textColor = request.form.get("textColor")
        textPositionX = request.form.get("textPositionX")
        textPositionY = request.form.get("textPositionY")

        # Log form data for debugging
        print(f"Text: {text}, Font: {font}, Font Size: {fontSize}, Text Color: {textColor}, X: {textPositionX}, Y: {textPositionY}")

        # Process the image based on the selected operation
        processed_filename = process_image(
            filename, operation, text, font, fontSize, textColor, textPositionX, textPositionY
        )

        processed_image_url = url_for('static', filename=f'uploads/{processed_filename}')
        return jsonify({'processed_image_url': processed_image_url}), 200

    return jsonify({'error': 'Invalid file type'}), 400


if __name__ == "__main__":
    app.run(debug=True)
