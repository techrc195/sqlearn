# SQLearn: An Interactive SQL Learning Platform

SQLearn is a Django-based web application designed to help you master SQL concepts through structured exercises, dynamic schema visualization, and personalized feedback powered by a large language model (Gemini).

**Prerequisites**

*   Python 3.x ([https://www.python.org/downloads/](https://www.python.org/downloads/)) 
*   pip (usually included with Python installation)
*   PostgreSQL ([https://www.postgresql.org/](https://www.postgresql.org/))
*  A code editor or IDE (e.g., Visual Studio Code, PyCharm)

**Setup Instructions**

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/techrc195/sqlearn.git]
    ```

2.  **Install Dependencies:**
    ```bash
    cd sqlearn
    pip install -r requirements.txt
    ```

3.  **Database Configuration**

    *   **Create a PostgreSQL database:**  Name it 'sqlearn' (or adjust the database name in `myproject/settings.py`)
    *   **Update Environment Variables:** 
        *   Create a `.env` file in the root of your project.
        *   Add the following, replacing placeholders with your database credentials:

        ```
        HOST=your_database_host
        DATABASE=sqlearn
        USER=your_database_user
        PASSWORD=your_database_password
        ```

4.  **Apply Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Generate Mock Data:**
    ```bash
    python manage.py shell  # Start the Django shell
    from exercises.generate_mock_data import *  # Import the data generation functions
    # Call the functions to populate the database, e.g., generate_owners(), generate_foods(), etc.
    exit()  # Exit the shell
    ```

**Running the Development Server**

```bash
python manage.py runserver
