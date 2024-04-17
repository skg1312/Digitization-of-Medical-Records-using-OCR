import cv2
import numpy as np
import io
import os
from google.cloud import vision
from google.cloud import language_v1

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-token.json'

def detect_handwritten_text(path):
    """Detects handwritten text in an image using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return response  # Return the response object

def correct_spelling_with_nlp_api(text, additional_terms):
    """Performs spelling correction using Google NLP API."""
    client = language_v1.LanguageServiceClient()

    # Combine additional medical terms with the text to analyze
    combined_text = '\n'.join([text] + additional_terms)

    # Create a request with the combined text to analyze
    document = {"content": combined_text, "type_": language_v1.Document.Type.PLAIN_TEXT}
    response = client.analyze_syntax(request={'document': document})

    # Retrieve the corrected text from the response
    corrected_text = response.tokens[0].text.content

    return corrected_text

def extract_handwritten_text(response, additional_terms):
    """Extracts handwritten text and performs spelling correction at the word level."""
    extracted_text = []

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    if word_text.lower() == 'r':
                        word_text = 'Rx'
                    elif word_text.lower() == 'me':
                        word_text = 'ml'
                    # Perform spelling correction using Google NLP API
                    corrected_word = correct_spelling_with_nlp_api(word_text, additional_terms)

                    vertices = [(vertex.x, vertex.y) for vertex in word.bounding_box.vertices]

                    extracted_text.append({
                        'original_text': word_text,
                        'corrected_text': corrected_word,
                        'boundingPoly': {'vertices': vertices}
                    })

    return extracted_text

def create_overlay_image(extracted_text, original_image_path, font_size):
    """Creates a new image with extracted text areas filled with empty pixels using OpenCV."""
    original_image = cv2.imread(original_image_path)
    new_image = original_image.copy()  # Create a copy of the original image

    for annotation in extracted_text:
        corrected_text = annotation['corrected_text']  # Get the corrected text for this annotation
        bounding_box = annotation['boundingPoly']['vertices']

        # Convert bounding box vertices to numpy array for OpenCV
        bounding_box_np = np.array([(vertex[0], vertex[1]) for vertex in bounding_box], dtype=np.int32)

        # Fill the bounding box area with empty pixels (white color)
        cv2.fillPoly(new_image, [bounding_box_np], (255, 255, 255))
        
        # Get the text position for overlay
        text_position = (bounding_box[0][0], bounding_box[0][1] + 10)  # Adjust Y coordinate for text placement

        # Draw the corrected text on top of the image with specified font size
        cv2.putText(new_image, corrected_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, font_size, (0, 0, 0), 1)

    return new_image
