# Expense Tracker Application

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Generating Balance Sheet](#generating-balance-sheet)
- [Downloading Balance Sheet as PDF](#downloading-balance-sheet-as-pdf)
- [License](#license)

## Introduction
The Expense Tracker Application is designed to help users manage their expenses efficiently. Users can create, track, and participate in various expenses, while also generating and downloading balance sheets to keep track of their financial contributions and dues. This allows splitting of enxpenses in three ways Equal, Percentage, or Exact. Users can add their friends in an expense using their email as the key. The expense, on creation gets linked to their friends' email. When they logs in, they can see those expenses in the dashboard. Though they doesn't have an account, their are saved and they can see it after registration. However, registration is not mandatory for a participant in expense.

## Features
- User authentication (login and logout)
- Create expenses
- Track participation in expenses
- Generate a balance sheet of contributions
- Download balance sheet as a CSV

## Technologies Used
- Python 3.x
- Django 5.1.2
- MySQL

## Installation
To set up the project on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gthejesh/expense-tracker.git
   cd expense-tracker

2. **Create a virtual environment**
   ```bash
    python -m venv expshare
    expshare\Scripts\activate

3. **Install the required packages:**
   ```bash
    pip install -r requirements.txt

4. **Create and connect to database**
Create a MySQL database named expense_sharing and turn the server on. You can configure the database in settings.py. 

    ```sh
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'expense_sharing', 
        'USER': 'root', 
        'PASSWORD': '', 
        'HOST': 'localhost',
        'PORT': '3306',
        }
    }
    ```
Run the following command to migrate the Database to your server

    ```bash
    python manage.py migrate
    ```
5. **Create a superuser (optional, for admin access)**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**

```bash
python manage.py runserver
```

## Usage
- Navigate to http://127.0.0.1:8000/ in your web browser.
- Register or log in to access the application.
- Create and manage your expenses through the user interface.

## Generating Balance Sheet
- After adding atleast one expense, navigate to the "Balance Sheet" section to view your contributions and dues.
- The balance sheet will display the amount paid, amount owed, balance, and descriptions for each user.

## Downloading Balance Sheet as PDF
- In the "Balance Sheet" section, you will find a button to download the balance sheet.
- Clicking the button will generate a CSV document containing the balance sheet details.

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.
