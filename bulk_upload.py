import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mosaic_project.settings')
django.setup()

from posts.models import Post
from django.core.files import File

def bulk_upload():
    # Path to sample images folder
    images_folder = 'sample_images'
    data_file = os.path.join(images_folder, 'image_data.txt')
    
    print(f"Looking for data file at: {data_file}")
    
    if not os.path.exists(data_file):
        print(f"ERROR: {data_file} not found!")
        return
    
    print(f"Found data file!")
    
    # Read the data file
    with open(data_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Read {len(lines)} lines from file")
    
    for line in lines:
        if line.strip():
            parts = line.strip().split(' | ')
            print(f"Line has {len(parts)} parts")
            if len(parts) == 5:
                filename, caption, description, link, keywords = parts
                
                image_path = os.path.join(images_folder, filename)
                print(f"Checking: {image_path}")
                
                if os.path.exists(image_path):
                    print(f"✓ Found: {filename}")
                    with open(image_path, 'rb') as img_file:
                        Post.objects.create(
                            image=File(img_file, name=filename),
                            caption=caption,
                            description=description,
                            link=link if link and link != 'none' else None,
                            keywords=keywords
                        )
                    print(f"✓ Uploaded: {caption}")
                else:
                    print(f"✗ File not found: {filename}")
            else:
                print(f"Skipping line - wrong format")
    
    print(f"\n✅ Bulk upload complete! Total posts: {Post.objects.count()}")

if __name__ == '__main__':
    bulk_upload()