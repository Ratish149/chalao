# CHALAO

Chalao - Bike Rental Platform

## Description

Chalao is a Django-based bike rental platform. This repository contains the source code for the backend of the project. The project allows users to book bikes, manage their bookings, and perform other related activities through REST APIs.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- Django 3.2 or higher
- pip (Python package installer)
- Virtualenv (for creating a virtual environment)

## Getting Started

Follow these instructions to set up and run the Django project on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/chalau.git
cd chalau
```

### 2. Create a Virtual Environment

Create a virtual environment outside the Clone directory to isolate the project dependencies:

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment using the appropriate command for your operating system:

```bash
On windows: venv\Scripts\activate
On MacOS: source venv/bin/activate
```

### 4. Install the Required Packages

Install the required packages using the requirements.txt file:

```bash
cd [project-folder-name]
pip install -r requirements.txt
```

### 5. Apply Migrations

Apply the database migrations to set up the database schema:

```bash
python manage.py migrate
```

### 6. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

### 7. Access API Documentation

You can access the API documentation by navigating to the following URL in your web browser:

```bash
http://127.0.0.1:8000/redoc/
```

### 8. Access API 

You can access the API by navigating to the following URL in your web browser:

```bash
http://127.0.0.1:8000/swagger/
```



