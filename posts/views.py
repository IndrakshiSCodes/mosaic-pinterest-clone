from .models import Post, UserTheme  
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.db.models import Q, Count
from django.contrib.auth import login, authenticate, logout  
from django.contrib.auth.models import User  
from django.contrib import messages  
import re


def home(request):
    posts = Post.objects.all()
    return render(request, 'posts/home.html', {'posts': posts})

def search(request):
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', None)
    
    if query:
        # Split query into words
        keywords = query.lower().split()
        
        # Find posts and count keyword matches
        if category_filter:
            posts = Post.objects.filter(category=category_filter)
        else:
            posts = Post.objects.all()
        
        post_scores = []
        
        for post in posts:
            post_keywords = post.keywords.lower()
            score = sum(1 for keyword in keywords if keyword in post_keywords)
            if score > 0:
                post_scores.append((post, score))
        
        # Sort by score (highest first)
        post_scores.sort(key=lambda x: x[1], reverse=True)
        posts = [post for post, score in post_scores]
    else:
        posts = []
    
    return render(request, 'posts/search.html', {'posts': posts, 'query': query})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Get visually similar posts using image features
    if post.image_features:
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity
        
        # Convert current post features to numpy array
        current_features = np.array([float(x) for x in post.image_features.split(',')])
        
        # Calculate similarity with all other posts
        similar_posts = []
        for other_post in Post.objects.exclude(pk=pk):
            if other_post.image_features:
                other_features = np.array([float(x) for x in other_post.image_features.split(',')])
                similarity = cosine_similarity([current_features], [other_features])[0][0]
                similar_posts.append((other_post, similarity))
        
        # Sort by similarity score (highest first) and get top 6
        similar_posts.sort(key=lambda x: x[1], reverse=True)
        similar_posts = [post for post, score in similar_posts[:6]]
    else:
        # Fallback to keyword-based similarity if no features
        post_keywords = post.keywords.lower().split(',')
        similar_posts = []
        
        for other_post in Post.objects.exclude(pk=pk):
            other_keywords = other_post.keywords.lower()
            score = sum(1 for keyword in post_keywords if keyword.strip() in other_keywords)
            if score > 0:
                similar_posts.append((other_post, score))
        
        similar_posts.sort(key=lambda x: x[1], reverse=True)
        similar_posts = [post for post, score in similar_posts[:6]]
    
    return render(request, 'posts/post_detail.html', {'post': post, 'similar_posts': similar_posts})

def upload_post(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption')
        description = request.POST.get('description')
        link = request.POST.get('link')
        keywords = request.POST.get('keywords')
        category = request.POST.get('category', 'neutral')
        
        Post.objects.create(
            image=image,
            caption=caption,
            description=description,
            link=link,
            keywords=keywords,
            category=category,
            user=request.user  
        )
        return redirect('home')
    
    return render(request, 'posts/upload.html')

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.user != request.user:
        messages.error(request, "hey bestie, you can't edit someone else's post! 🚫")
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
        post.caption = request.POST.get('caption')
        post.description = request.POST.get('description')
        post.link = request.POST.get('link')
        post.keywords = request.POST.get('keywords')
        post.category = request.POST.get('category', post.category)
        post.save()
        messages.success(request, "post updated successfully! ✨")
        return redirect('post_detail', pk=pk)
    
    return render(request, 'posts/edit_post.html', {'post': post})

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    
    if post.user != request.user:
        messages.error(request, "hey bestie, you can't delete someone else's post! 🚫")
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        post.image.delete()  # Delete the image file
        post.delete()  # Delete from database
        messages.success(request, "post deleted successfully! ✨")
        return redirect('home')
    
    return render(request, 'posts/delete_post.html', {'post': post})

def category(request, category_name):
    posts = Post.objects.filter(category=category_name)
    return render(request, 'posts/category.html', {'posts': posts, 'category': category_name})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Username validation
        if not re.match(r'^[A-Za-z][A-Za-z0-9-]*$', username):
            messages.error(request, "username must start with a letter and can only contain letters, numbers, and '-'")
            return redirect('signup')
        
        # Contact number validation
        if not contact_number.isdigit():
            messages.error(request, "contact number must contain only digits")
            return redirect('signup')

        if len(contact_number) != 10:
            messages.error(request, "contact number must be exactly 10 digits")
            return redirect('signup')

        if contact_number[0] in ['1','2','3','4','5']:
            messages.error(request, "contact number must start with 6, 7, 8, or 9")
            return redirect('signup')


        if password1 != password2:
            messages.error(request, "passwords don't match")
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "username already taken, try another one!")
            return redirect('signup')
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        user_theme, created = UserTheme.objects.get_or_create(user=user)
        user_theme.contact_number = contact_number
        user_theme.save()

        login(request, user)
        messages.success(request, f"welcome to mosaic, {username}! ✨")
        return redirect('home')
    
    return render(request, 'registration/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"hey {username}, you're back! ")
            return redirect('home')
        else:
            messages.error(request, "wrong username or password")
            return redirect('login')
    
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "logged out successfully! see you soon ✨")
    return redirect('home')

def change_theme(request, theme_name):
    if request.user.is_authenticated:
        user_theme, created = UserTheme.objects.get_or_create(user=request.user)
        user_theme.theme = theme_name
        user_theme.save()
        messages.success(request, f"theme changed to {theme_name}! ✨")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(user=profile_user).order_by('-upload_date')
    
    return render(request, 'posts/profile.html', {
        'profile_user': profile_user,
        'user_posts': user_posts,
        'post_count': user_posts.count()
    })