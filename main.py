import os
import requests

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


def main():
    if not os.path.exists("./raw_images"):
        os.makedirs("./raw_images")
        download_images()

if __name__ == "__main__":
    main()