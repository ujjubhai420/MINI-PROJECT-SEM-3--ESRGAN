# ESRGAN Web Interface

A Flask-based web application for enhancing images using the ESRGAN model. The application allows users to upload an image, process it with the ESRGAN model, and compare the original and enhanced images side-by-side in the browser.

---

## Features
- Upload and process low-resolution images.
- View the original and enhanced images side-by-side.
- Compare dimensions and file sizes of the original and enhanced images.
- Supports a modern, dark-themed UI styled with Tailwind CSS.
- Interactive modal to view images in full size on click.

---

## **Getting Started**

### Prerequisites
- Python 3.8 or higher.
- pip (Python package manager).
- Virtual environment (optional but recommended).

### **Steps to Run**

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd ESRGAN-FLASK
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv env
   ```

3. **Activate the Virtual Environment**
   - On **Windows**:
     ```bash
     .\env\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source env/bin/activate
     ```

4. **Install Required Libraries**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the Web Interface**
   Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---
