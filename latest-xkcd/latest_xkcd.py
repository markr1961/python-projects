
# download and display latest xkcd

# for Windows requires:
# pip install requests pillow
# for x-windows requires:
# pip install requests matplotlib

import requests

# Windows: opens the associated app.
# from PIL import Image

# x-windows
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from io import BytesIO

def fetch_latest_xkcd():
    # Fetching the latest xkcd comic metadata
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"Title: {data['title']}")
        print(f"Alt text: {data['alt']}")
        
        # Downloading the image
        img_url = data['img']
        img_response = requests.get(img_url)

        if img_response.status_code == 200:
            # Displaying the image using associated app
#            img = Image.open(BytesIO(img_response.content))
#            img.show()
            # Displaying the image in an X-window
            img = mpimg.imread(BytesIO(img_response.content), format='jpg')
            plt.imshow(img)
            plt.axis('off')  # Hide axis for better display
            plt.title(data['title'])  # Display the title as the image's title
            plt.show()
        else:
            print("Failed to download the image.")
    else:
        print("Failed to fetch the latest xkcd comic.")

if __name__ == "__main__":
    fetch_latest_xkcd()
