# social-media-app-photo
i have created a social media app project with django framework, hope you like this app
# Photo App - Django Social Media Project

Photo App is a simple social media web application built with Django. Users can create an account, log in, edit their profile, upload photo posts, like posts, comment on posts, search for other users, follow profiles, switch between light and dark mode, and delete their own posts.

## Features

- User registration and login
- Password change and password reset pages
- Editable user profile with profile photo and bio
- Photo post creation with title, caption, and image upload
- Feed page showing latest posts
- Like and unlike posts without refreshing the page
- Comment system with only the first 3 comments shown by default
- "View all comments" button for posts with more comments
- User search page for finding friends by username
- Public profile pages
- Follow and unfollow users
- Follower and following counters
- Owner-only post deletion with confirmation
- Light mode and dark mode
- Responsive UI for desktop and mobile screens

## Tech Stack

- Python
- Django 6.0.5
- SQLite
- Pillow
- HTML
- CSS
- JavaScript
- TailwindCSS 2.2.16

## Project Structure

```text
social-media-app-photo/
|-- README.md
|-- .gitignore
|-- venv/
`-- socialproject/
    |-- manage.py
    |-- db.sqlite3
    |-- package.json
    |-- media/
    |-- socialproject/
    |   |-- settings.py
    |   `-- urls.py
    |-- users/
    |   |-- models.py
    |   |-- views.py
    |   |-- forms.py
    |   |-- urls.py
    |   |-- tests.py
    |   |-- templates/users/
    |   `-- static/users/
    `-- posts/
        |-- models.py
        |-- views.py
        |-- forms.py
        |-- urls.py
        |-- tests.py
        `-- templates/posts/
```

## Database

This project uses the default Django development database: SQLite.

The database configuration is in `socialproject/socialproject/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

The database file is:

```text
socialproject/db.sqlite3
```

## Main Django Apps

### users

The `users` app handles:

- Registration
- Login
- Logout
- Profile editing
- Profile photos
- User search
- Public profile pages
- Follow and unfollow behavior

Important files:

- `users/models.py` - profile model and following relationship
- `users/forms.py` - registration, login, user edit, and profile edit forms
- `users/views.py` - login, register, profile, search, and follow logic
- `users/templates/users/` - user-related HTML pages
- `users/static/users/style.css` - main UI styling
- `users/static/users/app.js` - frontend interactions

### posts

The `posts` app handles:

- Creating posts
- Feed page
- Likes
- Comments
- Post deletion

Important files:

- `posts/models.py` - post and comment models
- `posts/forms.py` - post creation and comment forms
- `posts/views.py` - feed, create post, like post, and delete post logic
- `posts/templates/posts/feed.html` - main feed UI

## Important Models

### Profile

Located in `users/models.py`.

The profile model extends Django's default user system with:

- Profile photo
- Bio
- Following list

```python
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="users/%Y/%m/%d", blank=True)
    bio = models.CharField(max_length=240, blank=True)
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="followers",
        blank=True,
    )
```

### Post

Located in `posts/models.py`.

Each post belongs to one user and can be liked by many users.

```python
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/%y/%m/%d")
    caption = models.TextField(blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    created = models.DateField(auto_now_add=True)
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="posts_liked",
        blank=True,
    )
```

### Comment

Located in `posts/models.py`.

Each comment belongs to one post.

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    body = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)
    posted_by = models.CharField(max_length=100)
```

## Setup Instructions

Open a terminal in the project folder:

```powershell
cd C:\Users\user\Desktop\social-media-app-photo\socialproject
```

Activate the virtual environment:

```powershell
..\venv\Scripts\activate
```

Install Python dependencies if needed:

```powershell
pip install Django pillow
```

Run migrations:

```powershell
python manage.py migrate
```

Start the development server:

```powershell
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

If port `8000` gives a permission error, use another port:

```powershell
python manage.py runserver 127.0.0.1:8001
```

Then open:

```text
http://127.0.0.1:8001/
```

## Running Tests

From the `socialproject` folder, run:

```powershell
python manage.py test users posts
```

The tests cover:

- Registration validation
- Unique email validation
- User search
- Follow and unfollow
- Preventing users from following themselves
- Like endpoint JSON response
- Comment author protection
- Owner-only post deletion

## Frontend Behavior

The main JavaScript file is:

```text
users/static/users/app.js
```

It controls:

- Light and dark mode
- Like buttons
- Follow buttons
- Share button
- Comment expansion
- Delete confirmation
- Image preview before upload
- Loading state on forms

The main custom CSS file is:

```text
users/static/users/style.css
```

It controls:

- Layout
- Responsive design
- Profile cards
- Post cards
- Forms
- Buttons
- Light and dark color themes

## Useful Commands

```powershell
python manage.py check
python manage.py test users posts
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8001
```

## Notes

- This project is currently configured for development.
- `DEBUG = True` should be changed before production deployment.
- SQLite is good for learning and small projects, but PostgreSQL or MySQL is better for production.
- Uploaded user images are stored in the `media/` folder.
- Static CSS, JavaScript, and icons are stored in `users/static/users/`.
