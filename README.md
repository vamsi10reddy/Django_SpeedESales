
# Running the Django Project

Follow these steps to set up and run the Django project on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python** (version 3.x): You can download it from [python.org](https://www.python.org/downloads/).
- **pip**: This usually comes with Python, but you can check by running `pip --version`.
- **Django**: If Django is not installed, you can install it using pip:
  ```bash
  pip install django
  ```

## Clone the Repository

1. **Clone the project repository** to your local machine:
   ```bash
   git clone https://github.com/vamsi10reddy/Django_SpeedESales.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd Django_SpeedESales-main 
   ```
## Install Necessary Packages
Use the terminal in Visual Studio Code to install the required packages. Run the following command, using either `pip` or `pip3` depending on which one is supported in your environment:

```bash
pip3 install django
pip3 install paypalrestsdk
pip3 install django-jazzmin
pip3 install paypal
pip3 install paypal.standard
pip3 install django-paypal
pip3 install shortuuid
pip3 install Pillow
```

## Run the Migrations

Before running the server, you need to apply migrations:

```bash
python3 manage.py migrate
```

## Start the Development Server

To run the project, use the following command:

```bash
python3 manage.py runserver
```

## Access the Application

- Open your web browser and go to `http://127.0.0.1:8000/` to view the application.

## Stopping the Server

To stop the server, go back to your terminal and press `Ctrl + C`.


Summary

1. urls.py connects URLs to views.
2. views.py contains functions that handle requests and load templates.
3. templates hold HTML files that define the page structure.
4. index.html is a specific template that gets displayed to the user.
5. settings.py configures how Django finds templates and manages other settings.

 Step-by-Step Workflow of a Django Project

#### 1. **Starting the Server**
- **File**: `manage.py`
- **Action**: You run the command:
  ```bash
  python manage.py runserver
  ```
- **What Happens**: This command starts the Django development server, which listens for requests on `http://127.0.0.1:8000/`.

---

#### 2. **Handling a Request**
- **File**: `urls.py`
- **Action**: When you visit a URL (like `http://127.0.0.1:8000/`), Django looks at the `urls.py` file.
- **Connection**: 
  - `urls.py` has a mapping that tells Django which view function to call for that URL.
  - For example, it might have something like this:
    ```python
    from django.urls import path
    from core.views import index

    urlpatterns = [
        path('', index, name='index'),  # Connects the URL to the index view
    ]
    ```

---

#### 3. **Calling the View Function**
- **File**: `views.py`
- **Action**: Based on the mapping in `urls.py`, Django calls the `index` function in `views.py`.
- **What Happens**: The function processes the request and prepares to render a response.
- **Example Code**:
    ```python
    from django.shortcuts import render

    def index(request):
        return render(request, "core/index.html")  # Tells Django to load the template
    ```

---

#### 4. **Rendering the Template**
- **File**: `templates/core/index.html`
- **Action**: The `render` function uses the specified template (`index.html`).
- **Connection**: The `index.html` file contains the HTML structure that will be sent back to the browser.
- **Example Content**:
    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Welcome</title>
    </head>
    <body>
        <h1>Welcome to My Website</h1>
    </body>
    </html>
    ```

---

#### 5. **Sending the Response**
- **Action**: After rendering the template, the view function sends the generated HTML back to the user’s browser.
- **Connection**: The browser receives the HTML and displays the web page to the user.

---

#### 6. **Static Files and Media**
- **Files**: `settings.py`, `static` folder, `media` folder
- **Connection**: 
  - **Static Files**: For CSS, JavaScript, and images. These are defined in `settings.py` under `STATIC_URL` and `STATICFILES_DIRS`. Django will look for static files in specified directories.
  - **Media Files**: For user-uploaded content. This is set in `settings.py` with `MEDIA_URL` and `MEDIA_ROOT`.

---

#### 7. **Database Operations**
- **File**: Models defined in `models.py`
- **Action**: When you save or retrieve data, Django interacts with the database using the models defined in `models.py`.
- **Connection**: 
  - Models are classes that define the structure of your database tables.
  - When you call methods on these models, Django translates them into SQL queries to interact with the database.

---

### Summary of the Connections

1. **Start the Server**: Run `manage.py` to start listening for requests.
2. **Handle Requests**: `urls.py` maps URLs to view functions.
3. **Call View**: `views.py` contains functions that process requests.
4. **Render Template**: The view calls the template in the `templates` folder.
5. **Send Response**: The rendered HTML is sent back to the browser.
6. **Static and Media Files**: Managed through `settings.py` and organized in their respective folders.
7. **Database Operations**: Handled through models defined in `models.py`.

### Visualizing the Flow

1. **User** ➜ **Browser** (makes request to URL)
2. **Django Server** (starts via `manage.py`)
3. **urls.py** (finds the right view)
4. **views.py** (processes request and renders template)
5. **templates/core/index.html** (HTML structure sent back)
6. **User's Browser** (displays the web page)



