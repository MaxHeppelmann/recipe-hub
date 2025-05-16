FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run gunicorn
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} 'recipe_app.app:create_app()'
