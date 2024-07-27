import shutil

def copy_file_with_different_names(source_file_path, destination_folder, num_copies):
    # Get the filename from the source file path
    file_name = source_file_path.split('/')[-1]

    for i in range(1, num_copies + 1):
        # Construct the new file name with a suffix
        new_file_name = f"nachricht_{i}.xml"

        # Create the full path for the destination file
        destination_path = f"{destination_folder}/{new_file_name}"

        # Copy the source file to the destination with the new name
        shutil.copy2(source_file_path, destination_path)
        print(f"Copied {source_file_path} to {destination_path}")

# Example usage:
source_file_path = 'nachricht.xml'  # Replace with the path to your source file
destination_folder = 'nachrichten'  # Replace with the path to your destination folder
num_copies = 1000  # Number of copies you want to create

copy_file_with_different_names(source_file_path, destination_folder, num_copies)
