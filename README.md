# Expense-API
An expense tracker API built with django rest framework

# Features
- Autheentication
- CRUD Expenses and categories
- Add spend limit for category
- Stats for expenses and categories (for the current day, the previous day, the current week and the current year)

 # Testing the API 
- To test the functionality of the api, you can use the following login credentials to be authorized:
    email: steppaapitestuser@gmail.com
    password: testuser
- To use the API, all the endpoints are available on the API documentation page. You can access the API documentation by navigating to ```https://steppa-expense-api.vercel.app/api/v1/#/``` in your browser. The API documentation provides a list of all the endpoints available and the required parameters for each endpoint.
- I encourage frontend developers who have built expense tracker projects to use the API and provide feedback on how it can be improved.

# Installation Guide

- Download or clone this repostory using
  ```sh
  git@github.com:SteppaCodes/Expense-API.git
- Navigate into your project directory
  ```sh
  cd expense-api
- Create a virtual environment
  ```sh
  python -m venv env
- Activate the virtual environment
- On Windows:
  ```sh
  env\scripts\activate
- On Macos:
  ```sh 
  source env/bin/activate
- Install dependencies
  ```sh
  pip install -r requirements.txt
- Run migrations to setup initial database schema
  ```sh
  python manage.py migrate
- Create super user(optional)
  ```sh
  python manage.py createsuperuser
- Run the development server
  ```sh
  python manage.py runserver
- Access the API: on your browser, navigate to
   ``` sh
    http://127.0.0.1:8000/api/v1/

# Authentication 
Token-based authentication is used to secure the API endpoints. To access protected endpoints, include the token in the request headers:
