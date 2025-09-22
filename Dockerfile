# Stage 1: Build Angular frontend
FROM node:20 AS frontend-build
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build -- --configuration production


# Stage 2: Backend with Django + Gunicorn
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (curl + unzip needed for weights)
RUN apt-get update && apt-get install -y curl unzip && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cu129

# Copy Django project
COPY django_app/ ./django_app/
COPY upscaling/ ./upscaling/
COPY manage.py ./

# Copy Angular build into Django
COPY --from=frontend-build /app/frontend/dist/frontend/browser/ ./django_app/static/
COPY --from=frontend-build /app/frontend/dist/frontend/browser/index.html ./django_app/templates/

# Install gdown for Google Drive downloads
RUN pip install gdown

# Delete existing weights folder and download new weights
RUN rm -rf ./upscaling/services/weights && \
    gdown --id 16fph_2JdVmQ8kbixpkaQVGPi1OKDbIfv -O /tmp/weights.zip && \
    unzip /tmp/weights.zip -d ./upscaling/services/ && \
    rm /tmp/weights.zip

# Collect Django static files
RUN mkdir -p /app/staticfiles
RUN python manage.py collectstatic --noinput

# Expose Django port
EXPOSE 8000

# Run Django with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "django_app.wsgi:application"]