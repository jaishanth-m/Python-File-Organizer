import os
import shutil
from datetime import datetime

# Get folder path from user
folder_path = input("Enter folder path: ").strip()

# Check if folder exists
if not os.path.isdir(folder_path):
    print("Invalid folder path!")
    exit()

# File categories
file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".7z"]
}

# Statistics
count = {}

# Log file path
log_file = os.path.join(folder_path, "organizer_log.txt")

# Files to skip
skip_files = [
    "organizer_log.txt",
    os.path.basename(__file__)
]

with open(log_file, "w") as log:

    log.write("===== FILE ORGANIZER LOG =====\n")
    log.write(f"Date: {datetime.now()}\n\n")

    for file in os.listdir(folder_path):

        # Skip log file and script file
        if file in skip_files:
            continue

        file_path = os.path.join(folder_path, file)

        # Process only files
        if os.path.isfile(file_path):

            extension = os.path.splitext(file)[1].lower()

            destination_folder = "Others"

            # Find matching category
            for category, extensions in file_types.items():
                if extension in extensions:
                    destination_folder = category
                    break

            destination_path = os.path.join(
                folder_path,
                destination_folder
            )

            # Create folder if it doesn't exist
            os.makedirs(destination_path, exist_ok=True)

            new_location = os.path.join(
                destination_path,
                file
            )

            # Handle duplicate file names
            if os.path.exists(new_location):

                name, ext = os.path.splitext(file)
                counter = 1

                while os.path.exists(new_location):
                    new_location = os.path.join(
                        destination_path,
                        f"{name}_{counter}{ext}"
                    )
                    counter += 1

            # Move file
            shutil.move(file_path, new_location)

            # Update count
            count[destination_folder] = (
                count.get(destination_folder, 0) + 1
            )

            # Write log
            log.write(
                f"{file} --> {destination_folder}\n"
            )

# Display summary
print("\n================================")
print(" FILE ORGANIZATION COMPLETED ")
print("================================\n")

total_files = 0

for category, total in count.items():
    print(f"{category}: {total} file(s)")
    total_files += total

print(f"\nTotal files organized: {total_files}")
print("\nLog file created successfully!")