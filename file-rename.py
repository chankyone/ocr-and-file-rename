import os
from PIL import Image
import pytesseract

# Define the folder containing the images
folder_path = "/Users/chan/Library/CloudStorage/OneDrive-KBTC/Corporate Affair/CEO Office/KBTC_Global/KBTC_Global_Thailand/Finance - Budgeting/Bank statements/BBL screenshot"
output_folder = "/Users/chan/Library/CloudStorage/OneDrive-KBTC/Corporate Affair/CEO Office/KBTC_Global/KBTC_Global_Thailand/Finance - Budgeting/Bank statements/receipts"
os.makedirs(output_folder, exist_ok=True)

# Loop through each image in the folder
for filename in os.listdir(folder_path):
    if filename.endswith((".png", ".jpg", ".jpeg")):  # Check for image files
        image_path = os.path.join(folder_path, filename)
        image = Image.open(image_path)

        # Extract text using OCR
        extracted_text = pytesseract.image_to_string(image)

        # Extract a date (e.g., "07 May 24") from the text
        date = None
        for line in extracted_text.split("\n"):
            if "May" in line or "Jun" in line:  # Adjust for relevant months
                date = line.strip()
                break

        # Rename the file
        if date:
            new_filename = date.replace(" ", "-") + ".jpeg"
            new_path = os.path.join(output_folder, new_filename)
            os.rename(image_path, new_path)
            print(f"Renamed: {filename} to {new_filename}")
        else:
            print(f"No date found in {filename}, skipping.")

print("Renaming complete!")