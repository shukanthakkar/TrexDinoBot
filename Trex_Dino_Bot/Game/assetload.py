import pandas as pd
from PIL import Image

# Read the CSV file using pandas
df = pd.read_csv('assets\\images\\resources.csv')

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Extract information from the row
    resourceName = row['resourceName']
    x1, y1, x2, y2 = int(row['X1']), int(row['Y1']), int(row['X2']), int(row['Y2'])
    
    # Open the image file
    image = Image.open('assets\\images\\resources.png')
    
    # Crop the image based on the provided coordinates
    cropped_image = image.crop((x1, y1, x2, y2))
    
    # Convert the cropped image to RGB mode to remove any alpha channel
    cropped_image = cropped_image.convert("RGB")
    
    # Create a new white background image with the same dimensions as the cropped image
    background = Image.new('RGB', cropped_image.size, color='white')
    
    # Paste the cropped image onto the white background
    background.paste(cropped_image, (0, 0))
    
    # Save the image with the resource name
    background.save(f'assets\\images\\{resourceName}.png')

print("Images cropped and saved successfully!")
