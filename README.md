# Recipe App

A Flask application for creating and sharing recipes.

## Local Development Setup

1. **Set up a virtual environment**:
   ```
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root with the following variables:
   ```
   POSTGRESPASSWORD=your_password
   SECRET_KEY=your_secret_key
   DB_USERNAME=your_db_username
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=recipe-db
   FLASK_DEBUG=1  # For development only
   ```

4. **Initialize the database**:
   - Make sure PostgreSQL is installed and running
   - Create a database named 'recipe-db'
   - Run: `flask init-db`

5. **Run the application**:
   ```
   flask run
   ```

## Creating a Wheel Package for Deployment

### Building the Wheel

1. Install the build tools:
   ```
   pip install build wheel setuptools
   ```

2. Build the wheel package:
   ```
   python -m build --wheel
   ```
   This will create a `.whl` file in the `dist/` directory.

### Installing and Using the Wheel

1. Install the wheel on the target system:
   ```
   pip install path/to/recipe_app-0.1.0-py3-none-any.whl
   ```

2. Set up your environment variables (create a `.env` file or set them in your system)

3. Initialize the database:
   ```
   recipe-app-init-db
   ```

4. Run the application:
   ```
   recipe-app
   ```
   
   Or with gunicorn:
   ```
   gunicorn 'recipe_app.app:create_app()'
   ```

## Deployment

### Using Docker Compose (Local)

1. Make sure Docker and Docker Compose are installed
2. Run: `docker-compose up -d`
3. Access the application at http://localhost:5000

### Deploying to a Server

#### Option 1: Manual Deployment with Wheel

1. Set up a PostgreSQL database on your server or use a cloud service
2. Set environment variables on your server
3. Install the wheel package on your server:
   ```
   pip install recipe_app-0.1.0-py3-none-any.whl
   ```
4. Run with gunicorn:
   ```
   gunicorn 'recipe_app.app:create_app()'
   ```

#### Option 2: Docker Deployment

1. Build the Docker image:
   ```
   docker build -t recipe-app .
   ```

2. Run the container with appropriate environment variables:
   ```
   docker run -p 5000:5000 \
     -e DATABASE_URL=postgresql://user:password@host:port/dbname \
     -e SECRET_KEY=your_secret_key \
     -e PORT=5000 \
     recipe-app
   ```

### Cloud Deployment

The application is ready for deployment to services like Heroku:

1. Create a new app on Heroku
2. Add a PostgreSQL add-on
3. Set environment variables in Heroku settings
4. Deploy using Git: `git push heroku main`

## Database Migration

For future database changes, add Flask-Migrate to manage migrations:

1. Install Flask-Migrate: `pip install Flask-Migrate`
2. Initialize migrations in your code
3. Run migrations when database schema changes
