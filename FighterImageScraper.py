import requests
from bs4 import BeautifulSoup
import os




from ufcRatings import *


fighters_data = process_fights()


def format_name(name):
    """Format the athlete name to match the URL format."""
    return name.lower().replace(" ", "-")

def download_athlete_image(athlete_name, athlete ,output_folder="athlete_images"):
    # Step 1: Format the athlete's page URL
    formatted_name = format_name(athlete_name)
    base_url = f"https://www.ufc.com/athlete/{formatted_name}"
    print(f"Fetching data from: {base_url}")
    
    try:
        # Step 2: Send HTTP request to fetch the page
        response = requests.get(base_url)
        if response.status_code != 200:
            print(f"Failed to fetch the page for {athlete_name}. HTTP Status: {response.status_code}")
            return
        
        # Step 3: Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')




        
        # Step 4: Locate the image with the class 'hero-profile__image'
        img_tag = soup.find('img', class_='hero-profile__image')
        if not img_tag or not img_tag.get('src'):
            print(f"No image found for {athlete_name}")
            return
        
        img_url = img_tag['src']
        print(f"Image URL: {img_url}")


        record = soup.find('p',class_="hero-profile__division-body")
        if not record:
            print("NO RECORD FOUND")
        else :
            athlete["Record"] = record
            print(record)
        
        
        # Step 5: Download the image
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            # Ensure the output folder exists
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            # Create a file path to save the image
            filename = f"{athlete_name.replace(' ', '_')}.png"
            filepath = os.path.join(output_folder, filename)
            
            # Save the image
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image successfully downloaded: {filepath}")
        else:
            print(f"Failed to download the image. HTTP Status: {response.status_code}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def download_all_fighters():
    global current_image_index
    current_image_index = current_image_index + 1
    download_athlete_image((fighters_data[current_image_index]["Name"]), fighters_data[current_image_index])

current_image_index = 0


while current_image_index < 2653:
    download_all_fighters()






