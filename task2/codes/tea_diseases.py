import kagglehub
import os
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

# Download latest version
path = kagglehub.dataset_download("shashwatwork/identifying-disease-in-tea-leafs")

print("Path to dataset files:", path)


# Path to downloaded dataset
dataset_path = path

print("Contents of the dataset directory:")
for item in os.listdir(dataset_path):
    item_path = os.path.join(dataset_path, item)
    if os.path.isdir(item_path):
        print(f"Directory: {item}")
        # List a few files in each subdirectory
        sample_files = os.listdir(item_path)[:5]  # Adjust the number as needed
        for file in sample_files:
            print(f"  - {file}")
    else:
        print(f"File: {item}")

# Function to display a sample image from each category
def display_sample_images(dataset_path, categories, num_samples=1):
    plt.figure(figsize=(15, 10))
    for i, category in enumerate(categories):
        category_path = os.path.join(dataset_path, category)
        if os.path.exists(category_path):
            image_files = os.listdir(category_path)[:num_samples]
            for j, image_file in enumerate(image_files):
                image_path = os.path.join(category_path, image_file)
                try:
                    img = Image.open(image_path)
                    plt.subplot(len(categories), num_samples, i * num_samples + j + 1)
                    plt.imshow(img)
                    plt.title(f"{category} - Sample {j+1}")
                    plt.axis('off')
                except Exception as e:
                    print(f"Error loading image {image_path}: {e}")
        else:
            print(f"Category directory {category_path} does not exist.")
    plt.tight_layout()
    plt.show()

# Define the categories based on the dataset description
categories = [
    'Algal leaf spot',
    'Anthracnose',
    'Bird’s eye spot',
    'Brown blight',
    'Gray blight',
    'Healthy',
    'Red leaf spot',
    'White spot'
]

# Display sample images
display_sample_images(dataset_path, categories)