import os
from os import listdir
from os.path import isfile, join
import requests
from PIL import Image

def download_images(base_url, dir_name): 

    i = 1
    while True:

        # Send a GET request to the image URL
        image_url = f"{base_url}/{i}.jpg"
        response = requests.get(image_url)  

        # We have iterated over all images when we get a 404 response
        if response.status_code == 404:
            print(f"\n-----------------------------------\nDownloaded {i - 1} images\n-----------------------------------" if i > 1 else "No images found")
            return

        # Stop if the request was unsuccessful
        if response.status_code != 200:
            print(f"Exiting with unexpected response: {response.status_code} {response.reason}")
            return

        # Save the image to a file
        filename = f"{dir_name}/{i:04d}.jpg"
        with open(filename, "wb") as file:
            file.write(response.content)  
            
        print(f"Downloaded: {filename}")

        i += 1


def convert_images_to_pdf(image_dir, pdf_path):

    images = [Image.open(join(image_dir, f)) for f in listdir(image_dir) if isfile(join(image_dir, f)) and f.lower().split('.')[-1] in ('jpg', 'jpeg', 'png')]
    
    # Check if any images were found
    if not images:
        return print("No images found in directory")
    
    first_image = images[0]
    # Create a new PDF with the same mode, size, and format as the first image
    pdf = first_image.convert('RGB').save(pdf_path, save_all=True, append_images=images[1:])

    print(f"\nPdf path: {os.path.abspath(pdf_path)}\n")

def main():
    image_dir = "raw_images"
    base_url = "http://readonline.ebookstou.org/flipbook/40908/files/mobile"

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        download_images(base_url, image_dir)
    else: 
        print(f"Directory {image_dir} already exists. Skipping download")

    convert_images_to_pdf(image_dir, "result.pdf")

if __name__ == "__main__":
    main()