# 🍽️ Rust-Eze Recipes
A modern, dark‑themed Django recipe sharing platform.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.x-green.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

RecipeHub is a full‑stack Django web application that allows users to create, browse, categorize, and manage recipes through a clean, modern, dark‑themed interface. It includes user authentication, recipe submission, category filtering, admin management tools, and a responsive UI built with Bootstrap and custom CSS.

---

## ✨ Features

### 👤 User Accounts
- User registration and login  
- Edit account details  
- View all recipes created by the logged‑in user  
- Automatic author assignment for non‑admin users  

### 📚 Recipes
- Create, edit, and delete recipes  
- Upload recipe images  
- Detailed recipe pages with:
  - Ingredients  
  - Instructions  
  - Prep time, cook time, servings, difficulty  
  - Category pills  
- Category filtering (Breakfast, Lunch, Dinner, Health & Diet, etc.)  
- Search bar for recipe names and keywords  

### 🛠️ Admin Tools
- Admin dashboard for managing recipes  
- Category pills displayed in admin tables  
- Edit/delete actions for each recipe  

### 🎨 UI & Styling
- Fully responsive layout  
- Dark theme across navbar, footer, forms, and cards  
- Orange primary color + light‑grey secondary accents  
- Consistent pill styling across all pages  
- Clean, modern typography and spacing  

---

## 🧱 Tech Stack

- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, Bootstrap 5  
- **Database:** SQLite (default)  
- **Authentication:** Django’s built‑in auth system  
- **Media Handling:** Django `ImageField`  

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo

### 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Apply migrations
python manage.py migrate

5. Create a superuser (admin)
python manage.py createsuperuser

6. Run the development server
python manage.py runserver
