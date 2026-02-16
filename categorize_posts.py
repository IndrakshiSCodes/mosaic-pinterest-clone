import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mosaic_project.settings')
django.setup()

from posts.models import Post

def categorize_posts():
    """Automatically categorize posts based on keywords"""
    
    # Keywords that indicate women's/ladies items
    ladies_keywords = ['women', 'womens', 'ladies', 'dress', 'lehenga', 'kurti', 'sharara', 
                       'sundress', 'heels', 'heel', 'feminine', 'girl', 'girls', 'female']
    
    # Keywords that indicate men's/gentlemen items
    gentlemen_keywords = ['men', 'mens', 'gentlemen', 'male', 'masculine', 'boy', 'boys', 'guy', 'guys']
    
    posts = Post.objects.all()
    total = posts.count()
    
    ladies_count = 0
    gentlemen_count = 0
    neutral_count = 0
    
    print(f"Categorizing {total} posts...")
    
    for i, post in enumerate(posts, 1):
        keywords_lower = post.keywords.lower()
        
        # Check if it's a ladies item
        if any(keyword in keywords_lower for keyword in ladies_keywords):
            post.category = 'ladies'
            ladies_count += 1
        # Check if it's a gentlemen item
        elif any(keyword in keywords_lower for keyword in gentlemen_keywords):
            post.category = 'gentlemen'
            gentlemen_count += 1
        # Otherwise, it's neutral
        else:
            post.category = 'neutral'
            neutral_count += 1
        
        post.save()
        print(f"[{i}/{total}] {post.caption} → {post.category}")
    
    print(f"\n✅ Categorization complete!")
    print(f"Ladies: {ladies_count}")
    print(f"Gentlemen: {gentlemen_count}")
    print(f"Neutral: {neutral_count}")

if __name__ == '__main__':
    categorize_posts()