# Expense Sharing App

This is a Django-based application for managing and sharing expenses.

## Installation Guide

### Step 1: Environment Setup

#### Python Installation
Download and install Python from the [official Python website](https://www.python.org/downloads/). 
Ensure that Python and pip are correctly installed by running the following commands in your terminal:

```sh
python --version
pip --version
```

#### PostgreSQL Installation
Install PostgreSQL from the [official PostgreSQL website](https://www.postgresql.org/download/) and create a new database.

#### Virtual Environment Setup (optional)
Set up a virtual environment to manage dependencies locally:

```sh
python -m venv venv
source venv/bin/activate  # Use `venv\Scripts\activate` on Windows
```

### Step 2: Project Setup

#### Clone the Project Repository
Clone the project repository from GitHub:

```sh
git clone https://github.com/yourusername/expense-sharing-app.git
cd expense-sharing-app
```

#### Install Dependencies
Install the required dependencies:

```sh
pip install -r requirements.txt
```

#### Database Configuration
Configure your Django `settings.py` to connect to the PostgreSQL database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'expense_db',
        'USER': 'postgres',
        'PASSWORD': '',  # Add your PostgreSQL password here
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Step 3: Database Migrations

Initialize the database schema using Django's migration tools:

```sh
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Running the Application

Start the Django development server:

```sh
python manage.py runserver
```

Access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

