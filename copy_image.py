import os
import shutil

image_folder = "CollectedImages"
new_path = os.path.join(image_folder, "images")
os.makedirs(new_path, exist_ok=True)


for label in os.listdir(image_folder):
    label_path = os.path.join(image_folder, label)
    
    # skip the merged images folder
    if label == "images":
        continue

    for img in os.listdir(label_path):
        src = os.path.join(label_path, img)
        dst = os.path.join(new_path, img)

        print(f"Copying: {src} to: {dst}")
        shutil.copy(src=src, dst=dst)