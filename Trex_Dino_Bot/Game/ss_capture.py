# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 14:40:12 2024

@author: Amitr
"""

import cv2
import numpy as np
import pyautogui
import pandas as pd
import os
import matplotlib.pyplot as plt
import time
from pynput import keyboard

current_dir = os.path.dirname(os.path.abspath(__file__))
# current_dir=os.getcwd()
dir_path='assets\\images\\'
csv_path=os.path.join(current_dir, dir_path, 'resources.csv')
png_path=os.path.join(current_dir, dir_path, 'resources.png')
img_path=os.path.join(current_dir, dir_path, 'resources.png')
  

def shrink(image,x_scale,y_scale):
    return cv2.resize(image, (int(x_scale*image.shape[1]),int(y_scale*image.shape[0])), interpolation= cv2.INTER_LINEAR)


def load_assets(csvpath=csv_path,pngpath=png_path,x_scale=None,y_scale=None):
    """Load game assets."""
    assets={}
    # Read the CSV file using pandas
    csv_path = csvpath # os.path.join(current_dir, dir_path, 'resources.csv')
    df = pd.read_csv(csv_path)
    
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Extract information from the row
        resourceName = row['resourceName']
        x1, y1, x2, y2 = int(row['X1']), int(row['Y1']), int(row['X2']), int(row['Y2'])
        h=y2-y1;w=x2-x1
        # print(resourceName,h,w,sep='::')
        
        # Open the image file
        png_path=pngpath#os.path.join(current_dir, dir_path, 'resources.png')
        
        # image = Image.open(png_path)
        image=cv2.imread(png_path)
        
        # Crop the image based on the provided coordinates
        # cropped_image = image.crop((x1, y1, x2, y2))
        cropped_image = image[y1:y2,x1:x2]
        
        
        # Convert the cropped image to RGB mode to remove any alpha channel
        # cropped_image = cropped_image.convert("RGB")
        
        background=cropped_image
        
        if x_scale==None:
            x_scale=row['xscale']
        if y_scale==None:
            y_scale=row['yscale']
        
        
        # background=background.convert('RGBA')
        # background=background.resize(list(map(lambda x:x//2 , background.size)))
        
        assets[resourceName]=background
    return assets

# Load game assets
assets=load_assets()





# Load the main image (resources.png)
main_image = cv2.imread(img_path)

rname='obstacle4'

# #for init in chrome dino x=45,y=60 window: x1, y1, x2, y2 = 580, 180, 1150, 380
# #chrome:dino dino2 276:426,80:220 x=140,y=150 window: x1, y1, x2, y2 = 0, 340, 1870, 780

# refx1=80;refx2=220;refy1=276;refy2=426
# main_image_ref=main_image[refy1:refy2,refx1:refx2]
# print(f'ref:{main_image_ref.shape}')

# Load the dino.png template image
xscale=1#1.6129032258064515 # main_image_ref.shape[0]/assets[rname].shape[0]
yscale=1#1.627906976744186 # main_image_ref.shape[1]/assets[rname].shape[1]

# template_image = shrink(assets[rname],45/93,60/86)
template_image = shrink(assets[rname],xscale,yscale)

plt.imshow(template_image)
print(f'new template image shape:{template_image.shape} with scale x: {xscale} and y: {yscale}')

# Convert the images to grayscale
main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

if np.max(main_gray)<255:
    main_gray=255-main_gray

if np.max(template_gray)<255:
    main_gray=255-template_gray


main_gray=cv2.normalize(main_gray, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

template_gray=cv2.normalize(template_gray, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)


# Perform template matching
result = cv2.matchTemplate(main_gray, template_gray, cv2.TM_CCOEFF_NORMED)

# Define a threshold to consider a match
threshold = 0.9
loc = np.where(result >= threshold)

# Extract coordinates of the matches
matches = []
for pt in zip(*loc[::-1]):
    matches.append((pt[0], pt[1], pt[0] + template_image.shape[1], pt[1] + template_image.shape[0]))

# # Load coordinates from resources.csv'

# # df = pd.read_csv(csv_path)
# # dino_coords = df[df['resourceName'] == rname]  # Assuming the resource name for dino is 'dino0'
# # dino_x1, dino_y1, dino_x2, dino_y2 = dino_coords['X1'].values[0], dino_coords['Y1'].values[0], \
# #                                       dino_coords['X2'].values[0], dino_coords['Y2'].values[0]


# # print("\nCoordinates of the dino from resources.csv:")
# # print(f"X1: {dino_x1}, Y1: {dino_y1}, X2: {dino_x2}, Y2: {dino_y2}")

# # Display coordinates of the matches and from resources.csv
# print("Coordinates of the matches found by template matching:")
# for match in matches:
#     print(f"X1: {match[0]}, Y1: {match[1]}, X2: {match[2]}, Y2: {match[3]}")




def getcoords(m):
    a, b, c, d = zip(*m)
    return min(a), min(b), max(c), max(d)

coods = {};obstacles=0
for j in range(main_gray.shape[1] // template_gray.shape[1]):
    x = [i for i in matches if i[0] >= min([match[0] for match in matches]) + (template_gray.shape[1] * j) and i[0] <= min([match[0] for match in matches]) + (template_gray.shape[1] * (j + 1))]
    if len(x) > 0:
        coods[f"Obstacle_{obstacles}"] = x
        obstacles+=1

obstacles = len(coods)

# Create a new figure with subplots
plots = obstacles + 1
print(f'Num of obstacles matched: {obstacles}')
fig, axes = plt.subplots(plots // 2, 2)

for j in range(obstacles):
    refx1, refy1, refx2, refy2 = getcoords(coods[f"Obstacle_{j}"])    
    print(f'X1:{refx1}\tX2:{refx2}\tY1:{refy1}\tY2:{refy2}')

    # Display the main_gray image on the subplot
    axes[j // 2, (j % 2)].imshow(main_gray[refy1:refy2, refx1:refx2], cmap='gray')
    axes[j // 2, (j % 2)].set_title(f'Obstacle_{j}')

if obstacles == 0:
    # Display the main_gray image on the first subplot
    axes[0, 0].imshow(main_gray, cmap='gray')
    axes[0, 0].set_title('Main Image')

# Display the template_gray image on the last subplot
if plots % 2 == 0:
    axes[plots // 2 - 1, 1].imshow(template_gray, cmap='gray')
    axes[plots // 2-1, 1].set_title('Template Image')

else:
    axes[plots // 2, 0].imshow(template_gray, cmap='gray')
    axes[plots // 2, 0].set_title('Template Image')

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()

# # Define the region of interest (ROI) for the Dino game window
# # You need to adjust these coordinates according to your screen resolution

# # w=600
# # h=150
# # wt=w*1.63667
# # ht=h*1.63667+52.5

# # x1, y1, x2, y2 = 580, 180, 1150, 380  # Example coordinates, adjust as needed

# # Define the region of interest (ROI) for the Dino game window
# x1, y1, x2, y2 = 0, 340, 1870, 780  # Adjust these coordinates according to your screen resolution

# # Global variable to track whether the game is playing
# isplaying = False

# # Function to capture a screenshot
# def takess(x, y, width, height):
#     screenshot = pyautogui.screenshot(region=(x, y, width, height))
#     return np.array(screenshot)

# def checkstop(current_image, impath, threshold=10.0):
#     if not os.path.isfile(impath):
#         print("The PNG file does not exist at the specified path.")
#         return False
    
#     try:
#         png_image = cv2.imread(impath)
#         mse = np.mean((current_image - png_image) ** 2)
#         print(f"MSE: {mse}, Threshold: {threshold}")
#         if mse < threshold:
#             print("The images are the same.")
#             return True
#         else:
#             print("The images are different.")
#             return False
#     except Exception as e:
#         print(f"Error: {e}")
#         return False

# # Function to handle key presses
# def on_press(key):
#     global isplaying
#     try:
#         if key == keyboard.Key.up or key == keyboard.Key.space:
#             isplaying = True
#             while isplaying:
#                 captured_image = takess(x1, y1, x2 - x1, y2 - y1)
#                 istopped = checkstop(captured_image, path2)
#                 plt.imshow(captured_image)
#                 plt.draw()
#                 plt.pause(0.1)
#                 plt.imsave(path2, captured_image)
                
#                 if istopped:
#                     break
#             return False
#         elif key == keyboard.Key.q:
#             isplaying = False
#             return False
#     except AttributeError:
#         pass

# # Set up the keyboard listener
# with keyboard.Listener(on_press=on_press) as listener:
#     listener.join()

# # Close the plot
# plt.close()