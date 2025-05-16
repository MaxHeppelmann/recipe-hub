import os
from recipe_app.app import create_app

# Print debug information for troubleshooting
db_url = os.environ.get('DATABASE_URL')
if db_url:
    # For security, don't print the full URL with credentials
    print(f"Database URL found: {db_url.split('@')[0].split('://')[0]}://*****@{db_url.split('@')[1] if '@' in db_url else 'unknown'}")
else:
    print("No DATABASE_URL environment variable found")

app = create_app()

if __name__ == "__main__":
    app.run()
