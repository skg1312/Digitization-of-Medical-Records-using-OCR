# Digitization of Medical Records using OCR

Digitization of Medical Records using OCR is a Flask-based web application designed to extract and correct handwritten text from medical records using Google Cloud Vision and Natural Language Processing APIs. The application processes uploaded images of medical documents, detects handwritten text, applies medical spelling corrections, and provides a cleaned, digitized output image.

## Features

- **Image Upload & Preprocessing:** Users can upload medical record images. The app converts images to grayscale and applies adaptive thresholding to prepare for OCR.
- **Handwriting Recognition:** Utilizes Google Cloud Vision API to detect handwritten text in images.
- **Medical Spelling Correction:** Applies Google Cloud NLP API with a set of common medical terms to correct OCR output.
- **Text Overlay & Redaction:** Replaces detected text regions in the image with corrected text, producing a clean, binary processed image.
- **Web Interface:** Simple Flask frontend for easy interaction.

## How It Works

1. **Upload Image:** Users upload an image of a medical record via the web interface.
2. **Preprocessing:** The image is converted to grayscale and thresholded for optimal OCR results.
3. **Handwritten Text Detection:** The app calls the Google Cloud Vision API to extract handwritten text and bounding box data.
4. **Word Correction:** Each detected word is checked and corrected using Google Cloud NLP, especially for common medical terms.
5. **Image Overlay:** The original text regions are blanked out and replaced with corrected text.
6. **Output:** The processed image is returned to the user.

## Setup Instructions

### Prerequisites

- Python 3.10+
- Google Cloud account with Vision and NLP API enabled
- Service account credentials JSON file (named `service-token.json` by default)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/skg1312/Digitization-of-Medical-Records-using-OCR.git
   cd Digitization-of-Medical-Records-using-OCR
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Cloud credentials:**
   - Place your Google service account JSON key in the project root as `service-token.json`, or update `ocr_utils.py` to point to your credentials.

4. **Run the application:**
   ```bash
   python main.py
   ```

5. **Access the app:**
   - Open your browser and go to `http://127.0.0.1:5000/`

## Usage

1. Upload an image file (JPEG/PNG) containing handwritten medical records.
2. The app will process the image and return a new image with detected and corrected text.
3. Download the processed image for your records.

## File Structure

- `main.py` — Flask web server and main application logic.
- `ocr_utils.py` — Utility functions for OCR, NLP, and image processing.
- `requirements.txt` — List of required Python packages.
- `static/` — Static files (images, assets) served by Flask.
- `templates/` — HTML templates for the web UI.
- `service-token.json` — (Not included) Your Google Cloud credentials file.

## Dependencies

See `requirements.txt` for full list. Key dependencies:
- Flask
- google-cloud-vision
- google-cloud-language
- opencv-python
- numpy

## Notes

- This application is for demonstration and educational purposes. Always safeguard patient data and comply with medical data privacy regulations.
- You may need to adjust the list of `additional_medical_terms` in `main.py` for your use case.

## Acknowledgments

- Google Cloud Vision & NLP APIs
- OpenCV
- Flask
