from PIL import Image

def make_collage(images, rows, cols):
    # Resize images to the same size
    resized_images = []
    max_height = max([img.size[1] for img in images])
    max_width = max([img.size[0] for img in images])
    for img in images:
        resized_images.append(img.resize((max_width, max_height)))

    # Create a blank canvas
    collage_width = max_width * cols
    collage_height = max_height * rows
    collage = Image.new('RGB', (collage_width, collage_height))

    # Paste the images onto the canvas
    for i in range(rows):
        for j in range(cols):
            img_index = i * cols + j
            if img_index < len(resized_images):
                collage.paste(resized_images[img_index], (j * max_width, i * max_height))

    return collage
