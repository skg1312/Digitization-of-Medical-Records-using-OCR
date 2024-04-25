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

    # Load the uploaded image for image processing
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Save the binary image
    cv2.imwrite(image_path, gray)
    
    # Update progress to UI - Stage 1
    print("Image uploaded and pre-processing completed")

    # Additional medical terms to include
    additional_medical_terms = [
        'mg', 'ml', '%', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'perception', 'RX', 'tab'
    ]
    
    # Extract font size value from form data
    font_size = float(request.form.get('fontSize', 0.4))  # Default value 0.4 if not provided in form data
    
    # Detect handwritten text using Google Cloud Vision API
    response = detect_handwritten_text(image_path)
    
    # Update progress to UI - Stage 2
    print("Text detection completed")

    # Extract handwritten text and bounding box information from the response
    extracted_text = extract_handwritten_text(response, additional_medical_terms)
    
    # Update progress to UI - Stage 3
    print("Text Checking completed")
    
    # Create the new image with text areas filled with empty pixels and corrected text overlay
    new_image = create_overlay_image(extracted_text, image_path, font_size)
    
    # Update progress to UI - Stage 4 (Final)
    print("Processing completed")

    # Save the processed image
    processed_image_path = 'static/processed_image.jpg'
    cv2.imwrite(processed_image_path, new_image)

    return send_file(processed_image_path, mimetype='image/jpg')

if __name__ == '__main__':
    app.run(debug=True)
