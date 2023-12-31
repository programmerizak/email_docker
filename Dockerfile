# Use an official Python runtime as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY . /app/

# Install project dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the Django development server port
EXPOSE 8000

# Run the Django development server
CMD python manage.py runserver 0.0.0.0:8000
