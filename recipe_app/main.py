import os
from . import app as application

def main():
    """Entry point for the application."""
    app = application.create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
