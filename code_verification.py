import re
import pytesseract
from PIL import ImageDraw, Image

def load_professional_codes(file_path):
    with open(file_path, 'r') as file:
        codes = [line.strip() for line in file.readlines()]
    return set(codes)

def verify_code(extracted_text, image_path):
    img = Image.open(image_path)
    pattern = r'\b(\d{2}/\d{2}/\d{4})\s+(\d+\w?)\s+(\d{5}|\d{8})\b'
    matches = re.findall(pattern, extracted_text)
    professional_codes = load_professional_codes('code_verification.txt')
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    draw = ImageDraw.Draw(img)
    for match in matches:
        date_str, code, numero = match
        if numero in professional_codes:
            authenticity = "Authentique"
        else:
            authenticity = "Non authentique"
            for i, word in enumerate(data['text']):
                if re.match(numero, word):  # Vérifier si c'est une date potentielle
                    # Si la date est invalide, dessiner une boîte englobante
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    draw.rectangle([x, y, x + w, y + h], outline='red', width=2)
    img.save('output_with_invalid_dates.png')
