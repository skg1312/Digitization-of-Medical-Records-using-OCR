from flask import Flask, request, render_template, send_file
from ocr_utils import detect_handwritten_text, extract_handwritten_text, create_overlay_image
import cv2  # Import OpenCV

app = Flask(__name__, static_folder='static')



@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return "No image uploaded", 400

    image_file = request.files['image']
    if image_file.filename == '':
        return "No image selected", 400

    # Save the uploaded image
    image_path = 'uploaded_image.jpg'
    image_file.save(image_path)

    # Additional medical terms to include
    additional_medical_terms = [
        'mg', 'ml', '%', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'perception', 'RX', 'tab'
    ]

    # Extract font size value from form data
    font_size = float(request.form.get('fontSize', 0.3))  # Default value 0.3 if not provided in form data

    # Detect handwritten text using Google Cloud Vision API
    response = detect_handwritten_text(image_path)

    # Extract handwritten text and bounding box information from the response
    extracted_text = extract_handwritten_text(response, additional_medical_terms)

    # Create the new image with text areas filled with empty pixels and corrected text overlay
    new_image = create_overlay_image(extracted_text, image_path, font_size)

    # Save the processed image
    processed_image_path = 'static/processed_image.jpg'
    cv2.imwrite(processed_image_path, new_image)

    return send_file(processed_image_path, mimetype='image/jpg')

if __name__ == '__main__':
    app.run(debug=True)
