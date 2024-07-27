import io
import json
import re
from google.cloud import vision
from google.cloud import translate_v2 as translate
from PIL import Image, ImageFilter, ImageOps, ImageEnhance  # Added ImageEnhance import
import os

# Initialize the Vision API client and Translation client
client_vision = vision.ImageAnnotatorClient()
translate_client = translate.Client()

def read_image(image_path):
    with io.open(image_path, 'rb') as image_file:
        return image_file.read()

def get_text_from_image(image_content):
    image = vision.Image(content=image_content)
    try:
        response = client_vision.text_detection(image=image)
        texts = response.text_annotations
        if texts:
            description = texts[0].description
            return [line.strip() for line in description.split('\n') if line.strip()]
    except Exception as e:
        print(f"Google Cloud Vision API failed with error: {e}")
    return []

def get_barcode_from_image(image_content):
    image = vision.Image(content=image_content)
    try:
        response = client_vision.text_detection(image=image)
        texts = response.text_annotations
        if texts:
            description = texts[0].description
            # Look for long numeric sequences typically found in barcodes
            barcode_matches = re.findall(r'\b\d{12,}\b', description)
            if barcode_matches:
                return max(barcode_matches, key=len)  # Return the longest match
    except Exception as e:
        print(f"Google Cloud Vision API failed with error: {e}")
    return None

def translate_text(text, target_language='en'):
    if text and not is_english(text):
        translation = translate_client.translate(text, target_language=target_language)
        return translation['translatedText']
    return text

def is_english(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def pre_process_image(image_path):
    image = Image.open(image_path)
    # Convert to grayscale
    gray = ImageOps.grayscale(image)
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(gray)
    enhanced = enhancer.enhance(2)
    # Apply adaptive thresholding
    blurred = enhanced.filter(ImageFilter.GaussianBlur(2))
    threshold = blurred.point(lambda p: p > 128 and 255)
    return threshold

def extract_domicile_certificate_info(lines, barcode):
    info = {
        "Applicant's name": None,
        "Certificate number": None,
        "Issuing Authority": None,
        "Date of Issue": None,
        "District": None,
        "barcode": barcode  # Add barcode to the extracted info
    }

    name_pattern = re.compile(r'it is hereby certified that,?\s*(.*?),?\s*R/O', re.IGNORECASE)
    
    for line in lines:
        if "it is hereby certified that" in line.lower():
            match = name_pattern.search(line)
            if match:
                info["Applicant's name"] = match.group(1).strip()
        if "serial no." in line.lower():
            match = re.search(r'serial no.\s*:\s*(\d+)', line, re.IGNORECASE)
            if match:
                info["Certificate number"] = match.group(1).strip()
        if "tehsildar" in line.lower() or "tahsildar" in line.lower():
            info["Issuing Authority"] = "Tehsildar"
        if "date:" in line.lower():
            match = re.search(r'date:\s*(\d{2}/\d{2}/\d{4})', line, re.IGNORECASE)
            if match:
                info["Date of Issue"] = match.group(1).strip()
        if "district" in line.lower():
            match = re.search(r'district\s*(\w+)', line, re.IGNORECASE)
            if match:
                info["District"] = match.group(1).strip()

    return info

def extract_info(lines, certificate_type, barcode):
    if certificate_type == 'domicile':
        return extract_domicile_certificate_info(lines, barcode)
    else:
        raise ValueError(f"Unknown certificate type: {certificate_type}")

def process_image(image_path, certificate_type):
    image_content = read_image(image_path)
    pre_processed_image = pre_process_image(image_path)
    extracted_text = get_text_from_image(image_content)
    barcode = get_barcode_from_image(image_content)  # Extract barcode

    extracted_info = extract_info(extracted_text, certificate_type, barcode)

    translated_info = {key: translate_text(value) for key, value in extracted_info.items() if value}

    output_file = f"extracted_{certificate_type}_info_{os.path.basename(image_path)}.json"
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(translated_info, json_file, ensure_ascii=False, indent=4)

    return translated_info

if __name__ == "__main__":
    directory_path = r"C:\Users\HP\Desktop\Study\Internship\MahaDBT-Doc\DOMCILE"
    
    if not os.path.isdir(directory_path):
        print(f"Directory not found: {directory_path}. Please enter a valid directory path.")
    else:
        image_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        image_files.sort()  # Sort to ensure consistent order
        total_images = len(image_files)
        print(f"Found {total_images} images in the directory.")
        
        if total_images == 0:
            print("No images found in the directory. Exiting.")
        else:
            certificate_type = 'domicile'  # Set the certificate type to 'domicile'
            index = 0
            
            while index < total_images:
                batch = image_files[index:index + 10]
                for image_path in batch:
                    print(f"Processing {image_path}...")
                    extracted_info = process_image(image_path, certificate_type)
                    print(json.dumps(extracted_info, indent=4))
                index += 10

                if index < total_images:
                    cont = input("Do you want to process the next set of images? (yes/no): ").strip().lower()
                    if cont != 'yes':
                        break
            print("Processing complete.")
