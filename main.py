import os
from os import listdir
from os.path import isfile, join
import requests
from PIL import Image

# Download images from a base URL and save them to a directory
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


# Get a list of all paths to images in a directory
def get_all_images(dir):
    images = []
    for filename in listdir(dir):
        path = join(dir, filename)
        if isfile(path):
            extension = filename.lower().split('.')[-1]
            if extension in ('jpg', 'jpeg', 'png'):
                images.append(path)
    return images    


# Open images from a list of paths
def open_images(image_paths):
    images = []
    for image_path in image_paths:
        images.append(Image.open(image_path))
    return images


# Find all images in a directory and concatenate them to a PDF
def concat_images_to_pdf(image_dir, pdf_path):

    # Find an open all images in the directory
    image_paths = get_all_images(image_dir)
    images = open_images(image_paths)
    
    # Check if any images were found
    if not images:
        print("No images found in directory")
        return

    # Create a new PDF with the same mode, size, and format as the first image
    first_image = images[0]
    pdf = first_image.convert('RGB').save(pdf_path, save_all=True, append_images=images[1:])

    print(f"\nPdf created at: {os.path.abspath(pdf_path)}\n")


def main():
    image_dir = "images"
    base_url = "http://readonline.ebookstou.org/flipbook/40908/files/mobile"

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        download_images(base_url, image_dir)
    else: 
        print(f"\nSkipping download, found source images in directory: {os.path.abspath(image_dir)}")

    concat_images_to_pdf(image_dir, "result.pdf")


if __name__ == "__main__":
    main()