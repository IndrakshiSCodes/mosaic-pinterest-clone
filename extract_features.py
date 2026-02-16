import os
import django
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mosaic_project.settings')
django.setup()

from posts.models import Post

# Load pre-trained ResNet model
model = models.resnet50(pretrained=True)
model.eval()

# Remove the final classification layer to get features
feature_extractor = torch.nn.Sequential(*list(model.children())[:-1])

# Image preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def extract_image_features(image_path):
    """Extract features from an image using ResNet50"""
    try:
        img = Image.open(image_path).convert('RGB')
        img_tensor = preprocess(img).unsqueeze(0)
        
        with torch.no_grad():
            features = feature_extractor(img_tensor)
        
        # Flatten and convert to list
        features = features.squeeze().numpy().flatten()
        return features.tolist()
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def extract_all_features():
    """Extract features for all posts in the database"""
    posts = Post.objects.all()
    total = posts.count()
    
    print(f"Extracting features for {total} images...")
    
    for i, post in enumerate(posts, 1):
        if post.image_features:
            print(f"[{i}/{total}] Skipping {post.caption} (already has features)")
            continue
        
        image_path = post.image.path
        features = extract_image_features(image_path)
        
        if features:
            # Store as comma-separated string
            post.image_features = ','.join(map(str, features))
            post.save()
            print(f"[{i}/{total}] ✓ Extracted features for: {post.caption}")
        else:
            print(f"[{i}/{total}] ✗ Failed: {post.caption}")
    
    print("\n✅ Feature extraction complete!")

if __name__ == '__main__':
    extract_all_features()