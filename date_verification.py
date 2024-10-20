import re
from datetime import datetime
import pytesseract
from PIL import ImageDraw, Image

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def verify_date(extracted_text, image_path):
    img = Image.open(image_path)
    pattern = r'\b(\d{2}/\d{2}/\d{4})\s+(\d+\w?)\s+(\d{8})\b'
    matches = re.findall(pattern, extracted_text)
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    draw = ImageDraw.Draw(img)
    for i, word in enumerate(data['text']):
        if re.match(r'\d{2}/\d{2}/\d{4}', word):  # Vérifier si c'est une date potentielle
            if not is_valid_date(word):
                # Si la date est invalide, dessiner une boîte englobante
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                draw.rectangle([x, y, x + w, y + h], outline='red', width=2)
                print(f"Date invalide trouvée : {word} à la position ({x}, {y})")
    img.save('output_with_invalid_dates.png')
