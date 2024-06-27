import os
from os import listdir
from os.path import isfile, join
import requests
from PIL import Image

def download_images(): 
    base_url = "http://readonline.ebookstou.org/flipbook/40908/files/mobile"
    for i in range(1, 71):  # Iterate from 1 to 70
        
        image_url = f"{base_url}/{i}.jpg"  # Construct the URL for each image
        
        response = requests.get(image_url)  
        if response.status_code == 200:  
            
            with open(f"raw_images/{i}.jpg", "wb") as file:  # Open a file for each image
                file.write(response.content)  # Write the content of the response to the file
            print(f"Downloaded: {i}.")
        else:
            print(f"Failed: {i}.jpg -- {response.status_code} {response.reason}")

def convert_images_to_pdf(image_dir, output_filename):
    """
    Converts all images in a directory to a single PDF file.

    Args:
    image_dir: Path to the directory containing images.
    output_filename: Name of the output PDF file.
    """
    
    images = [Image.open(join(image_dir, f)) for f in listdir(image_dir) if isfile(join(image_dir, f)) and f.lower().split('.')[-1] in ('jpg', 'jpeg', 'png')]
    # Check if any images were found
    if not images:
        print("No images found in directory")
        return
    
    first_image = images[0]
    # Create a new PDF with the same mode, size, and format as the first image
    pdf_path = f"{image_dir}/{output_filename}.pdf"
    pdf = first_image.convert('RGB').save(pdf_path, save_all=True, append_images=images[1:])

    print(f"Successfully converted images to PDF: {pdf_path}")

def main():
    if not os.path.exists("./raw_images"):
        os.makedirs("./raw_images")
        download_images()
    convert_images_to_pdf("raw_images", "output")

if __name__ == "__main__":
    main()