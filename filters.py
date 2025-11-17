import cv2
import numpy as np
import os
from PIL import Image
from AnimeGANv2Model import Generator as AnimeGanv2Generator
import torch
from torchvision.transforms.functional import to_tensor, to_pil_image



# Vintage filter class
class Vintage:
    """Applies a sepia tone to give an image a vintage look."""

    def render(self, img_rgb):
        new_image = img_rgb.copy()
        for x in range(img_rgb.shape[0]):
            for y in range(img_rgb.shape[1]):
                R = img_rgb[x, y, 2] * 0.393 + img_rgb[x, y, 1] * 0.769 + img_rgb[x, y, 0] * 0.189
                G = img_rgb[x, y, 2] * 0.349 + img_rgb[x, y, 1] * 0.686 + img_rgb[x, y, 0] * 0.168
                B = img_rgb[x, y, 2] * 0.272 + img_rgb[x, y, 1] * 0.534 + img_rgb[x, y, 0] * 0.131
                new_image[x, y] = [min(255, B), min(255, G), min(255, R)]
        return new_image


# AnimeGANv2 filter class
class AnimeGanv2GeneratorFilter:
    """Applies the AnimeGANv2 filter to transform an image."""

    def apply(self, img, filename):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        net = AnimeGanv2Generator()
        net.load_state_dict(torch.load("models/face_paint_512_v2.pt", map_location=device))
        net.to(device).eval()

        b, g, r = cv2.split(img)
        img_rgb = cv2.merge((r, g, b))
        pil_img = Image.fromarray(img_rgb)

        image_tensor = to_tensor(pil_img).unsqueeze(0) * 2 - 1
        with torch.no_grad():
            out = net(image_tensor.to(device), False).cpu()
            out = out.squeeze(0).clip(-1, 1) * 0.5 + 0.5
            out_pil = to_pil_image(out)

            out_img = np.array(out_pil)
            b, g, r = cv2.split(out_img)
            img = cv2.merge((r, g, b))

        # Ensure the processed image is saved in the 'static/uploads/' folder
        processed_image_path = os.path.join("static", "uploads", filename)
        cv2.imwrite(processed_image_path, img)
