import os
from PIL import Image
import concurrent.futures

def combine_images_vertically(folder_path, max_height=65500):
    print(f"Processing folder: {folder_path}")
    
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    
    # Filter out non-JPG files and sort the JPG files numerically
    jpg_files = sorted([f for f in files if f.endswith('.jpg')], key=lambda x: int(os.path.splitext(x)[0]))
    
    # Open the images and store them in a list
    images = [Image.open(os.path.join(folder_path, f)) for f in jpg_files]
    
    # Get the width and height of the first image
    width, height = images[0].size
    
    # Create a list to store the chunks of the combined image
    combined_image_chunks = []
    
    # Iterate over the images and paste them into chunks
    y_offset = 0
    chunk = Image.new('RGB', (width, max_height))
    for img in images:
        if y_offset + img.size[1] > max_height:
            # If the current image exceeds the maximum height, save the chunk and create a new one
            combined_image_chunks.append(chunk)
            chunk = Image.new('RGB', (width, max_height))
            y_offset = 0
        chunk.paste(img, (0, y_offset))
        y_offset += img.size[1]
    
    # Crop the last chunk to remove any black space at the bottom
    chunk = chunk.crop((0, 0, width, y_offset))
    
    # Append the last chunk to the list
    combined_image_chunks.append(chunk)
    
    # Return the list of combined image chunks
    return combined_image_chunks


def process_chapters(root_folder, output_directory, prefix, create_master=False):
    print(f"Starting processing of chapters in root folder: {root_folder}")
    
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Create a list to store the image pages from all chapters
    all_pages = []

    # Sort the chapter directories based on their numerical order
    chapter_dirs = sorted([d for d in os.listdir(root_folder) if d.startswith("Chapter")], key=lambda x: int(x.split()[-1]))
    
    # Process each chapter directory
    for chapter_dir in chapter_dirs:
        dirpath = os.path.join(root_folder, chapter_dir)
        combined_image_chunks = combine_images_vertically(dirpath)
        all_pages.extend(combined_image_chunks)
    
    # Save all the image pages to a single PDF file
    master_filename = f"{prefix}MASTER.pdf"
    master_path = os.path.join(output_directory, master_filename)
    all_pages[0].save(master_path, save_all=True, append_images=all_pages[1:], format='PDF')
    print(f"MASTER PDF saved to: {master_path}")

    print("Processing of chapters completed.")

# Example usage
prefix = "Leviathan_"
root_folder = '/Users/justinlin/Documents/Mangas/Leviathan'  # Change this to the path of your root folder
output_directory = '/Users/justinlin/Desktop/combinedPDF/output'  # Change this to the path of your output directory
process_chapters(root_folder, output_directory, prefix)
