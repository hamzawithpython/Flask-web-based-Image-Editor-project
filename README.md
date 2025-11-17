📸 Flask Web-Based Image Editing Website
A full-featured web-based image editor built with Flask, OpenCV, Pillow, and AnimeGANv2.
This project allows users to upload images, apply creative filters, adjust image attributes, add text overlays, create collages, and download the final edited images — all through a simple and modern web interface.
________________________________________
🚀 Features
🔧 Image Editing Tools
    •	Upload images (JPG, JPEG, PNG)
    •	Apply filters:
        o	Monochrome
        o	Clarendon/Card Effect
        o	Retro/Vintage
        o	AnimeGANv2 Anime Filter (AI-based)
    •	Adjustments:
        o	Brightness
        o	Saturation
        o	Inversion
        o	Grayscale
    •	Transformations:
        o	Rotate (LEFT/RIGHT)
        o	Flip (Horizontal/Vertical)
        o	Reset Image
✍️ Text Tools
    •	Add custom text to any position
    •	Font options (Arimo, Tinos, Anton, Playwrite, Allan)
    •	Adjustable:
        o	Font size
        o	Font color
        o	Text position (x, y)
🗓 Day + Date Watermark
Automatically add a stylish vertical day/date stamp to the image.
🖼 Collage Generator
    •	Upload multiple images
    •	Choose number of rows & columns
    •	Generates a clean collage grid
    •	Downloadable result
💾 Download Edited Image
Every processed image is saved and made available for download.
________________________________________
🧠 Technologies Used
Category	                             Tech
Backend	                             Flask, Python
Image Processing	                 OpenCV, Pillow (PIL), scikit-image
AI Filter	                         AnimeGANv2 (PyTorch)
Filters	                             Pilgram CSS filters
ML/Models	                         Torch, torchvision, facelib, gfgan
Frontend	                         HTML, CSS, JavaScript (AJAX for live previews)
________________________________________
📦 Project Structure
Flask-web-based-Image-Editor-project/
│── app.py
│── AnimeGANv2Model.py
│── collage.py
│── filters.py
│── utils.py
│── image_processing.py
│── requirements.txt
│── static/
│    ├── uploads/
│    ├── collages/
│    ├── css/
│    ├── js/
│    └── fonts/
│── templates/
│    ├── index.html
│    ├── collage.html
│── uploads/
│── collage/
________________________________________
⚙️ Installation & Setup
1️⃣ Create & Activate Virtual Environment
    python -m venv .venv
    source .venv/bin/activate      # Linux / macOS
    .venv\Scripts\activate         # Windows
2️⃣ Install Dependencies
    pip install -r requirements.txt
3️⃣ Download AnimeGANv2 Model Weights
    Place the file:
        models/face_paint_512_v2.pt
        inside a /models folder.
4️⃣ Run the Flask App
    python app.py
    The app will run at:
        http://127.0.0.1:5000/
________________________________________
🛠 API Endpoints
Method	        Endpoint	               Description
GET	            /	                Homepage – main editor
GET	            /collage	        Collage UI
POST	        /edit	            Apply filters/text adjustments
POST	        /add-date	        Add date/day watermark
POST	        /collage/create	    Generate collage
________________________________________
🧩 How the Anime Filter Works
The AnimeGANv2 filter uses:
    •	Pre-trained AnimeGANv2 Generator
    •	Converts input → RGB → normalized tensor
    •	Runs inference on PyTorch model
    •	Converts output back to image format
This produces a smooth anime-style transformation.
________________________________________
📘 Screenshots (Optional)
You can add images like:
    ![Homepage](static/screenshots/homepage.png)
    ![Editing Preview](static/screenshots/editor.png)
________________________________________
📄 License
This project is for educational and personal use.
You may extend and modify it as needed.
________________________________________
⭐ Future Improvements
    •	Add face beautification filters
    •	Add drag-and-drop to change collage structure
    •	Add photo cropping tool
    •	Add support for more AI filters (Sketch, Portrait, etc.)
    •	Add upload history for each session
________________________________________
🙌 Author
Hamza Asif
Python Developer

