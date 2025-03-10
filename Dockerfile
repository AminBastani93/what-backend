FROM python:3.12

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements.in and .env.local files into the container
COPY requirements.in /app/

# Install pip-tools
RUN pip install --upgrade pip && \
    pip install pip-tools

# Compile requirements.in to requirements.txt and install pip requirements
RUN pip-compile requirements.in && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . /app/

RUN python manage.py makemigrations products
RUN python manage.py migrate
RUN python manage.py populate_products

# Make port 80 available to the world outside this container
EXPOSE 80

# Define the command to run your application
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:80"]