import os
from os import listdir
from os.path import isfile, join
import requests
from PIL import Image

def download_images(): 
    base_url = "http://readonline.ebookstou.org/flipbook/40908/files/mobile"
    
    for i in range(1, 71):  # Iterate from 1 to 70

        # Send a GET request to the image URL
        image_url = f"{base_url}/{i}.jpg"
        response = requests.get(image_url)  

        # Stop if the request was unsuccessful
        if response.status_code != 200:
            return print(f"Failed to download images: {response.status_code} {response.reason}")

        # Save the image to a file
        filename = f"raw_images/{i:03d}.jpg"
        with open(filename, "wb") as file:
            file.write(response.content)  
        print(f"Downloaded: {filename}")


def convert_images_to_pdf(image_dir, output_filename):

    pdf_path = f"{image_dir}/{output_filename}.pdf"
    if os.path.exists(pdf_path):
        return print(f"PDF already exists: {pdf_path}")

    images = [Image.open(join(image_dir, f)) for f in listdir(image_dir) if isfile(join(image_dir, f)) and f.lower().split('.')[-1] in ('jpg', 'jpeg', 'png')]
    
    # Check if any images were found
    if not images:
        return print("No images found in directory")
    
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