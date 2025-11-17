# 📸 Flask Web-Based Image Editing Website

A full-featured **web-based image editor** built with **Flask**, **OpenCV**, **Pillow**, and **AnimeGANv2**.  
This project allows users to upload images, apply creative filters, adjust attributes, add text overlays, create collages, and download the final edited images.

---

## 🚀 Features

### 🔧 Image Editing Tools
- Upload images (JPG, JPEG, PNG)
- Filters:
  - **Monochrome**
  - **Clarendon/Card Effect**
  - **Retro/Vintage**
  - **AnimeGANv2 Anime Filter (AI-based)**
- Adjustments:
  - Brightness  
  - Saturation  
  - Inversion  
  - Grayscale  
- Transformations:
  - Rotate  
  - Flip  
  - Reset  

### ✍️ Text Tools
- Add custom text
- Choose fonts (Arimo, Tinos, Anton, Playwrite, Allan)
- Adjustable:
  - Font size  
  - Font color  
  - Text position (X, Y)

### 🗓 Day & Date Watermark
- Automatically adds a **vertical day/date stamp**.

### 🖼 Collage Generator
- Upload multiple images
- Choose rows & columns
- Generates a downloadable collage

### 💾 Save Edited Images
- Download your final edited result

---

## 🧠 Technologies Used

| Category | Tools |
|----------|-------|
| Backend | Flask, Python |
| Image Processing | OpenCV, Pillow, scikit-image |
| AI Filter | AnimeGANv2 (PyTorch) |
| Filters | Pilgram CSS filters |
| ML/Models | Torch, torchvision, GFPGAN, facelib |
| Frontend | HTML, CSS, JavaScript |

---

## 📁 Project Structure

```
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
```

---

## ⚙️ Installation

### 1️⃣ Create a virtual environment
```bash
python -m venv .venv
```

### 2️⃣ Activate it  
**Windows:**
```bash
.venv\Scripts\activate
```
**Linux/macOS:**
```bash
source .venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Download AnimeGANv2 weights  
Place the file below inside the **models/** folder:
```
models/face_paint_512_v2.pt
```

### 5️⃣ Run the app
```bash
python app.py
```

App will run at:
```
http://127.0.0.1:5000/
```

---

## 🛠 API Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main Editor Page |
| GET | `/collage` | Collage Creator |
| POST | `/edit` | Apply filters & edits |
| POST | `/add-date` | Add date/day watermark |
| POST | `/collage/create` | Build collage |

---

## 🤖 How AnimeGANv2 Works
- Converts input image → RGB  
- Normalizes to tensor  
- Passes through pre-trained AnimeGANv2 generator  
- Denormalizes output  
- Converts back to OpenCV image  

Produces smooth **anime-style transformations**.

---

## 📄 License
This project is for personal and educational use. Feel free to modify and extend.

---

## 🙌 Author
**Hamza Asif**  
Python Developer
