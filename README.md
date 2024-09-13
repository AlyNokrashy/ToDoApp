# ToDo App
#### Video Demo:  <URL HERE>
#### Description:

This project is a To-Do list web application built using Flask, SQLAlchemy, and other Python libraries. The app allows users to create, update, delete, and manage tasks with features like user authentication, task prioritization, and date handling. Each user can register, log in, and have their personal list of tasks, which are stored securely in a database. The application includes features like search functionality, task sorting by criteria, filtering tasks by status.

The primary goal of this project was to develop a fully functional web app that meets the requirements of CS50’s final project while enhancing my understanding of web development concepts such as backend routing, database interactions, form handling, and user authentication.

## Features

- **User Registration and Authentication**: Users can register for an account, log in, and manage their tasks. Passwords are hashed for security using Flask-Bcrypt.
- **Task Management**: Users can add new tasks, mark them as complete or incomplete, edit task details, and delete tasks.
- **Task Prioritization**: Each task can be assigned a priority level (High, Medium, Low), and tasks can be sorted by priority.
- **Date Handling**: Tasks have creation and due dates. Dates are displayed in the user's local timezone (Egyptian time) and stored in UTC for consistency.
- **Search and Filter**: Users can search for tasks based on titles and filter tasks by their completion status (completed or not completed).
- **Sorting**: Tasks can be sorted by various criteria, such as due date, priority level, and title.
- **Responsive Design**: Fully responsive using Bootstrap

## Files and Structure

### 1. `app.py`
This is the main Python file for the application, containing all routes, models, and logic for the backend. It initializes the Flask app, configures the database, sets up Flask-Migrate for database migrations, and handles user sessions using Flask-Login.

- **Routes**:
  - `/`: Redirects to the dashboard if logged in; otherwise, it redirects to the registration page.
  - `/dashboard`: Displays the main page for managing tasks, showing all tasks, completed and pending counts, and a form for searching tasks.
  - `/login`: Displays the login form. Authenticates users by verifying their credentials.
  - `/logout`: Logs the user out and redirects to the login page.
  - `/register`: Displays the registration form. Registers new users with a username and a hashed password.
  - `/add`: Allows users to add new tasks with details like title, due date, priority, and description.
  - `/update/<int:todo_id>`: Toggles the completion status of a task based on its ID.
  - `/delete/<int:todo_id>`: Deletes a task by its ID.
  - `/status/<string:status>`: Filters tasks by their status (completed or not completed).
  - `/edit/<int:todo_id>`: Allows users to edit the details of a task by its ID.
  - `/sort`: Allows sorting tasks by different criteria like date, priority, or title.

- **Models**:
  - `User`: Represents a user with attributes like username and password. A user can have multiple tasks.
  - `Todo`: Represents a task with attributes like title, description, due date, priority, and a foreign key linking it to its owner (user).

### 2. `templates/`
This folder contains all HTML templates used in the project. The templates use Jinja2 syntax for rendering data passed from the backend.

- **`layout.html`**: The base template that includes common structure elements like the header and footer. And uses Bootstrap for responsive design. it includes:
-**Navigation bar**: Links to the dashboard, login and registeration pages. Also features a search form on the dashboard page and buttons for login/logout based on user authentication status.
-**Footer**: a sticky footer at the bottom of the page.

- **`dashboard.html`**: Main page for managing tasks, displays the user's tasks in card format (with detials like title, priority, due date, description, and status.), search bar, and buttons for sorting and filtering tasks. Also features task statistics and a progress bar for completed tasks
- **`login.html`**: The login page template with a form for user authentication.
- **`register.html`**: The registration page template with a form for creating a new account.
- **`add.html`**: The template for adding new tasks with fields for task details.
- **`edit.html`**: The template for editing an existing task's details.

### 3. `requirements.txt`
Lists all the dependencies required to run the app, including Flask, Flask-Login, Flask-WTF, Flask-Bcrypt, SQLAlchemy, and others.

## Design Choices

1. **Flask for Simplicity and Flexibility**: Flask was chosen as the web framework due to its lightweight nature, allowing for more control over routing, session management, and database interaction.

2. **SQLAlchemy for ORM**: SQLAlchemy was used to manage database interactions. It provides a clean, Pythonic way to interact with the database, making it easier to manage relationships between users and their tasks.

3. **WTForms for Form Validation**: WTForms was used to handle form validation.

4. **Flask-Bcrypt for Password Hashing**: To ensure user data security, passwords are hashed before being stored in the database. Flask-Bcrypt was chosen for its simplicity and security.

## Conclusion

This project was an excellent opportunity to apply my web development skills in a real-world scenario, integrating various technologies to build a functional and user-friendly To-Do list app. The combination of Flask, SQLAlchemy, and modern web design techniques helped create an application that is not only functional but also visually appealing and user-centric.


## Installation

To set up the ToDo web application on your local machine, follow these steps:

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/AlyNokrashy/ToDoApp.git
cd ToDoApp
```

### 2. Create a virtual environment

For Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

With the virtual environment activated, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory of the project to configure your environment variables. You will need to include the following:

- `SECRET_KEY`: A secret key for session management.
- `DATABASE_URL`: The URL for your database.

Example `.env` file:

```env
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///your_database_file.db
```

### 5. Initalize database

Run the following command to create the necessary database tables:

```bash
flask db upgrade
```

### 6. Run the app

Start the Flask development server:

```bash
flask run
```

The application will be available at http://127.0.0.1:5000/

## Troubleshooting

### Dependencies Not Installed
Ensure you have activated the virtual environment before running pip install.

### Database Issues
Verify your DATABASE_URL and run the flask db upgrade command if you encounter errors related to database migration.





