# MOSAIC - Pinterest-Inspired Image Sharing Platform

A visually stunning image sharing and discovery platform built with Django, featuring ML-powered image recommendations, customizable themes, and category-based browsing.

## 🎨 Features

### Core Functionality
- **Image Upload & Management**: Users can upload images with captions, descriptions, links, and keywords
- **Smart Search**: Keyword-based search with ranking algorithm that prioritizes best matches
- **Category Filtering**: Browse images by Ladies, Gentlemen, or view all
- **Edit & Delete**: Full CRUD operations for managing your uploads

### Advanced Features
- **ML-Powered Recommendations**: Uses ResNet50 deep learning model to find visually similar images
- **User Authentication**: Secure login/signup system with personalized experiences
- **Multiple Themes**: 6 beautiful themes to customize your experience:
  - Default (Navy & Pale Blue)
  - Benito (Warm Coral & Pink)
  - Earthy (Sage Green & Cream)
  - Marty Supreme (Orange & Teal)
  - Lanacore (Burgundy & Olive)
  - Italian Summer (Brown & Golden Yellow)

### UI/UX
- **Masonry Grid Layout**: Pinterest-style responsive image grid
- **Smooth Animations**: Fade-in effects and page transitions
- **Hover Effects**: Translucent image overlays on hover
- **Responsive Design**: Works beautifully on desktop, tablet, and mobile
- **Custom Fonts**: Didot-style typography for elegant aesthetics

## 🛠️ Tech Stack

- **Backend**: Django 4.x (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite (easily switchable to PostgreSQL)
- **ML/AI**: PyTorch, TorchVision (ResNet50)
- **Image Processing**: Pillow
- **Icons**: Font Awesome 6

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation & Setup

### 1. Clone or Download the Project
```bash
cd Desktop
# Extract mosaic folder to Desktop
cd mosaic
```

### 2. Install Required Packages
```bash
python -m pip install django pillow torch torchvision numpy scikit-learn
```

### 3. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Admin User (Optional)
```bash
python manage.py createsuperuser
```

### 5. Extract ML Features for Existing Images
```bash
python extract_features.py
```

### 6. Run Development Server
```bash
python manage.py runserver
```

### 7. Access the Application
Open your browser and navigate to: `http://127.0.0.1:8000/`

## 📁 Project Structure
```
mosaic/
├── mosaic_project/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── posts/                   # Main application
│   ├── migrations/
│   ├── templates/
│   │   ├── posts/          # Main templates
│   │   └── registration/   # Auth templates
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── urls.py             # URL routing
│   └── admin.py            # Admin configuration
├── media/                   # Uploaded images
├── static/                  # Static files (CSS, images)
├── sample_images/           # Bulk upload images
├── extract_features.py      # ML feature extraction
├── categorize_posts.py      # Auto-categorization script
├── bulk_upload.py           # Bulk image upload script
├── manage.py                # Django management
└── db.sqlite3              # Database file
```

## 💡 Usage Guide

### For Users

**Signing Up**
1. Click "Sign Up" in the navbar
2. Create username and password
3. Start uploading and customizing!

**Uploading Images**
1. Click "Upload" button
2. Select image file
3. Add caption, description, optional link
4. Add comma-separated keywords
5. Choose category (Ladies/Gentlemen/Neutral)
6. Click "Upload Post"

**Searching**
- Type keywords in search bar
- Results ranked by keyword relevance
- Can search within specific categories

**Changing Themes**
1. Click "Theme" dropdown (when logged in)
2. Select your preferred theme
3. Theme persists across sessions

### For Developers

**Adding Bulk Images**
1. Place images in `sample_images/` folder
2. Create `image_data.txt` with format:
```
   filename.jpg | Caption | Description | link | keywords, separated, by, commas
```
3. Run: `python bulk_upload.py`
4. Run: `python extract_features.py`

**Auto-Categorizing Images**
```bash
python categorize_posts.py
```

**Accessing Admin Panel**
Navigate to `http://127.0.0.1:8000/admin/`

## 🎯 Key Algorithms

### Keyword-Based Search Ranking
- Splits search query into individual words
- Counts keyword matches for each post
- Sorts results by match count (descending)

### ML Visual Similarity
- Uses pre-trained ResNet50 model
- Extracts 2048-dimensional feature vectors
- Computes cosine similarity between vectors
- Returns top 6 most similar images

### Auto-Categorization
- Analyzes keywords for gender-specific terms
- Automatically assigns Ladies/Gentlemen/Neutral
- Runs on all existing posts

## 🔮 Future Enhancements

- [ ] Pinterest-style boards for saving images
- [ ] Image download functionality
- [ ] Social features (likes, comments)
- [ ] User profiles
- [ ] Image tagging
- [ ] Advanced filters
- [ ] API endpoints

## 👨‍💻 Development

**Author**: [Your Name]
**Institution**: [Your College Name]
**Course**: [Your Course]
**Year**: 2026

## 📄 License

This project was created as a college assignment and is available for educational purposes.

## 🙏 Acknowledgments

- Django Documentation
- PyTorch Documentation
- Bootstrap Framework
- Font Awesome Icons
- Code with Harry (Django Tutorial)