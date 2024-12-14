import os
import re
import logging
from PIL import Image
import pytesseract

# Configure logging
log_file = "image_processing.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define the folder containing the images
folder_path = "/Users/chan/Library/CloudStorage/OneDrive-KBTC/Corporate Affair/CEO Office/KBTC_Global/KBTC_Global_Thailand/Finance - Budgeting/Bank statements/BBL screenshot"
output_folder = "/Users/chan/Library/CloudStorage/OneDrive-KBTC/Corporate Affair/CEO Office/KBTC_Global/KBTC_Global_Thailand/Finance - Budgeting/Bank statements/receipts"
os.makedirs(output_folder, exist_ok=True)

# Regex pattern to extract date and time (e.g., "20 Oct 24, 14:47")
datetime_pattern = r"\b(\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2}),\s(\d{1,2}:\d{2})\b"

# Loop through each image in the folder
for filename in os.listdir(folder_path):
    if filename.endswith((".png", ".jpg", ".jpeg")):  # Check for image files
        image_path = os.path.join(folder_path, filename)
        try:
            # Open and preprocess the image
            image = Image.open(image_path)
            image = image.convert("L")  # Convert to grayscale for better OCR accuracy

            # Extract text using OCR
            extracted_text = pytesseract.image_to_string(image)

            # Extract date and time using regex
            match = re.search(datetime_pattern, extracted_text)
            if match:
                date = match.group(1).replace(" ", "-")  # Format the date (e.g., 20-Oct-24)
                time = match.group(2).replace(":", "-")  # Format the time (e.g., 14-47)
                new_filename = f"{date}_{time}.jpeg"  # Combine date and time in the file name
                new_path = os.path.join(output_folder, new_filename)
                image.save(new_path)
                logging.info(f"Renamed {filename} to {new_filename}")
                print(f"Renamed {filename} to {new_filename}")
            else:
                logging.warning(f"No date and time found in {filename}, skipping.")
                print(f"No date and time found in {filename}, skipping.")

        except Exception as e:
            logging.error(f"Error processing {filename}: {str(e)}")
            print(f"Error processing {filename}: {str(e)}")

print(f"Processing complete. Check {log_file} for details.")