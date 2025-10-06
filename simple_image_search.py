import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import os
import requests
from io import BytesIO
import faiss

# Lets load the Restnet 18 model    
model = models.resnet18(pretrained=True).eval()

transform = transforms.Compose([
    transforms.Resize(256), transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def get_features(path_or_url):
    try:
        if path_or_url.startswith(('http://', 'https://')):
            img = Image.open(BytesIO(requests.get(path_or_url).content)).convert("RGB")
        else:
            img = Image.open(path_or_url).convert("RGB")
        
        with torch.no_grad():
            return model(transform(img).unsqueeze(0))[0].numpy()
    except Exception as e:
        print(f"Error processing {path_or_url}: {e}")
        return None

# now here lets make sure the image directory exists    
image_dir = "./images"
if not os.path.exists(image_dir):
    print(f"Error: {image_dir} not found")
    exit(1)

#from this line 40 to 53, we are indexing the images that are in my images folder
print("Processing images...")
paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir)]
fileFeatures = [get_features(p) for p in paths]
vectors = [v for v in fileFeatures if v is not None]


if not vectors:
    print("No valid images found")
    exit(1)


# Lets now create and populate vector index
index = faiss.IndexFlatL2(vectors[0].shape[0])
index.add(np.stack(vectors))


# now let the user input their Getpath or url 
query = input("\nEnter image path or URL: ").strip()
query_vector = get_features(query)
if query_vector is None:
    print("Error processing query image")
    exit(1)

# here we are printing the query image and the similar images   
print("\nQuery:", query)
print("Similar images:")
for idx in index.search(query_vector.reshape(1, -1), 3)[1][0]:
    print(f" - {paths[idx]}") 