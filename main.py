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
            
            filename = f"raw_images/{i:03d}.jpg"  # Construct the file name for each image with 3 decimals

            with open(filename, "wb") as file:  # Open a file for each image
                file.write(response.content)  # Write the content of the response to the file
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed: {i}.jpg -- {response.status_code} {response.reason}")

def convert_images_to_pdf(image_dir, output_filename):

    pdf_path = f"{image_dir}/{output_filename}.pdf"
    if os.path.exists(pdf_path):
        return

    images = [Image.open(join(image_dir, f)) for f in listdir(image_dir) if isfile(join(image_dir, f)) and f.lower().split('.')[-1] in ('jpg', 'jpeg', 'png')]
    
    # Check if any images were found
    if not images:
        print("No images found in directory")
        return
    
    first_image = images[0]
    # Create a new PDF with the same mode, size, and format as the first image
    pdf = first_image.convert('RGB').save(pdf_path, save_all=True, append_images=images[1:])

    print(f"Successfully converted images to PDF: {pdf_path}")

def main():
    image_dir = "raw_images"

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        download_images()

    convert_images_to_pdf(image_dir, "0_book")

if __name__ == "__main__":
    main()