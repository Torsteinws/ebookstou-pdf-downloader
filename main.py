import os
import sys
import requests
from PIL import Image
from urllib.parse import urlparse

# Download images from a base URL and save them to a directory
def download_images(base_url, dir_name): 
    i = 1
    while True:
        # Send a GET request to the image URL
        image_url = f"{base_url}/{i}.jpg"
        response = requests.get(image_url)  

        # We have iterated over all images when we get a 404 response
        if response.status_code == 404:
            print(f"\n-----------------------------------\nDownloaded {i - 1} images\n-----------------------------------" if i > 1 else f"No images found at: {base_url}")
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
    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        if os.path.isfile(path):
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


def images_exists(image_dir):
    images = get_all_images(image_dir)
    return len(images) > 0


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def main(base_url):
    image_dir = "images"
    os.makedirs(image_dir, exist_ok=True)

    if not images_exists(image_dir):
        download_images(base_url, image_dir)
    else: 
        print(f"\nSkipping download, found source images in directory: {os.path.abspath(image_dir)}")

    if images_exists(image_dir):
        concat_images_to_pdf(image_dir, "result.pdf")
    else:
        print("\nDid not create pdf file :-(")


if __name__ == "__main__":
    # Override the base URL if a command line argument is provided
    base_url = "http://readonline.ebookstou.org/flipbook/40908/files/mobile"
    if len(sys.argv) > 1:
        if not is_valid_url(sys.argv[1]):
            print(f"Invalid base URL: {sys.argv[1]}")
            sys.exit()
        base_url = sys.argv[1]

    main(base_url)