import os
import re
import logging
from PIL import Image, ImageEnhance
import pytesseract
import shutil  # To move skipped files

# Configure logging
log_file = "image_processing.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define the date and time regex pattern
datetime_pattern = r"\b(\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2})[,:\s]*(\d{1,2}:\d{2})\b"

# Define the folder containing the images
input_folder = "/Users/chan/Library/CloudStorage/OneDrive-KBTC/Corporate Affair/CEO Office/KBTC_Global/KBTC_Global_Thailand/Finance - Budgeting/Bank statements/BBL screenshot"
output_folder = "/Users/chan/Library/CloudStorage/OneDrive-KBTC/Corporate Affair/CEO Office/KBTC_Global/KBTC_Global_Thailand/Finance - Budgeting/Bank statements/receipts"
skipped_folder = "/Users/chan/Library/CloudStorage/OneDrive-KBTC/Corporate Affair/CEO Office/KBTC_Global/KBTC_Global_Thailand/Finance - Budgeting/Bank statements/skipped_files"
os.makedirs(output_folder, exist_ok=True)
os.makedirs(skipped_folder, exist_ok=True)

def preprocess_image(image_path):
    """
    Preprocess the image to improve OCR accuracy.
    """
    # Open the image
    image = Image.open(image_path)
    
    # Step 1: Convert to grayscale
    image = image.convert("L")
    
    # Step 2: Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Adjust contrast level (default is 1)
    
    # Step 3: Resize the image (enlarge small text)
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.LANCZOS)
    
    # Step 4: Apply a threshold to binarize the image (convert to black and white)
    image = image.point(lambda x: 0 if x < 128 else 255, '1')
    
    return image

def extract_date_and_time(image_path):
    """
    Perform OCR on the preprocessed image and extract date and time.
    """
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)
    
    # Perform OCR
    ocr_output = pytesseract.image_to_string(preprocessed_image)
    
    # Debug: Print OCR output (optional)
    print(f"OCR Output for {image_path}:\n{ocr_output}\n")
    
    # Refine regex to handle different date/time formats
    datetime_pattern = r"(\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2})[^\d]*(\d{1,2}:\d{2})"
    match = re.search(datetime_pattern, ocr_output)
    
    if match:
        date = match.group(1).replace(" ", "-")  # Format date (e.g., 07-Sep-24)
        time = match.group(2).replace(":", "-")  # Format time (e.g., 15-12)
        return f"{date}_{time}"
    else:
        # Log the entire OCR output for skipped files
        logging.warning(f"No date and time found in {image_path}. OCR output: {ocr_output}")
        return None

# Process each image in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith((".png", ".jpg", ".jpeg")):  # Check for image files
        image_path = os.path.join(input_folder, filename)
        try:
            # Extract date and time from the image
            result = extract_date_and_time(image_path)
            
            if result:
                # Rename the file with the extracted date and time
                new_filename = f"{result}.jpeg"
                new_path = os.path.join(output_folder, new_filename)
                
                # Save the preprocessed image with the new name
                image = preprocess_image(image_path)
                image.save(new_path)
                
                logging.info(f"Renamed {filename} to {new_filename}")
                print(f"Renamed {filename} to {new_filename}")
            else:
                # Move skipped files to the skipped folder
                skipped_path = os.path.join(skipped_folder, filename)
                shutil.move(image_path, skipped_path)
                logging.warning(f"No date and time found in {filename}, moved to skipped_files.")
                print(f"No date and time found in {filename}, moved to skipped_files.")
        
        except Exception as e:
            # Move files with errors to the skipped folder
            skipped_path = os.path.join(skipped_folder, filename)
            shutil.move(image_path, skipped_path)
            logging.error(f"Error processing {filename}: {str(e)}. Moved to skipped_files.")
            print(f"Error processing {filename}: {str(e)}. Moved to skipped_files.")

print(f"Processing complete. Check {log_file} for details.")